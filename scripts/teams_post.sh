#!/bin/bash
# Post to Teams channel using Azure CLI (delegated user permissions)
# Usage: ./teams_post.sh <channel> <title> <message>

TEAM_ID="${M365_TEAM_ID:-724b4b22-6936-41c9-918f-b7aecf05c31f}"

CHANNEL_NAME="$1"
TITLE="$2"
MESSAGE="$3"

if [ -z "$CHANNEL_NAME" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: $0 <channel> <title> <message>"
    echo "Channels: general, alerts, handoffs"
    exit 1
fi

# Channel mapping (POSIX-compatible)
case "$CHANNEL_NAME" in
    general|amplifier-general)
        CHANNEL_ID="19:ec912d8300ce415786f158f0894eea2d@thread.tacv2"
        ;;
    alerts|amplifier-alerts)
        CHANNEL_ID="19:b768c53adcd647169dc09c8212716bde@thread.tacv2"
        ;;
    handoffs|amplifier-handoffs)
        CHANNEL_ID="19:ebb7657e6d794ad9b2e488b8b088c479@thread.tacv2"
        ;;
    *)
        echo "Unknown channel: $CHANNEL_NAME"
        echo "Available: general, alerts, handoffs"
        exit 1
        ;;
esac

# Format content
if [ -n "$TITLE" ]; then
    CONTENT="<b>$TITLE</b><br/><br/>$MESSAGE"
else
    CONTENT="$MESSAGE"
fi

# Escape for JSON
CONTENT=$(echo "$CONTENT" | sed 's/"/\\"/g')

az rest --method POST \
    --url "https://graph.microsoft.com/v1.0/teams/$TEAM_ID/channels/$CHANNEL_ID/messages" \
    --body "{\"body\": {\"contentType\": \"html\", \"content\": \"$CONTENT\"}}" \
    --query 'webUrl' -o tsv 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Posted to $CHANNEL_NAME"
else
    echo "❌ Failed to post"
    exit 1
fi
