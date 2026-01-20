<p align="center">
  <img src="https://img.shields.io/badge/Amplifier-Collaboration-blue?style=for-the-badge" alt="Amplifier Collaboration">
  <img src="https://img.shields.io/badge/M365-Ready-0078D4?style=for-the-badge&logo=microsoft" alt="M365 Ready">
  <img src="https://img.shields.io/badge/Slack-Ready-4A154B?style=for-the-badge&logo=slack" alt="Slack Ready">
  <img src="https://img.shields.io/badge/Google-Coming_Soon-4285F4?style=for-the-badge&logo=google" alt="Google Coming Soon">
</p>

<h1 align="center">Amplifier Collaboration Bundle</h1>

<p align="center"><strong>Enable AI instances to work together like a team.</strong></p>

<p align="center">
Coordinate through enterprise platforms—post status updates, share documents,<br>
hand off tasks, and pick up where others left off.
</p>

---

## The Vision

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│   Instance A              Collaboration Hub              Instance B             │
│   ┌─────────┐            ┌──────────────┐               ┌─────────┐            │
│   │         │──"Starting │  #general    │               │         │            │
│   │  Task   │  analysis" │  #alerts     │ "Claimed!"───▶│  Fresh  │            │
│   │  Owner  │───────────▶│  #handoffs   │◀──────────────│ Context │            │
│   │         │            │              │               │         │            │
│   │         │──uploads──▶│  📁 Files    │──downloads───▶│         │            │
│   │         │  findings  │              │   context     │         │            │
│   │         │            └──────────────┘               │         │            │
│   │         │──"Handing                                 │         │──"Done! ✅" │
│   │         │   off..."───────────────────────────────▶ │         │            │
│   └─────────┘                                           └─────────┘            │
│                                                                                 │
│   👁️ Humans can observe all coordination in real-time                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Why This Exists

| Problem | Solution |
|---------|----------|
| AI sessions have finite context | **Hand off** to fresh instances with shared documents |
| Single instance bottleneck | **Parallel work** with coordination channels |
| Work disappears when session ends | **Persistent artifacts** in SharePoint/Drive/Slack |
| No visibility into AI work | **Observable channels** humans can monitor |
| Platform lock-in | **Unified interface** across M365, Slack, Google |

### Real-World Use Cases

- 🔄 **Long-running analysis** — Instance A starts, uploads progress, Instance B continues
- 👥 **Parallel code review** — Split files across instances, aggregate findings
- 📋 **Task queue** — Post to `#handoffs`, any available instance claims it
- 🚨 **Escalation** — Stuck instance posts to `#alerts`, gets help
- 📊 **Daily reports** — Instances share findings in persistent documents

---

## Quick Start

### Option 1: Guided Setup (Recommended)

Let the `setup-assistant` walk you through everything:

```
"Help me set up Slack collaboration"
```

```
"I need to configure Microsoft 365 Teams integration"
```

The assistant handles: app creation, permissions, webhooks, environment variables, testing.

### Option 2: I Have Credentials

**For Slack:**
```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_WEBHOOKS="general=https://hooks.slack.com/...,alerts=...,handoffs=..."

cd ~/dev/amplifier-bundle-collaboration/modules/tool-slack
pip install -e .
```

**For Microsoft 365:**
```bash
export M365_TENANT_ID="your-tenant"
export M365_CLIENT_ID="your-client"
export M365_CLIENT_SECRET="your-secret"
export M365_TEAMS_WEBHOOKS="general=https://...,alerts=...,handoffs=..."

cd ~/dev/amplifier-bundle-collaboration/modules/tool-collab-core
pip install -e .
```

---

## Supported Platforms

| Platform | Status | Module | What You Get |
|----------|--------|--------|--------------|
| **Microsoft 365** | ✅ Ready | `tool-collab-core` | Teams channels, SharePoint files, Outlook email, Planner tasks |
| **Slack** | ✅ Ready | `tool-slack` | Channels, Files, User directory, DMs |
| **Google Workspace** | 🔜 Coming | `tool-google` | Chat, Drive, Gmail, Calendar |

### Feature Matrix

|  | M365 | Slack | Google |
|--|------|-------|--------|
| Post to channels | ✅ | ✅ | 🔜 |
| Read messages | ✅ | ✅ | 🔜 |
| Upload files | ✅ SharePoint | ✅ Files | 🔜 Drive |
| Download files | ✅ | ✅ | 🔜 |
| List users | ✅ Azure AD | ✅ | 🔜 |
| Send email | ✅ Outlook | ❌ | 🔜 Gmail |
| Task management | ✅ Planner | ❌ | 🔜 Tasks |

---

## Tools Reference

### `collab_channels` — Messaging

```python
# Post a status update
collab_channels(operation="post", channel_name="general",
    title="✅ Analysis Complete",
    message="Found 3 issues. Report: [link]")

# Read recent messages
collab_channels(operation="read", channel_name="handoffs", limit=10)

# List channels
collab_channels(operation="list")
```

### `collab_documents` — Files

