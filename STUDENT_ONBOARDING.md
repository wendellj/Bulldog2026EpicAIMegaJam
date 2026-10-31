# Bulldog MegaJam 2026: Student Onboarding Guide

You're building a VR game for the 2026 Epic AI MegaJam. This guide covers everything you need to do before Nov 11.

## The Event

- **Dates**: Nov 12-15, 2026 (theme reveals Nov 11 at 11am PT)
- **What we're building**: Quest 3 VR experience in Unreal Engine 5
- **Team category**: Best Student Project (all team members must be enrolled students)
- **Prizes**: 1st $7,500 / 2nd $5,000 / 3rd $2,500 + possible modifier prizes

## Your Prep Schedule

| Date | What | Where |
|------|------|-------|
| Nov 1 (Sat) | Git 101 + Build Pipeline | N250 Lab or Discord |
| Nov 2 (Sun) | Equipment Pickup Day 1 | Library D126 |
| Nov 3 (Mon) | Equipment Pickup Day 2 + Software Install | Library D126 / XR Lab D126P |
| Nov 4 (Tue) | AI Tools Workshop | Discord / XR Lab |
| Nov 5 (Wed) | Asset Pipeline + Your First Contribution | Discord |
| Nov 7 (Fri) | Mini-Jam (2-hour prototype) | Discord / XR Lab |
| Nov 9 (Sun) | Theme Prep + Roles Confirmed | Discord |
| Nov 10 (Mon) | Final Sync + Submission Checklist | Discord |

---

## Nov 1: Git 101 + Build Pipeline

You'll learn these on lab computers before you pick up equipment. This way you can hit the ground running.

### Git Basics

Git tracks every change to our project. You don't need to master it, just know these commands:

```bash
# Get the project (do this once)
git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git

# Before you start working (always do this first)
git pull

# After you make changes
git add <filename>           # Stage specific file
git add .                    # Stage all changes (be careful)
git commit -m "What I did"   # Save changes locally
git push                     # Upload to GitHub
```

**The Golden Rule**: Always `git pull` before you start working. Always.

**When things go wrong**: If you see merge conflicts or errors, don't panic. Post in Discord. We'll fix it together.

### Build Pipeline Overview

The build process turns our Unreal project into an APK that runs on Quest 3:

1. **Cook** - Converts assets to Android format
2. **Package** - Builds the APK via Gradle
3. **Deploy** - Installs APK on Quest via USB
4. **Test** - Put on headset, run app

You'll watch Wendell do this end-to-end. During the jam, you won't need to build yourself unless you're assigned to it. But you should understand what happens.

**Key point**: Building takes time (15-45 minutes depending on changes). We don't rebuild constantly. We test in VR Preview mode during development, then do full builds for milestones.

---

## Nov 2-3: Equipment Pickup

### Laptop (Library Tech Hub, Room D126)

Walk up to the desk with your BC Student ID. Say:

> "I need a quarterly laptop loan. I need a high-performance machine capable of running Unreal Engine 5 for a game jam."

Do NOT accept a Chromebook or basic laptop. You need a machine with a dedicated GPU.

**Hours**: Mon-Thu 7:45am-8pm, Fri 7:45am-5pm, Sat-Sun 11am-5pm

### Quest 3 (XR Lab, Room D126P)

You should have already emailed xrlab@bellevuecollege.edu requesting an off-campus loan. If approved, visit during drop-in hours to sign the waiver and pick up the headset.

**Drop-in hours**: Tue/Wed/Thu 12pm-5pm

**What you get**: Quest 3 headset, controllers, charging cable

**Your responsibility**: Keep it safe. Charge it. Don't break it.

### After Pickup

1. Update Quest 3 firmware to latest version
2. Enable Developer Mode via Meta Developer account (ask if you need help)
3. Install Unreal Engine 5.8 on your laptop
4. Clone the project repo
5. Open the project in Unreal, let it compile shaders (this takes a while)
6. Confirm you can see the editor without errors

Post in Discord when you're set up: "Equipment picked up, project opens, ready to go."

---

