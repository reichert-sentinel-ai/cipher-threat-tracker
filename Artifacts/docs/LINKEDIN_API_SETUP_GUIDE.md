# LinkedIn API Setup Guide

Complete guide to setting up automatic LinkedIn posting for your Criminal Intelligence Database GSD project milestones.

---

## 🎯 Overview

**What This Enables:**
- Automatic posting to LinkedIn with one command
- No manual copy-paste needed
- Direct API integration

**What You Need:**
- LinkedIn account
- LinkedIn Developer App (free)
- 15 minutes for initial setup
- Token renewal every 60 days

---

## 📋 Prerequisites

### Required
- ✅ LinkedIn account (personal or company page)
- ✅ Python 3.11+ installed
- ✅ `requests` library: `pip install requests`

### Optional (Recommended)
- ✅ LinkedIn Company Page (for professional posting)
- ✅ `.env` file support for secure credential storage

---

## 🚀 Quick Start (5 Steps)

### Step 1: Create LinkedIn App (5 min)

1. **Go to LinkedIn Developers:**
   https://www.linkedin.com/developers/apps

2. **Click "Create app"**

3. **Fill in app details:**
   ```
   App name: HEDIS GSD Publisher
   LinkedIn Page: [Your page or create test page]
   App logo: [Optional - use project logo]
   Legal agreement: Check the box
   ```

4. **Click "Create app"**

5. **Verify the app** (LinkedIn may send verification email)

---

### Step 2: Configure App Permissions (2 min)

1. **Go to "Auth" tab in your app**

2. **Add Redirect URLs:**
   ```
   http://localhost:8888/callback
   ```
   Click "Add redirect URL"

3. **Request OAuth 2.0 scopes:**
   - ✅ `r_liteprofile` - Read your profile
   - ✅ `w_member_social` - Post, comment and react as you

4. **Note your credentials:**
   - Copy **Client ID**
   - Copy **Client Secret** (click "Show" to reveal)

---

### Step 3: Set Environment Variables (1 min)

**Windows (PowerShell):**
```powershell
$env:LINKEDIN_CLIENT_ID="your_client_id_here"
$env:LINKEDIN_CLIENT_SECRET="your_client_secret_here"
```

**Windows (CMD):**
```batch
set LINKEDIN_CLIENT_ID=your_client_id_here
set LINKEDIN_CLIENT_SECRET=your_client_secret_here
```

**Or create `.env` file** (recommended):
```ini
# .env file in project root
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
```

**⚠️ Important:** Add `.env` to `.gitignore` to keep credentials secure!

---

### Step 4: Run OAuth Setup Script (3 min)

```batch
python scripts/linkedin_oauth_setup.py
```

**What happens:**
1. Script opens LinkedIn authorization URL in browser
2. You click "Allow" to authorize the app
3. Browser redirects to `http://localhost:8888/callback?code=...`
4. Copy the FULL redirect URL (page won't load, that's OK!)
5. Paste URL back into the script
6. Script exchanges code for access token
7. Token is saved to `set_linkedin_token.bat`

**Example output:**
```
✅ Access token obtained!
Token: AQXh8J2k3l4m5n6o7p8q9r0s1t2u3v...
Expires in: 5184000 seconds (60 days)

✅ Token is valid and working!
✅ Created: set_linkedin_token.bat
```

---

### Step 5: Test Automatic Posting (1 min)

**Set token for session:**
```batch
call set_linkedin_token.bat
```

**Test posting (dry run):**
```batch
python scripts/publish_to_linkedin.py --milestone 1 --dry-run
```

**Real post:**
```batch
python scripts/publish_to_linkedin.py --milestone 1
```

**Success output:**
```
✅ Successfully posted to LinkedIn!
📄 Content saved to: reports/linkedin_milestone_1_20251022.txt
```

---

## 📖 Detailed Setup Instructions

### Creating LinkedIn Developer App

#### 1. Navigate to Developer Portal
- URL: https://www.linkedin.com/developers/apps
- Sign in with your LinkedIn account

#### 2. Create New App
Click "Create app" button (top right)

#### 3. Fill Application Form

**App name:**
```
HEDIS GSD Publisher
```
*Or any name that describes your automation*

**LinkedIn Page:**
- **Option A:** Select existing Company Page
- **Option B:** Create test page:
  1. Go to https://www.linkedin.com/company/setup/new/
  2. Create page: "HEDIS GSD Project" (or similar)
  3. Return to app creation and select this page

