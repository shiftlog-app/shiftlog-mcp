# ShiftLog.it MCP server

[ShiftLog.it](https://shiftlog.it) is a work log and timesheet app for
contractors and freelancers: log your hours, then generate the monthly
timesheet or work report your client needs, as a PDF, CSV or Excel file.

This is its hosted MCP server. Connect it to Claude, Claude Code, ChatGPT
or any other MCP client, and log the work you just did, or look up what you
logged, without leaving the conversation:

- "Log today's work: 3 hours, the checkout bug fix we just did. Reference JIRA-482."
- "What did I log for Acme last week, and how many hours in total?"
- "Log yesterday from 9:00 to 12:30: workshop with the client on the new onboarding flow."

There is nothing to install or run. You need a ShiftLog.it account (the
connection works on every plan, including Free).

| | |
|---|---|
| Endpoint | `https://shiftlog.it/mcp` |
| Transport | Streamable HTTP |
| Authentication | OAuth 2.1 with dynamic client registration: sign in to ShiftLog.it and approve the app |
| Registry name | `it.shiftlog/mcp` ([MCP Registry](https://registry.modelcontextprotocol.io/?q=shiftlog)) |

## Connect it

### Claude (claude.ai and the desktop app)

ShiftLog.it is in [Claude's connector directory](https://claude.ai/directory/connectors/shiftlog):

1. Open **Plugins** in the sidebar (**Customize** on Team and Enterprise
   plans), search for **ShiftLog** and click **+ Add**, or open
   [claude.ai/plugins?q=shiftlog](https://claude.ai/plugins?q=shiftlog).
2. Claude sends you to ShiftLog.it. Sign in if you aren't already.
3. The consent page shows which app is asking and what it will be able
   to do. Click **Allow**, and you're back in Claude.

It can also be added as a custom connector with the URL
`https://shiftlog.it/mcp`.

### Claude Code

Added on claude.ai, it shows up in Claude Code signed in with the same
account: run `/mcp`, choose **claude.ai ShiftLog.it** and authenticate.
Or add it directly:

```
claude mcp add --transport http shiftlog https://shiftlog.it/mcp
```

Then run `/mcp`, choose **shiftlog** and authenticate. Your browser opens
the same sign-in and consent page.

### ChatGPT

1. Open **Plugins**, click **+** and choose **Add custom MCP server**.
2. Enter the URL `https://shiftlog.it/mcp` and choose **OAuth**. No client
   ID is needed: ChatGPT registers itself.
3. Connect, sign in to ShiftLog.it and click **Allow**. ChatGPT asks you to
   confirm before it logs a task.

Guide: [Connect ShiftLog.it to ChatGPT](https://shiftlog.it/blog/connect-shiftlog-to-chatgpt)

### Other MCP clients

Add a remote (HTTP) server with the URL `https://shiftlog.it/mcp`. The
client finds the sign-in page by itself: an unauthenticated request gets
a `401` whose `WWW-Authenticate` header points to the protected resource
metadata (RFC 9728), and from there to the authorization server's
metadata at `https://shiftlog.it/.well-known/oauth-authorization-server`.
A typical JSON configuration:

```json
{
  "mcpServers": {
    "shiftlog": {
      "type": "http",
      "url": "https://shiftlog.it/mcp"
    }
  }
}
```

Redirect URIs must be `https`, or `http` to `localhost` or `127.0.0.1`.

## Tools

| Tool | What it does | Permission |
|---|---|---|
| `list_agents` | Lists your agents (the businesses or clients you log work for) and which one is current. | `tasks:read` |
| `list_tasks` | Lists an agent's tasks for a range of days (up to 92 days and 500 tasks), with dates, hours, titles, descriptions, your references and whether a task is already in a report. | `tasks:read` |
| `log_task` | Adds one task to an agent's work log: a date, the hours (or a start and end time), a description, and optionally a title and a reference such as a ticket id. | `tasks:write` |

What the connection can't do:

- **It only adds.** No tool changes or deletes a task; edit tasks in the app.
- **It doesn't guess hours.** A task needs the duration you state.
- **It can't reach anything else** in your account: no settings, billing,
  reports or AI features.

A task logged through MCP is like any other: it gets the agent's hourly
rate and appears in the work log, reports and exports.

## Permissions

The consent page asks for two scopes:

- `tasks:read`: see your agents and the tasks in your work log
- `tasks:write`: add tasks to your work log

## Privacy and disconnecting

The app you connect sees only what it reads through these tools at your
request. What ShiftLog.it keeps about each connection, and for how long,
is in section 2.9 of the [Privacy Policy](https://shiftlog.it/privacy).

To end a connection, open **Settings**, then **Connected apps** in
ShiftLog.it and click **Disconnect**. Access ends at once. A connection
you don't use for 30 days ends on its own.

## Links

- Website: https://shiftlog.it
- Pricing: https://shiftlog.it/pricing
- Guides: [Connect ShiftLog.it to Claude](https://shiftlog.it/blog/connect-shiftlog-to-claude),
  [Connect ShiftLog.it to ChatGPT](https://shiftlog.it/blog/connect-shiftlog-to-chatgpt)
- Support: support@shiftlog.it

This repository holds the server's documentation and its MCP Registry
entry (`server.json`). The server itself is part of the ShiftLog.it app
and is not open source.

## ChatGPT plugin package

`chatgpt-plugin/` is the package submitted to the ChatGPT plugin
directory: the listing and review test cases (`plugin.json`), the MCP
connection (`mcp.json`), a skill and the icon. To build the ZIP for
platform.openai.com/plugins (bump `version` in `plugin.json` first):

```
cd chatgpt-plugin && rm -f ../shiftlog-chatgpt-plugin.zip && zip -r -X ../shiftlog-chatgpt-plugin.zip . -x '*.DS_Store'
```
