# Bulldogs Directors Cut - Game Jam Retrospective

**Event:** 2026 Epic AI MegaJam (Nov 11-15)
**Team:** Bellevue College Bulldogs (5 members)
**Result:** Submitted VR experience with 6 levels for Meta Quest 3

---

## Executive Summary

We shipped a hand-tracking-only VR game with 6 levels inspired by iconic movie scenes. The pre-jam infrastructure investment (MCP servers, build scripts, VR framework) paid off significantly. The main challenges were Android build pipeline issues and coordinating remote team members. AI tools (Claude Code, Hyper3D Rodin) were essential for velocity.

---

## What We Built

### Final Product
- **6 Levels:** MainMenu, TheFall, CliffPath, CanyonBridge, Highway, CarHop
- **Platform:** Meta Quest 3, hand tracking only (no controllers)
- **Engine:** Unreal Engine 5.8 + Meta XR SDK + ISDK
- **APK Size:** 293 MB (all data bundled)

### Team Contributions
| Member | Contribution |
|--------|-------------|
| Wendell | Lead dev, VR integration, TheFall, CarHop, build pipeline |
| Rob | CliffPath level (rock dodge), delivered during family emergency |
| Brian | Highway level layout |
| ln37 | 3D modeling (bridge, canyon assets) |
| Jacob | Audio design |

---

## What Worked Well

### 1. Pre-Jam Infrastructure Investment

**MCP Server Setup (UnrealMCPython/GenOrca)**
- Automated actor spawning, material creation, Blueprint node wiring
- Reduced repetitive editor clicking by ~70%
- Could iterate on level layouts via code instead of manual placement

**Build Scripts**
- `build_full_apk.bat`, `deploy_quest.bat`, `push_paks.bat`
- One-command build-to-device workflow
- Saved 10-15 minutes per iteration vs manual process

**VR Framework (XRFramework)**
- Pre-built input mappings, grab components, teleport system
- BP_VRPawn_ISDK ready to drop into any level
- Didn't waste jam time on VR boilerplate

### 2. AI Tools Integration

**Claude Code**
- Fixed obscure build errors (GameFeatureData, Gradle config cache)
- Generated Blueprint wiring documentation when GenOrca couldn't automate
- Managed git, Discord search, submission packaging
- Estimated 40% of coding velocity came from AI assistance

**Hyper3D Rodin**
- Generated car models for CarHop level
- Faster than searching asset stores or modeling from scratch

**metavr MCP**
- Device management, APK installation, logcat debugging
- Screenshot capture for visual verification
- Didn't need to remember ADB commands

### 3. Documentation-First Approach

- Created setup guides before teammates needed them
- `Quest3_Setup_Guide.md`, `Git_Quickstart_Guide.md`
- Reduced support burden during crunch time
- Team could self-serve instead of waiting for help

### 4. Standalone APK Strategy

- Set `bPackageDataInsideApk=True` early
- No OBB file management headaches
- Simpler sideloading instructions for judges
- 293 MB is acceptable for Quest 3

---

## What Didn't Work

### 1. Android Build Pipeline Fragility

**Problem:** Multiple build failures requiring manual fixes after each cook
- Gradle configuration cache incompatible with UE5.8
- NDK_VERSION set to invalid "NDK" string
- AssetManagerSettings in wrong .ini file

**Impact:** Lost 3-4 hours debugging build issues on final day

**Root Cause:**
- Using Unity's Android SDK instead of Unreal's (SDK r27c not configured)
- UE5.8 + Gradle 8.13 compatibility issues not documented
- Unreal overwrites gradle.properties on each cook

### 2. GenOrca Limitations Hit at Critical Moments

**Couldn't Automate:**
- BreakStruct nodes (needed for ISDK poke filtering)
- Object reference pins (sounds, materials)
- Component bound events
- Deleting Blueprint nodes

**Impact:** Had to write manual wiring documentation instead of automation

**Workaround:** Created detailed markdown guides for manual steps

### 3. Team Coordination Gaps

**Problem:** Brian's submission info (itch.io, Epic email) never collected

**Impact:** Submission may list only 4 of 5 team members

**Root Cause:**
- Relied on Discord bot ping instead of direct outreach
- No single owner for "collect team info" task
- Left until final hours

