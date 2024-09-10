JOB_SUBMIT_EXAMPLE = """\
$ anyscale job submit --name my-job --wait -- python main.py
Output
(anyscale +1.0s) Submitting job with config JobConfig(name='my-job', image_uri=None, compute_config=None, env_vars=None, py_modules=None, cloud=None, project=None, ray_version=None, job_queue_config=None).
(anyscale +1.7s) Uploading local dir '.' to cloud storage.
(anyscale +2.6s) Including workspace-managed pip dependencies.
(anyscale +3.2s) Job 'my-job' submitted, ID: 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe'.
(anyscale +3.2s) View the job in the UI: https://console.anyscale.com/jobs/prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe
(anyscale +3.2s) Waiting for the job to run. Interrupting this command will not cancel the job.
(anyscale +3.5s) Waiting for job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' to reach target state SUCCEEDED, currently in state: STARTING
(anyscale +1m19.7s) Job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' transitioned from STARTING to SUCCEEDED
(anyscale +1m19.7s) Job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' reached target state, exiting
"""

JOB_STATUS_EXAMPLE = """\
$ anyscale job status -n my-job
id: prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe
name: my-job
state: STARTING
runs:
- name: raysubmit_ynxBVGT1SmzndiXL
  state: SUCCEEDED
"""

JOB_TERMINATE_EXAMPLE = """\
$ anyscale job terminate -n my-job
(anyscale +5.4s) Marked job 'my-job' for termination
(anyscale +5.4s) Query the status of the job with `anyscale job status --name my-job`.
"""

JOB_ARCHIVE_EXAMPLE = """\
$ anyscale job archive -n my-job
(anyscale +8.5s) Job prodjob_vzq2pvkzyz3c1jw55kl76h4dk1 is successfully archived.
"""

JOB_LOGS_EXAMPLE = """\
$ anyscale job logs -n my-job
2024-08-23 20:31:10,913 INFO job_manager.py:531 -- Runtime env is setting up.
hello world
"""

JOB_WAIT_EXAMPLE = """\
$ anyscale job wait -n my-job
(anyscale +5.7s) Waiting for job 'my-job' to reach target state SUCCEEDED, currently in state: STARTING
(anyscale +1m34.2s) Job 'my-job' transitioned from STARTING to SUCCEEDED
(anyscale +1m34.2s) Job 'my-job' reached target state, exiting
"""

JOB_LIST_EXAMPLE = """\
$ anyscale job list -n my-job
Output
View your Jobs in the UI at https://console.anyscale.com/jobs
JOBS:
NAME    ID                                    COST  PROJECT NAME    CLUSTER NAME                                    CURRENT STATE           CREATOR           ENTRYPOINT
my-job  prodjob_s9x4uzc5jnkt5z53g4tujb3y2e       0  default         cluster_for_prodjob_s9x4uzc5jnkt5z53g4tujb3y2e  SUCCESS                 doc@anyscale.com  python main.py
"""

SCHEDULE_APPLY_EXAMPLE = """\
$ anyscale schedule apply -n my-schedule -f my-schedule.yaml
(anyscale +0.5s) Applying schedule with config ScheduleConfig(job_config=JobConfig(name='my-schedule', image_uri=None, compute_config=None, env_vars=None, py_modules=None, cloud=None, project=None, ray_version=None, job_queue_config=None), cron_expression='0 0 * * * *', timezone='UTC').
(anyscale +2.3s) Uploading local dir '.' to cloud storage.
(anyscale +3.7s) Including workspace-managed pip dependencies.
(anyscale +4.9s) Schedule 'my-schedule' submitted, ID: 'cronjob_vrjrbwcnfjjid7fsld3sfkn8jz'.

$ cat my-schedule.yaml
timezone: local
cron_expression: 0 0 * * * *
job_config:
    name: my-job
    entrypoint: python main.py
    max_retries: 5
"""

SCHEDULE_LIST_EXAMPLE = """\
$ anyscale schedule list -n my-schedule
Output
+------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------+
| ID                                 | NAME        | DESCRIPTION   | PROJECT   | CRON        | NEXT TRIGGER     | TIMEZONE   | CREATOR          | LATEST EXECUTION ID   |
|------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------|
| cronjob_vrjrbwcnfjjid7fsld3sfkn8jz | my-schedule |               | default   | 0 0 * * * * | 2 hours from now | UTC        | doc@anyscale.com |                       |
+------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------+
"""

