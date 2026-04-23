# unc-system — Claude Code 컨텍스트

## 프로젝트 한 줄 요약

가상회사 프레임으로 팀의 일상 루틴을 업무화하고, 자동 집계 + 시각화하는 시스템.

## 컨셉

> "나와의 약속을 업무화하라."

기간 제한 없이, 팀원들이 매일 채널톡에 업무계획/보고를 올린다.
이 시스템은 그 메시지를 자동으로 파싱 · 집계하고, 대시보드로 시각화한다.

## 프로젝트 구조

```
unc-system/
├── backend/        FastAPI 서버 (리마인더 봇, Webhook 수신, 파서, 집계 엔진)
└── frontend/       Next.js 대시보드 (달성률, 스트릭, 멤버 현황)
```

## 현재 개발 단계

- **Phase 1 진행 중** — 리마인더 봇 기반 구축
  - 채널톡 Webhook 수신 서버 (FastAPI)
  - 규칙 기반 메시지 파서 (완료/미완료 항목 추출)
  - APScheduler — 09:00 리마인더, 23:00 집계 고지

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Python 3.11 + FastAPI + uvicorn |
| 스케줄러 | APScheduler |
| DB | PostgreSQL (Supabase) |
| AI 파싱 폴백 | Anthropic Claude API — Haiku 모델 |
| 대시보드 | Next.js 16.2.4 + React 19 + TypeScript + Tailwind CSS 4 |
| 차트 | Recharts (Phase 3에서 설치 예정) |
| 채널 연동 | 채널톡 Open API v5 |

## 핵심 설계 원칙

1. **원본 데이터 보존** — 멤버가 입력한 태스크명을 절대 덮어쓰지 않는다. 카테고리 매핑은 별도 테이블로 관리하고 집계 시에만 사용한다.

2. **파싱 우선순위** — 규칙 기반 파서를 먼저 실행하고, 신뢰도가 낮을 때만 Claude API를 호출한다. Claude API는 폴백이지 기본이 아니다.

3. **채널톡 Webhook 주의사항** — `actAsManager` 옵션은 팀챗에서 422 에러 발생. 사용 금지.

4. **환경변수는 절대 하드코딩 금지** — 모든 키/시크릿은 `.env` 파일에서만 관리.

## 메시지 포맷 예시

**업무계획 (아침)**
```
04.23 Charco 업무계획
• 듀오링고 영어
• 운동
• 독서 10분
```

**업무보고 (저녁)**
```
04.23 Charco 업무보고
• 듀오링고 영어 ○
• 운동 x
• 독서 10분 ✅
```

## 완료 표기 패턴 (파서 참고)

완료로 인식: `o`, `O`, `○`, `ㅇ`, `✅`, `☑`, `완료`, `했다`, `했음`, `done`
미완료로 인식: `x`, `X`, `✗`, `☐`, `미완`, `못함`, `못했`, `skip`
표기 없으면: 미완료로 처리

## 개발 명령어

```bash
# 백엔드 실행
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# 프론트엔드 실행
cd frontend && npm run dev

# 백엔드 패키지 추가
cd backend && source venv/bin/activate && pip install {패키지명} && pip freeze > requirements.txt
```

## 코드 스타일 규칙

- Python: 함수명/변수명 snake_case, 클래스명 PascalCase
- TypeScript: 컴포넌트명 PascalCase, 함수/변수 camelCase
- 커밋 메시지: `type: 설명` 형식 (`feat:`, `fix:`, `chore:`, `docs:`)
- 주석은 한국어로 작성

## 참고 문서

- 전체 기획: `README.md`
- 개발 태스크 목록: `TODO.md`
- 채널톡 API: https://developers.channel.io
- Anthropic API: https://docs.anthropic.com