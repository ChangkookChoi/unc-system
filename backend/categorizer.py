import re
import logging
from difflib import SequenceMatcher
from database import get_pool

logger = logging.getLogger(__name__)

SIMILARITY_THRESHOLD = 0.7


def _normalize(name: str) -> str:
    """비교용 정규화: 소문자, 공백 제거, 특수문자 제거."""
    return re.sub(r'[\s\-/·]', '', name.lower())


async def _load_mappings() -> dict[str, int]:
    """task_mappings 전체를 {clean_name: category_id} 딕셔너리로 로드."""
    pool = await get_pool()
    rows = await pool.fetch("SELECT clean_name, category_id FROM task_mappings")
    return {row['clean_name']: row['category_id'] for row in rows}


async def _load_categories() -> dict[int, str]:
    """categories 전체를 {id: name} 딕셔너리로 로드."""
    pool = await get_pool()
    rows = await pool.fetch("SELECT id, name FROM categories")
    return {row['id']: row['name'] for row in rows}


async def categorize(clean_name: str) -> tuple[int | None, str]:
    """
    태스크명을 카테고리로 분류한다.

    Returns:
        (category_id, match_type)
        match_type: 'exact' | 'similarity' | 'split' | 'unmapped'
    """
    mappings = await _load_mappings()

    # 1. 정확 매칭
    if clean_name in mappings:
        return mappings[clean_name], 'exact'

    # 2. 복합 태스크 분리 (/ 기준)
    if '/' in clean_name:
        parts = [p.strip() for p in clean_name.split('/') if p.strip()]
        for part in parts:
            if part in mappings:
                return mappings[part], 'split'
        # 분리된 각 파트로 유사도 매칭 시도
        for part in parts:
            cat_id, match_type = await _similarity_match(part, mappings)
            if cat_id:
                return cat_id, f'split+{match_type}'

    # 3. 유사도 매칭
    cat_id, match_type = await _similarity_match(clean_name, mappings)
    if cat_id:
        return cat_id, match_type

    # 4. 미분류
    logger.info("미분류 태스크: '%s'", clean_name)
    return None, 'unmapped'


async def _similarity_match(
    name: str, mappings: dict[str, int]
) -> tuple[int | None, str]:
    norm_name = _normalize(name)
    best_score = 0.0
    best_cat_id = None

    for mapped_name, cat_id in mappings.items():
        score = SequenceMatcher(None, norm_name, _normalize(mapped_name)).ratio()
        if score > best_score:
            best_score = score
            best_cat_id = cat_id

    if best_score >= SIMILARITY_THRESHOLD:
        return best_cat_id, 'similarity'
    return None, 'unmapped'


async def add_mapping(clean_name: str, category_name: str) -> bool:
    """수동 매핑 등록. 카테고리명이 없으면 False 반환."""
    pool = await get_pool()
    cat = await pool.fetchrow(
        "SELECT id FROM categories WHERE name = $1", category_name
    )
    if not cat:
        return False
    await pool.execute(
        """
        INSERT INTO task_mappings (clean_name, category_id)
        VALUES ($1, $2)
        ON CONFLICT (clean_name) DO UPDATE SET category_id = EXCLUDED.category_id
        """,
        clean_name, cat['id'],
    )
    return True


async def list_unmapped_from_reports(limit: int = 50) -> list[str]:
    """DB의 completions에서 task_mappings에 없는 태스크명 목록 반환."""
    pool = await get_pool()
    rows = await pool.fetch(
        """
        SELECT DISTINCT t.raw_name
        FROM tasks t
        WHERE NOT EXISTS (
            SELECT 1 FROM task_mappings tm WHERE tm.clean_name = t.raw_name
        )
        LIMIT $1
        """,
        limit,
    )
    return [r['raw_name'] for r in rows]
