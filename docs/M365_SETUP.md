# Microsoft 365 Setup Guide

This guide walks through setting up Microsoft 365 integration for the collaboration bundle.

## Prerequisites

- Microsoft 365 tenant (production or developer)
- Azure AD admin access to register applications
- Teams channels for collaboration

## Step 1: Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
2. Click "New registration"
3. Configure:
   - **Name:** `Amplifier Collaboration`
   - **Supported account types:** Single tenant
   - **Redirect URI:** Leave blank (not needed for client credentials)
4. Click "Register"
5. Note the **Application (client) ID** and **Directory (tenant) ID**

## Step 2: Create Client Secret

1. In your app registration, go to "Certificates & secrets"
2. Click "New client secret"
3. Add description: `Amplifier`
4. Select expiration (recommend 24 months)
5. Click "Add"
6. **Copy the secret value immediately** (it won't be shown again)

## Step 3: Configure API Permissions

1. Go to "API permissions"
2. Click "Add a permission" → "Microsoft Graph" → "Application permissions"
3. Add these permissions:

| Permission | Purpose |
|------------|---------|
| `User.Read.All` | List/read users |
| `Group.Read.All` | List groups and teams |
| `ChannelMessage.Read.All` | Read channel messages |
| `Files.ReadWrite.All` | SharePoint file operations |
| `Mail.Send` | Send emails |
| `Tasks.Read.All` | Read Planner tasks |

4. Click "Grant admin consent for [tenant]"

## Step 4: Create Teams Webhooks

For each collaboration channel (general, alerts, handoffs):

1. In Teams, go to the channel
2. Click "..." → "Connectors"
3. Find "Incoming Webhook" → "Configure"
4. Name it (e.g., "Amplifier - General")
5. Click "Create"
6. **Copy the webhook URL**

## Step 5: Configure Environment Variables

```bash
# Azure AD credentials
export M365_TENANT_ID="your-tenant-id"
export M365_CLIENT_ID="your-client-id"
export M365_CLIENT_SECRET="your-client-secret"

# Teams webhooks (comma-separated name=url pairs)
export M365_TEAMS_WEBHOOKS="general=https://webhook1...,alerts=https://webhook2...,handoffs=https://webhook3..."
```

## Step 6: Verify Setup

Test the connection:

```bash
cd modules/tool-collaboration
python -c "
import asyncio
from amplifier_module_tool_collaboration.providers import get_provider

async def test():
    provider = get_provider('m365')
    users = await provider.list_users(limit=3)
    print(f'Found {len(users)} users')
    for u in users:
        print(f'  - {u.display_name} ({u.email})')

asyncio.run(test())
"
```

## Troubleshooting

### "Insufficient privileges"
- Ensure admin consent was granted for all permissions
- Wait a few minutes after granting consent

### "Invalid client secret"
- Secret may have expired
- Create a new secret and update environment variable

### "Tenant not found"
- Verify tenant ID is correct
- Ensure you're logging in to the right tenant

### Webhook returns 400/403
- Verify the webhook URL is complete and correct
- Check the connector is still active in Teams
- Recreate the webhook if needed

## Security Notes

- Store credentials in a secrets manager in production
- Use separate app registrations for dev/prod
- Rotate client secrets before expiration
- Monitor Graph API usage in Azure portal
- Consider using certificate auth instead of secrets for production
