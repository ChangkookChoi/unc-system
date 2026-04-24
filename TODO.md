# TODO.md

unc-system 개발 태스크 목록.

---

## Phase 1 — 리마인더 봇 기반 구축

**목표:** 채널톡 Webhook 수신 → 메시지 파싱 → DB 저장 → 리마인더 자동 발송  
**완료 기준:** 봇이 09:00 리마인더를 보내고, 23:00에 달성 요약이 자동 발송됨

### 1-1. 프로젝트 초기 세팅 ✅

- [x] `backend/.env.example` 작성
- [x] `backend/main.py` — FastAPI 앱 기본 구조 (lifespan, CORS, 라우터)
- [x] `backend/models.py` — Pydantic 모델 (WebhookPayload, ParseResult, DailyReport)

### 1-2. DB 세팅 ✅

- [x] Supabase 프로젝트 생성 + `DATABASE_URL` 발급
- [x] `backend/database.py` — asyncpg 커넥션 풀
- [x] `migrations/001_init.sql` 실행 (members, categories, tasks, reports, completions)
- [x] 초기 멤버 시딩 (Charco, HYOM, EEEE) + 카테고리 시딩 (운동, 어학, 독서/학습, 루틴)

### 1-3. 채널톡 연동 ⏸ 대기 중

> 채널톡 워크스페이스 관리자 권한 확보 후 진행

- [ ] 채널톡 API 키 발급 (Access Key / Access Secret)
- [ ] 공개 URL 확보 (개발: ngrok / 운영: Railway 또는 Render)
- [ ] 채널톡 Webhook 등록
- [ ] `backend/routes/webhook.py` — 실제 구현
  - 채널톡 서명 검증 (HMAC)
  - `2_Work_report` 채널 필터링
  - 멤버 식별 (채널톡 유저 ID → members 테이블 매핑)
- [ ] `backend/channel_client.py` — 메시지 발송 클라이언트

### 1-4. 메시지 파서 1차 (규칙 기반) ✅

- [x] `backend/parser.py` — 규칙 기반 파서 구현
  - 6명 멤버별 완료 표기 패턴 반영 (O/ㅇ/세모/(미완료)/(o) 등)
  - 신뢰도 계산 (명시적 표기 비율)
  - Google Docs/Notion URL, 삭제 메시지 등 무시 처리
- [x] `backend/test_parser.py` + `sample_messages.txt` — 실데이터 검증 (208건, 92% 성공)

### 1-5. 스케줄러 🔜 다음 작업

- [ ] `backend/scheduler.py` — APScheduler 설정 (타임존: Asia/Seoul)
  - 09:00 잡: 아침 리마인더 발송
  - 23:00 잡: 당일 리포트 집계 → 팀챗 고지
- [ ] `main.py` lifespan에 scheduler.start() / shutdown() 연결

---

## Phase 2 — 파서 고도화 + 집계 엔진

**목표:** 다양한 완료 표기 대응, 카테고리 매핑, 집계 데이터 축적  
**완료 기준:** 표기법을 정확히 파싱하고 집계 데이터가 DB에 쌓임

### 2-1. 하이브리드 파서 (Claude API 폴백)

- [ ] `backend/parser.py` — Claude Haiku 폴백 추가
  - 신뢰도 < 0.5 이면 Claude API 호출
  - EEEE/Natae "표기 없음 = 완료" 패턴 처리
  - 모델: `claude-haiku-4-5` (건당 약 $0.0001)
- [ ] Claude API 호출 로깅 (비용 추적용)

### 2-2. 태스크 카테고리 매핑

- [ ] `backend/categorizer.py`
  - 정확 매칭 → DB 조회
  - 유사도 매칭: `difflib.SequenceMatcher` 임계값 0.7
  - 매칭 실패 시 `미분류` 처리 후 로깅
- [ ] 어드민 CLI (`backend/cli.py`)
  - `python cli.py map "러닝" "운동"`
  - `python cli.py list-unmapped`

### 2-3. 집계 엔진

- [ ] `backend/aggregator.py`
  - 멤버별 일일 달성률 (완료 수 / 전체 태스크 수)
  - 스트릭 계산 (연속 달성일, 태스크별 + 멤버별)
  - 팀 평균 달성률 / 미제출 멤버 감지
- [ ] `backend/routes/reports.py` 실제 구현
  - `GET /reports/daily?date=`
  - `GET /reports/weekly?week=`
  - `GET /reports/members/{member_id}/streak`

### 2-4. 저녁 집계 메시지 고도화

- [ ] 스트릭 강조 표시 (`🔥 듀오링고 영어: 팀 전원 7일 연속 달성 중!`)
- [ ] 오늘 최다 달성 멤버 / 미제출 멤버 별도 표기

---

## Phase 3 — 대시보드 웹앱

**목표:** 시각화 대시보드 완성 및 배포  
**완료 기준:** 웹 URL로 팀 현황을 언제든 한눈에 확인 가능

### 3-1. 프론트엔드 초기 세팅

- [ ] `frontend/.env.local.example` 작성
- [ ] Supabase JS 클라이언트 설치 (`@supabase/supabase-js`)
- [ ] Recharts 설치
- [ ] 공통 레이아웃 + 공통 타입 정의 (`types/index.ts`)

### 3-2. 주요 컴포넌트

- [ ] `StatCard.tsx` — 지표 카드 (팀 평균, 제출 현황, 최다 달성)
- [ ] `MemberCard.tsx` — 오늘 멤버 카드 (달성률, 태스크 체크 현황)
- [ ] `AchievementChart.tsx` — 멤버별 달성률 바 차트
- [ ] `StreakChart.tsx` — 공통 루틴 스트릭 점 그래프
- [ ] `TaskTable.tsx` — 태스크별 팀 달성 현황 테이블

### 3-3. 페이지 조립 및 배포

- [ ] `app/page.tsx` — 대시보드 메인 (Supabase 실시간 구독)
- [ ] 백엔드: Railway 또는 Render 배포
- [ ] 프론트엔드: Vercel 배포

---

## 향후 확장 아이디어 (백로그)

- [ ] AI Work Report 자동 생성기
- [ ] 주간 회고 자동 생성
- [ ] 게이미피케이션 (포인트, 랭킹, 월말 리포트)
- [ ] 멀티 채널 어댑터 (슬랙 / 디스코드 / 텔레그램)
- [ ] 카테고리 자동 매핑 고도화 (Claude 임베딩)
