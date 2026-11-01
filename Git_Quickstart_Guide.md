# Git Quickstart Guide for Artists

This guide covers the basics you need to contribute art to the project. No prior Git experience required.

---

## What is Git?

Git tracks every change to the project files. If something breaks, we can go back to a working version. It also lets multiple people work on the same project without overwriting each other's work.

**GitHub** is where our project lives online. Git is the tool that syncs your local files with GitHub.

---

## One-Time Setup

### 1. Install GitHub Desktop

Download and install from: https://desktop.github.com/

GitHub Desktop gives you a visual interface instead of typing commands.

### 2. Sign into GitHub

1. Open GitHub Desktop
2. Click **File** > **Options** (or **GitHub Desktop** > **Preferences** on Mac)
3. Click **Sign in** and log into your GitHub account
4. If you don't have an account, create one at https://github.com/join

### 3. Clone the Project

"Cloning" downloads a copy of the project to your computer.

1. In GitHub Desktop, click **File** > **Clone Repository**
2. Click the **URL** tab
3. Paste this URL: `https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git`
4. Choose where to save it (suggestion: `C:\Bulldog\Game`)
5. Click **Clone**

You now have the project on your computer.

---

## Daily Workflow

### Before You Start Working: Pull

Always pull before starting work. This downloads any changes your teammates made.

1. Open GitHub Desktop
2. Make sure **Bulldog2026EpicAIMegaJam** is selected in the top-left
3. Click **Fetch origin** (top right)
4. If it changes to **Pull origin**, click it again

You're now up to date.

### After You Finish Working: Commit and Push

When you've created or changed files, you need to commit (save a snapshot) and push (upload to GitHub).

1. Open GitHub Desktop
2. On the left side, you'll see a list of changed files
3. Check the boxes next to files you want to include
4. At the bottom left, type a short description of what you did:
   - Good: "Add character concept sketches"
   - Good: "Update environment textures"
   - Bad: "stuff" or "changes"
5. Click **Commit to master**
6. Click **Push origin** (top right)

Your files are now on GitHub for everyone to see.

---

## Where to Put Your Files

```
C:\Bulldog\Game\Content\
├── Art\
│   ├── Characters\      <- character art, concepts
│   ├── Environment\     <- backgrounds, props
│   ├── UI\              <- menus, icons, HUD elements
│   └── Textures\        <- texture files
└── Audio\               <- if you're also doing audio
```

Create subfolders as needed. Keep things organized.

### File Formats

| Type | Recommended Format |
|------|-------------------|
| Textures | PNG (with transparency) or TGA |
| 3D Models | FBX |
| Concepts/Reference | PNG or JPG |
| Audio | WAV (we'll compress later) |

---

## Common Situations

### "I see other people's changes but mine aren't showing"

You committed but forgot to push. Click **Push origin**.

### "It says I have conflicts"

This happens when you and someone else changed the same file. Don't panic.

1. Ask in Discord for help
2. Wendell or another programmer can help resolve it

For art files, the fix is usually: keep your version or keep theirs. We'll figure out which.

### "I accidentally deleted something"

Git remembers everything. Right-click the file in GitHub Desktop and look for **Discard changes** to restore it. If you already committed the deletion, ask for help in Discord.

### "I want to undo my last commit"

In GitHub Desktop: **Repository** > **Undo** (only works if you haven't pushed yet)

### "I made a mess and want to start fresh"

Delete your local folder and clone again. Your old work is gone locally, but anything you pushed is safe on GitHub.

---

## Quick Reference

| Task | How |
|------|-----|
| Get latest changes | **Fetch origin**, then **Pull origin** if available |
| Save your work | Check files, write description, **Commit**, then **Push** |
| See what changed | Look at the **Changes** tab in GitHub Desktop |
| See project history | Click **History** tab in GitHub Desktop |

---

## Tips

- **Pull before you start, push when you're done.** Make this a habit.
- **Commit often.** Small commits are easier to undo than big ones.
- **Write clear commit messages.** Future you will thank present you.
- **Don't commit Unreal's intermediate files.** The `.gitignore` file handles this automatically, but if you see thousands of files to commit, something's wrong. Ask for help.

---

## Getting Help

- **Git confusion**: Ask in #programming on Discord
- **GitHub account issues**: https://docs.github.com/en/get-started

