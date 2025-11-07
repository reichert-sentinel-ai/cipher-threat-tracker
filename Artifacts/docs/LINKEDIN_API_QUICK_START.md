# LinkedIn API Quick Start

**⚡ Fast track to automatic LinkedIn posting - 10 minutes**

---

## 🎯 Goal
Enable one-command automatic posting to LinkedIn for your Criminal Intelligence Database GSD milestones.

---

## 📋 What You'll Need
- LinkedIn account
- 10 minutes
- Python 3.11+ installed

---

## 🚀 5-Step Setup

### Step 1: Create LinkedIn App (3 min)

1. **Open:** https://www.linkedin.com/developers/apps
2. **Click:** "Create app"
3. **Fill in:**
   - App name: `HEDIS GSD Publisher`
   - LinkedIn Page: Select yours or create test page
   - Check legal agreement
4. **Click:** "Create app"

---

### Step 2: Configure App (2 min)

1. **Click:** "Auth" tab
2. **Copy these:**
   - Client ID: `78a9s8df...`
   - Client Secret: Click "Show" → copy
3. **Add redirect URL:**
   - `http://localhost:8888/callback`
   - Click "Add"
4. **Request scopes:**
   - `r_liteprofile`
   - `w_member_social`

---

### Step 3: Set Credentials (30 sec)

**Open PowerShell and run:**
```powershell
$env:LINKEDIN_CLIENT_ID="paste_your_client_id"
$env:LINKEDIN_CLIENT_SECRET="paste_your_client_secret"
```

---

### Step 4: Run Setup Script (3 min)

```batch
setup_linkedin_api.bat
```

**What happens:**
1. Browser opens LinkedIn authorization page
2. Click "Allow"
3. Copy redirect URL from browser (page won't load, that's OK!)
4. Paste URL into script
5. Script saves token to `set_linkedin_token.bat`

**Expected output:**
```
✅ Access token obtained!
✅ Token is valid and working!
✅ Created: set_linkedin_token.bat
```

---

### Step 5: Test Posting (1 min)

```batch
REM Set token for this session
call set_linkedin_token.bat

REM Test post (won't actually post)
python scripts/publish_to_linkedin.py --milestone 1 --dry-run

REM Real post
python scripts/publish_to_linkedin.py --milestone 1
```

**Success!** 🎉
```
✅ Successfully posted to LinkedIn!
```

---

## 🎯 Daily Usage

**Before each session:**
```batch
call set_linkedin_token.bat
```

**Then publish:**
```batch
publish_linkedin.bat
> Enter milestone: 1
> Enter choice: 1  (automatic posting)
```

**Or use master script:**
```batch
call set_linkedin_token.bat
publish_all.bat
```

---

## 🔄 Token Expires in 60 Days

**When token expires, re-run:**
```batch
setup_linkedin_api.bat
```

---

## ⚠️ Important Notes

### Security
**Add to `.gitignore`:**
```gitignore
.linkedin_token.json
set_linkedin_token.bat
.env
```

**Never commit:**
- Client ID
- Client Secret  
- Access Token

### Troubleshooting

**"redirect_uri_mismatch"**
- Check redirect URL is exactly: `http://localhost:8888/callback`

**"Token invalid"**
- Token expired (60 days) → re-run setup
- Run: `python scripts/linkedin_oauth_setup.py --test-token`

**"Credentials not found"**
- Set environment variables again:
```powershell
$env:LINKEDIN_CLIENT_ID="your_id"
$env:LINKEDIN_CLIENT_SECRET="your_secret"
```

---

## 📚 Full Documentation

For complete details:
- **Setup Guide:** `docs/LINKEDIN_API_SETUP_GUIDE.md`
- **Troubleshooting:** See guide above
- **API Docs:** https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin

---

## ✅ Setup Checklist

- [ ] Created LinkedIn app
- [ ] Got Client ID and Client Secret
- [ ] Set environment variables
- [ ] Ran `setup_linkedin_api.bat`
- [ ] Got access token
- [ ] Added files to `.gitignore`
- [ ] Tested with `--dry-run`
- [ ] Successfully posted

**Done?** You can now post automatically! 🚀

---

## 🎉 What's Next?

**Complete workflow:**
```batch
REM 1. Set token (once per session)
call set_linkedin_token.bat

REM 2. Publish everything
publish_all.bat

REM This will:
REM - Update GitHub
REM - Post to LinkedIn automatically
REM - Generate resume
```

**Time saved:** 40 minutes per milestone (85% reduction)

**Enjoy your automation!** 🚀



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
