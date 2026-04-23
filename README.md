# unc-system

> 나와의 약속을 업무화하라.  
> 가상회사 프레임으로 팀의 일상 루틴을 자동으로 추적하고 시각화하는 시스템.

- **최초 기획:** 2026-04-23 (목)
- **GitHub:** `github.com/ChangkookChoi/unc-system` (private)
- **로컬 경로:** `~/workspace/unc-system`

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [배경 및 현재 운영 방식](#2-배경-및-현재-운영-방식)
3. [핵심 기능](#3-핵심-기능)
4. [디렉토리 구조](#4-디렉토리-구조)
5. [시스템 아키텍처](#5-시스템-아키텍처)
6. [개발 단계 (Phase)](#6-개발-단계-phase)
7. [기술 스택](#7-기술-스택)
8. [Quick Start (로컬 실행)](#8-quick-start-로컬-실행)
9. [메시지 파싱 전략](#9-메시지-파싱-전략)
10. [태스크 카테고리 설계](#10-태스크-카테고리-설계)
11. [채널 연동 전략](#11-채널-연동-전략)
12. [비용 구조](#12-비용-구조)
13. [대시보드 기획](#13-대시보드-기획)
14. [향후 확장 아이디어](#14-향후-확장-아이디어)
15. [참고 링크](#15-참고-링크)

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | unc-system |
| **컨셉** | 가상회사 프레임 — 개인/팀의 일상 루틴을 "업무"로 프레이밍해 실행력을 높임 |
| **목적** | 매일 팀챗에 올라오는 업무계획/보고를 자동 집계하고 달성률을 시각화 |
| **핵심 기능** | 스마트 리마인더 봇 + 팀 달성률 대시보드 |
| **대상 사용자** | 소규모 스터디/업무 팀 (현재 4명: Charco, HYOM, EEEE 등) |
| **플랫폼** | 채널톡 팀챗 (`2_Work_report` 채널) 연동 |

### 컨셉 배경

> *"스스로와의 약속엔 한없이 약해지는 당신, 나와의 약속을 업무화해보는 건 어때요?"*

기간 제한 없이, 가상회사의 직원처럼 매일 업무 계획을 수립하고 보고한다.
unc-system은 그 워크플로우를 자동화하고, 팀 전체의 달성 현황을 한눈에 볼 수 있게 만든다.

---

## 2. 배경 및 현재 운영 방식

### 현재 팀 워크플로우

팀원들은 매일 채널톡 팀챗 `2_Work_report` 채널에 아래 형식으로 업무를 공유한다.

**아침 — 업무 계획 공유**
```
04.23 Charco 업무계획
• 듀오링고 영어
• 경제신문 읽기
• 운동
• 독서 10분
• AI 스터디 목표 세우기
• 간단한 스터디 및 리포트
```

**저녁 — 업무 보고**
```
04.22 HYOM 업무보고
• 듀오링고 영어 ○
• 저녁 일정 ○
• 회사 짐 정리 (내일까지) 세모!!
```

**별도 Work Report 문서** (노션 / 구글 독스)

| 섹션 | 내용 |
|------|------|
| Today's Tasks | 오늘 할 일 목록 |
| Current Status | 완료(☑) / 미완료(☐) 체크 현황 |
| Tasks for Tomorrow | 내일 할 일 목록 |

### 현재 불편함

- 리포트 작성이 수동 → 반복적이고 번거로움
- 팀 전체 달성률을 한눈에 볼 수 없음
- 리마인더가 없어 보고를 잊는 경우 발생
- 완료 표기 방식이 멤버마다 다름 (`o`, `○`, `✅`, `했음`, `세모` 등)

---

## 3. 핵심 기능

### 기능 1 — 스마트 리마인더 봇

| 시간 | 동작 |
|------|------|
| 매일 09:00 | 팀챗에 업무 계획 작성 독려 메시지 발송 |
| 매일 23:00 | 당일 집계 후 팀 달성 현황 요약을 팀챗에 자동 고지 |

**저녁 고지 예시**
```
📊 04.23 팀 달성 현황 (23:00 기준)

Charco   ✅ 5/6  83%
HYOM     ✅ 2/4  50%
EEEE     ⚠️ 미제출

팀 평균: 67% | 오늘 최다 달성: Charco
🔥 듀오링고 영어: 팀 전원 7일 연속 달성 중!
```

### 기능 2 — 팀 달성률 대시보드

- 일간 / 주간 / 월간 뷰 전환
- 멤버별 달성률 바 차트
- 공통 루틴 연속 달성 스트릭 (GitHub 잔디 스타일)
- 태스크별 팀 달성 현황 테이블 (카테고리 통합 포함)
- 오늘 멤버 카드 (실시간 체크 현황)
- 리포트 미제출 멤버 표시

---

## 4. 디렉토리 구조

```
unc-system/
├── CLAUDE.md                  ← Claude Code 컨텍스트 파일 (루트 전체용)
├── README.md
├── .gitignore
│
├── backend/                   ← FastAPI 서버
│   ├── CLAUDE.md              ← 백엔드 전용 Claude 컨텍스트
│   ├── venv/                  ← Python 가상환경 (git 제외)
│   ├── requirements.txt
│   ├── main.py                ← FastAPI 앱 진입점
│   ├── scheduler.py           ← APScheduler 리마인더
│   ├── parser.py              ← 메시지 파서 (규칙 + Claude API)
│   ├── models.py              ← DB 모델
│   ├── routes/
│   │   ├── webhook.py         ← 채널톡 Webhook 수신
│   │   └── reports.py         ← 리포트 API
│   └── .env                   ← 환경변수 (git 제외)
│
└── frontend/                  ← Next.js 대시보드
    ├── CLAUDE.md              ← 프론트 전용 Claude 컨텍스트
    ├── app/
    │   ├── page.tsx           ← 대시보드 메인
    │   └── layout.tsx
    ├── components/
    │   ├── MemberCard.tsx
    │   ├── StreakChart.tsx
    │   └── TaskTable.tsx
    ├── package.json
    └── .env.local             ← 환경변수 (git 제외)
```

---

## 5. 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                채널톡 팀챗 (2_Work_report)                 │
│  멤버들이 매일 업무계획 / 업무보고 메시지 올림             │
└────────────────┬─────────────────────────────────────────┘
                 │ Webhook POST 이벤트
                 ▼
┌──────────────────────────────────────────────────────────┐
│                   백엔드 서버 (FastAPI)                    │
│                                                           │
│  ┌──────────────────┐   ┌──────────────────────────────┐ │
│  │  Webhook 수신기   │   │  스케줄러 (APScheduler)       │ │
│  │  POST /webhook   │   │  09:00 → 아침 리마인더 발송   │ │
│  └────────┬─────────┘   │  23:00 → 저녁 집계 + 고지    │ │
│           │             └──────────────┬─────────────────┘ │
│           ▼                            │                   │
│  ┌──────────────────┐                  │                   │
│  │   메시지 파서     │                  │                   │
│  │  1차: 규칙 기반   │                  │                   │
│  │  2차: Claude API │                  │                   │
│  └────────┬─────────┘                  │                   │
│           │                            │                   │
│           ▼                            ▼                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                  태스크 집계 엔진                     │  │
│  │  - 멤버별 완료 / 미완료 항목 정리                     │  │
│  │  - 태스크 카테고리 매핑 (러닝 / 헬스 → 운동)          │  │
│  │  - 달성률 계산 및 스트릭 갱신                         │  │
│  └──────────────────────┬──────────────────────────────┘  │
└─────────────────────────┼──────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │  채널톡 API  │  │  대시보드    │
│  (Supabase)  │  │  메시지 발송 │  │  (Next.js)   │
│              │  │  리마인더    │  │              │
│  members     │  │  달성 고지   │  │  차트 / 스트릭│
│  tasks       │  └──────────────┘  │  멤버 현황   │
│  reports     │                    └──────────────┘
│  completions │
│  categories  │
└──────────────┘
```

### DB 스키마 (초안)

```sql
-- 멤버
CREATE TABLE members (
  id       SERIAL PRIMARY KEY,
  name     TEXT NOT NULL,
  chat_id  TEXT UNIQUE           -- 채널톡 유저 ID
);

-- 태스크 카테고리 (운동, 어학, 독서/학습 등)
CREATE TABLE categories (
  id    SERIAL PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE
);

-- 원본 태스크 (멤버가 입력한 그대로 보존)
CREATE TABLE tasks (
  id           SERIAL PRIMARY KEY,
  raw_name     TEXT NOT NULL,                   -- "러닝", "헬스" 등 원본
  category_id  INT REFERENCES categories(id),   -- → "운동"
  member_id    INT REFERENCES members(id)
);

-- 일일 리포트
CREATE TABLE reports (
  id           SERIAL PRIMARY KEY,
  member_id    INT REFERENCES members(id),
  report_date  DATE NOT NULL,
  submitted    BOOLEAN DEFAULT FALSE,
  submitted_at TIMESTAMPTZ
);

-- 태스크 완료 기록
CREATE TABLE completions (
  id          SERIAL PRIMARY KEY,
  report_id   INT REFERENCES reports(id),
  task_id     INT REFERENCES tasks(id),
  is_done     BOOLEAN NOT NULL,
  raw_status  TEXT    -- 원본 표기 ("o", "✅", "했음" 등) 보존
);
```

---

## 6. 개발 단계 (Phase)

### Phase 1 — 리마인더 봇 기반 구축 `(예상 2~3주)`

**목표:** 채널톡 Webhook 연동 → 메시지 수신 → DB 저장 → 리마인더 발송

- [ ] FastAPI 서버 기본 구조 세팅
- [ ] 채널톡 API 키 발급 및 Webhook 등록
- [ ] 공개 URL 확보 (Railway / Render 배포 또는 ngrok 임시)
- [ ] Webhook 수신 → 멤버 식별 → DB 저장 파이프라인
- [ ] 규칙 기반 파서 1차 구현 (완료/미완료 기호 패턴 매칭)
- [ ] APScheduler — 09:00 아침 리마인더 발송
- [ ] APScheduler — 23:00 집계 후 팀챗 고지

**완료 기준:** 팀챗에서 봇이 리마인더를 보내고, 저녁에 달성 요약이 자동 발송됨

---

### Phase 2 — 파서 고도화 + 집계 엔진 `(예상 2주)`

**목표:** 다양한 표기 대응, 태스크 카테고리 매핑 완성

- [ ] 하이브리드 파서 구현 (규칙 기반 → 신뢰도 낮으면 Claude API 폴백)
- [ ] 태스크 카테고리 매핑 테이블 초기 세팅
- [ ] 어드민 CLI — 수동 카테고리 매핑 관리
- [ ] 달성률 계산 로직 완성
- [ ] 스트릭 계산 로직 (연속 달성일 추적)
- [ ] 저녁 집계 메시지 포맷 고도화

**완료 기준:** 멤버마다 다른 표기법을 정확히 파싱하고, 의미 있는 집계 데이터가 DB에 쌓임

---

### Phase 3 — 대시보드 웹앱 `(예상 3주)`

**목표:** 시각화 대시보드 완성 및 배포

- [ ] Supabase 연동 (실시간 데이터 구독)
- [ ] 멤버별 달성률 바 차트 (Recharts)
- [ ] 공통 루틴 스트릭 시각화 (점 그래프)
- [ ] 일간 / 주간 / 월간 뷰 전환
- [ ] 오늘 멤버 카드 (실시간 체크 현황)
- [ ] 태스크별 팀 달성 현황 테이블 (카테고리 통합 표시)
- [ ] Vercel 배포

**완료 기준:** 웹 URL로 언제든 팀 현황을 한눈에 확인 가능

---

## 7. 기술 스택

| 영역 | 기술 | 선택 이유 |
|------|------|-----------|
| **백엔드** | Python 3.11 + FastAPI | 빠른 개발, Anthropic SDK 포함 AI 라이브러리 풍부, 비동기 지원 |
| **스케줄러** | APScheduler | FastAPI 내장, 시간 기반 리마인더 발송에 적합 |
| **DB** | PostgreSQL (Supabase) | 무료 호스팅, 실시간 구독, Next.js 연동 쉬움 |
| **AI 파싱** | Claude API — Haiku 모델 | 자연어 완료 표기 추출, 건당 약 $0.0001로 매우 저렴 |
| **대시보드** | Next.js 14 (App Router) + Recharts | Vercel 배포 간편, 차트 라이브러리 풍부 |
| **서버 배포** | Railway 또는 Render | 무료 플랜으로 시작 가능 |
| **채널 연동** | 채널톡 Open API v5 | 팀이 현재 사용 중인 플랫폼 |

---

## 8. Quick Start (로컬 실행)

### 사전 요구사항

- Python 3.11+
- Node.js 18+
- Git

### 백엔드 실행

```bash
cd ~/workspace/unc-system/backend

# 가상환경 활성화
source venv/bin/activate

# 환경변수 설정
cp .env.example .env
# .env 파일에 아래 값 입력

# 서버 실행
uvicorn main:app --reload --port 8000
```

### 프론트엔드 실행

```bash
cd ~/workspace/unc-system/frontend

# 환경변수 설정
cp .env.local.example .env.local

# 패키지 설치 및 실행
npm install
npm run dev
# → http://localhost:3000
```

### 환경변수 목록

| 변수명 | 설명 | 위치 |
|--------|------|------|
| `CHANNEL_ACCESS_KEY` | 채널톡 API 키 | backend/.env |
| `CHANNEL_ACCESS_SECRET` | 채널톡 API 시크릿 | backend/.env |
| `ANTHROPIC_API_KEY` | Claude API 키 | backend/.env |
| `DATABASE_URL` | Supabase PostgreSQL URL | backend/.env |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase 프로젝트 URL | frontend/.env.local |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon 키 | frontend/.env.local |

---

## 9. 메시지 파싱 전략

멤버마다 완료 표기 방식이 달라 3단계 하이브리드 파서를 사용한다.

### 방법 A — 규칙 기반 파싱 (1차, 무료)

```python
import re

DONE_PATTERNS = r'[✅☑oO○ㅇ]|완료|\(o\)|했다|했음|done|완'
MISS_PATTERNS = r'[☐✗xX]|미완|\(x\)|못함|못했|skip'

def parse_report(text: str) -> dict:
    done, todo = [], []
    for line in text.strip().split('\n'):
        line = line.strip().lstrip('•-* ')
        if not line:
            continue
        if re.search(DONE_PATTERNS, line, re.IGNORECASE):
            done.append(clean_task_name(line))
        else:
            todo.append(clean_task_name(line))
    return {"done": done, "todo": todo}
```

### 방법 B — Claude API 폴백 (신뢰도 낮을 때)

```python
async def parse_with_claude(message: str) -> dict:
    prompt = f"""
다음 업무 보고 메시지에서 완료된 항목과 미완료된 항목을 JSON으로만 추출해줘.
완료 표시: ✅ o ○ ㅇ 체크표시 "했다" "완료" "done" 등
미완료: ☐ x 아무 표시 없는 항목 등

메시지:
{message}

응답은 반드시 아래 JSON 형식만:
{{"done": ["항목1", "항목2"], "todo": ["항목3"]}}
"""
    # Claude Haiku 호출 — 건당 약 $0.0001
```

### 방법 C — 하이브리드 흐름 (최종 전략)

```
메시지 수신
    │
    ▼
규칙 기반 파싱
    │
    ├─ 신뢰도 높음 (패턴 매칭 50% 이상) → DB 저장
    │
    └─ 신뢰도 낮음 (패턴 매칭 50% 미만) → Claude API 폴백 → DB 저장
```

---

## 10. 태스크 카테고리 설계

### 핵심 원칙

> **원본 데이터는 절대 버리지 않는다.**  
> 대시보드 표시 시에만 카테고리로 집계하고, 드릴다운으로 원본도 볼 수 있게 유지한다.

### 매핑 예시

```
원본 태스크        카테고리
──────────────    ──────────────
"러닝"        →   운동
"헬스"        →   운동
"홈트"        →   운동
"듀오링고"    →   어학
"스페인어"    →   어학
"경제신문"    →   독서 / 학습
"책 읽기"     →   독서 / 학습
```

### 카테고리 매핑 단계별 전략

**Phase 1~2: 수동 관리 테이블**
- 관리자가 직접 `러닝 → 운동` 매핑 설정
- CLI 또는 간단한 어드민 페이지

**Phase 3+: 유사도 기반 자동 매핑**
- 신규 태스크 입력 시 기존 카테고리와 유사도 계산
- `difflib.SequenceMatcher` 사용, 임계값 0.7 이상이면 자동 매핑

**선택 사항: Claude API 임베딩**
- 의미적 유사성 기반 자동 그룹핑
- 구현 복잡도가 높아 안정화 이후 검토

---

## 11. 채널 연동 전략

### 채널톡 연동 (현재 팀 사용 플랫폼)

| 항목 | 내용 |
|------|------|
| Webhook 수신 | Open API v5 — `POST /open/v5/webhooks` |
| 봇 메시지 발송 | `POST /open/v5/messages` |
| 주의사항 | `actAsManager` 옵션 팀챗에서 사용 불가 (422 에러) |
| 공개 URL 필요 | Railway / Render 또는 ngrok (개발 중) |
| API 문서 | https://developers.channel.io |

### 대안 플랫폼 비교

| 플랫폼 | 봇 개발 난이도 | 무료 | 비고 |
|--------|-------------|------|------|
| **슬랙** | ⭐ 쉬움 | 무료 플랜 있음 | Bot API 문서 최고 수준 |
| **디스코드** | ⭐ 쉬움 | 완전 무료 | 개발자 친화적 |
| **텔레그램** | ⭐⭐ 보통 | 완전 무료 | 소규모 팀에 최적 |
| **채널톡** | ⭐⭐⭐ 어려움 | 유료 플랜 확인 필요 | 기존 사용 중이면 연동 가치 있음 |

---

## 12. 비용 구조

| 항목 | 월 예상 비용 | 비고 |
|------|------------|------|
| **Claude API (Haiku)** | $1 ~ $5 | 파싱 폴백 용도, 건당 $0.0001 |
| **서버 호스팅 (Railway/Render)** | 무료 ~ $5 | 무료 플랜으로 시작 |
| **DB (Supabase)** | 무료 | 무료 플랜 500MB — 4인 팀에 충분 |
| **대시보드 배포 (Vercel)** | 무료 | 무료 플랜으로 충분 |
| **채널톡** | 현재 요금제 따름 | API 사용 시 유료 플랜 확인 필요 |

> **초기 운영 비용: 월 $1~5 수준. Claude API 외에는 무료.**

---

## 13. 대시보드 기획

### 화면 구성

```
┌──────────────────────────────────────────────────────────────┐
│  unc-system                          [일간] [주간] [월간]     │
│  2026.04.23 기준 · 23:00 집계                                │
├──────────┬──────────┬────────────┬──────────────────────────┤
│ 팀 평균  │ 오늘 제출 │ 최다 완료  │ 이번 주 최고 달성자       │
│ 달성률   │ 현황      │ 태스크     │                           │
│  73%     │  3 / 4   │ 듀오링고   │  Charco 86%               │
├──────────┴──────────┴────────────┴──────────────────────────┤
│  오늘 현황 (04.23)                         집계: 23:00        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ Charco   │  │ HYOM     │  │ EEEE     │                   │
│  │ 5/6  83% │  │ 2/4  50% │  │  미제출  │                   │
│  │ ✅듀오링고│  │ ✅짐싸기  │  │          │                   │
│  │ ❌운동   │  │ ❌대청소  │  │          │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
├──────────────────────┬───────────────────────────────────────┤
│ 멤버별 주간 달성률    │ 공통 루틴 스트릭                       │
│ Charco  ██████  86% │ 듀오링고  ●●●●●●●  7일 연속            │
│ HYOM    █████   72% │ 운동      ●○●●○●○  2일 연속            │
│ EEEE    ████    68% │ 독서      ●●○●●●○  4일 연속            │
├──────────────────────┴───────────────────────────────────────┤
│ 태스크별 팀 달성 현황 (이번 주)                                │
│ 듀오링고                 75%   21/28회  ✅ 완료 빈도 높음     │
│ 운동 (헬스·러닝 통합)    64%   18/28회  ✅ 꾸준함             │
│ AI 스터디 목표 세우기    43%   12/28회  ⚠️ 가끔 누락          │
└──────────────────────────────────────────────────────────────┘
```

### 주요 컴포넌트

| 컴포넌트 | 설명 |
|----------|------|
| 지표 카드 | 팀 평균 달성률, 오늘 제출 현황, 최고 달성자 |
| 오늘 멤버 카드 | 각 멤버의 태스크 완료 현황 실시간 표시 |
| 멤버별 달성률 바 차트 | 주간 / 월간 달성률 비교 |
| 스트릭 점 그래프 | 7일치 연속 달성 여부 |
| 태스크 달성 테이블 | 카테고리 통합 후 완료 횟수 및 달성률 |

---

## 14. 향후 확장 아이디어

1. **AI Work Report 자동 생성기** — 계획 메시지 입력 → 오늘/현황/내일 형식 자동 생성
2. **목표 트래킹 & 회고 생성기** — 장기 목표를 주 단위로 분해하고 주간 회고 자동 생성
3. **게이미피케이션** — 달성 포인트, 멤버 간 랭킹, 월말 통계 리포트
4. **멀티 채널 어댑터** — 슬랙 / 디스코드 / 텔레그램 플랫폼 독립 지원
5. **모바일 앱** — 리포트 제출 및 체크 전용 경량 앱

---

## 15. 참고 링크

| 항목 | URL |
|------|-----|
| 채널톡 개발자 문서 | https://developers.channel.io |
| 채널톡 Webhook API | https://developers.channel.io/docs/create-a-webhook-1 |
| Anthropic Claude API | https://docs.anthropic.com |
| Supabase 시작하기 | https://supabase.com/docs |
| FastAPI 공식 문서 | https://fastapi.tiangolo.com |
| APScheduler 문서 | https://apscheduler.readthedocs.io |
| Next.js 공식 문서 | https://nextjs.org/docs |
| Recharts | https://recharts.org |

---

*최초 작성: 2026-04-23 (목) — Claude AI와의 기획 대화 기반*  
*마지막 업데이트: 2026-04-23 (목)*