# GitHub Setup Guide

Step-by-step instructions for uploading this project to GitHub.

## Step 1: Create a GitHub Account (if you don't have one)

1. Go to [github.com](https://github.com)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create a New Repository

1. Click the **"+"** icon in the top right corner
2. Select **"New repository"**
3. Fill in the details:
   - **Repository name**: `peptide-toxicity-prediction` (or your preferred name)
   - **Description**: "Machine learning web application for predicting peptide toxicity"
   - **Visibility**: Choose Public or Private
   - **DO NOT** check "Initialize with README" (we already have files)
   - **DO NOT** add .gitignore or license (we already have them)
4. Click **"Create repository"**

## Step 3: Initialize Git in Your Project (if not already done)

Open a terminal in your project directory and run:

```bash
git init
```

## Step 4: Add All Files

```bash
git add .
```

**Note:** The `.gitignore` file will automatically exclude:
- `node_modules/`
- `venv/`
- `results/`
- `data/raw/*.fasta`
- Documentation files (LEARNING_GUIDE.md, COMPLETE_DOCUMENTATION.md, etc.)

## Step 5: Make Your First Commit

```bash
git commit -m "Initial commit: Peptide toxicity prediction web app"
```

## Step 6: Connect to GitHub

Copy the repository URL from GitHub (it looks like: `https://github.com/yourusername/peptide-toxicity-prediction.git`)

Then run:

```bash
git remote add origin https://github.com/yourusername/peptide-toxicity-prediction.git
```

Replace `yourusername` with your actual GitHub username.

## Step 7: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

You'll be prompted for your GitHub username and password/token.

## Step 8: Verify Upload

1. Go to your repository page on GitHub
2. Refresh the page
3. You should see all your project files

## Step 9: Update README.md (Optional)

Edit the main `README.md` file to:
- Add a project description
- Add screenshots
- Update installation instructions
- Add your name/credits

Then commit and push:

```bash
git add README.md
git commit -m "Update README with project details"
git push
```

## Excluded Files

These files are automatically excluded from GitHub (in `.gitignore`):

- **Documentation files**:
  - `LEARNING_GUIDE.md`
  - `COMPLETE_DOCUMENTATION.md`
  - `COMPLETE_SETUP_GUIDE.md`
  - `DATA_SETUP.md`

- **Dependencies**:
  - `node_modules/` (backend and frontend)
  - `venv/` (Python virtual environment)

- **Build outputs**:
  - `backend/dist/`
  - `frontend/dist/`
  - `results/` (trained models, plots)

- **Data files**:
  - `data/raw/*.fasta`
  - `data/predictions.db`

- **IDE/OS files**:
  - `.vscode/`
  - `.idea/`
  - `.DS_Store`

## Updating Your Repository

After making changes, update GitHub:

```bash
git add .
git commit -m "Description of your changes"
git push
```

## Adding a License (Optional)

1. Go to your repository on GitHub
2. Click "Add file" → "Create new file"
3. Name it `LICENSE`
4. Choose a license template (e.g., MIT, Apache 2.0)
5. Commit the file

## Adding Topics/Tags (Optional)

1. Go to your repository page
2. Click the gear icon next to "About"
3. Add topics like: `machine-learning`, `bioinformatics`, `python`, `vue`, `nestjs`, `peptides`

## Setting Up GitHub Pages (Optional - For Demo)

If you want to host a static demo:

1. Go to Settings → Pages
2. Select source branch: `main`
3. Select folder: `/frontend/dist`
4. Save

## Troubleshooting

### "Permission denied" error

- Use a Personal Access Token instead of password
- Generate token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when pushing

### "Remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/yourusername/peptide-toxicity-prediction.git
```

### "Large file" error

If you have large files, GitHub has a 100MB limit. The `.gitignore` should prevent this, but if you see this error:

```bash
# Remove large files from git history
git rm --cached path/to/large/file
git commit -m "Remove large file"
git push
```

## Done! 🎉

Your project is now on GitHub! Share the repository URL with others.

