# Bulldog 2026 Epic AI MegaJam - Git Setup

## Working from a Lab Computer (USB Drive)

If you're working from a campus lab, you'll need a **64GB USB drive** (minimum 32GB).

**First time setup on USB:**

1. Plug in your USB drive and note the drive letter (e.g., `E:`)
2. Install Git Portable (no admin needed):
   - Download from https://git-scm.com/download/win
   - Choose "64-bit Git for Windows Portable"
   - Extract to your USB drive (e.g., `E:\GitPortable`)
3. Run `E:\GitPortable\git-bash.exe` to open Git Bash
4. Clone the repo to your USB:
   ```
   cd /e
   git lfs install
   git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git
   ```

**Each lab session:**

1. Plug in USB, open `E:\GitPortable\git-bash.exe`
2. Navigate to project: `cd /e/Bulldog2026EpicAIMegaJam`
3. Pull latest changes: `git pull`
4. Open the `.uproject` file in Unreal (should be installed on lab machines)
5. Before leaving: commit and push your changes

**Important:** The Intermediate and DerivedDataCache folders are not saved to Git. They rebuild automatically when you open the project, which takes a few minutes on first launch.

---

## Installing on Your Own Computer

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

## Set Up Claude AI (Free)

We're using Claude as our AI coding assistant.

1. Go to https://claude.ai
2. Click "Sign up"
3. Use your @students.bellevuecollege.edu email
4. Verify your email

Free tier gives you limited messages per day. For heavier use during the jam, consider Claude Pro ($20/month).

**Claude Code (CLI tool):**
If you want Claude in your terminal:
```
npm install -g @anthropic-ai/claude-code
claude
```
Requires Node.js 18+. Download from https://nodejs.org if needed.

## Need Help?

Post in the Slack channel: **Bulldog2026EpicAIMegaJam**

## Links

- Repository: https://github.com/wendellj/Bulldog2026EpicAIMegaJam
- Epic AI MegaJam: https://itch.io/jam/2026-epic-ai-megajam
- Jam Dates: November 12-15, 2026
