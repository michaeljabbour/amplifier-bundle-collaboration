# Collaboration System Instructions

You have access to multi-instance collaboration tools through enterprise platforms (Microsoft 365, Google Workspace).

## Available Tools

### collab_channels
Post and read messages from collaboration channels.

| Operation | Description |
|-----------|-------------|
| `list` | List available channels |
| `read` | Read recent messages from a channel |
| `post` | Post a message to a channel |

**Channels:**
- `general` - Status updates, completions
- `alerts` - Urgent issues, blockers  
- `handoffs` - Task delegation between instances

### collab_documents
Upload, download, and list shared documents.

| Operation | Description |
|-----------|-------------|
| `list` | List documents in a folder |
| `upload` | Upload a document |
| `download` | Download a document |

### collab_directory
Find users and groups in the organization.

| Operation | Description |
|-----------|-------------|
| `list_users` | List users in the organization |
| `get_user` | Get details about a specific user |

### collab_email
Send email notifications.

| Operation | Description |
|-----------|-------------|
| `send` | Send an email |

## Coordination Patterns

### Starting Work
```python
# Announce you're starting
collab_channels(operation="post", channel_name="general", 
    title="🚀 Starting Work",
    message="Beginning work on [task]. Session: {session_id}")
```

### Completing Work
```python
# Share artifacts
collab_documents(operation="upload", file_name="results.md", content="...")

# Announce completion
collab_channels(operation="post", channel_name="general",
    title="✅ Complete",
    message="Finished [task]. Results: [link]")
```

### Handing Off
```python
# Upload context
collab_documents(operation="upload", file_name="handoff.md", content="...")

# Post handoff
collab_channels(operation="post", channel_name="handoffs",
    title="🔄 Handoff: [task]",
    message="Context: [link]\nNext steps: [what to do]")
```

### Picking Up Work
```python
# Check for handoffs
collab_channels(operation="read", channel_name="handoffs")

# Claim task
collab_channels(operation="post", channel_name="handoffs",
    title="✋ Claimed",
    message="Session {session_id} picking up this task")

# Download context
collab_documents(operation="download", document_id="...")
```

## Best Practices

1. **Announce your work** - Post to `general` when starting/completing
2. **Share artifacts** - Upload to shared documents, link in channels
3. **Check handoffs** - Look for unclaimed work in `handoffs` channel
4. **Fail loudly** - Post to `alerts` when stuck
5. **Include session ID** - For tracing across instances
