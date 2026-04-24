-- tasks: (raw_name, member_id) 중복 방지
ALTER TABLE tasks
  ADD CONSTRAINT uq_tasks_raw_name_member UNIQUE (raw_name, member_id);

-- completions: 동일 report에 동일 task 중복 방지
ALTER TABLE completions
  ADD CONSTRAINT uq_completions_report_task UNIQUE (report_id, task_id);

-- completions: is_comment 컬럼 추가 (계획에 없던 항목 표시)
ALTER TABLE completions
  ADD COLUMN IF NOT EXISTS is_comment BOOLEAN NOT NULL DEFAULT FALSE;