### 4. Package Name Inconsistency

**Problem:** Two different package names in config files
- `gradle.properties`: `com.YourCompany.BulldogMegaJam`
- `DefaultGame.ini`: `com.bulldog.directorscut`

**Impact:** Minor (sideloading works), but unprofessional for store submission

**Root Cause:** Changed name mid-project, didn't update all locations

### 5. No Automated Testing

**Problem:** No way to verify levels worked without putting on headset

**Impact:**
- Bugs discovered late in process
- Manual QA bottleneck on one person with Quest 3
- Couldn't parallelize testing

---

## Lessons Learned

### Technical

1. **Fix build pipeline BEFORE jam starts**
   - Do a full Android build to device during pre-jam week
   - Document every manual fix needed
   - Create scripts that apply fixes automatically

2. **Know your tools' limits**
   - GenOrca is powerful but has gaps
   - Have fallback plan (manual docs) ready
   - File GitHub issues during jam for post-jam fixes

3. **Pin your dependency versions**
   - Gradle version, NDK version, SDK version
   - Don't let Unreal auto-detect and overwrite

4. **Test on device daily**
   - Don't save device testing for final day
   - Each level should run on Quest before merging

### Process

5. **Collect team info on Day 1**
   - itch.io username, Epic email, Discord ID
   - Put in shared doc immediately
   - Don't rely on people responding to pings

6. **Single source of truth for project settings**
   - Package name, version, display name in ONE file
   - Script to propagate to all config locations

7. **Pre-assign submission tasks**
   - Cover image, video capture, description copy, README
   - Don't assume "someone will do it"

8. **Buffer time for build issues**
   - Plan for 4-6 hours of build debugging
   - Don't schedule submission for deadline hour

### Team

9. **Daily async standups work**
   - Discord #standup channel kept everyone informed
   - Format: What I did / What I'm doing / Blockers
   - Didn't need synchronous meetings

10. **Respect life happens**
    - Rob delivered a full level while his mom was in ICU
    - Remote async work enabled this
    - Don't require camera-on calls during crunch

---

## Recommendations for Next Jam

### One Week Before

- [ ] Full Android build to device, document all fixes
- [ ] Create `fix_gradle.bat` script to apply fixes automatically
- [ ] Verify all team members can clone repo and open project
- [ ] Collect itch.io usernames and Epic emails in shared doc
- [ ] Test MCP servers work on all dev machines

### Day 1

- [ ] Agree on package name, stick to it
- [ ] Create placeholder levels for each planned experience
- [ ] Assign level ownership explicitly
- [ ] Set up CI build if possible (even just "does it cook")

### Daily

- [ ] Post standup by noon
- [ ] Test at least one level on device
- [ ] Commit working code before signing off

### Final Day

- [ ] Code freeze 6 hours before deadline
- [ ] Build buffer for 2 failed builds
- [ ] Have submission materials ready (cover, video, description)
- [ ] Designate one person to click "Submit"

---

## Tools We'd Use Again

| Tool | Verdict | Notes |
|------|---------|-------|
| Claude Code | Essential | Build debugging, code generation, docs |
| UnrealMCPython (GenOrca) | Essential | Editor automation, despite limitations |
| metavr MCP | Essential | Device management, no ADB memorization |
| Hyper3D Rodin | Useful | Fast 3D assets, quality varies |
| Discord MCP | Nice to have | Team coordination, message search |

## Tools We'd Add

| Tool | Why |
|------|-----|
| Automated build CI | Catch breaks early |
| VR replay/recording | Test without wearing headset |
| Asset validation | Catch missing refs before cook |

---

## Final Thoughts

The jam was a success despite the challenges. We shipped a complete, playable VR experience with 6 levels in 4 days. The pre-jam infrastructure investment was the difference between shipping and not shipping.

The biggest time sink was build pipeline issues on the final day. Solving this before the next jam would free up 4-6 hours for actual development.

AI tools weren't a gimmick—they provided real velocity gains. Claude Code's ability to debug obscure Gradle/Unreal errors and generate documentation was particularly valuable.

For the next jam: fix the build pipeline first, collect team info immediately, and buffer more time for submission.

---

*Generated: November 15, 2026*
*Team Bulldogs - Bellevue College*