**Privacy policy URL:** (Optional)
```
https://your-website.com/privacy
```

**App logo:** (Optional)
- Upload project logo or healthcare icon
- Size: 100x100px minimum

**Legal Agreement:**
- ✅ Check "I have read and agree to these terms"

#### 4. Click "Create app"

---

### Configuring OAuth Settings

#### 1. Go to "Auth" Tab
In your newly created app, click the "Auth" tab

#### 2. Note Your Credentials

**Client ID:**
```
Example: 78a9s8df7a9s8df7
```

**Client Secret:**
- Click "Show" to reveal
- Copy immediately (won't show again)

```
Example: A1B2C3D4E5F6G7H8
```

**⚠️ Keep these secure!** Don't commit to git.

#### 3. Add Redirect URLs

Click "Add redirect URL"

**For local development:**
```
http://localhost:8888/callback
```

**For production (if deploying):**
```
https://your-domain.com/linkedin/callback
```

Click "Add"

#### 4. OAuth 2.0 Scopes

Request these scopes:

| Scope | Purpose | Required |
|-------|---------|----------|
| `r_liteprofile` | Read your name, photo, headline | ✅ Yes |
| `w_member_social` | Post on your behalf | ✅ Yes |

**How to request:**
1. Scroll to "OAuth 2.0 scopes"
2. Click each scope
3. Click "Request access"
4. LinkedIn may require verification (email confirmation)

#### 5. Save Settings
Click "Update" at bottom of page

---

### Running OAuth Flow

#### Interactive Setup (Recommended)

```batch
python scripts/linkedin_oauth_setup.py
```

**Step-by-step prompts:**

**1. Enter Credentials** (if not in environment):
```
LinkedIn Client ID: [paste your client ID]
LinkedIn Client Secret: [paste your client secret]
```

**2. Authorize in Browser:**
- Script opens URL automatically
- Click "Allow" on LinkedIn page
- You'll be redirected to `http://localhost:8888/callback?code=...`

**3. Copy Redirect URL:**
```
Paste the redirect URL here: http://localhost:8888/callback?code=AQT...&state=hedis_gsd_publisher
```

**4. Get Token:**
```
✅ Access token obtained!
Token: AQXh8J2k3l4m5n6o7p8q9r0s1t2u3v...
Expires in: 5184000 seconds (60 days)
```

**5. Test Token:**
```
✅ Token valid! Authenticated as: John Doe
```

**6. Save Token:**
```
Save token to file? (y/n): y
✅ Token saved to: .linkedin_token.json
```

---

#### Manual Setup (Advanced)

If the interactive script doesn't work:

**1. Generate Auth URL:**
```python
from scripts.linkedin_oauth_setup import LinkedInOAuth

oauth = LinkedInOAuth(
    client_id='your_client_id',
    client_secret='your_client_secret'
)

auth_url = oauth.get_authorization_url()
print(auth_url)
```

**2. Visit URL in Browser**
Copy the auth URL and open in browser

**3. Authorize App**
Click "Allow"

**4. Extract Code from Redirect URL:**
```
Redirect URL: http://localhost:8888/callback?code=AQTa9b8c7d6e5f4&state=hedis_gsd_publisher

Code: AQTa9b8c7d6e5f4
```

**5. Exchange Code for Token:**
```python
token_data = oauth.exchange_code_for_token('AQTa9b8c7d6e5f4')
access_token = token_data['access_token']
print(f"Token: {access_token}")
```

**6. Save Token:**
```python
oauth.save_token_to_file(token_data)
```

---

## 🔐 Security Best Practices

### 1. Protect Credentials

**Never commit these to git:**
- ❌ Client ID
- ❌ Client Secret
- ❌ Access Token

**Add to `.gitignore`:**
```gitignore
# LinkedIn credentials
.env
.linkedin_token.json
set_linkedin_token.bat
```

### 2. Environment Variables

**Option A: Session Variables** (temporary)
```batch
set LINKEDIN_CLIENT_ID=xxx
set LINKEDIN_CLIENT_SECRET=yyy
set LINKEDIN_ACCESS_TOKEN=zzz
```

**Option B: `.env` File** (recommended)
```ini
LINKEDIN_CLIENT_ID=xxx
LINKEDIN_CLIENT_SECRET=yyy
LINKEDIN_ACCESS_TOKEN=zzz
```

**Option C: System Variables** (permanent)
1. Windows Settings → System → Advanced → Environment Variables
2. Add User Variables
3. Restart terminal

### 3. Token Storage

**Generated files:**
- ✅ `.linkedin_token.json` - Token data (add to .gitignore)
- ✅ `set_linkedin_token.bat` - Token setter (add to .gitignore)

**Loading token in scripts:**
```python
# Automatically loads from environment
publisher = LinkedInPublisher(milestone_id=1)

# Or from file
oauth = LinkedInOAuth()
token_data = oauth.load_token_from_file()
```

---

## 🧪 Testing the Integration

### Test 1: Verify Credentials

```batch
python scripts/linkedin_oauth_setup.py --test-token --token YOUR_ACCESS_TOKEN
```

**Expected output:**
```
✅ Token valid! Authenticated as: John Doe
✅ Token is valid!
```

### Test 2: Dry Run Posting

```batch
call set_linkedin_token.bat
python scripts/publish_to_linkedin.py --milestone 1 --dry-run
```

**Expected output:**
```
=== DRY RUN - Post Content ===
🎯 **Milestone 1 Complete: Core ML Pipeline**
... [post content] ...
==================================================
✅ DRY RUN complete. Content generated above.
```

### Test 3: Generate Content Only

```batch
python scripts/publish_to_linkedin.py --milestone 1 --save-only
```

**Expected output:**
```
✅ Post content saved to: reports/linkedin_milestone_1_20251022.txt
You can manually post this to LinkedIn or run without --save-only flag to auto-post
```

### Test 4: Real Posting

```batch
call set_linkedin_token.bat
python scripts/publish_to_linkedin.py --milestone 1
```

**Expected output:**
```
✅ Successfully posted to LinkedIn!
📄 Content saved to: reports/linkedin_milestone_1_20251022.txt
```

---

## 🔄 Token Renewal (Every 60 Days)

LinkedIn access tokens expire after **60 days**.

### Check Token Expiration

```batch
python scripts/linkedin_oauth_setup.py --test-token
```

**If expired:**
```
❌ Token is invalid or expired
```

### Renew Token

**Option 1: Run Setup Again**
```batch
python scripts/linkedin_oauth_setup.py
```

**Option 2: Manual Renewal**
1. Delete `.linkedin_token.json`
2. Run setup script
3. Follow OAuth flow again

**Option 3: Refresh Token** (Advanced)
LinkedIn doesn't provide refresh tokens for OAuth 2.0, so you must re-authenticate.

---

## 🛠️ Troubleshooting

### Issue 1: "redirect_uri_mismatch"

**Error:**
```
redirect_uri_mismatch: Redirect URI does not match
```

**Solution:**
1. Check LinkedIn app "Auth" tab
2. Ensure redirect URI is EXACTLY: `http://localhost:8888/callback`
3. No trailing slashes
4. HTTP not HTTPS for localhost

---

### Issue 2: "insufficient_permissions"

**Error:**
```
insufficient_permissions: Missing required scope
```

**Solution:**
1. Go to LinkedIn app → Auth tab
2. Request scopes:
   - `r_liteprofile`
   - `w_member_social`
3. Wait for approval (may take a few minutes)
4. Re-run OAuth flow

---

### Issue 3: "invalid_token"

**Error:**
```
invalid_token: The access token is invalid
```

**Causes:**
- Token expired (60 days)
- Token revoked
- Wrong token format

**Solution:**
```batch
# Re-run OAuth setup
python scripts/linkedin_oauth_setup.py
```

---

### Issue 4: "Could not open browser"

**Error:**
```
⚠️ Could not open browser automatically
```

**Solution:**
1. Manually copy the authorization URL
2. Open in any browser
3. Continue with OAuth flow

---

### Issue 5: Environment Variables Not Found

**Error:**
```
❌ LinkedIn credentials not found
Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET
```

**Solution:**

**PowerShell:**
```powershell
$env:LINKEDIN_CLIENT_ID="your_id"
$env:LINKEDIN_CLIENT_SECRET="your_secret"
```

**CMD:**
```batch
set LINKEDIN_CLIENT_ID=your_id
set LINKEDIN_CLIENT_SECRET=your_secret
```

**Verify:**
```batch
echo %LINKEDIN_CLIENT_ID%
echo %LINKEDIN_CLIENT_SECRET%
```

---

## 📱 LinkedIn App Verification

LinkedIn may require **app verification** for production use:

### Verification Process

1. **During development:** No verification needed
2. **After 90 days:** LinkedIn may review usage
3. **For production:** Submit verification request

### What LinkedIn Checks:
- ✅ Valid privacy policy
- ✅ Legitimate use case
- ✅ No spam or abuse
- ✅ Proper OAuth implementation

### Verification Timeline:
- Development: Immediate
- Light usage: 2-4 weeks
- Production: 4-6 weeks

**For this project:** Development mode is sufficient (posting from your own account)

---

## 🎯 Usage Examples

### Example 1: Post Milestone 1

```batch
REM Set token for session
call set_linkedin_token.bat

REM Post automatically
python scripts/publish_to_linkedin.py --milestone 1
```

### Example 2: Different Post Styles

```batch
REM Technical post
python scripts/publish_to_linkedin.py --milestone 1 --post-type technical

REM Impact-focused post
python scripts/publish_to_linkedin.py --milestone 1 --post-type impact

REM Storytelling post
python scripts/publish_to_linkedin.py --milestone 1 --post-type storytelling
```

### Example 3: Test Before Posting

```batch
REM 1. Generate content only
python scripts/publish_to_linkedin.py --milestone 1 --save-only

REM 2. Review the file
type reports\linkedin_milestone_1_*.txt

REM 3. If good, post for real
python scripts/publish_to_linkedin.py --milestone 1
```

### Example 4: Automated Workflow

```batch
REM Complete publishing workflow
call set_linkedin_token.bat
publish_all.bat
> Enter milestone: 1

REM This will:
REM - Update GitHub
REM - Post to LinkedIn automatically (if token set)
REM - Generate resume
```

---

## 📊 API Rate Limits

LinkedIn API limits (as of 2024):

| Limit Type | Limit | Window |
|------------|-------|--------|
| Posts per day | 25 | 24 hours |
| Posts per hour | 5 | 1 hour |
| API calls | 500 | 24 hours |

**For this project:**
- You're posting 1 milestone every few weeks
- Well within rate limits
- No concern about throttling

---

## 🔄 Updating Existing Scripts

The `publish_linkedin.bat` script automatically detects if you have a token set:

**Without token:**
```batch
python scripts/publish_to_linkedin.py --milestone 1 --save-only
> ✅ Post content saved (manual posting)
```

**With token:**
```batch
call set_linkedin_token.bat
python scripts/publish_to_linkedin.py --milestone 1
> ✅ Successfully posted to LinkedIn!
```

**To switch to automatic posting:**
1. Set up OAuth (this guide)
2. Run `call set_linkedin_token.bat` before publishing
3. Scripts automatically use API posting

---

## ✅ Setup Checklist

- [ ] Created LinkedIn Developer App
- [ ] Copied Client ID and Client Secret
- [ ] Added redirect URI: `http://localhost:8888/callback`
- [ ] Requested OAuth scopes: `r_liteprofile`, `w_member_social`
- [ ] Set environment variables (CLIENT_ID, CLIENT_SECRET)
- [ ] Ran `python scripts/linkedin_oauth_setup.py`
- [ ] Authorized app in browser
- [ ] Got access token
- [ ] Token saved to `set_linkedin_token.bat`
- [ ] Added to `.gitignore`: `.linkedin_token.json`, `set_linkedin_token.bat`
- [ ] Tested with dry run: `--dry-run`
- [ ] Successfully posted to LinkedIn

---

## 📞 Support

### LinkedIn Developer Documentation
- OAuth 2.0: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication
- Share API: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin
- Troubleshooting: https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/error-handling

### Project Help
- Run setup: `python scripts/linkedin_oauth_setup.py`
- Test token: `python scripts/linkedin_oauth_setup.py --test-token`
- Documentation: This file!

---

## 🎉 Next Steps

After setup is complete:

1. **Test posting:**
   ```batch
   call set_linkedin_token.bat
   python scripts/publish_to_linkedin.py --milestone 1 --dry-run
   ```

2. **Use in workflow:**
   ```batch
   call set_linkedin_token.bat
   publish_all.bat
   ```

3. **Set calendar reminder:**
   - Renew token every 60 days
   - Re-run `python scripts/linkedin_oauth_setup.py`

**Enjoy automatic LinkedIn posting!** 🚀



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
