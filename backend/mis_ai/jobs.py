"""This project's scheduled jobs.

@register_job adds a job to the platform's scheduler when this module is
imported (extension.py imports it). The platform then lists it under
Administration → Scheduled Jobs, where it can also be run by hand, and runs
it on its cron schedule wherever SCHEDULER_ENABLED is true.
"""

from __future__ import annotations

from datetime import date

from savic_common.scheduler.registry import register_job

from mis_ai import service


@register_job(
    job_code="MIS_AI_OVERDUE_TASKS",
    job_name="MIS AI: count overdue tasks",
    description="Counts open tasks past their due date.",
    cron_expression="0 2 * * *",  # 02:00 UTC every day
)
def count_overdue_tasks(db, company_id):
    """company_id is None for a scheduled run (every company), or the
    company of the user who started it by hand."""
    overdue = service.count_overdue(db, company_id, date.today())
    return {"overdue_tasks": overdue}
