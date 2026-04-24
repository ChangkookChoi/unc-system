# unc-system — Claude Code 컨텍스트

## 프로젝트 한 줄 요약

가상회사 프레임으로 팀의 일상 루틴을 업무화하고, 자동 집계 + 시각화하는 시스템.

## 컨셉

> "나와의 약속을 업무화하라."

팀원들이 매일 채널톡에 업무계획/보고를 올린다.
이 시스템은 그 메시지를 자동으로 파싱 · 집계하고, 대시보드로 시각화한다.

## 현재 개발 단계

| 단계 | 상태 |
|------|------|
| 1-1. 프로젝트 초기 세팅 | ✅ |
| 1-2. DB 세팅 (Supabase + asyncpg) | ✅ |
| 1-3. 채널톡 Webhook 연동 | ⏸ 대기 (관리자 권한 확보 후 진행) |
| 1-4. 규칙 기반 파서 | ✅ |
| 1-5. APScheduler 리마인더 | ✅ |
| 2-1. Claude API 폴백 파서 | ✅ (Anthropic 크레딧 충전 후 활성화) |
| 2-2. 카테고리 매핑 + CLI | ✅ |
| 2-3. 집계 엔진 + reports API | ✅ |
| 2-4. 저녁 집계 메시지 포맷터 | ✅ |
| 3-1~3. 대시보드 (일간/주간 뷰) | ✅ |
| 배포 — Fly.io (백엔드) | 🔧 진행 중 (DB 연결 문제 해결 중) |
| 배포 — Vercel (프론트엔드) | 🔜 백엔드 배포 완료 후 진행 |

상세 태스크: `TODO.md` / 결정 기록: `DECISIONS.md`

## 프로젝트 구조

```
unc-system/
├── backend/
│   ├── main.py            FastAPI 앱 (lifespan, CORS, 라우터)
│   ├── database.py        asyncpg 커넥션 풀 (Supabase SSL 지원)
│   ├── models.py          Pydantic 모델
│   ├── parser.py          규칙 기반 파서 + Claude API 폴백
│   ├── aggregator.py      DB 저장 + 집계 쿼리
│   ├── notifier.py        저녁 집계 / 아침 리마인더 메시지 포맷터
│   ├── scheduler.py       APScheduler (09:00/23:00, Asia/Seoul)
│   ├── categorizer.py     태스크 → 카테고리 매핑
│   ├── cli.py             어드민 CLI
│   ├── Dockerfile         Fly.io 배포용
│   ├── fly.toml           Fly.io 설정 (앱명: unc-system-api, 리전: nrt)
│   ├── routes/
│   │   ├── webhook.py     POST /webhook
│   │   └── reports.py     GET /reports/daily|weekly|categories, /members/{id}/streak
│   └── migrations/
│       ├── 001_init.sql   초기 스키마
│       ├── 002_category_mappings.sql  카테고리 매핑 테이블 + 143개 초기 데이터
│       └── 003_constraints.sql        유니크 제약 + is_comment 컬럼
└── frontend/
    ├── app/
    │   ├── page.tsx       대시보드 메인 (Server Component, 일간/주간 뷰)
    │   └── layout.tsx
    ├── components/
    │   ├── StatCard.tsx
    │   ├── MemberCard.tsx
    │   ├── AchievementChart.tsx  ('use client', Recharts)
    │   ├── WeeklyChart.tsx       ('use client', Recharts)
    │   ├── TaskTable.tsx
    │   └── DateNav.tsx           ('use client', URL searchParams 기반 날짜 이동)
    ├── lib/api.ts         FastAPI 백엔드 API 클라이언트
    └── types/index.ts     공통 TypeScript 타입
```

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.13 + FastAPI + uvicorn |
| DB 연결 | asyncpg (커넥션 풀, Supabase 풀러 Session mode) |
| DB | PostgreSQL (Supabase, 서울 리전) |
| 스케줄러 | APScheduler (Asia/Seoul) |
| AI 파싱 폴백 | Anthropic Claude Haiku 4.5 |
| 대시보드 | Next.js 16.2.4 + React 19 + TypeScript + Tailwind CSS 4 |
| 차트 | Recharts |
| 채널 연동 | 채널톡 Open API v5 (연동 대기 중) |
| 백엔드 배포 | Fly.io (앱명: unc-system-api, 리전: nrt 도쿄) |
| 프론트 배포 | Vercel (예정) |

## 핵심 설계 원칙

1. **원본 데이터 보존** — 태스크명 덮어쓰지 않음. 카테고리 매핑은 별도 테이블, 집계 시에만 사용.
2. **파싱 우선순위** — 규칙 기반 먼저, 신뢰도 < 0.5일 때만 Claude API 폴백.
3. **채널톡 주의사항** — `actAsManager` 옵션은 팀챗에서 422 에러. 사용 금지.
4. **환경변수 하드코딩 금지** — `.env` 파일 / Fly.io secrets로만 관리.

## Fly.io 배포 관련

- **앱명:** `unc-system-api`
- **리전:** `nrt` (도쿄)
- **DB 연결:** Supabase 직접 연결(5432)은 IPv6 문제로 차단 → **Session 풀러** 사용
  - 풀러 호스트: `aws-1-ap-northeast-2.pooler.supabase.com:5432`
  - 유저명 형식: `postgres.sbotiiispplrdwfzofgb` (프로젝트 ID 포함)
- **Fly.io secrets:** `DATABASE_URL`, `ANTHROPIC_API_KEY`, `ALLOWED_ORIGINS`
- **머신:** 1대 (shared-cpu-1x, 256MB, min_machines_running=1 → 슬립 없음)

## 멤버별 완료 표기 (파서 참고)

| 멤버 | 완료 | 미완료 | 특이사항 |
|------|------|--------|---------|
| Charco (차르코) | `O` | `X`, `ing` | |
| HYOM | `ㅇ` | `x`, `세모` | 세모 = 부분완료 → 미완료 처리 |
| PK-B (피카부) | `ㅇ`, `o` | `X`, `x` | |
| EEEE | 표기 없음 | `(미완료)` | 신뢰도 0% → Claude 폴백 |
| 무지 | `(o)`, `(완)`, 수치 | `(x)` | Notion 링크 보고 시 파싱 불가 |
| Natae | 표기 없음 | | EEEE와 동일 패턴 |

## 개발 명령어

```bash
# 백엔드 로컬 실행
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# 파서 테스트
cd backend && source venv/bin/activate && python test_parser.py

# 카테고리 CLI
cd backend && source venv/bin/activate && python cli.py check "러닝"
cd backend && source venv/bin/activate && python cli.py map "새태스크" "운동"

# 프론트엔드 로컬 실행
cd frontend && npm run dev

# Fly.io 배포
cd backend && flyctl deploy --app unc-system-api

# Fly.io 로그 확인
flyctl logs --app unc-system-api

# Fly.io secrets 설정
flyctl secrets set KEY="value" --app unc-system-api

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
- 결정 기록: `DECISIONS.md`
- 운영 규칙: `RULES.md`
- 채널톡 API: https://developers.channel.io
- Anthropic API: https://docs.anthropic.com
- Fly.io 대시보드: https://fly.io/apps/unc-system-api
