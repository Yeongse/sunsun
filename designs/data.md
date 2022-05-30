# Worker
- id
- name(姓名, スペース無し)
- email
- password
- tasks(WorkとTaskは多対多)

# Task
- id 
- name
- specification
- date
- startTime
- endTime
- restTime
- class(CL業務, 外業務など)
- capacity
- extra(特別なこと)
- workers(WorkとTaskは多対多)