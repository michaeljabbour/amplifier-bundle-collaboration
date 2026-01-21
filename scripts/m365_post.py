#!/usr/bin/env python3
"""Direct M365 Teams posting via Graph API.

This script posts messages to Teams channels using the Graph API directly,
bypassing the need for webhook configuration.

Usage:
    python m365_post.py --channel amplifier-handoffs --title "Test" --message "Hello"

Environment variables required:
    M365_TENANT_ID, M365_CLIENT_ID, M365_CLIENT_SECRET, M365_TEAM_ID
"""

import argparse
import asyncio
import os
import sys

from azure.identity import ClientSecretCredential
from msgraph.graph_service_client import GraphServiceClient
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody


# Channel name to ID mapping (set during setup)
CHANNEL_IDS = {
    "amplifier-general": "19:ec912d8300ce415786f158f0894eea2d@thread.tacv2",
    "amplifier-alerts": "19:b768c53adcd647169dc09c8212716bde@thread.tacv2",
    "amplifier-handoffs": "19:ebb7657e6d794ad9b2e488b8b088c479@thread.tacv2",
    # Aliases
    "general": "19:ec912d8300ce415786f158f0894eea2d@thread.tacv2",
    "alerts": "19:b768c53adcd647169dc09c8212716bde@thread.tacv2",
    "handoffs": "19:ebb7657e6d794ad9b2e488b8b088c479@thread.tacv2",
}


async def post_to_teams(
    channel_name: str, message: str, title: str | None = None
) -> str:
    """Post a message to a Teams channel via Graph API."""
    # Get config from environment
    tenant_id = os.environ.get("M365_TENANT_ID")
    client_id = os.environ.get("M365_CLIENT_ID")
    client_secret = os.environ.get("M365_CLIENT_SECRET")
    team_id = os.environ.get("M365_TEAM_ID", "724b4b22-6936-41c9-918f-b7aecf05c31f")

    if not tenant_id or not client_id or not client_secret:
        raise ValueError("Missing M365 credentials in environment")

    # Get channel ID
    channel_id = CHANNEL_IDS.get(channel_name)
    if not channel_id:
        raise ValueError(
            f"Unknown channel: {channel_name}. Available: {list(CHANNEL_IDS.keys())}"
        )

    # Create Graph client
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    client = GraphServiceClient(credentials=credential)

    # Format message content
    if title:
        content = f"<b>{title}</b><br/><br/>{message}"
    else:
        content = message

    # Create and post message
    chat_message = ChatMessage(
        body=ItemBody(
            content_type=BodyType.Html,
            content=content,
        )
    )

    result = await (
        client.teams.by_team_id(team_id)
        .channels.by_channel_id(channel_id)
        .messages.post(chat_message)
    )

    if result and result.web_url:
        return result.web_url
    return "Posted successfully"


def main() -> None:
    parser = argparse.ArgumentParser(description="Post to Teams channel")
    parser.add_argument(
        "--channel",
        "-c",
        required=True,
        help="Channel name (general, alerts, handoffs)",
    )
    parser.add_argument("--message", "-m", required=True, help="Message content")
    parser.add_argument("--title", "-t", help="Optional title/header")

    args = parser.parse_args()

    try:
        result = asyncio.run(post_to_teams(args.channel, args.message, args.title))
        print(f"✅ Posted to {args.channel}")
        print(f"   URL: {result}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
