-- 업무 카테고리 추가
INSERT INTO categories (name) VALUES ('업무'), ('기타')
ON CONFLICT (name) DO NOTHING;

-- 태스크명 → 카테고리 전역 매핑 테이블
CREATE TABLE IF NOT EXISTS task_mappings (
  id          SERIAL PRIMARY KEY,
  clean_name  TEXT NOT NULL UNIQUE,
  category_id INT NOT NULL REFERENCES categories(id),
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- 초기 매핑 시딩
-- (category_id는 서브쿼리로 categories 테이블에서 조회)

-- 운동
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('운동',              (SELECT id FROM categories WHERE name='운동')),
  ('헬스',              (SELECT id FROM categories WHERE name='운동')),
  ('홈트',              (SELECT id FROM categories WHERE name='운동')),
  ('러닝',              (SELECT id FROM categories WHERE name='운동')),
  ('PT 가기',           (SELECT id FROM categories WHERE name='운동')),
  ('개인운동',           (SELECT id FROM categories WHERE name='운동')),
  ('개인 운동',          (SELECT id FROM categories WHERE name='운동')),
  ('개인운동 30분+',     (SELECT id FROM categories WHERE name='운동')),
  ('등산',              (SELECT id FROM categories WHERE name='운동')),
  ('자전거 출퇴근',      (SELECT id FROM categories WHERE name='운동'))
ON CONFLICT (clean_name) DO NOTHING;

-- 어학
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('듀오링고 영어',            (SELECT id FROM categories WHERE name='어학')),
  ('듀오링고 일본어',          (SELECT id FROM categories WHERE name='어학')),
  ('듀오링고 스페인어',        (SELECT id FROM categories WHERE name='어학')),
  ('듀오링고 일본어 / 스페인어',(SELECT id FROM categories WHERE name='어학')),
  ('듀오링고영어',             (SELECT id FROM categories WHERE name='어학')),
  ('듀오잉고 스페인어',        (SELECT id FROM categories WHERE name='어학')),
  ('말해보카',                 (SELECT id FROM categories WHERE name='어학')),
  ('N5 공부',                  (SELECT id FROM categories WHERE name='어학')),
  ('영어 회화',                (SELECT id FROM categories WHERE name='어학')),
  ('영어회화',                 (SELECT id FROM categories WHERE name='어학')),
  ('영어회화 가기',            (SELECT id FROM categories WHERE name='어학')),
  ('영어회화 모임 참석',       (SELECT id FROM categories WHERE name='어학')),
  ('오픽 공부',                (SELECT id FROM categories WHERE name='어학')),
  ('아이엘츠 공부',            (SELECT id FROM categories WHERE name='어학')),
  ('가타카나 외우기',          (SELECT id FROM categories WHERE name='어학'))
ON CONFLICT (clean_name) DO NOTHING;

-- 독서/학습
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('경제신문 읽기',            (SELECT id FROM categories WHERE name='독서/학습')),
  ('독서',                     (SELECT id FROM categories WHERE name='독서/학습')),
  ('책 읽기',                  (SELECT id FROM categories WHERE name='독서/학습')),
  ('책읽기',                   (SELECT id FROM categories WHERE name='독서/학습')),
  ('책 20p',                   (SELECT id FROM categories WHERE name='독서/학습')),
  ('독서 10분',                (SELECT id FROM categories WHERE name='독서/학습')),
  ('AI 스터디',                (SELECT id FROM categories WHERE name='독서/학습')),
  ('AI 개인 스터디',           (SELECT id FROM categories WHERE name='독서/학습')),
  ('AI 스터디 가기',           (SELECT id FROM categories WHERE name='독서/학습')),
  ('AI 스터디 출석',           (SELECT id FROM categories WHERE name='독서/학습')),
  ('AI 모임 가기',             (SELECT id FROM categories WHERE name='독서/학습')),
  ('모닝 경제 노트',           (SELECT id FROM categories WHERE name='독서/학습')),
  ('한 주 경제 정리',          (SELECT id FROM categories WHERE name='독서/학습')),
  ('앰플 상페 읽기',           (SELECT id FROM categories WHERE name='독서/학습')),
  ('영상공부',                 (SELECT id FROM categories WHERE name='독서/학습')),
  ('영상 공부 (카메라 편)',     (SELECT id FROM categories WHERE name='독서/학습')),
  ('간단한 스터디 및 리포트',  (SELECT id FROM categories WHERE name='독서/학습'))
ON CONFLICT (clean_name) DO NOTHING;

-- 루틴
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('영양제 먹기',                      (SELECT id FROM categories WHERE name='루틴')),
  ('영양제 복용',                      (SELECT id FROM categories WHERE name='루틴')),
  ('영양제먹기',                       (SELECT id FROM categories WHERE name='루틴')),
  ('영양제/위염약 복용',               (SELECT id FROM categories WHERE name='루틴')),
  ('위염약 복용',                      (SELECT id FROM categories WHERE name='루틴')),
  ('유산균 챙겨먹기',                  (SELECT id FROM categories WHERE name='루틴')),
  ('금연',                             (SELECT id FROM categories WHERE name='루틴')),
  ('대청소',                           (SELECT id FROM categories WHERE name='루틴')),
  ('집 청소',                          (SELECT id FROM categories WHERE name='루틴')),
  ('집청소',                           (SELECT id FROM categories WHERE name='루틴')),
  ('집 대청소',                        (SELECT id FROM categories WHERE name='루틴')),
  ('간단한 청소',                      (SELECT id FROM categories WHERE name='루틴')),
  ('빨래하기',                         (SELECT id FROM categories WHERE name='루틴')),
  ('이불 빨래',                        (SELECT id FROM categories WHERE name='루틴')),
  ('침구 빨래',                        (SELECT id FROM categories WHERE name='루틴')),
  ('장보기',                           (SELECT id FROM categories WHERE name='루틴')),
  ('이마트 장보기',                    (SELECT id FROM categories WHERE name='루틴')),
  ('저녁밥 해먹기',                    (SELECT id FROM categories WHERE name='루틴')),
  ('도시락 먹기',                      (SELECT id FROM categories WHERE name='루틴')),
  ('세차',                             (SELECT id FROM categories WHERE name='루틴')),
  ('다이어리 작성',                    (SELECT id FROM categories WHERE name='루틴')),
  ('다이어리 작성 및 주간 , 월간 계획 수립', (SELECT id FROM categories WHERE name='루틴')),
  ('옷방 정리',                        (SELECT id FROM categories WHERE name='루틴')),
  ('겨울옷 정리 여름옷 정리',          (SELECT id FROM categories WHERE name='루틴')),
  ('쓰레기 분리수거',                  (SELECT id FROM categories WHERE name='루틴')),
  ('반찬 및 식자재 소분',              (SELECT id FROM categories WHERE name='루틴')),
  ('경제루틴',                         (SELECT id FROM categories WHERE name='루틴')),
  ('집 정리',                          (SELECT id FROM categories WHERE name='루틴')),
  ('집안 업무',                        (SELECT id FROM categories WHERE name='루틴'))
ON CONFLICT (clean_name) DO NOTHING;

-- 업무
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('위클리 리포트',                        (SELECT id FROM categories WHERE name='업무')),
  ('기획서 작성',                          (SELECT id FROM categories WHERE name='업무')),
  ('계획서 작성',                          (SELECT id FROM categories WHERE name='업무')),
  ('블로그',                               (SELECT id FROM categories WHERE name='업무')),
  ('콘텐츠 설계자',                        (SELECT id FROM categories WHERE name='업무')),
  ('콘텐츠설계자',                         (SELECT id FROM categories WHERE name='업무')),
  ('개인 SNS 콘텐츠 제작',                 (SELECT id FROM categories WHERE name='업무')),
  ('개인 sns 콘텐츠 제작',                 (SELECT id FROM categories WHERE name='업무')),
  ('개인 SNS 콘텐츠 레퍼런스 서치',       (SELECT id FROM categories WHERE name='업무')),
  ('힉스필드 이미지 제작',                 (SELECT id FROM categories WHERE name='업무')),
  ('힉스필드 이미지 / 영상 제작 및 편집', (SELECT id FROM categories WHERE name='업무')),
  ('포폴 자기소개 및 시디부분 업데이트',   (SELECT id FROM categories WHERE name='업무')),
  ('포폴용 영상 제작',                     (SELECT id FROM categories WHERE name='업무')),
  ('포폴용 스토리보드 스케치',             (SELECT id FROM categories WHERE name='업무')),
  ('포폴용 연출 레퍼런스 서치',            (SELECT id FROM categories WHERE name='업무')),
  ('포폴용 영상 자막 편집',               (SELECT id FROM categories WHERE name='업무')),
  ('소재 만들기',                          (SELECT id FROM categories WHERE name='업무')),
  ('소재 제작',                            (SELECT id FROM categories WHERE name='업무')),
  ('광고셋팅',                             (SELECT id FROM categories WHERE name='업무')),
  ('매출 시트 등록',                       (SELECT id FROM categories WHERE name='업무')),
  ('메일 확인',                            (SELECT id FROM categories WHERE name='업무')),
  ('메일 회신',                            (SELECT id FROM categories WHERE name='업무')),
  ('외주 소통',                            (SELECT id FROM categories WHERE name='업무')),
  ('변리업무 진행시작 하기',               (SELECT id FROM categories WHERE name='업무')),
  ('변리사 개인사업자 등록 알아보기',      (SELECT id FROM categories WHERE name='업무')),
  ('Ai 생성물 베타테스트',                 (SELECT id FROM categories WHERE name='업무')),
  ('클로드 실험',                          (SELECT id FROM categories WHERE name='업무')),
  ('AI 스터디 목표 세우기',               (SELECT id FROM categories WHERE name='업무')),
  ('오퍼레터 회신',                        (SELECT id FROM categories WHERE name='업무')),
  ('인계자료 / 퇴직 품의 진행 마무리',    (SELECT id FROM categories WHERE name='업무')),
  ('마무리 콘텐츠 만들기',                 (SELECT id FROM categories WHERE name='업무')),
  ('퇴직 메일 작성',                       (SELECT id FROM categories WHERE name='업무')),
  ('패키지 디자인 시안 3종 제작',          (SELECT id FROM categories WHERE name='업무')),
  ('메타용 광고 기획 및 제작',             (SELECT id FROM categories WHERE name='업무')),
  ('펀딩 알람신청자 공지 메세지 발송',     (SELECT id FROM categories WHERE name='업무')),
  ('텀블벅 메세지 발송',                   (SELECT id FROM categories WHERE name='업무')),
  ('스마트스토어 상세페이지 제작',         (SELECT id FROM categories WHERE name='업무')),
  ('상세페이지 제작',                      (SELECT id FROM categories WHERE name='업무')),
  ('포스터 컨셉 주제 알아보기',            (SELECT id FROM categories WHERE name='업무')),
  ('일본 각종 브랜드 인스타/웹사이트 서치',(SELECT id FROM categories WHERE name='업무')),
  ('일본 포폴용 광고 영상 제작',           (SELECT id FROM categories WHERE name='업무')),
  ('영상 생성 연습',                       (SELECT id FROM categories WHERE name='업무'))
ON CONFLICT (clean_name) DO NOTHING;

-- 기타
INSERT INTO task_mappings (clean_name, category_id) VALUES
  ('저녁 약속',              (SELECT id FROM categories WHERE name='기타')),
  ('저녁 일정',              (SELECT id FROM categories WHERE name='기타')),
  ('오후일정',               (SELECT id FROM categories WHERE name='기타')),
  ('오후 일정',              (SELECT id FROM categories WHERE name='기타')),
  ('외부일정',               (SELECT id FROM categories WHERE name='기타')),
  ('개인 약속',              (SELECT id FROM categories WHERE name='기타')),
  ('전시회',                 (SELECT id FROM categories WHERE name='기타')),
  ('가족 나들이',            (SELECT id FROM categories WHERE name='기타')),
  ('장례식장 방문',          (SELECT id FROM categories WHERE name='기타')),
  ('본가다녀오기',           (SELECT id FROM categories WHERE name='기타')),
  ('시댁 다녀오기',          (SELECT id FROM categories WHERE name='기타')),
  ('점심 친구 만나기',       (SELECT id FROM categories WHERE name='기타')),
  ('짐싸기',                 (SELECT id FROM categories WHERE name='기타')),
  ('여권 찾기',              (SELECT id FROM categories WHERE name='기타')),
  ('항공권 서치',            (SELECT id FROM categories WHERE name='기타')),
  ('항공권 / 숙소 예약',     (SELECT id FROM categories WHERE name='기타')),
  ('여행 계획 세우기',       (SELECT id FROM categories WHERE name='기타')),
  ('차 서류 제출',           (SELECT id FROM categories WHERE name='기타')),
  ('자전거 수리점 방문',     (SELECT id FROM categories WHERE name='기타')),
  ('한의원 다녀오기',        (SELECT id FROM categories WHERE name='기타')),
  ('혼주 한복 업체 정하기',  (SELECT id FROM categories WHERE name='기타')),
  ('촬영복 구매',            (SELECT id FROM categories WHERE name='기타')),
  ('JLPT 원서 접수',         (SELECT id FROM categories WHERE name='기타')),
  ('교육 1건 수료',          (SELECT id FROM categories WHERE name='기타')),
  ('테스트 면접',            (SELECT id FROM categories WHERE name='기타')),
  ('보건소',                 (SELECT id FROM categories WHERE name='기타')),
  ('깨비 병원 방문',         (SELECT id FROM categories WHERE name='기타')),
  ('정기검사 받고 오기',     (SELECT id FROM categories WHERE name='기타')),
  ('책 대여',                (SELECT id FROM categories WHERE name='기타')),
  ('나물 만들기',            (SELECT id FROM categories WHERE name='기타')),
  ('AI 모임 가기',           (SELECT id FROM categories WHERE name='기타'))
ON CONFLICT (clean_name) DO NOTHING;
