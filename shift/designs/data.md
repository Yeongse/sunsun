# Worker
- id
- name(姓名, スペース無し)
- email
- password(hash化したものを格納)
- tasks(WorkとTaskは多対多)

# Task
- id 
- name
- specification
- date
- startTime
- endTime
- restTime
- type(CL業務, 外業務など)
- capacity
- extra(特別なこと)
- workers(WorkとTaskは多対多)

# Feedback
- id
- text
- response(デフォルトは空白でユーザからの入力は無し)