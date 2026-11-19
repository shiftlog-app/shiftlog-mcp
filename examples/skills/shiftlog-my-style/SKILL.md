---
name: shiftlog-my-style
description: Use whenever logging work to ShiftLog.it (the log_task tool) or writing or summarising ShiftLog.it tasks, to follow my own rules for wording, clients, references and durations.
---

<!--
An example skill for ShiftLog.it's MCP server. Copy this folder, rename it if
you like, and edit the rules below to match how you work: delete what you
don't need, change the examples. The AI reads this file as instructions,
so plain sentences work best. More: https://github.com/shiftlog-app/shiftlog-mcp
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

- For Acme, put the Jira ticket in `externalRef` (e.g. `ACME-482`) when the work names one.
- Never make up a reference.

## Durations

- Use only the duration I state, or a start and end time I give. If I didn't say, ask me.
- Round to the nearest 15 minutes (0.25 hours).
- Never log more than 8 hours for one task; split a longer day into separate tasks.

## Before logging

- Show me the date, hours, agent and description, and log only after I confirm.
- At the end of a coding session, offer to log the work with a summary of what changed.
