# Publishing Automation Guide

Complete guide to automated publishing of Criminal Intelligence Database GSD milestones to LinkedIn, GitHub, and Word resume.

---

## 🚀 Quick Start

### **One Command to Publish Everything:**
```batch
publish_all.bat
```
Enter your milestone number (1-6) and the script will:
- ✅ Update GitHub (README, badges, release)
- ✅ Generate LinkedIn post content
- ✅ Create Word resume
- ⏳ Canva remains manual

---

## 📋 Individual Platform Publishing

### **1. LinkedIn Publishing**
```batch
publish_linkedin.bat
```

**What it does:**
- Generates professional LinkedIn post content
- 3 post styles: Technical, Impact, or Storytelling
- Saves content to `reports/` directory
- Optionally posts directly via LinkedIn API

**Options:**
1. **Technical** - Detailed, for data science audience
2. **Impact** - Business-focused, broader appeal
3. **Storytelling** - Engaging narrative format

**Manual Steps:**
1. Run the batch file
2. Review generated content in `reports/linkedin_milestone_X_YYYYMMDD.txt`
3. Copy to LinkedIn
4. Add images from `reports/figures/` or `visualizations/`
5. Post on Tuesday-Thursday, 8-10 AM for best engagement

**API Setup (Optional):**
To enable automatic posting:
1. Create LinkedIn App: https://www.linkedin.com/developers/apps
2. Get Access Token
3. Set environment variable:
   ```batch
   set LINKEDIN_ACCESS_TOKEN=your_token_here
   ```
4. Run without `--save-only` flag

---

### **2. GitHub Publishing**
```batch
publish_github.bat
```

**What it does:**
- Updates README.md with milestone status
- Adds/updates GitHub badges
- Creates GitHub releases (requires GitHub CLI)
- Commits changes automatically

**Options:**
1. Update README only
2. Add/update badges
3. Create GitHub release
4. Commit changes
5. Do everything (recommended)

**GitHub CLI Setup (Optional):**
For automatic release creation:
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`
3. Script will create releases automatically

**Manual Steps if CLI not installed:**
1. Script generates release notes in `reports/`
2. Go to GitHub → Releases → Draft new release
3. Copy content from release notes file

---

### **3. Word Resume Generation**
```batch
generate_resume.bat
```

**What it does:**
- Generates professional one-page Word resume (.docx)
- Highlights completed milestones
- Includes AI-assisted development achievements
- Automatically opens in Microsoft Word

**Output:**
- File: `reports/Resume_HEDIS_GSD_YYYYMMDD_HHMMSS.docx`
- Format: One-page, ATS-friendly
- Content: Featured project + skills + metrics

**Customization:**
1. Open generated Word document
2. Update contact information (name, phone, email, etc.)
3. Review and adjust content as needed
4. Save as PDF for applications

---

## 🛠️ Setup Instructions

### **Initial Setup (One Time)**

1. **Install Python Dependencies:**
   ```batch
   pip install -r requirements.txt
   ```
   
   This installs:
   - `requests` - For LinkedIn API (optional)
   - `python-docx` - For Word resume generation (required)

2. **Configure Environment Variables (Optional):**
   ```batch
   # For LinkedIn API automation
   set LINKEDIN_ACCESS_TOKEN=your_token_here
   
   # For GitHub API (if not using gh CLI)
   set GITHUB_TOKEN=your_github_token
   ```

3. **Test Installation:**
   ```batch
   python scripts/publish_to_linkedin.py --help
   python scripts/publish_to_github.py --help
   python scripts/generate_resume_word.py --help
   ```

---

## 📊 Automation Scripts

### **Python Scripts (scripts/ directory)**

| Script | Purpose | Requirements |
|--------|---------|--------------|
| `publish_to_linkedin.py` | LinkedIn content generation & posting | requests (optional) |
| `publish_to_github.py` | GitHub updates & releases | GitHub CLI (optional) |
| `generate_resume_word.py` | Word resume generation | python-docx (required) |

### **Batch Files (root directory)**

| Batch File | Purpose | Platforms |
|------------|---------|-----------|
| `publish_all.bat` | **All-in-one publishing** | LinkedIn, GitHub, Resume |
| `publish_linkedin.bat` | LinkedIn content only | LinkedIn |
| `publish_github.bat` | GitHub updates only | GitHub |
| `generate_resume.bat` | Resume generation only | Resume |

---

## 🔄 Complete Publishing Workflow

### **After Completing a Milestone:**

#### **Step 1: Run Master Script**
```batch
publish_all.bat
```
- Enter milestone number (e.g., 1)
- Script runs all automation

#### **Step 2: GitHub** (Automated)
- README updated with milestone status ✅
- Badges added/updated ✅
- Release notes generated ✅
- Changes committed locally ✅

**Manual action:**
```bash
git push origin main
```

#### **Step 3: LinkedIn** (Semi-Automated)
- Post content generated ✅
- Saved to reports/ directory ✅

**Manual actions:**
1. Open `reports/linkedin_milestone_X_YYYYMMDD.txt`
2. Copy content
3. Paste to LinkedIn
4. Add images:
   - `reports/figures/model_performance_dashboard.png`
   - `visualizations/shap_importance.png`
5. Post on Tuesday-Thursday, 8-10 AM

#### **Step 4: Resume** (Automated)
- Word document generated ✅
- Opens automatically in Word ✅

**Manual actions:**
1. Update contact information
2. Review content
3. Save as PDF
4. Use for applications

#### **Step 5: Canva** (Manual)
```batch
optimize_portfolio.bat
```
- Follow existing manual process
- Copy content from generated file
- Update portfolio manually

---

## 📝 Command Line Usage

### **LinkedIn Publishing**

```bash
# Save content only (default, no API needed)
python scripts/publish_to_linkedin.py --milestone 1 --save-only

