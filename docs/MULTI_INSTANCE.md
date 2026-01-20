# Multi-Instance Collaboration Patterns

This guide explains how to coordinate work across multiple Amplifier instances.

## Core Concepts

### Session Identity
Each Amplifier instance has a unique session ID. Include this in messages for traceability:

```python
# In handoff messages
message = f"Session {session_id} handing off task..."
```

### Channels as Coordination Points
Channels serve specific purposes:
- **general**: Broadcast status to all instances
- **alerts**: Signal need for help
- **handoffs**: Transfer ownership of work

### Documents as Shared Memory
Shared documents persist context across instance lifetimes:
- Handoff docs contain full context
- Artifacts shared via document links
- No need to repeat context in messages

## Patterns

### Pattern 1: Parallel Work Distribution

Multiple instances work on different parts of a problem simultaneously.

```
Coordinator                   Workers
    │
    ├── Split task ──────────►  Instance A (subtask 1)
    │                           Instance B (subtask 2)
    │                           Instance C (subtask 3)
    │
    ├── Monitor general ◄────── Status updates
    │
    └── Aggregate results ◄──── Completion messages
```

**Coordinator posts:**
```markdown
🔄 Handoff: Subtask 1 - User API
Context: [doc link]
Scope: Only the user endpoints
```

**Worker claims:**
```markdown
✋ Claimed
Session ABC123 taking subtask 1
```

**Worker completes:**
```markdown
✅ Complete: Subtask 1 - User API
Results: [doc link]
```

### Pattern 2: Sequential Handoff Chain

Work passes through instances in sequence, each adding value.

```
Instance A ──► Instance B ──► Instance C
(research)     (design)       (implement)
```

**Each handoff includes:**
1. What was done
2. Key findings/decisions
3. Next steps
4. All relevant documents

### Pattern 3: On-Call Coverage

Instances monitor alerts and respond to issues.

```
Instance A (working)
    │
    ├── Encounters error
    │
    ├── Posts to alerts ─────► 🚨 Alert: API timeout
    │                          Need help debugging
    │
Instance B (available)
    │
    ├── Reads alert
    │
    └── Responds ─────────────► ✋ Investigating
                                Session XYZ picking up
```

### Pattern 4: Knowledge Sync

Share discoveries across all instances.

```
Instance A                    All Instances
    │
    ├── Discovers pattern
    │
    ├── Documents it ─────────► Upload to shared/
    │
    └── Broadcasts ───────────► 📢 New Pattern: [name]
                                See: [doc link]
```

## Best Practices

### 1. Announce Everything
```python
# Starting work
collab_channels(operation="post", channel_name="general",
    title="🚀 Starting",
    message="Working on X. Session: {id}")

# Completing work
collab_channels(operation="post", channel_name="general",
    title="✅ Complete",
    message="Finished X. Results: [link]")
```

### 2. Link, Don't Paste
```python
# Upload artifact
result = collab_documents(operation="upload", ...)

# Reference in message
collab_channels(operation="post", ...,
    message=f"Full details: {result['web_url']}")
```

### 3. Structured Handoffs
Always include:
- **What** was being worked on
- **Why** you're handing off
- **Where** the context is
- **What** to do next

### 4. Fail Loudly
```python
# Don't suffer in silence
collab_channels(operation="post", channel_name="alerts",
    title="🚨 Blocked",
    message="Can't proceed because X. Need help with Y.")
```

### 5. Check Before Starting
```python
# Always check for existing work
existing = collab_channels(operation="read", channel_name="handoffs")
# Look for unclaimed tasks before starting new work
```

## Example: Code Review Workflow

```yaml
# Recipe: distributed-code-review
steps:
  - id: split-files
    prompt: "Divide files into groups for parallel review"
    
  - id: post-assignments
    foreach: "{{steps.split-files.groups}}"
    prompt: "Post handoff for file group to handoffs channel"
    
  - id: wait-for-reviews
    prompt: "Monitor general for completion messages"
    
  - id: aggregate
    prompt: "Combine all review findings into summary"
    
  - id: post-summary
    prompt: "Post final review to general with doc link"
```

## Scaling Considerations

### Channel Volume
- Keep messages concise
- Use documents for details
- Consider channel per project for large teams

### Document Organization
```
Amplifier/
├── project-alpha/
│   ├── handoffs/
│   └── artifacts/
├── project-beta/
│   ├── handoffs/
│   └── artifacts/
└── shared/
    └── templates/
```

### Conflict Resolution
When multiple instances claim same task:
- First claim wins
- Others should check before claiming
- Coordinator can arbitrate if needed
