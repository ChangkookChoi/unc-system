"""sample_messages.txt 로 파서 동작 검증"""
import re
from parser import parse_message

# 타임스탬프 + 멤버명 줄 제거 후 메시지 블록 분리
BLOCK_SEP_RE = re.compile(
    r'^\S.*\n\d{1,2}:\d{2}\s*(?:AM|PM)\n',   # "멤버명\n시간\n"
    re.MULTILINE,
)

def split_messages(raw: str) -> list[str]:
    # "멤버명\n시간\n메시지본문" 형태를 메시지 본문만 추출
    blocks = []
    parts = re.split(r'\n(?=\S+\n\d{1,2}:\d{2}\s*(?:AM|PM)\n)', raw)
    for part in parts:
        # 첫 두 줄(멤버명, 시간) 제거
        lines = part.splitlines()
        if len(lines) >= 2 and re.match(r'^\d{1,2}:\d{2}\s*(?:AM|PM)$', lines[1].strip()):
            body = '\n'.join(lines[2:])
        else:
            body = part
        blocks.append(body.strip())
    return [b for b in blocks if b]


def main():
    with open('sample_messages.txt', encoding='utf-8') as f:
        raw = f.read()

    messages = split_messages(raw)
    results = []
    failed = []

    for msg in messages:
        result = parse_message(msg)
        if result:
            results.append(result)
        else:
            # 제목 패턴이 있는데 파싱 실패한 경우만 수집
            if re.search(r'\d{2}\.\s*\d{2}\s+\S+\s+업무\s*(?:계획|보고)', msg):
                failed.append(msg[:80].replace('\n', ' / '))

    print(f'=== 파싱 결과 ===')
    print(f'성공: {len(results)}건 / 실패: {len(failed)}건\n')

    # 멤버별 통계
    from collections import defaultdict
    stats: dict[str, dict] = defaultdict(lambda: {'plan': 0, 'report': 0})
    for r in results:
        stats[r.member_name][r.report_type] += 1

    print('멤버별 파싱 건수:')
    for member, s in sorted(stats.items()):
        print(f'  {member}: 계획 {s["plan"]}건 / 보고 {s["report"]}건')

    print('\n샘플 파싱 결과 (보고 5건):')
    reports = [r for r in results if r.report_type == 'report'][:5]
    for r in reports:
        done = sum(1 for t in r.tasks if t.is_done)
        total = len(r.tasks)
        print(f'\n  [{r.report_date} {r.member_name}] {done}/{total} 완료 (신뢰도 {r.confidence:.0%})')
        for t in r.tasks:
            mark = '✅' if t.is_done else '❌'
            print(f'    {mark} {t.clean_name}  ← raw: "{t.raw_status}"')

    if failed:
        print(f'\n파싱 실패 샘플 ({min(3, len(failed))}건):')
        for f in failed[:3]:
            print(f'  {f}')


if __name__ == '__main__':
    main()
