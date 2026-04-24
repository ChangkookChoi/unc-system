# unc-system — Claude Code 컨텍스트

## 프로젝트 한 줄 요약

가상회사 프레임으로 팀의 일상 루틴을 업무화하고, 자동 집계 + 시각화하는 시스템.

## 컨셉

> "나와의 약속을 업무화하라."

팀원들이 매일 채널톡에 업무계획/보고를 올린다.
이 시스템은 그 메시지를 자동으로 파싱 · 집계하고, 대시보드로 시각화한다.

## 현재 개발 단계

**Phase 1 진행 중** — 채널톡 연동(1-3) 대기 중, 스케줄러(1-5) 다음 예정

| 단계 | 상태 |
|------|------|
| 1-1. 프로젝트 초기 세팅 | ✅ 완료 |
| 1-2. DB 세팅 (Supabase + asyncpg) | ✅ 완료 |
| 1-3. 채널톡 Webhook 연동 | ⏸ 대기 (관리자 권한 확보 후 진행) |
| 1-4. 규칙 기반 파서 | ✅ 완료 |
| 1-5. APScheduler 리마인더 | 🔜 다음 작업 |

상세 태스크: `TODO.md` 참고

## 프로젝트 구조

```
unc-system/
├── backend/
│   ├── main.py          FastAPI 앱 진입점 (lifespan, CORS, 라우터)
│   ├── database.py      asyncpg 커넥션 풀
│   ├── models.py        Pydantic 모델 (WebhookPayload, ParseResult, DailyReport)
│   ├── parser.py        규칙 기반 메시지 파서
│   ├── routes/
│   │   ├── webhook.py   POST /webhook (스텁)
│   │   └── reports.py   GET /reports/daily (스텁)
│   └── migrations/
│       └── 001_init.sql 초기 스키마
└── frontend/            Next.js 대시보드 (Phase 3에서 본격 개발)
```

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.13 + FastAPI + uvicorn |
| DB 연결 | asyncpg (커넥션 풀) |
| DB | PostgreSQL (Supabase) |
| 스케줄러 | APScheduler |
| AI 파싱 폴백 | Anthropic Claude API — Haiku 모델 |
| 대시보드 | Next.js 16.2.4 + React 19 + TypeScript + Tailwind CSS 4 |
| 차트 | Recharts (Phase 3에서 설치 예정) |
| 채널 연동 | 채널톡 Open API v5 |

## 핵심 설계 원칙

1. **원본 데이터 보존** — 멤버가 입력한 태스크명을 덮어쓰지 않는다. 카테고리 매핑은 별도 테이블로 관리하고 집계 시에만 사용한다.

2. **파싱 우선순위** — 규칙 기반 파서 먼저, 신뢰도 < 0.5일 때만 Claude API 폴백. Claude API는 기본이 아닌 폴백이다.

3. **채널톡 Webhook 주의사항** — `actAsManager` 옵션은 팀챗에서 422 에러. 사용 금지.

4. **환경변수 하드코딩 금지** — 모든 키/시크릿은 `.env` 파일에서만 관리.

## 메시지 포맷 및 완료 표기

**제목 패턴:** `MM.DD 이름 업무계획` / `MM.DD 이름 업무보고`

**멤버별 완료 표기 (실제 데이터 기반):**

| 멤버 | 완료 | 미완료 | 특이사항 |
|------|------|--------|---------|
| Charco (차르코) | `O` | `X`, `ing` | `- ing`, `- 자료 수집 중` = 미완료 |
| HYOM | `ㅇ` | `x`, `세모` | `세모` = 부분완료 → 미완료 처리 |
| PK-B (피카부) | `ㅇ`, `o` | `X`, `x` | |
| EEEE | 표기 없음 | `(미완료)` | 표기 없음 = 완료 → 신뢰도 0% → Claude 폴백 |
| 무지 | `(o)`, `(완)`, 수치`(12m)`, 진행률`(95/443)` | `(x)` | Notion 링크로만 보고하는 경우 있음 |
| Natae | 표기 없음 | | EEEE와 동일한 패턴 |

**파싱에서 무시:** Google Docs/Notion URL, `삭제된 메시지입니다.`, `(수정됨)`, 날짜 헤더

## 개발 명령어

```bash
# 백엔드 실행
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# 파서 테스트
cd backend && source venv/bin/activate && python test_parser.py

# 프론트엔드 실행
cd frontend && npm run dev

# 백엔드 패키지 추가
cd backend && source venv/bin/activate && pip install {패키지명} && pip freeze > requirements.txt
```

## 코드 스타일

- Python: snake_case 함수/변수, PascalCase 클래스
- TypeScript: PascalCase 컴포넌트, camelCase 함수/변수
- 커밋: `type: 설명` (`feat:`, `fix:`, `chore:`, `docs:`)
- 주석은 한국어

## 참고 문서

- 전체 기획: `README.md`
- 개발 태스크: `TODO.md`
- 주요 결정 기록: `DECISIONS.md`
- 채널톡 API: https://developers.channel.io
- Anthropic API: https://docs.anthropic.com
