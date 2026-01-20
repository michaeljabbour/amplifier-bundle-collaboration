---
bundle:
  name: collaboration
  version: 1.0.0
  description: Multi-instance AI collaboration via Microsoft 365, Slack, Google Workspace

# External modules (published separately)
tools:
  - module: tool-collab-core
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-collab-core@main
    config:
      default_provider: ${COLLAB_PROVIDER:-m365}

  - module: tool-m365
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-m365@main

  - module: tool-slack
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-slack@main

  # Coming soon
  # - module: tool-google
  #   source: git+https://github.com/michaeljabbour/amplifier-module-tool-google@main

behaviors:
  - behaviors/collaboration-protocol.md
  - behaviors/workspace-conventions.md

context:
  - context/collaboration-instructions.md

agents:
  setup-assistant:
    path: agents/setup-assistant.md
    description: Walks users through complete M365/Slack/Google setup
  coordinator:
    path: agents/coordinator.md
    description: Orchestrates multi-instance collaboration
  document-manager:
    path: agents/document-manager.md
    description: Document operations specialist
  channel-communicator:
    path: agents/channel-communicator.md
    description: Teams/channels messaging specialist
---

# Collaboration Bundle

Multi-instance AI collaboration through enterprise platforms.

## Supported Platforms

| Platform | Module | Status |
|----------|--------|--------|
| **Microsoft 365** | `tool-m365` | ✅ Ready |
| **Slack** | `tool-slack` | ✅ Ready |
| **Google Workspace** | `tool-google` | 🔜 Coming |

## Quick Start

**Need help setting up?** Use the `setup-assistant` agent:
```
"Help me set up M365 collaboration"
"Help me set up Slack collaboration"
```

## Module Repositories

| Module | Description | Repository |
|--------|-------------|------------|
| Core | Shared interfaces | https://github.com/michaeljabbour/amplifier-module-tool-collab-core |
| M365 | Teams, SharePoint, Outlook | https://github.com/michaeljabbour/amplifier-module-tool-m365 |
| Slack | Channels, Files, Users | https://github.com/michaeljabbour/amplifier-module-tool-slack |
| Google | Chat, Drive, Gmail | https://github.com/michaeljabbour/amplifier-module-tool-google |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    amplifier-bundle-collaboration           │
│  (config, agents, behaviors, recipes)                       │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   tool-m365     │  │   tool-slack    │  │   tool-google   │
│  (M365Provider) │  │ (SlackProvider) │  │ (GoogleProvider)│
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
              ┌───────────────────────────────┐
              │      tool-collab-core         │
              │  (CollaborationProvider ABC)  │
              │  User, Channel, Message, etc. │
              └───────────────────────────────┘
```

## Collaboration Channels

| Channel | Purpose |
|---------|---------|
| `general` | Status updates, completions |
| `alerts` | Urgent issues, blockers |
| `handoffs` | Task delegation between instances |

## Agents

| Agent | Purpose |
|-------|---------|
| `setup-assistant` | **Start here** - walks through complete setup |
| `coordinator` | Orchestrates multi-instance workflows |
| `document-manager` | File operations specialist |
| `channel-communicator` | Messaging specialist |

@collaboration:context/collaboration-instructions.md
