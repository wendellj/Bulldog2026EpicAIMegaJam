# Bulldog MegaJam - Development Log

**Project:** ColdStart VR (Bulldog 2026 Epic AI MegaJam)
**Team:** [Your team name]
**Event Dates:** November 11-15, 2026
**Target:** Glass Box Prize ($2,500 for best dev log)

---

## How to Use This Dev Log

**Daily entries should include:**
- Screenshots/screen recordings of progress
- Key decisions made (why we chose X over Y)
- Technical challenges solved
- AI tools used (Claude Code, GenOrca, etc.)
- Team collaboration moments

**Media Locations:**
- Screenshots: `devlog_media/screenshots/`
- Videos: `devlog_media/videos/`
- Discord exports: `devlog_media/discord/`

**Auto-Generated Evidence:**
- Git commits (timeline of code changes)
- Discord standup posts (decision rationale)
- Python scripts in `Game/` (AI-assisted development)

---

## Pre-Jam Setup (Nov 2-3, 2026)

### Nov 2: Initial Project Setup

**What we built:**
- Unreal Engine 5.8 project configured for Meta Quest 3
- Android build pipeline using Unity's SDK (workaround for UE5.8 SDK issue)
- UnrealMCPython (GenOrca) integration for AI-assisted development

**Key decisions:**
- **Platform:** Meta Quest 3 standalone (no PC tethering)
- **Genre:** VR escape room / puzzle (ColdStart MVP)
- **Scope:** First 10 minutes only (Phases 0-2, no drone)

**Tools:**
- Claude Code for development assistance
- GenOrca (UnrealMCPython) for procedural level editing
- Git for version control

**Evidence:**
- Initial commit: `efb2638` (Git quickstart guide)
- Setup documentation: `SETUP_GENORCA_INSTRUCTIONS.md`

### Nov 3: ColdStart MVP - Level Design

**What we built:**
- 2.7m x 2.7m ship interior room (matches Quest 3 guardian)
- 4 interactive controls (CO2 button, guard cover, switch, breaker)
- Emissive material system for glowing controls in darkness
- VR pawn with hand tracking support

**Technical challenges solved:**

1. **Lighting in VR darkness:**
   - Problem: Default lighting too bright, controls not visible
   - Solution: Reduced ambient to 1.25% intensity, used emissive materials (HDR 10.0+) for self-illuminated controls
   - Tools: GenOrca for batch lighting adjustment

2. **Control visibility:**
   - Problem: Blueprint components not rendering in VR
   - Solution: Repositioned from ±138cm to ±130cm (inside wall bounds), fixed scales
   - Tools: GenOrca structured actions instead of raw Python API

3. **Hand tracking setup:**
   - Problem: Controllers showing instead of hands
   - Solution: Added Meta XR Building Blocks VR Pawn with OculusXRHandComponent
   - Config: DefaultEngine.ini already had HandTrackingSupport=ControllersAndHands

**AI assistance:**
- Claude Code wrote ~50 Python scripts for level manipulation
- GenOrca API prevented type conversion issues vs raw Python
- Automated material parameter setting for colored glows

**Screenshots:**
- `editor_screenshot.png` - Level layout in editor
- `editor_screenshot2.png` - Control placements
- `quest_screen.png` - VR view (dark scene with glowing controls)

**Git commits:**
- Multiple WIP commits (see git log for full timeline)

---

## Day 1: [Date] - [Title]

### Morning Session

**Goal:** [What you're trying to accomplish]

**Progress:**
- [Bullet points of what got done]

**Screenshots:**
- [Link to media file]

**Technical notes:**
- [Any interesting solutions or AI-assisted wins]

### Afternoon Session

**Goal:** [What you're trying to accomplish]

**Progress:**
- [Bullet points]

**Blockers:**
- [Any issues that need solving]

---

## Day 2: [Date] - [Title]

[Continue daily format]

---

## Reflection: What Worked

**AI Tools:**
- [How Claude/GenOrca helped]
- [Specific examples of time saved]

**Team Collaboration:**
- [Communication wins]
- [Division of labor]

**Technical Wins:**
- [Clever solutions]
- [Performance optimizations]

---

## Reflection: What We'd Do Differently

**Process:**
- [Lessons learned]

**Technical:**
- [Better approaches we discovered]

**Scope:**
- [Feature cut decisions]

---

## Final Submission

**Build info:**
- Platform: Meta Quest 3
- Engine: Unreal Engine 5.8
- Package: `com.YourCompany.BulldogMegaJam`

**Play time:** ~10 minutes

**Core mechanic:** [Brief description]

**Team credits:**
- [Names and roles]

**Special thanks:**
- Claude Code / Anthropic (AI development assistant)
- GenOrca / zenoengine (Unreal Python automation)
- Bellevue College XR Lab (equipment loan)

---

## Appendix: Key Files

**Documentation:**
- `DEVELOPMENT.md` - Setup and workflow guide
- `SETUP_GENORCA_INSTRUCTIONS.md` - Team onboarding
- `VR_TEST_CHECKLIST.md` - QA checklist

**Build Scripts:**
- `cook_android.bat` - Content cooking
- `build_apk_nocache.bat` - APK build
- `create_obb.ps1` - OBB packaging
- `deploy_quest.bat` - Quest deployment

**Level Files:**
- `Content/ColdStart/Levels/L_ColdStart.umap` - Main level
- `Content/ColdStart/Blueprints/` - Interactive components
- `Content/ColdStart/Materials/` - Emissive glow materials

**Git Stats:**
- Total commits: [tbd]
- Contributors: [tbd]
- Files changed: [tbd]
- Lines of code: [tbd]

---

**Last Updated:** 2026-11-03
**Status:** Pre-jam preparation complete, ready for Nov 11 kickoff
