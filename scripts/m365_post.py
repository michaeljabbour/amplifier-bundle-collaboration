#!/usr/bin/env python3
"""Direct M365 Teams posting via Graph API.

This script posts messages to Teams channels using the Graph API directly,
bypassing the need for webhook configuration.

Usage:
    python m365_post.py --channel amplifier-handoffs --title "Test" --message "Hello"

Required environment variables:
    M365_TENANT_ID          - Azure AD tenant ID
    M365_CLIENT_ID          - App registration client ID
    M365_CLIENT_SECRET      - App registration client secret
    M365_TEAM_ID            - Teams team ID
    M365_CHANNEL_GENERAL    - Channel ID for 'general'
    M365_CHANNEL_ALERTS     - Channel ID for 'alerts'
    M365_CHANNEL_HANDOFFS   - Channel ID for 'handoffs'
"""

import argparse
import asyncio
import os
import sys

from azure.identity import ClientSecretCredential
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody
from msgraph.graph_service_client import GraphServiceClient


def get_required_env(name: str) -> str:
    """Get a required environment variable or raise ValueError."""
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_channel_id(channel_name: str) -> str:
    """Get channel ID from environment variable based on channel name."""
    channel_map = {
        "general": "M365_CHANNEL_GENERAL",
        "amplifier-general": "M365_CHANNEL_GENERAL",
        "alerts": "M365_CHANNEL_ALERTS",
        "amplifier-alerts": "M365_CHANNEL_ALERTS",
        "handoffs": "M365_CHANNEL_HANDOFFS",
        "amplifier-handoffs": "M365_CHANNEL_HANDOFFS",
    }

    env_var = channel_map.get(channel_name)
    if not env_var:
        available = ["general", "alerts", "handoffs"]
        raise ValueError(f"Unknown channel: {channel_name}. Available: {available}")

    channel_id = os.environ.get(env_var)
    if not channel_id:
        raise ValueError(
            f"Missing environment variable {env_var} for channel '{channel_name}'"
        )

    return channel_id


async def post_to_teams(
    channel_name: str, message: str, title: str | None = None
) -> str:
    """Post a message to a Teams channel via Graph API."""
    # Get config from environment (all required)
    tenant_id = get_required_env("M365_TENANT_ID")
    client_id = get_required_env("M365_CLIENT_ID")
    client_secret = get_required_env("M365_CLIENT_SECRET")
    team_id = get_required_env("M365_TEAM_ID")

    # Get channel ID from environment
    channel_id = get_channel_id(channel_name)

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
