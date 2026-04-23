# TODO.md

unc-system 개발 태스크 목록.  
채널톡 팀챗 메시지를 자동 파싱해 달성률을 집계하고 시각화하는 봇 + 대시보드.

---

## Phase 1 — 리마인더 봇 기반 구축

**목표:** 채널톡 Webhook 수신 → 메시지 파싱 → DB 저장 → 리마인더 자동 발송  
**완료 기준:** 팀챗에서 봇이 09:00 리마인더를 보내고, 23:00에 달성 요약이 자동 발송됨

### 1-1. 프로젝트 초기 세팅

- [ ] `backend/.env.example` 작성 (환경변수 목록 문서화)
  - `CHANNEL_ACCESS_KEY`, `CHANNEL_ACCESS_SECRET`
  - `ANTHROPIC_API_KEY`
  - `DATABASE_URL`
- [ ] `backend/main.py` — FastAPI 앱 기본 구조 작성
  - lifespan 이벤트 핸들러 (startup: scheduler 시작, shutdown: scheduler 종료)
  - CORS 미들웨어 설정
  - 라우터 등록 (`/webhook`, `/reports`)
- [ ] `backend/models.py` — Pydantic 모델 정의
  - `WebhookPayload` (채널톡 Webhook 수신 스키마)
  - `TaskItem`, `DailyReport` (파싱 결과 스키마)

### 1-2. DB 세팅

- [ ] Supabase 프로젝트 생성 + `DATABASE_URL` 발급
- [ ] `backend/database.py` — DB 연결 설정 (SQLAlchemy or `asyncpg`)
- [ ] 스키마 마이그레이션 실행
  ```sql
  members, categories, tasks, reports, completions
  ```
  (상세 스키마는 README.md §5 참고)
- [ ] 초기 멤버 데이터 시딩 (Charco, HYOM, EEEE 등)

### 1-3. 채널톡 연동

- [ ] 채널톡 개발자 콘솔에서 API 키 발급
- [ ] 공개 URL 확보
  - 개발 중: `ngrok http 8000` 으로 임시 URL 사용
  - 이후: Railway 또는 Render 배포로 영구 URL 확보
- [ ] 채널톡 Webhook 등록 (공개 URL + `/webhook` 경로)
- [ ] `backend/routes/webhook.py` 작성
  - `POST /webhook` 엔드포인트
  - 채널톡 서명 검증 (HMAC)
  - 메시지 타입 필터링 (`message` 이벤트만 처리)
  - 채널 필터링 (`2_Work_report` 채널만 처리)
  - 멤버 식별 (채널톡 유저 ID → `members` 테이블 매핑)
- [ ] `backend/channel_client.py` — 채널톡 API 클라이언트
  - `send_message(channel_id, text)` — 팀챗 메시지 발송
  - 주의: `actAsManager` 옵션은 팀챗에서 사용 불가 (422 에러)

### 1-4. 메시지 파서 1차 (규칙 기반)

- [ ] `backend/parser.py` — 규칙 기반 파서 구현
  - 업무계획 vs 업무보고 구분 (제목 패턴: `업무계획` / `업무보고`)
  - 완료 패턴 매칭: `[✅☑oO○ㅇ완료했다했음done]`
  - 미완료 패턴 매칭: `[☐✗xX미완못함못했skip]`
  - 불릿 기호 제거 (`•`, `-`, `*`)
  - 태스크명 클렌징 (완료 기호 제거 후 순수 태스크명 추출)
  - 신뢰도 계산 (파싱된 라인 수 / 전체 라인 수)
- [ ] 파서 단위 테스트 작성
  - 멤버별 실제 메시지 샘플 케이스 포함 (`세모`, `○`, `했음` 등)

### 1-5. 스케줄러

- [ ] `backend/scheduler.py` — APScheduler 설정
  - 09:00 잡: 아침 리마인더 발송
    ```
    📋 오늘 업무계획을 공유해주세요!
    형식: [날짜] [이름] 업무계획
    ```
  - 23:00 잡: 당일 리포트 집계 → 팀챗 고지
    ```
    📊 04.23 팀 달성 현황 (23:00 기준)
    Charco   ✅ 5/6  83%
    HYOM     ✅ 2/4  50%
    EEEE     ⚠️ 미제출
    팀 평균: 67%
    ```
  - 타임존: `Asia/Seoul`

---

## Phase 2 — 파서 고도화 + 집계 엔진

**목표:** 다양한 완료 표기 대응, 카테고리 매핑, 의미 있는 집계 데이터 축적  
**완료 기준:** 멤버마다 다른 표기법을 정확히 파싱하고 집계 데이터가 DB에 쌓임

### 2-1. 하이브리드 파서 (Claude API 폴백)

- [ ] `backend/parser.py` — Claude Haiku 폴백 추가
  - 규칙 기반 신뢰도 < 0.5 이면 Claude API 호출
  - 프롬프트: 완료/미완료 항목 JSON 추출
  - 모델: `claude-haiku-4-5` (건당 약 $0.0001)