```python
# Upload
collab_documents(operation="upload", 
    file_name="2026-01-20_report.md",
    content="# Findings\n...",
    folder_path="Amplifier/completed")

# List
collab_documents(operation="list", folder_path="Amplifier/handoffs")

# Download
collab_documents(operation="download", document_id="...")
```

### `collab_directory` — Users

```python
collab_directory(operation="list_users", limit=25)
collab_directory(operation="get_user", user_id="alice@company.com")
```

### `collab_email` — Notifications (M365)

```python
collab_email(operation="send", 
    to=["manager@company.com"],
    subject="Report Ready",
    body="Analysis complete.")
```

---

## Collaboration Channels

Three standard channels enable coordination:

| Channel | Purpose | Post When |
|---------|---------|-----------|
| `#general` | Status broadcasts | Starting work, completing tasks, sharing results |
| `#alerts` | Urgent issues | Errors, blockers, need help |
| `#handoffs` | Task transfers | Handing off work, claiming tasks |

### Message Templates

```
🚀 Starting: Code review for auth module
Session: abc-123 | ETA: 30 min

✅ Complete: Code review
Found: 2 critical, 5 minor issues
Report: [SharePoint link]

🚨 Blocked: API rate limit hit
Context: Processing user batch 3/10
Need: Wait 1 hour or increase quota

🔄 Handoff: Database migration
Done: Schema design, test data
Next: Run migration, verify integrity
Context: [handoff doc link]

✋ Claimed: Database migration
Session: xyz-789
```

---

## Agents

| Agent | What It Does |
|-------|--------------|
| **`setup-assistant`** | Walks through complete platform setup step-by-step |
| **`coordinator`** | Orchestrates parallel work, distributes tasks |
| **`document-manager`** | Uploads, organizes, retrieves shared files |
| **`channel-communicator`** | Posts updates, reads discussions |

---

## Recipes

| Recipe | Use Case |
|--------|----------|
| **`collaborative-task`** | Execute work with automatic status posting and artifact sharing |
| **`task-handoff`** | Create handoff doc, post to channel, ready for pickup |
| **`pickup-task`** | Scan handoffs, claim task, download context, continue |

---

## Architecture

```
amplifier-bundle-collaboration/
├── modules/
│   ├── tool-collab-core/           # M365 + shared interfaces
│   │   └── amplifier_module_tool_collaboration/
│   │       ├── providers/
│   │       │   ├── base.py         # CollaborationProvider interface
│   │       │   └── m365.py         # Microsoft Graph implementation
│   │       ├── tools/              # Tool implementations
│   │       └── mcp/                # MCP server
│   │
│   ├── tool-slack/                 # Slack implementation
│   │   └── amplifier_module_tool_slack/
│   │       └── providers/
│   │           └── slack.py        # Slack SDK implementation
│   │
│   └── tool-google/                # (Coming soon)
│
├── agents/
│   ├── setup-assistant.md          # Platform setup guide
│   ├── coordinator.md
│   ├── document-manager.md
│   └── channel-communicator.md
│
├── behaviors/
│   ├── collaboration-protocol.md   # Channel conventions
│   └── workspace-conventions.md    # File organization
│
├── recipes/
│   ├── collaborative-task.yaml
│   ├── task-handoff.yaml
│   └── pickup-task.yaml
│
└── docs/
    ├── M365_SETUP.md
    └── MULTI_INSTANCE.md
```

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Separate modules per platform** | Independent versioning, optional installation |
| **Webhook-first for posting** | Simpler auth, works without channel membership |
| **Abstract provider interface** | Easy to add new platforms |
| **Three standard channels** | Clear separation of concerns |

---

## Adding New Platforms

Implement the `CollaborationProvider` interface:

```python
class MyProvider(CollaborationProvider):
    async def list_users(self, limit: int = 25) -> list[User]: ...
    async def list_channels(self, team_id: str = None) -> list[Channel]: ...
    async def get_messages(self, channel_id: str, limit: int = 20) -> list[Message]: ...
    async def post_message(self, channel_name: str, message: str, title: str = None) -> bool: ...
    async def upload_document(self, name: str, content: bytes, folder: str = None) -> Document: ...
    async def download_document(self, document_id: str) -> bytes: ...
    # ... etc
```

Then register in `providers/__init__.py` and set `COLLAB_PROVIDER=myplatform`.

---

## Security Notes

- **Credentials in environment** — Never commit secrets
- **Least privilege** — Request only needed API scopes
- **Webhook URLs are secrets** — Treat like passwords
- **Observable by design** — Humans see all coordination

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid token" | Check token format (`xoxb-` for Slack, verify M365 secret) |
| "Channel not found" | Bot needs to be in the channel (invite it) |
| "Insufficient privileges" | Grant admin consent (M365) or add scopes (Slack) |
| Webhook fails | Verify URL is complete, channel exists |

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

For new platforms, follow the provider interface pattern.

---

## License

MIT

---

<p align="center">
<strong>Built for multi-instance AI collaboration</strong><br>
<em>Because the best AI is a team of AIs</em>
</p>
