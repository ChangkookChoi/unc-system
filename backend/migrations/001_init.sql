-- unc-system 초기 스키마

CREATE TABLE IF NOT EXISTS members (
  id       SERIAL PRIMARY KEY,
  name     TEXT NOT NULL,
  chat_id  TEXT UNIQUE  -- 채널톡 유저 ID
);

CREATE TABLE IF NOT EXISTS categories (
  id    SERIAL PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks (
  id           SERIAL PRIMARY KEY,
  raw_name     TEXT NOT NULL,
  category_id  INT REFERENCES categories(id),
  member_id    INT REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS reports (
  id           SERIAL PRIMARY KEY,
  member_id    INT REFERENCES members(id),
  report_date  DATE NOT NULL,
  report_type  TEXT NOT NULL DEFAULT 'report',  -- 'plan' | 'report'
  submitted    BOOLEAN NOT NULL DEFAULT FALSE,
  submitted_at TIMESTAMPTZ,
  UNIQUE (member_id, report_date, report_type)
);

CREATE TABLE IF NOT EXISTS completions (
  id          SERIAL PRIMARY KEY,
  report_id   INT REFERENCES reports(id),
  task_id     INT REFERENCES tasks(id),
  is_done     BOOLEAN NOT NULL,
  raw_status  TEXT  -- 원본 완료 표기 보존 ("o", "✅", "했음" 등)
);

-- 초기 카테고리 시딩
INSERT INTO categories (name) VALUES
  ('운동'),
  ('어학'),
  ('독서/학습'),
  ('루틴')
ON CONFLICT (name) DO NOTHING;

-- 초기 멤버 시딩
INSERT INTO members (name) VALUES
  ('Charco'),
  ('HYOM'),
  ('EEEE')
ON CONFLICT DO NOTHING;