SCHEDULE_PAUSE_EXAMPLE = """\
$ anyscale schedule pause -n my-schedule
(anyscale +3.6s) Set schedule 'my-schedule' to state DISABLED
"""

SCHEDULE_RESUME_EXAMPLE = """\
$ anyscale schedule resume -n my-schedule
(anyscale +4.1s) Set schedule 'my-schedule' to state ENABLED
"""

SCHEDULE_STATUS_EXAMPLE = """\
$ anyscale schedule status -n my-schedule
id: cronjob_vrjrbwcnfjjid7fsld3sfkn8jz
name: my-schedule
state: ENABLED
"""

SCHEDULE_RUN_EXAMPLE = """\
$ anyscale schedule run -n my-schedule
(anyscale +2.5s) Triggered job for schedule 'my-schedule'.
"""

SCHEDULE_URL_EXAMPLE = """\
$ anyscale schedule url -n my-schedule
Output
(anyscale +2.3s) View your schedule at https://console.anyscale.com/scheduled-jobs/cronjob_7zj
"""

WORKSPACE_CREATE_EXAMPLE = """\
$ anyscale workspace_v2 create -f config.yml
(anyscale +2.7s) Workspace created successfully id: expwrk_jstjkv15a1vmle2j1t59s4bm35
(anyscale +3.9s) Applied dynamic requirements to workspace id: my-workspace
(anyscale +4.8s) Applied environment variables to workspace id: my-workspace

$ cat config.yml
name: my-workspace
idle_termination_minutes: 10
env_vars:
    HUMPDAY: WEDS
requirements: requirements.txt
"""

WORKSPACE_START_EXAMPLE = """\
$ anyscale workspace_v2 start --name my-workspace
(anyscale +5.8s) Starting workspace 'my-workspace'
"""

WORKSPACE_TERMINATE_EXAMPLE = """\
$ anyscale workspace_v2 terminate --name my-workspace
(anyscale +2.5s) Terminating workspace 'my-workspace'
"""

WORKSPACE_STATUS_EXAMPLE = """\
$ anyscale workspace_v2 status --name my-workspace
(anyscale +2.3s) STARTING
"""

WORKSPACE_WAIT_EXAMPLE = """\
$ anyscale workspace_v2 wait --name my-workspace --state RUNNING
(anyscale +2.5s) Waiting for workspace 'expwrk_jstjkv15a1vmle2j1t59s4bm35' to reach target state RUNNING, currently in state: RUNNING
(anyscale +2.8s) Workspace 'expwrk_jstjkv15a1vmle2j1t59s4bm35' reached target state, exiting
"""

WORKSPACE_SSH_EXAMPLE = """\
$ anyscale workspace_v2 ssh --name my-workspace
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
(base) ray@ip-10-0-24-60:~/default$
"""

WORKSPACE_RUN_COMMAND_EXAMPLE = """\
$ anyscale workspace_v2 run_command --name my-workspace "echo hello world"
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
hello world
"""

WORKSPACE_PULL_EXAMPLE = """\
$ anyscale workspace_v2 pull --name my-workspace --local-dir my-local
Warning: Permanently added '54.212.209.253' (ED25519) to the list of known hosts.
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
receiving incremental file list
created directory my-local
./
my-local/
my-local/main.py

sent 118 bytes  received 141 bytes  172.67 bytes/sec
total size is 0  speedup is 0.00
"""

WORKSPACE_PUSH_EXAMPLE = """\
$ anyscale workspace_v2 push --name my-workspace --local-dir my-local
Warning: Permanently added '52.10.22.124' (ED25519) to the list of known hosts.
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
sending incremental file list
my-local/
my-local/main.py

sent 188 bytes  received 39 bytes  151.33 bytes/sec
total size is 0  speedup is 0.00
"""

MACHINE_POOL_CREATE_EXAMPLE = """\
$ anyscale machine-pool create --name can-testing
Machine pool can-testing has been created successfully (ID mp_8ogdz85mdwxb8a92yo44nn84ox).
"""

MACHINE_POOL_DELETE_EXAMPLE = """\
$ anyscale machine-pool delete --name can-testing
Deleted machine pool 'can-testing'.
"""

MACHINE_POOL_LIST_EXAMPLE = """\
$ anyscale machine-pool list
MACHINE POOL       ID                             Clouds
can-testing        mp_8ogdz85mdwxb8a92yo44nn84ox
"""
