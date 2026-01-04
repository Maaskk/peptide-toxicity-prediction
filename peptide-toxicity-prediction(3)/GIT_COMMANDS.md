# Git Commands to Update GitHub

Quick reference for pushing your changes to GitHub.

## Commands to Run

```bash
# 1. Check what files have changed
git status

# 2. Add all new and modified files
git add .

# Or add specific files:
# git add INSTALLATION.md START_HERE.md README.md GITHUB_SETUP.md .gitignore

# 3. Check what will be committed
git status

# 4. Commit with a message
git commit -m "Add installation guides and improve documentation"

# 5. Push to GitHub
git push

# If this is your first push, use:
# git push -u origin main
```

## Full Command Sequence (Copy & Paste)

```bash
git add .
git commit -m "Add installation guides: START_HERE.md, INSTALLATION.md, GITHUB_SETUP.md and update README"
git push
```

## If You Get Errors

### "Please tell me who you are"
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### "Permission denied"
- Use a Personal Access Token instead of password
- GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Use the token as your password when pushing

### "Remote origin already exists"
```bash
# Check current remote
git remote -v

# Update if needed
git remote set-url origin https://github.com/yourusername/peptide-toxicity-prediction.git
```

## What Will Be Uploaded

✅ **Included:**
- `START_HERE.md` (new)
- `INSTALLATION.md` (updated)
- `README.md` (updated)
- `GITHUB_SETUP.md` (new)
- `.gitignore` (updated)

❌ **Excluded** (by .gitignore):
- `LEARNING_GUIDE.md`
- `COMPLETE_DOCUMENTATION.md`
- `COMPLETE_SETUP_GUIDE.md`
- `DATA_SETUP.md`
- `node_modules/`
- `venv/`
- `results/`
- `data/raw/*.fasta`

