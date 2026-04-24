import re
from datetime import date
from models import TaskItem, ParseResult

# ── 멤버 닉네임 정규화 ───────────────────────────────────────────
MEMBER_NAME_MAP: dict[str, str] = {
    '차르코': 'Charco',
    'charco': 'Charco',
    '피카부': 'PK-B',
    'pk-b': 'PK-B',
    'hyom': 'HYOM',
    'eeee': 'EEEE',
    '무지': '무지',
    'natae': 'Natae',
    'june': 'June',
}

# ── 완료 패턴 ────────────────────────────────────────────────────
# Charco: O/o, HYOM/PK-B: ㅇ, 무지: (o)/(완)/수치/진행률, 공통: ✅☑
DONE_RE = re.compile(
    r'(?<!\w)[Oo○ㅇ✅☑](?!\w)'        # O, o, ○, ㅇ (단독 문자)
    r'|\(o\)|\(완\)'                    # (o), (완)
    r'|했다|했음'                        # 텍스트 완료
    r'|\(\d+[mhkm분]+\)'               # (12m), (5km), (1h44m) — 무지 수치 기록
    r'|\(\d+h\s*\d*m?\)'               # (2h), (1h30m)
    r'|\(\d+/\d+\)'                    # (126/443) — 무지 진행률
    r'|!!+',                            # 했음 !!!
    re.IGNORECASE,
)

# ── 미완료 패턴 ──────────────────────────────────────────────────
# x/X, (x), (미완료), 진행중/ing, (나중에), 세모, 🔺, (찔끔), 취소됨
MISS_RE = re.compile(
    r'(?<!\w)[Xx✗☐](?!\w)'            # X, x (단독 문자)
    r'|\(x\)'                           # (x)
    r'|\(미완료\)|\(미완\)'             # (미완료)
    r'|진행중|진행 중'                   # 진행중
    r'|(?<![a-zA-Z])ing(?=\s*$)'       # ing (줄 끝)
    r'|\(나중에\)'                       # (나중에)
    r'|세모'                             # 세모 — 부분 완료 → 미완료 처리
    r'|🔺'                              # 부분 완료 이모지
    r'|\(찔끔\)'                         # (찔끔)
    r'|취소됨',                          # 취소됨
    re.IGNORECASE,
)

# ── 파싱에서 무시할 줄 ───────────────────────────────────────────
SKIP_LINE_RE = re.compile(
    r'^\d{4}년 \d{1,2}월 \d{1,2}일'    # 날짜 구분 헤더
    r'|^삭제된 메시지입니다\.'           # 삭제된 메시지
    r'|^\(수정됨\)$'                    # 수정됨 태그
    r'|^\d+개의 댓글$'                  # 댓글 수 표시
    r'|^https?://'                      # URL
    r'|^오늘$'                          # "오늘" 구분선
    r'|님이 대화에 들어왔습니다'          # 입장 시스템 메시지
    r'|^Work Report'                    # EEEE Google Docs 캡처 텍스트
    r'|Google Docs$'                    # Google Docs 푸터
    r'|업무 일지$'                      # EEEE 업무 일지 헤더
    r'|^댓글을 남김:'                   # 댓글 알림
    r'|^\d{1,2}:\d{2}\s*(?:AM|PM)$',   # 타임스탬프 (export 형식)
)

# ── 제목 패턴: "MM.DD 이름 업무계획/보고" ─────────────────────────
TITLE_RE = re.compile(
    r'^(\d{2})\.\s*(\d{2})\s+(\S+)\s+(업무\s*(?:계획|보고))'
)


def normalize_member(raw: str) -> str:
    return MEMBER_NAME_MAP.get(raw.lower()) or MEMBER_NAME_MAP.get(raw) or raw


def _extract_raw_status(line: str) -> str:
    m = DONE_RE.search(line) or MISS_RE.search(line)
    return m.group(0).strip() if m else ''


