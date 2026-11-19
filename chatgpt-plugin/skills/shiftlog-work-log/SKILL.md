---
name: shiftlog-work-log
description: Use when the user wants to log work they did (hours, a task, a client call, a day's notes) in ShiftLog.it, or to look up, total or summarise work already logged there, for example to answer how many hours went to a client or to draft a client update from the logged tasks.
---

# Logging and reading work in ShiftLog.it

ShiftLog.it is the user's work log and timesheet app. Each **agent** is one business or client
the user logs work for; tasks logged to an agent end up on the timesheets and reports the user
sends that client.

## Logging work

- Use `log_task`, one call per task. When the user describes several pieces of work, log each
  as its own task.
- The duration must come from the user: hours, or a start and end time. If they didn't say how
  long something took, ask before logging. Never estimate it.
- The description is what the user's client will read on the timesheet: what was done and its
  outcome, in a sentence or two of plain language. Leave out code, file paths and secrets.
- Pass a reference (`externalRef`) only when the user or their work names one, such as a ticket
  or purchase order number.
- If the user names a client or business, call `list_agents` first and pass that agent's id.
  Otherwise the task goes to their current agent. Without a date, it goes to today in the
  user's timezone.
- After logging, tell the user what was stored: the date, hours, agent and description.

## Reading work

- Use `list_tasks` for a range of days (up to 92 days per call; split longer periods). Totals
  are the sum of `hours`.
- `reported: true` means the task is already in a timesheet report.
- To summarise for a client, read the tasks first, then write the summary from what was
  actually logged, without adding work that isn't there.

## Limits

The tools can't edit or delete tasks. If the user asks for that, explain that it's done in the
ShiftLog.it app, at https://shiftlog.it.
