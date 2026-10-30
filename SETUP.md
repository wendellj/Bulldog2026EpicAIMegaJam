# Bulldog 2026 Epic AI MegaJam - Git Setup

## 1. Install Git

**Windows:**
Download and install from https://git-scm.com/download/win

Use default settings. When asked about line endings, choose "Checkout Windows-style, commit Unix-style."

**Mac:**
```
xcode-select --install
```

## 2. Install Git LFS

**Windows:**
Download and install from https://git-lfs.com

**Mac:**
```
brew install git-lfs
```

## 3. Configure Git (first time only)

Open a terminal (Git Bash on Windows, Terminal on Mac) and run:

```
git config --global user.name "Your Name"
git config --global user.email "your.email@students.bellevuecollege.edu"
git lfs install
```

## 4. Clone the Repository

```
git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git
```

This downloads the project to a folder called `Bulldog2026EpicAIMegaJam`.

## 5. Open the Project

```
cd Bulldog2026EpicAIMegaJam
```

Read the manifesto:
```
cat Manifesto.txt
```

## Daily Workflow

**Before you start working:**
```
git pull
```

**After making changes:**
```
git add .
git commit -m "Brief description of what you changed"
git push
```

**If push fails (someone else pushed first):**
```
git pull --rebase
git push
```

## Need Help?

Post in the Slack channel: **Bulldog2026EpicAIMegaJam**

## Links

- Repository: https://github.com/wendellj/Bulldog2026EpicAIMegaJam
- Epic AI MegaJam: https://itch.io/jam/2026-epic-ai-megajam
- Jam Dates: November 12-15, 2026
