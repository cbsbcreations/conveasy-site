# n8n: website chat demo

Copy of the two Code nodes of the n8n workflow "Conveasy — Website chat demo (WhatsApp)" (id 9eb0PIubSSJ6ovPe),
kept here so changes to the demo's menu and rules have a history. The workflow in n8n is the one that runs.

Flow: Chat In (webhook, POST /webhook/conveasy-site-wa-demo) -> Build Request -> Message OK? -> Ask Claude (HTTP, Claude Haiku 5.5)
-> Read Answer -> Reply To Page -> Problem? -> Fail Run (only when Claude gave no answer, so it shows under failed executions).

- build-request.js : checks the message, daily limit, menu + rules, builds the request for Claude.
- read-answer.js   : turns Claude's JSON answer {reply, buttons} into what the page shows.
