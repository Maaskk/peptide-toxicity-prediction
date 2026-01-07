# GitHub Setup

This guide explains how to upload this project to GitHub.

## Prerequisites

- Git installed
- A GitHub account
- A GitHub repository created (empty is easiest)

## Steps

1. Initialize git in the project folder:

```bash
git init
```

2. Add the GitHub remote:

```bash
git remote add origin https://github.com/<username>/<repo>.git
```

3. Commit your files:

```bash
git add -A
git commit -m "Initial commit"
```

4. Push to GitHub:

```bash
git branch -M main
git push -u origin main
```

## Notes

- If the GitHub repository already contains commits, you may need to pull first and resolve conflicts.
- If you use SSH, replace the remote URL with the SSH URL from GitHub.