- [ ] API 호출 로깅 (비용 추적용)
- [ ] 파서 통합 테스트 (규칙 기반 → 폴백 흐름 검증)

### 2-2. 태스크 카테고리 매핑

- [ ] 초기 카테고리 데이터 시딩
  - `운동` (러닝, 헬스, 홈트, 수영 등)
  - `어학` (듀오링고, 영어, 스페인어 등)
  - `독서/학습` (경제신문, 책 읽기, AI 스터디 등)
  - `루틴` (기타 반복 루틴)
- [ ] `backend/categorizer.py` — 카테고리 매핑 로직
  - 정확 매칭 → DB 조회
  - 유사도 매칭: `difflib.SequenceMatcher` 임계값 0.7
  - 매칭 실패 시 `미분류` 처리 후 로깅
- [ ] 어드민 CLI (`backend/cli.py`)
  - `python cli.py map "러닝" "운동"` — 수동 매핑 등록
  - `python cli.py list-unmapped` — 미분류 태스크 목록 확인

### 2-3. 집계 엔진

- [ ] `backend/aggregator.py`
  - 멤버별 일일 달성률 계산 (완료 수 / 전체 태스크 수)
  - 스트릭 계산 (연속 달성일 추적, 태스크별 + 멤버별)
  - 팀 평균 달성률 계산
  - 미제출 멤버 감지 (23:00 기준 `reports.submitted = FALSE`)
- [ ] `backend/routes/reports.py` — 대시보드용 REST API
  - `GET /reports/daily?date=2026-04-23` — 일간 리포트
  - `GET /reports/weekly?week=2026-W17` — 주간 리포트
  - `GET /reports/members/{member_id}/streak` — 멤버 스트릭

### 2-4. 저녁 집계 메시지 고도화

- [ ] 연속 달성 스트릭 강조 표시
  ```
  🔥 듀오링고 영어: 팀 전원 7일 연속 달성 중!
  ```
- [ ] 오늘 최다 달성 멤버 표시
- [ ] 미제출 멤버 별도 표기 + 부드러운 독려 문구

---

## Phase 3 — 대시보드 웹앱

**목표:** 시각화 대시보드 완성 및 배포  
**완료 기준:** 웹 URL로 팀 현황을 언제든 한눈에 확인 가능

### 3-1. 프론트엔드 초기 세팅

- [ ] `frontend/.env.local.example` 작성
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `NEXT_PUBLIC_API_BASE_URL`
- [ ] Supabase JS 클라이언트 설치 및 설정 (`@supabase/supabase-js`)
- [ ] Recharts 설치 (`recharts`)
- [ ] 공통 레이아웃 (`app/layout.tsx`) — 헤더, 뷰 전환 탭 (일간/주간/월간)
- [ ] 공통 타입 정의 (`types/index.ts`) — `Member`, `Report`, `Task`, `Streak`

### 3-2. 주요 컴포넌트 구현

- [ ] `components/StatCard.tsx` — 지표 카드
  - 팀 평균 달성률, 오늘 제출 현황 (n/4), 오늘 최다 완료 태스크, 이번 주 최고 달성자
- [ ] `components/MemberCard.tsx` — 오늘 멤버 카드
  - 멤버 이름, 달성률 (n/m, %)
  - 완료 ✅ / 미완료 ❌ 태스크 목록
  - 미제출 상태 표시
- [ ] `components/AchievementChart.tsx` — 멤버별 달성률 바 차트 (Recharts)
  - 주간 / 월간 전환
- [ ] `components/StreakChart.tsx` — 공통 루틴 스트릭 점 그래프
  - 7일치 ● / ○ 표시
  - 연속 달성일 수 표기
- [ ] `components/TaskTable.tsx` — 태스크별 팀 달성 현황 테이블
  - 카테고리 통합 표시 (운동: 헬스·러닝·홈트 드릴다운 가능)
  - 달성률, 완료 횟수, 상태 아이콘

### 3-3. 페이지 조립

- [ ] `app/page.tsx` — 대시보드 메인 페이지
  - Supabase 실시간 구독으로 멤버 카드 자동 갱신
  - 일간/주간/월간 뷰 상태 관리
  - 로딩 스켈레톤 UI

### 3-4. 배포

- [ ] 백엔드: Railway 또는 Render 배포
  - 환경변수 설정
  - 채널톡 Webhook URL을 영구 URL로 교체
- [ ] 프론트엔드: Vercel 배포
  - 환경변수 설정
  - 도메인 연결 (선택)

---

## 향후 확장 아이디어 (백로그)

- [ ] AI Work Report 자동 생성기 — 계획 메시지 입력 → 오늘/현황/내일 형식 자동 작성
- [ ] 주간 회고 자동 생성 — 장기 목표 대비 달성률 요약
- [ ] 게이미피케이션 — 달성 포인트, 멤버 랭킹, 월말 통계 리포트
- [ ] 멀티 채널 어댑터 — 슬랙 / 디스코드 / 텔레그램 지원
- [ ] 태스크 카테고리 자동 매핑 고도화 (Claude 임베딩 기반 의미 유사도)