## Nov 4: AI Tools Workshop

This is an AI MegaJam. You're allowed (encouraged) to use AI tools. Here's what's available:

### Allowed Before the Jam (Prep Now)
- AI tool configurations
- MCP (Model Context Protocol) settings
- Prompt libraries
- Scripts and automation

### Must Be Created During the Jam (Nov 12-15)
- All gameplay
- All levels
- All art assets (unless sourced and documented)
- All game content

### Tools You Should Know

| Tool | What It Does | How to Access |
|------|--------------|---------------|
| **Claude** | Code help, Blueprints, problem solving | claude.ai or Claude Code CLI |
| **ChatGPT** | Same, alternative | chatgpt.com |
| **GitHub Copilot** | Code completion in editor | VS Code extension (free for students) |
| **Suno** | AI music generation | suno.ai |
| **ElevenLabs** | AI voice generation | elevenlabs.io |
| **Midjourney/DALL-E** | Concept art, textures | midjourney.com / openai.com |
| **Meshy/Tripo** | 3D model generation | meshy.ai / tripo.ai |

### The Ten-Minute Rule (from TEAM_KICKOFF)

When you're stuck:
- 0-10 min: Try to solve it yourself
- 10-20 min: Ask Claude or ChatGPT
- 20-30 min: Post in Discord
- 30+ min: Tag Wendell directly

Do not sit stuck in silence. That wastes project time.

### Workshop Tasks

