# VR Preview Quick Test - No Pawn Required

**Goal:** Test if the level is visible in VR and controls are glowing properly

**Time:** 2-3 minutes

---

## Setup (One-Time)

### Enable VR Preview Mode

1. In Unreal Editor, click the **▼** dropdown next to the **Play** button (top toolbar)
2. Select **"VR Preview"**
3. The Play button icon should change to show VR headset

### Connect Quest 3

**Option 1: Quest Link (USB Cable)**
1. Connect Quest 3 to PC via USB-C cable
2. Put on headset
3. Allow USB connection
4. Quest Link should start automatically

**Option 2: Air Link (Wireless)**
1. Put on Quest 3
2. Go to Quick Settings → Quest Link
3. Select your PC from the list
4. Enable Air Link

**Verify connection:**
- You should see your PC desktop in VR
- Quest controllers should work as mouse/pointer

---

## Quick Test Procedure

### In Unreal Editor:

1. **Open level:** `Content/ColdStart/Levels/L_ColdStart`
2. **Save level:** Ctrl+S
3. **Click Play** (VR Preview mode should be active)
4. **Put on Quest 3 headset**

### What You Should See:

**✅ Success indicators:**
- You appear in a dark room
- You can look around (head tracking works)
- You see glowing colored controls on the walls:
  - **Red** control on West wall (CO2 button)
  - **Orange/Yellow** controls on West wall (guard cover + switch)
  - **Cyan/Green** control on East wall (breaker)
- **Green text** on North wall (SystemStatusDisplay)
- Room is dark but controls are clearly visible

**❌ Problems to watch for:**
- **Black screen** = lighting too dark (increase SkyLight)
- **White/washed out** = lighting too bright (reduce ambient)
- **Controls not visible** = materials not set correctly
- **No head tracking** = VR Link not connected

### Testing Checklist:

- [ ] Level loads (not black screen)
- [ ] Can look around (360° head tracking)
- [ ] See 4 colored controls glowing
- [ ] Controls are distinct colors (red, orange, cyan)
- [ ] SystemStatusDisplay text visible on North wall
- [ ] Room feels dark (like emergency lighting)
- [ ] No performance issues (smooth 72fps)

### Stop Testing:

Press **Esc** key (or click Stop in editor)

---

## Troubleshooting

### "Black screen in VR"
**Cause:** Camera spawn point might be wrong
**Fix:**
- Stop VR Preview
- In World Outliner, find **PlayerStart** (if it exists)
- Set Location to (0, 0, 100)
- Or VR Preview will spawn you at world origin

### "Can't enter VR Preview"
**Cause:** Quest Link not connected
**Fix:**
- Verify Quest Link is active (you see PC desktop in headset)
- Try unplugging/replugging USB cable
- Or restart Air Link

### "Controls not glowing"
**Cause:** Material parameters may have reverted
**Fix:** We'll check this after your test (report what you see)

### "Everything is white/bright"
**Cause:** SkyLight intensity too high
**Fix:** After test, adjust lighting values

### "Performance is stuttering"
**Cause:** Editor overhead
**Fix:**
- Close other programs
- Or test on Quest (build APK) for real performance
- VR Preview is heavier than standalone Quest

---

## What to Report Back

After testing, tell me:

1. **Did it work?** (Yes/No/Partially)
2. **What you saw:**
   - Colors of controls (red? orange? cyan?)
   - Brightness (too dark? too bright? just right?)
   - Text visible?
3. **Any issues:**
   - Black screen?
   - Performance problems?
   - Controls not visible?

---

## After Testing

Once you confirm the level works in VR Preview, we'll proceed to **Option B**: Adding proper hand tracking pawn so you can interact with controls using your hands.

---

**Ready to test?**

1. Make sure Quest Link/Air Link is active
2. Open `L_ColdStart` level in Unreal
3. Click Play (VR Preview)
4. Put on headset
5. Report what you see!

---

**Estimated test time:** 2-3 minutes
