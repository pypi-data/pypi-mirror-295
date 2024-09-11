Django database task queue

Django Transaction Task Queue
=============================

A short and simple Celery replacement for my Django projects.

* *Database is the only backend.* The task is a simple Django model, it uses the same transaction and connection as other models. No more ``transaction.on_commit`` hooks to schedule tasks.
* *Tasks do not produce any results*, there is no ``get`` or ``join`` and there is no "result backend".  This is not a distrubuted await. If you need to store results, pass a unique key into the task and store the result in some DIY model.
* *No workflows and chaining of jobs.*
* *ETA (estimated time of arrival) is a first-class citizen.* It does not depend on whether backends support the feature or not.
* *The worker is a single-threaded process*, you start several of those to scale. I have seen too many issues with autoscaling workers, worker processes killed by OS, workers stuck: simple is better.
* *No prefetching or visibility timeouts*. The worker picks the first available task and processes it.
* *Dead letter queue* built in. You get access to failed tasks and can retry them from Django admin.
* *Django admin for monitoring.* You can view pending tasks, future, failed, and "dirty" (crashed in the middle of work).
* *Easy to get the metrics* from Django shell and export to your favorite monitoring tool
* *Task records are removed after successful execution*. Unlike Celery SQLAlchemy's backend, records are removed so you don't have to care about archiving. It also keeps the table small, properly indexed and efficient.

Celery API
----------

The main API is the Celery API (``shared_task``) with ``delay``, ``apply_async`` and ``s``. Just to make switching between implementations easier.

.. code-block:: python
  
  from django_taskq.celery import shared_task

  @shared_task(autoretry_for(MyException,), retry_kwargs={"max_retries": 10, "countdown": 5})
  def my_task(foo, bar=None):
      ...

.. code-block:: python
  
  my_task.delay(1,bar=2)
  my_task.appy_async((1,2))
  my_task.s(1,2).apply_async()


Internals
---------

Adding a new task to the queue is just creating a new instance of the Task model.

Executing a task is a bit more expensive:
# A task is picked up from a queue and the state is updated to "started" within a single transaction.
# Python code is executed, a background thread updates "alive at" field every second ("a liveness probe").
# Successful tasks are deleted from the table. Failed tasks are marked as such and retried (based on configuration).

This is a bit more expensive than necessary but:
* we can recognize running tasks - the task is "started" and the record is updated in the last couple seconds.
* we can recognize "dirty" tasks that got killed or lost database connection in the middle - the task is "started" and the record has not been updated for a while.

In an ideal world tasks should be idempotent but things happen and I prefer to know which tasks crashed and double-check if some cleanup is necessary.

Performance
-----------

A single process can execute around 150 dummy tasks per second which is more than enough. After years of struggling with Celery, correctness and observability are more important.
On the other hand, to handle more "tasks" you probably want to store many events not tasks and have a single task that processes them in batches.