1. Sign up for Claude (if you haven't)
2. Try generating a Blueprint script with AI assistance
3. Try generating a sound effect with Suno
4. Try generating a texture with an image AI
5. Report what worked and what didn't

---

## Nov 5: Asset Pipeline + Your First Contribution

### How Assets Get Into Unreal

| Asset Type | Source Tool | Export Format | Import Location |
|------------|-------------|---------------|-----------------|
| 3D Models | Blender, Maya | FBX | Content/Models/ |
| Textures | Photoshop, GIMP | PNG, TGA | Content/Textures/ |
| Audio | Audacity, Suno | WAV (44.1kHz, 16-bit) | Content/Audio/ |
| UI Graphics | Figma, Photoshop | PNG | Content/UI/ |

### Naming Conventions

```
SM_RockLarge.fbx        # Static Mesh
SK_PlayerHand.fbx       # Skeletal Mesh
T_Rock_Diffuse.png      # Texture (Diffuse/Albedo)
T_Rock_Normal.png       # Texture (Normal map)
M_Rock.uasset           # Material
SFX_FootstepDirt.wav    # Sound Effect
MUS_Ambient01.wav       # Music
UI_ButtonPlay.png       # UI Element
```

### Your First Contribution

By end of Nov 5, everyone submits something to the repo:

- **Artists**: One placeholder asset (a cube, a texture, anything)
- **Audio**: One sound effect or music clip
- **Designers**: One design note in the docs folder
- **Programmers**: One Blueprint or code comment
- **Generalists**: Any of the above

This confirms your Git workflow works before the jam.

```bash
git pull
# Add your file to the appropriate folder
git add <your-file>
git commit -m "Add placeholder rock model - [YourName]"
git push
```

Post in Discord when done: "First commit pushed."

---

## Nov 7: Mini-Jam (2-Hour Prototype)

We're doing a practice run. Same rules as the real jam, compressed into 2 hours.

### Schedule (2 hours total)

| Time | Phase |
|------|-------|
| 0:00-0:10 | Theme reveal (Wendell picks a random word) |
| 0:10-0:20 | Brainstorm as team |
| 0:20-1:30 | Build something (anything) |
| 1:30-1:50 | Polish/fix |
| 1:50-2:00 | "Submit" (show what you made) |

### The Point

- Shake out communication issues
- See how fast 2 hours goes (hint: very fast)
- Practice making decisions under pressure
- Find gaps in your setup before they matter

### What We're NOT Doing

- Building something good
- Stressing about quality
- Working on the real game

This is practice. It's supposed to be messy.

---

## Nov 9: Theme Prep + Roles Confirmed

### Past MegaJam Themes

| Year | Theme |
|------|-------|
| 2025 | (Check closer to event) |
| 2023 | "Antiquated Future" |
| 2022 | "As Above, So Below" |
| 2021 | "Running Out of Space" |
| 2020 | "It's Been a Long Time, But We're Not Done Yet" |
| 2019 | "Down to Earth" |
| 2018 | "Reality Is Often Inaccurate" |

Themes are interpreted loosely. "Running Out of Space" spawned games about storage limits, cramped rooms, AND outer space.

### Theme Adaptation Strategy

Our core mechanic (edge-proximity locomotion in VR) can fit many themes:

| Theme Type | How We Adapt |
|------------|--------------|
| Space/cosmic | Zero-G environment, asteroid field |
| Memory/time | Memory palace, fading world |
| Contrast | Light/dark zones, inside/outside |
| Limits | Shrinking boundaries, resource scarcity |
| Nature | Cave exploration, forest |

When the theme drops Nov 11, we brainstorm for 30 minutes, pick a direction, and commit. No second-guessing.

### Role Confirmation

By Nov 9, confirm your role in Discord:

```
Name: [Your name]
Primary role: [Art / Audio / Design / Programming / Writing / Generalist]
Secondary role: [Your backup when primary is done or blocked]
Hours Nov 12-15: [Your availability each day]
```

---

## Nov 10: Final Sync + Submission Checklist

### Submission Requirements (from Official Rules)

Your submission MUST include:

| Requirement | Details |
|-------------|---------|
| **Playable build** | Windows packaged, playable on Win10/11 (Quest build is bonus) |
| **30-60 second video** | Recorded gameplay demonstrating the game |
| **Team info** | Full name and email of all team members |
| **Team owner** | One person designated to receive prize/communications |
| **Sourced assets list** | Any non-original assets must be documented |
| **itch.io page** | Submission goes through itch.io |

### Content Rules

- All content (text, audio, video) must be in English
- Must be appropriate for Teen audience (ESRB Teen equivalent)
- No trademarks except Unreal Engine logo
- No offensive, hateful, or illegal content

### Glass Box Prize ($2,500)

There's a $2,500 prize for best dev log. To be eligible:

- Document how you built the game
- Submit the dev log WITH your game

Our dev log sources:
- Git commit history
- Discord standup posts
- Screenshots/recordings during development
- Post-jam writeup

**Assign someone** to compile this on Nov 15.

### Final Checklist (Confirm by Nov 10)

- [ ] Project opens and runs on your machine
- [ ] You can pull/push to Git without errors
- [ ] You've made at least one commit
- [ ] You know your role and hours
- [ ] You have Discord notifications enabled
- [ ] Your Quest 3 is charged and developer mode is on
- [ ] You know where you'll be working Nov 12-15

---

## Judging Criteria

Judges score each category up to 5 points:

| Category | What They're Looking For |
|----------|-------------------------|
| **Ambition and Innovation** | Did you try something interesting? |
| **Use of Contest Theme** | Does the theme come through? |
| **Fun Factor** | Is it enjoyable to play? |
| **Gameplay** | Do the mechanics work? |
| **Visuals** | Does it look good (stylized counts)? |
| **Level Design** | Is the space well-designed? |
| **Audio** | Does sound enhance the experience? |

**Note**: AI use is considered for context but doesn't increase or decrease your score on its own. What matters is the final game.

---

## Quick Reference: Key Links

| Resource | Link |
|----------|------|
| GitHub Repo | https://github.com/wendellj/Bulldog2026EpicAIMegaJam |
| GitHub Issues | https://github.com/wendellj/Bulldog2026EpicAIMegaJam/issues |
| Epic AI MegaJam Page | https://itch.io/jam/2026-epic-ai-megajam |
| Official Rules | (see Rules folder in repo) |
| Theme Reveal Stream | https://www.twitch.tv/unrealengine (Nov 11, 11am PT) |

---

## Questions?

Post in Discord. Use the ten-minute rule. Don't sit stuck.

See you Nov 11.
