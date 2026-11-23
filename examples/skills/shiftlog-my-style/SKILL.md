---
name: shiftlog-my-style
description: Use whenever logging work to ShiftLog.it (the log_task tool) or writing or summarising ShiftLog.it tasks, to follow my own rules for wording, clients, references and durations.
---

<!--
An example skill for ShiftLog.it's MCP server. Copy this folder, rename it if
you like, and edit the rules below to match how you work: delete what you
don't need, change the examples. The AI reads this file as instructions,
so plain sentences work best. Keep session_time.py next to it if you use
Claude Code: it works out the hours from the session (change --round to
round differently). More: https://github.com/shiftlog-app/shiftlog-mcp
-->

# How I log work in ShiftLog.it

## Wording

- Write task descriptions in English, in the past tense ("Fixed", "Reviewed", "Prepared").
- One or two sentences: what was done and its outcome, as my client reads it on the timesheet.
- No code, file paths, branch names or internal jargon. Name the feature or document instead.
- Add a short title (`topic`) of up to five words, e.g. "Checkout bug fix".

## Clients

Each client is an agent in ShiftLog.it. Pick the agent by these rules and pass its id
(from `list_agents`):

- Work for Acme or anything in the `acme-*` repositories goes to the agent "Acme GmbH".
- Work for Northwind goes to the agent "Northwind".
- Anything else goes to my current agent. If you're not sure which client it was, ask me.

## References

- A reference I give always wins.
- For Acme, put the Jira ticket in `externalRef` (e.g. `ACME-482`) when the work names one.
- Otherwise, in a git repository, use the short hash of the commit holding the task's work
  (check `git log` and `git status`). If the work isn't committed yet, say so and offer to log
  after I commit; never use an older commit's hash.
- Never make up a reference.

## Durations

A duration I state, or a start and end time I give, always wins. Otherwise:

- **In Claude Code:** work it out from the session transcript with `session_time.py`, in this
  skill's folder (run it from the project folder):
  1. Find Python 3 (`python3`, `py` or `python`, whichever prints `Python 3.x`). If there's none,
     tell me and offer to install it (`winget install -e --id Python.Python.3.13` on Windows,
     `brew install python` or `xcode-select --install` on macOS, the system's package on Linux),
     and only install it after I say yes.
  2. `python3 <this folder>/session_time.py` lists the session's prompts with their times.
  3. Count from the prompt where I said "start timer", or else from the first one asking for
     actual work: chat and questions before it don't count.
  4. `python3 <this folder>/session_time.py --from N --round 15` gives the active minutes
     (breaks over 30 minutes left out) and the hours rounded to 15 minutes. Use `--to M` to
     end a task at prompt M when the session covered several tasks.
  5. Show me the start prompt and the active minutes with the hours, so I can correct them.
- **Anywhere else**, or if the script can't find a transcript: ask me.
- Round to the nearest 15 minutes (0.25 hours), at least 15 minutes.
- Never log more than 8 hours for one task; split a longer day into separate tasks.

## Before logging

- Show me the date, hours, agent and description, and log only after I confirm.
- At the end of a coding session, offer to log the work with a summary of what changed.
