# Usage Examples

> **Generated:** 2026-01-20 | **Phase:** 3 of 3 (Documentation Sprint)

Practical examples demonstrating the collaboration bundle capabilities.

---

## Table of Contents

1. [Basic Operations](#basic-operations)
2. [Multi-Instance Handoff](#multi-instance-handoff)
3. [Document Workflows](#document-workflows)
4. [Recipe Examples](#recipe-examples)
5. [Complete Workflow](#complete-workflow-documentation-sprint)

---

## Basic Operations

### Posting Status Updates

```python
# Post to general channel when starting work
collab_channels(
    operation="post",
    channel_name="general",
    title="🚀 Starting: Code Review",
    message="Beginning review of authentication module. Session: abc123"
)

# Post completion
collab_channels(
    operation="post",
    channel_name="general",
    title="✅ Complete: Code Review",
    message="**Reviewed:** 12 files\n**Issues:** 3 minor\n**Report:** [link]"
)
```

### Reading Channel History

```python
# Check handoffs channel for work to pick up
messages = collab_channels(
    operation="read",
    channel_name="handoffs",
    limit=10
)

# Look for unclaimed tasks
for msg in messages:
    if "Handoff:" in msg.content and "Claimed" not in msg.content:
        print(f"Available: {msg.content}")
```

### Listing Users

```python
# Find team members
users = collab_directory(
    operation="list_users",
    limit=25
)

for user in users:
    print(f"{user.display_name} ({user.email})")
```

---

## Multi-Instance Handoff

### Creating a Handoff

When you need to pass work to another instance:

```python
# Step 1: Upload context document
handoff_doc = collab_documents(
    operation="upload",
    file_name="2026-01-20_handoff_api-review.md",
    content="""# Handoff: API Review

## Status
- Progress: 60% complete
- Reason: Session timeout approaching

## Work Done
- [x] Reviewed GET endpoints
- [x] Reviewed POST endpoints  
- [ ] Review DELETE endpoints
- [ ] Write summary

## Key Findings
- Rate limiting not implemented on /users endpoint
- Missing validation on POST /orders

## Next Steps
1. Complete DELETE endpoint review
2. Write findings summary
3. Post to general channel
""",
    folder_path="Amplifier/handoffs"
)

# Step 2: Post handoff notice to channel
collab_channels(
    operation="post",
    channel_name="handoffs",
    title="🔄 Handoff: API Review",
    message=f"""**Task:** Complete API security review
**Progress:** 60%
**Context:** {handoff_doc.web_url}
**Next:** Review DELETE endpoints, write summary"""
)
```

### Picking Up a Handoff

When starting a new session:

```python
# Step 1: Check for available work
messages = collab_channels(operation="read", channel_name="handoffs", limit=10)

# Step 2: Find unclaimed handoff
for msg in messages:
    if "Handoff:" in msg.title and "Claimed" not in msg.content:
        task = msg
        break

# Step 3: Claim the task
collab_channels(
    operation="post",
    channel_name="handoffs",
    title="✋ Claimed",
    message=f"Session xyz789 picking up: {task.title}"
)

# Step 4: Download context
context_doc = collab_documents(
    operation="download",
    document_id=extract_doc_id(task.content)
)

# Step 5: Continue work based on context...
```

---

## Document Workflows

### Uploading Work Artifacts

```python
# Upload analysis results
result = collab_documents(
    operation="upload",
    file_name="2026-01-20_report_security-audit.md",
    content="""# Security Audit Report

## Summary
Reviewed 45 endpoints across 3 services.

## Critical Issues
1. SQL injection vulnerability in search endpoint
2. Missing authentication on admin routes

## Recommendations
- Implement parameterized queries
- Add auth middleware to admin routes
""",
    folder_path="Amplifier/completed"
)

# Share the link
collab_channels(
    operation="post",
    channel_name="general",
    title="📄 New Report: Security Audit",
    message=f"Full report available: {result.web_url}"
)
```

### Listing Available Documents

```python
# List completed artifacts
docs = collab_documents(
    operation="list",
    folder_path="Amplifier/completed"
)

for doc in docs:
    print(f"{doc.name} - {doc.web_url}")
```

### Downloading for Reference

```python
# Get a previous report for reference
content = collab_documents(
    operation="download",
    document_id="abc123"
)

# Parse and use the content
previous_findings = parse_report(content)
```

---

## Recipe Examples

### Recipe: collaborative-task.yaml

Execute a task with full collaboration workflow:

```yaml
# Run with: amplifier recipe execute collaborative-task.yaml
name: collaborative-task
description: Execute a task with status updates and artifact sharing

inputs:
  task_description: "What needs to be done"
  notify_channel: "general"
  share_artifacts: true

steps:
  - id: announce-start
    prompt: |
      Post to {{notify_channel}} channel announcing you're starting:
      Task: {{task_description}}
      Include your session ID.

  - id: execute-task
    prompt: |
      Execute the task: {{task_description}}
      Document your findings and create any necessary artifacts.

  - id: upload-artifacts
    condition: "{{share_artifacts}}"
    prompt: |
      Upload your work artifacts to Amplifier/completed/
      Use naming convention: [date]_[type]_[description].md

  - id: announce-complete
    prompt: |
      Post completion to {{notify_channel}}:
      - What was done
      - Key findings
      - Links to artifacts
```

### Recipe: pickup-task.yaml

Scan for and claim available work:

```yaml
name: pickup-task
description: Check for and pick up available handoffs

inputs:
  auto_claim: true

steps:
  - id: scan-handoffs
    prompt: |
      Read the last 10 messages from the handoffs channel.
      Look for unclaimed tasks (no "Claimed" reply).
      List available tasks.

  - id: select-task
    prompt: |
      From the available tasks, select one that matches your capabilities.
      If no tasks available, report that and end.

  - id: claim-task
    condition: "{{auto_claim}}"
    prompt: |
      Post to handoffs channel claiming the selected task.
      Include your session ID.

  - id: download-context
    prompt: |
      Download the handoff context document.
      Summarize what needs to be done.

  - id: continue-work
    prompt: |
      Continue the work from where the previous instance left off.
      Follow the "Next Steps" from the handoff document.
```

---

## Complete Workflow: Documentation Sprint

This example shows the full workflow used to create this documentation:

### Phase 1: Initial Scan

```python
# 1. Announce start
collab_channels(
    operation="post",
    channel_name="general",
    title="🚀 Starting: Codebase Documentation Sprint",
    message="Beginning comprehensive documentation. Phases: Scan, Interfaces, Examples"
)

# 2. Execute Phase 1 (scan codebase, create catalog)
# ... work happens ...

# 3. Create artifact
collab_documents(
    operation="upload",
    file_name="2026-01-20_report_component-catalog.md",
    content="# Component Catalog\n...",
    folder_path="Amplifier/completed"
)

# 4. Announce completion
collab_channels(
    operation="post", 
    channel_name="general",
    title="✅ Phase 1 Complete",
    message="Component catalog created. 4 agents, 2 behaviors, 3 recipes documented."
)
```

### Phase 2: Handoff

```python
# 1. Create handoff document
collab_documents(
    operation="upload",
    file_name="2026-01-20_handoff_phase2.md",
    content="# Handoff: Phase 2...",
    folder_path="Amplifier/handoffs"
)

# 2. Post handoff
collab_channels(
    operation="post",
    channel_name="handoffs",
    title="🔄 Handoff: Phase 2 - Provider Interfaces",
    message="Phase 1 complete. Next: Document all provider interfaces."
)

# 3. Claim handoff (same or different instance)
collab_channels(
    operation="post",
    channel_name="handoffs",
    title="✋ Claimed",
    message="Picking up Phase 2"
)

# 4. Execute Phase 2...
```

### Phase 3: Completion

```python
# 1. Final artifact
collab_documents(
    operation="upload",
    file_name="2026-01-20_report_usage-examples.md",
    content="# Usage Examples\n...",
    folder_path="Amplifier/completed"
)

# 2. Final announcement
collab_channels(
    operation="post",
    channel_name="general",
    title="🎉 Documentation Sprint Complete",
    message="""**Created:**
- Component Catalog
- Provider Interfaces Reference  
- Usage Examples Guide

**Files:** Amplifier/completed/
**Duration:** 3 phases across multiple instances"""
)
```

---

## Shell Script Usage

For quick posting from command line:

```bash
# Post status update
./scripts/teams_post.sh general "Status Title" "Message content here"

# Post alert
./scripts/teams_post.sh alerts "🚨 Alert" "Something needs attention"

# Post handoff
./scripts/teams_post.sh handoffs "🔄 Handoff: Task Name" "Context and next steps"
```

---

## Tips & Best Practices

### Do

- ✅ Always announce when starting significant work
- ✅ Include session ID in handoff messages for tracing
- ✅ Upload documents rather than pasting long content
- ✅ Use consistent naming conventions for files
- ✅ Post completion status with links to artifacts

### Don't

- ❌ Paste large content directly in channel messages
- ❌ Leave work unclaimed in handoffs for too long
- ❌ Forget to check handoffs channel when starting
- ❌ Skip the completion announcement

---

*Generated as part of the Codebase Documentation Sprint*
