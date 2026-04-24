# TODO.md

unc-system 개발 태스크 목록.

---

## Phase 1 — 리마인더 봇 기반 구축 ✅

- [x] 1-1. 프로젝트 초기 세팅 (main.py, models.py, .env.example)
- [x] 1-2. DB 세팅 (Supabase + asyncpg, 스키마 마이그레이션, 초기 데이터 시딩)
- [x] 1-4. 규칙 기반 파서 (멤버별 완료 표기 패턴, 실데이터 검증 208건)
- [x] 1-5. APScheduler (09:00 리마인더, 23:00 집계 고지, Asia/Seoul)

### 1-3. 채널톡 연동 ⏸ 대기 중

> 채널톡 워크스페이스 관리자 권한 확보 후 진행

- [ ] 채널톡 API 키 발급 (Access Key / Access Secret)
- [ ] 채널톡 Webhook 등록 (Fly.io 배포 URL 사용)
- [ ] `backend/routes/webhook.py` 실제 구현
  - 채널톡 서명 검증 (HMAC)
  - `2_Work_report` 채널 필터링
  - 멤버 식별 (채널톡 유저 ID → members 테이블 매핑)
- [ ] `backend/channel_client.py` — 메시지 발송 클라이언트
- [ ] `backend/notifier.py` TODO 주석 해제 (실제 메시지 발송 활성화)
- [ ] `backend/scheduler.py` TODO 주석 해제 (실제 발송 활성화)

---

## Phase 2 — 파서 고도화 + 집계 엔진 ✅

- [x] 2-1. Claude API 폴백 파서 (신뢰도 < 0.5 시 Haiku 호출, 토큰 로깅)
- [x] 2-2. 카테고리 매핑 (143개 초기 매핑, categorizer.py, cli.py)
- [x] 2-3. 집계 엔진 (save_parse_result, 일간/주간/스트릭/카테고리 API)
- [x] 2-4. 저녁 집계 메시지 포맷터 (달성률 아이콘, MVP, 스트릭 강조, 독려)

---

## Phase 3 — 대시보드 웹앱 ✅ (배포 제외)

- [x] 3-1. 프론트엔드 초기 세팅 (Recharts, types, lib/api.ts, .env.local)
- [x] 3-2. 컴포넌트 (StatCard, MemberCard, AchievementChart, WeeklyChart, TaskTable, DateNav)
- [x] 3-3. 페이지 조립 (일간/주간 뷰, URL searchParams 기반 날짜 이동)

### 3-4. 배포 🔧 진행 중

- [x] Fly.io 앱 생성 (`unc-system-api`, 리전: nrt)
- [x] Dockerfile, fly.toml 작성
- [x] Fly.io secrets 설정 (DATABASE_URL, ANTHROPIC_API_KEY, ALLOWED_ORIGINS)
- [ ] **백엔드 배포 완료** — Supabase 풀러 연결 문제 해결 중
  - 문제: Fly.io → Supabase 직접 연결(5432) IPv6 차단
  - 해결: Supabase Session 풀러 URL로 변경 (`pooler.supabase.com:5432`)
  - 현황: ECIRCUITBREAKER (너무 많은 인증 실패) → 5~10분 대기 후 재시도
  - 다음 단계: `flyctl deploy --app unc-system-api` 재실행
- [ ] Vercel 배포 (백엔드 URL 확정 후)
  - `NEXT_PUBLIC_API_BASE_URL` = Fly.io URL
  - `ALLOWED_ORIGINS` secrets에 Vercel URL 추가

---

## 향후 확장 아이디어 (백로그)

- [ ] 스트릭 시각화 컴포넌트 (실데이터 쌓인 후 의미 있음)
- [ ] AI Work Report 자동 생성기
- [ ] 주간 회고 자동 생성
- [ ] 게이미피케이션 (포인트, 랭킹, 월말 리포트)
- [ ] 멀티 채널 어댑터 (슬랙 / 디스코드 / 텔레그램)
- [ ] 카테고리 자동 매핑 고도화 (Claude 임베딩)
