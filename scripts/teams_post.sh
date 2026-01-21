#!/bin/bash
# Post to Teams channel using Azure CLI (delegated user permissions)
# Usage: ./teams_post.sh <channel> <title> <message>
#
# Required environment variables:
#   M365_TEAM_ID              - Teams team ID
#   M365_CHANNEL_GENERAL      - Channel ID for 'general'
#   M365_CHANNEL_ALERTS       - Channel ID for 'alerts'
#   M365_CHANNEL_HANDOFFS     - Channel ID for 'handoffs'

TEAM_ID="${M365_TEAM_ID}"

if [ -z "$TEAM_ID" ]; then
    echo "❌ Error: M365_TEAM_ID environment variable is required"
    exit 1
fi

CHANNEL_NAME="$1"
TITLE="$2"
MESSAGE="$3"

if [ -z "$CHANNEL_NAME" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: $0 <channel> <title> <message>"
    echo "Channels: general, alerts, handoffs"
    exit 1
fi

# Channel mapping from environment variables
case "$CHANNEL_NAME" in
    general|amplifier-general)
        CHANNEL_ID="${M365_CHANNEL_GENERAL}"
        ;;
    alerts|amplifier-alerts)
        CHANNEL_ID="${M365_CHANNEL_ALERTS}"
        ;;
    handoffs|amplifier-handoffs)
        CHANNEL_ID="${M365_CHANNEL_HANDOFFS}"
        ;;
    *)
        echo "Unknown channel: $CHANNEL_NAME"
        echo "Available: general, alerts, handoffs"
        exit 1
        ;;
esac

if [ -z "$CHANNEL_ID" ]; then
    echo "❌ Error: M365_CHANNEL_${CHANNEL_NAME^^} environment variable is required"
    exit 1
fi

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
