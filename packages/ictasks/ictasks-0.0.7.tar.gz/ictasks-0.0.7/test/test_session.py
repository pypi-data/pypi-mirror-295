from pathlib import Path
import os
import shutil

from ictasks.session import Session
from ictasks.environment import BasicEnvironment
from ictasks.tasks import (Task,
                           TaskCollection,
                           ShellTaskLauncher,
                           TaskfarmFile)

def test_basic_tasks_session():

    job_dir = Path(os.getcwd()) / "test_basic_tasks_session"

    tasks = TaskCollection(job_dir)
    tasks.add_tasks([Task("0", "echo 'hello from task 0'"),
                     Task("1", "echo 'hello from task 1'")])

    session = Session(tasks)
    session.run()

    shutil.rmtree(job_dir)
    

def test_taskfarm_session():

    job_dir = Path(os.getcwd()) / "test_taskfarm_session"

    env = BasicEnvironment(job_id="1234")

    taskfarm_file = TaskfarmFile(job_dir)
    tasklist = "echo 'hello from task 1'\necho 'hello from task 2'"
    num_grouped, tasks = taskfarm_file.load(tasklist)
    assert len(tasks) == 2
    
    task_collection = TaskCollection(job_dir)
    task_collection.num_grouped_tasks = num_grouped
    task_collection.add_tasks(tasks)

    launcher = ShellTaskLauncher()
    
    session = Session(task_collection, env, launcher)
    session.run()

    shutil.rmtree(job_dir)


