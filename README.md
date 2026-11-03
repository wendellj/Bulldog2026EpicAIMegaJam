# ColdStart MVP - Bulldog MegaJam 2026

**A VR escape room experience for Meta Quest 3**

**Event:** Epic AI MegaJam 2026 (November 11-15)
**Engine:** Unreal Engine 5.8
**Platform:** Meta Quest 3 Standalone

---

## Quick Links

- **[Team Onboarding](SETUP_GENORCA_INSTRUCTIONS.md)** - Get started developing
- **[Development Guide](DEVELOPMENT.md)** - Workflows and best practices
- **[VR Test Checklist](VR_TEST_CHECKLIST.md)** - QA before build/deploy
- **[Dev Log](DEVLOG.md)** - Glass Box prize submission ($2,500)

---

## Project Overview

**ColdStart MVP** is a VR puzzle experience set in a darkened spaceship. Players use hand tracking to manipulate physical controls to restore emergency power.

**Scope:** First 10 minutes (Phases 0-2)
- Phase 0: Cold open, CO2 emergency
- Phase 1: Restore emergency power
- Phase 2: Diagnose fault tree

**Play Space:** 2.7m x 2.7m room-scale (matches Quest 3 guardian)

---

## Getting Started

### Prerequisites
- Windows 10/11
- Unreal Engine 5.8
- Python 3.11
- Meta Quest 3
- Git

### Setup (First Time)
1. Clone repo: `git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git`
2. Follow: **[SETUP_GENORCA_INSTRUCTIONS.md](SETUP_GENORCA_INSTRUCTIONS.md)**
3. Launch editor: `Game\LaunchEditor.bat`
4. Test VR Preview works

### Daily Workflow
1. Run cleanup: `python Game/cleanup_level.py`
2. Develop and test in VR Preview
3. Follow: **[VR_TEST_CHECKLIST.md](VR_TEST_CHECKLIST.md)**
4. Update: **[DEVLOG.md](DEVLOG.md)**
5. Commit and push

---

## Build & Deploy

### Quick Deploy (PC VR Testing)
- Click **⋮** next to Play → **VR Preview**
- Requires Quest Link (USB or Air Link)

### Full Quest Build
```bash
cook_android.bat         # 1. Cook content
build_apk_nocache.bat    # 2. Build APK
create_obb.ps1           # 3. Create OBB
deploy_quest.bat         # 4. Deploy to Quest
```

### Content-Only Update
```bash
push_paks.bat            # Skip APK rebuild, just update paks
```

---

## Key Features

### AI-Assisted Development
- **Claude Code** - AI pair programmer
- **GenOrca (UnrealMCPython)** - Procedural editor automation
- **Structured actions** - Reliable Python API for Unreal

### VR Interaction
- **Hand tracking** - Controller-free interaction
- **Physical controls** - Buttons, switches, breakers
- **Emissive feedback** - Glowing colored indicators

### Performance Optimized
- 72fps on Quest 3
- Minimal real-time lighting (emissive materials)
- Efficient post-processing

---

## Project Structure

```
Game/
├── Content/ColdStart/
│   ├── Levels/L_ColdStart.umap
│   ├── Blueprints/          # Interactive components
│   ├── Materials/           # Emissive glow materials
│   └── UI/                  # Fault displays
├── Config/DefaultEngine.ini
├── Plugins/UnrealMCPython/  # GenOrca AI tools
└── .mcp.json               # MCP server config

devlog_media/               # Glass Box assets
├── screenshots/
├── videos/
└── discord/

DEVLOG.md                   # Dev log (Glass Box submission)
VR_TEST_CHECKLIST.md        # QA checklist
DEVELOPMENT.md              # Detailed workflows
SETUP_GENORCA_INSTRUCTIONS.md  # Team onboarding
```

---

## Team

- [Your names and roles]

---

## Documentation

- **Development Guide:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **VR Testing:** [VR_TEST_CHECKLIST.md](VR_TEST_CHECKLIST.md)
- **Setup Instructions:** [SETUP_GENORCA_INSTRUCTIONS.md](SETUP_GENORCA_INSTRUCTIONS.md)
- **Dev Log:** [DEVLOG.md](DEVLOG.md)

---

## Support

**Issues:** GitHub Issues
**Communication:** Discord #standup
**AI Assistant:** Claude Code (already integrated)

---

## License

[Your license here]

---

**Last Updated:** 2026-11-03
**Status:** Pre-jam preparation complete