# Generate different post styles
python scripts/publish_to_linkedin.py --milestone 1 --post-type technical
python scripts/publish_to_linkedin.py --milestone 1 --post-type impact
python scripts/publish_to_linkedin.py --milestone 1 --post-type storytelling

# Dry run (show what would be posted)
python scripts/publish_to_linkedin.py --milestone 1 --dry-run

# Actually post (requires LinkedIn API setup)
python scripts/publish_to_linkedin.py --milestone 1 --post-type technical
```

### **GitHub Publishing**

```bash
# Update README only
python scripts/publish_to_github.py --update-readme

# Add badges only
python scripts/publish_to_github.py --add-badges

# Create release (requires milestone)
python scripts/publish_to_github.py --milestone 1 --create-release

# Do everything
python scripts/publish_to_github.py --milestone 1 --all

# Dry run
python scripts/publish_to_github.py --milestone 1 --all --dry-run
```

### **Resume Generation**

```bash
# Generate resume
python scripts/generate_resume_word.py

# Generate and mark milestone as published
python scripts/generate_resume_word.py --milestone 1

# Specify output filename
python scripts/generate_resume_word.py --output MyResume.docx

# Choose style
python scripts/generate_resume_word.py --style modern
```

---

## 🎯 Milestone Publishing Status

The automation automatically tracks publishing status in `milestones.json`:

```json
{
  "id": 1,
  "title": "Foundation & Data Pipeline",
  "status": "completed",
  "publishing_status": {
    "github": "published",    // Auto-updated
    "linkedin": "published",   // Auto-updated
    "canva": "pending",       // Manual
    "resume": "published"     // Auto-updated
  }
}
```

---

## 🔍 Troubleshooting

### **Python Dependencies Missing**
```batch
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt

# Install specific package
pip install python-docx
pip install requests
```

### **LinkedIn API Not Working**
- Check access token is set
- Token may have expired (regenerate)
- Fallback: Use `--save-only` flag and post manually

### **GitHub CLI Not Found**
- Install from: https://cli.github.com/
- Or use manual release creation
- Script still generates release notes file

### **Word Resume Not Opening**
- Ensure Microsoft Word is installed
- File still created in reports/ directory
- Open manually if auto-open fails

### **Script Errors**
```batch
# Check Python version
python --version  # Should be 3.11+

