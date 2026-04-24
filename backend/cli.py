"""어드민 CLI — 카테고리 매핑 관리."""
import asyncio
import click
from categorizer import add_mapping, list_unmapped_from_reports, categorize
from database import get_pool, close_pool


def run(coro):
    async def _run():
        try:
            return await coro
        finally:
            await close_pool()
    return asyncio.run(_run())


@click.group()
def cli():
    """unc-system 어드민 CLI"""


@cli.command('map')
@click.argument('task_name')
@click.argument('category')
def cmd_map(task_name, category):
    """태스크명을 카테고리에 매핑한다.

    \b
    사용 예:
      python cli.py map "러닝" "운동"
      python cli.py map "기획서 작성" "업무"
    """
    async def _():
        ok = await add_mapping(task_name, category)
        if ok:
            click.echo(f'✅ 매핑 완료: "{task_name}" → "{category}"')
        else:
            pool = await get_pool()
            cats = await pool.fetch("SELECT name FROM categories ORDER BY id")
            names = [r['name'] for r in cats]
            click.echo(f'❌ 카테고리 "{category}" 없음. 사용 가능: {names}')
    run(_())


@cli.command('list-unmapped')
def cmd_list_unmapped():
    """DB tasks 테이블에서 매핑되지 않은 태스크 목록 출력."""
    async def _():
        items = await list_unmapped_from_reports()
        if not items:
            click.echo('미분류 태스크 없음 🎉')
        else:
            click.echo(f'미분류 태스크 {len(items)}건:')
            for name in items:
                click.echo(f'  - {name}')
    run(_())


@cli.command('show-mappings')
@click.option('--category', '-c', default=None, help='특정 카테고리만 표시')
def cmd_show_mappings(category):
    """전체 매핑 테이블 출력."""
    async def _():
        pool = await get_pool()
        if category:
            rows = await pool.fetch(
                """
                SELECT tm.clean_name, c.name as category
                FROM task_mappings tm
                JOIN categories c ON c.id = tm.category_id
                WHERE c.name = $1
                ORDER BY tm.clean_name
                """, category,
            )
        else:
            rows = await pool.fetch(
                """
                SELECT tm.clean_name, c.name as category
                FROM task_mappings tm
                JOIN categories c ON c.id = tm.category_id
                ORDER BY c.id, tm.clean_name
                """
            )
        if not rows:
            click.echo('매핑 없음')
            return
        cur_cat = None
        for r in rows:
            if r['category'] != cur_cat:
                cur_cat = r['category']
                click.echo(f'\n[{cur_cat}]')
            click.echo(f'  {r["clean_name"]}')
        click.echo(f'\n총 {len(rows)}개')
    run(_())


@cli.command('check')
@click.argument('task_name')
def cmd_check(task_name):
    """태스크명이 어떤 카테고리로 분류되는지 확인."""
    async def _():
        cat_id, match_type = await categorize(task_name)
        if cat_id is None:
            click.echo(f'❓ "{task_name}" → 미분류')
            return
        pool = await get_pool()
        cat = await pool.fetchval("SELECT name FROM categories WHERE id = $1", cat_id)
        click.echo(f'"{task_name}" → [{cat}] ({match_type})')
    run(_())


if __name__ == '__main__':
    cli()