def _clean_task_name(line: str) -> str:
    # 불릿 기호 제거
    line = re.sub(r'^[\s•\-\*\t]+', '', line).strip()

    # 완료/미완료 기호 제거 (줄 끝 단독 문자)
    line = re.sub(r'\s+[OoㅇXx✅☑✗☐○🔺]$', '', line)
    # 괄호 완료 표기 제거
    line = re.sub(
        r'\s*\((?:o|x|완|미완료|미완|진행중|나중에|취소됨|찔끔)\)\s*$',
        '', line, flags=re.IGNORECASE,
    )
    # 수치 기록 제거 (무지 스타일)
    line = re.sub(r'\s*\(\d+[mhkm분]+\)\s*$', '', line)
    line = re.sub(r'\s*\(\d+h\s*\d*m?\)\s*$', '', line)
    line = re.sub(r'\s*\(\d+/\d+\)\s*$', '', line)
    # 세모 제거
    line = re.sub(r'\s*세모[!]*\s*$', '', line)
    # 했음 !! 제거
    line = re.sub(r'\s*했음[!\s]*$', '', line)
    # - ing, - 진행중, - 취소됨, - 자료 수집 중 등 제거
    line = re.sub(r'\s*[-–]\s*(?:ing|진행중|자료 수집.*|취소됨.*)\s*$', '', line, flags=re.IGNORECASE)

    return line.strip()


def _parse_task_line(line: str, report_type: str) -> TaskItem | None:
    cleaned = re.sub(r'^[\s•\-\*\t]+', '', line).strip()

    if not cleaned:
        return None
    if re.match(r'^https?://', cleaned):
        return None
    # 타임스탬프, 날짜 줄 무시
    if re.match(r'^\d{1,2}:\d{2}', cleaned):
        return None

    raw_status = _extract_raw_status(cleaned)
    task_name = _clean_task_name(cleaned)

    if not task_name:
        return None

    if report_type == 'plan':
        is_done = False
    else:
        if DONE_RE.search(cleaned):
            is_done = True
        elif MISS_RE.search(cleaned):
            is_done = False
        else:
            is_done = False  # 표기 없으면 미완료 (기본값)

    return TaskItem(
        raw_name=cleaned,
        clean_name=task_name,
        is_done=is_done,
        raw_status=raw_status,
    )


def parse_message(
    text: str,
    member_name: str | None = None,  # Webhook payload의 실제 유저명 (우선 사용)
    year: int | None = None,
) -> ParseResult | None:
    """
    단일 메시지 본문을 파싱한다.

    - Webhook 경로: member_name에 채널톡 실제 유저명을 전달 → 텍스트 내 작성 이름 무시
    - 테스트 경로: member_name 생략 → 텍스트에서 이름 추출 (sample_messages.txt 검증용)
    """
    lines = [l.rstrip() for l in text.splitlines()]
    y = year or date.today().year

    # 제목 줄 탐색
    title_idx = -1
    report_date: date | None = None
    parsed_member = ''
    report_type = ''

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        m = TITLE_RE.match(line.strip())
        if m:
            month, day, member_raw, rtype_raw = m.group(1), m.group(2), m.group(3), m.group(4)
            try:
                report_date = date(y, int(month), int(day))
            except ValueError:
                continue
            # Webhook에서 실제 유저명이 주어지면 텍스트 내 이름은 무시
            parsed_member = member_name if member_name else normalize_member(member_raw)
            report_type = 'plan' if '계획' in rtype_raw else 'report'
            title_idx = i
            break

    if title_idx < 0 or report_date is None:
        return None

    # 태스크 파싱
    tasks: list[TaskItem] = []
    for line in lines[title_idx + 1:]:
        if SKIP_LINE_RE.search(line.strip()):
            continue
        task = _parse_task_line(line, report_type)
        if task:
            tasks.append(task)

    member_name = parsed_member

    if not tasks:
        return None

    # 신뢰도: 업무보고에서 명시적 표기가 있는 비율
    if report_type == 'report':
        marked = sum(1 for t in tasks if t.raw_status)
        confidence = marked / len(tasks)
    else:
        confidence = 1.0

    return ParseResult(
        member_name=member_name,
        report_date=report_date,
        report_type=report_type,
        tasks=tasks,
        confidence=confidence,
        used_claude=False,
    )