# Test scripts individually
python scripts/publish_to_linkedin.py --help
python scripts/publish_to_github.py --help
python scripts/generate_resume_word.py --help
```

---

## 📈 Advanced Usage

### **Customize Resume Content**

Edit `scripts/generate_resume_word.py`:
- Update `add_header()` with your information
- Modify `add_summary()` for custom summary
- Adjust `add_skills()` for your skills

### **Customize LinkedIn Posts**

Edit `scripts/publish_to_linkedin.py`:
- Modify `_generate_technical_post()` for technical style
- Update `_generate_impact_post()` for impact style
- Customize `_generate_storytelling_post()` for storytelling

### **Batch Processing Multiple Milestones**

```bash
# Publish milestones 1 and 2
for /l %i in (1,1,2) do python scripts/publish_to_github.py --milestone %i --all
```

---

## 🔐 Security Best Practices

### **API Tokens**
- Never commit tokens to Git
- Use environment variables only
- Rotate tokens regularly
- Use minimal required permissions

### **File Permissions**
- Generated files saved to reports/ (gitignored)
- Review content before publishing
- Don't commit sensitive information

---

## 📚 File Locations

### **Generated Files**

| File | Location | Purpose |
|------|----------|---------|
| LinkedIn posts | `reports/linkedin_milestone_X_*.txt` | Post content |
| Release notes | `reports/release_notes_milestone_X.md` | GitHub releases |
| Resumes | `reports/Resume_HEDIS_GSD_*.docx` | Word resumes |

### **Configuration**

| File | Purpose |
|------|---------|
| `milestones.json` | Milestone data and status |
| `requirements.txt` | Python dependencies |

---

## ✅ Success Checklist

After running `publish_all.bat`:

- [ ] GitHub README updated with milestone status
- [ ] GitHub badges added/refreshed
- [ ] GitHub release notes generated
- [ ] Changes committed locally
- [ ] LinkedIn post content generated
- [ ] Word resume created
- [ ] Manual: Push to GitHub
- [ ] Manual: Post to LinkedIn
- [ ] Manual: Update Canva portfolio
- [ ] Manual: Save resume as PDF

---

## 🎓 Tips & Best Practices

### **LinkedIn Posting**
- Post Tuesday-Thursday, 8-10 AM EST for best engagement
- Always include images (SHAP plots, performance dashboards)
- Use hashtags in comments, not in main post
- Respond to comments within 2 hours

### **GitHub**
- Create releases for major milestones (1, 2, 3)
- Keep README badges up-to-date
- Link to releases in LinkedIn posts
- Tag releases with semantic versioning

### **Resume**
- Generate new resume after each milestone
- Keep Word version for easy updates
- Export to PDF for applications
- Maintain consistent formatting

### **Automation**
- Run `publish_all.bat` after completing milestone
- Review all generated content before publishing
- Update milestones.json manually if needed
- Test with `--dry-run` flag first

---

## 📞 Support

### **Documentation**
- Main guide: `README_AUTOMATION.md`
- This guide: `docs/PUBLISHING_AUTOMATION_GUIDE.md`
- Script help: `python scripts/[script_name].py --help`

### **Common Issues**
1. **Dependencies:** Run `pip install -r requirements.txt`
2. **Permissions:** Run scripts from project root
3. **API Issues:** Use manual fallback options

---

## 🚀 Summary

**Fully Automated:**
- ✅ GitHub README & badges
- ✅ GitHub release notes generation
- ✅ Word resume generation
- ✅ LinkedIn content generation

**Semi-Automated (API Optional):**
- ⚠️ LinkedIn posting (can be automated with API)
- ⚠️ GitHub releases (requires GitHub CLI)

**Manual:**
- ⏳ LinkedIn posting (copy-paste content)
- ⏳ GitHub push (git push)
- ⏳ Resume customization
- ⏳ Canva portfolio updates

**One-Click Solution:**
```batch
publish_all.bat
```

---

**Last Updated:** October 21, 2025  
**Version:** 1.0.0




---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
