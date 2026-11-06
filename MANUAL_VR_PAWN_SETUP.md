# Manual VR Pawn Setup - Step by Step

**Problem:** Meta XR Building Blocks tool not available in UE 5.8
**Solution:** Create VR pawn with hand tracking manually (10 minutes)

---

## Option 1: Create in Content Browser (Recommended)

### Step 1: Create Pawn Blueprint

1. In Content Browser, navigate to `/Game/ColdStart/Blueprints/`
2. Right-click in empty space → **Blueprint Class**
3. In "Pick Parent Class" window:
   - Click **"All Classes"** dropdown at top
   - Search for **"Pawn"**
   - Select **Pawn** (NOT DefaultPawn, NOT Character)
   - Click **Select**
4. Name it: **BP_VRPawn_HandTracking**
5. **Double-click** to open the blueprint editor

### Step 2: Add Camera Component

1. In **Components** panel (left side), click **+ Add** button
2. Search for **"Camera"**
3. Select **Camera** component
4. It will be added as a child of DefaultSceneRoot
5. This is the player's viewpoint

### Step 3: Add Left Motion Controller

1. Click **+ Add** again
2. Search for **"Motion Controller"**
3. Select **Motion Controller Component**
4. In **Details** panel (right side):
   - Find **Motion Source** property
   - Set to **"Left"**
5. Rename component to **MotionController_Left** (F2 key)

### Step 4: Add Left Hand Tracking

1. In **Components** panel, **select MotionController_Left**
2. Click **+ Add** button (this adds as child of selected component)
3. Search for **"Oculus Hand"** or **"OculusXR Hand"**
4. Select **OculusXR Hand Component**
5. In **Details** panel:
   - Find **Skeleton Type** property
   - Set to **"Hand Left"**
   - Find **Mesh Type** property
   - Set to **"Hand Left"**
6. Rename to **OculusXRHand_Left**

### Step 5: Add Right Motion Controller

1. In **Components** panel, **select DefaultSceneRoot** (click it)
2. Click **+ Add** button
3. Search for **"Motion Controller"**
4. Select **Motion Controller Component**
5. In **Details** panel:
   - Find **Motion Source** property
   - Set to **"Right"**
6. Rename to **MotionController_Right**

### Step 6: Add Right Hand Tracking

1. **Select MotionController_Right**
2. Click **+ Add** button
3. Search for **"Oculus Hand"**
4. Select **OculusXR Hand Component**
5. In **Details** panel:
   - **Skeleton Type** → **"Hand Right"**
   - **Mesh Type** → **"Hand Right"**
6. Rename to **OculusXRHand_Right**

### Step 7: Compile and Save

1. Click **Compile** button (top toolbar)
2. Click **Save** button
3. Close blueprint editor

### Step 8: Add to Level

1. In Content Browser, find **BP_VRPawn_HandTracking**
2. **Drag it** into the viewport
3. In **Details** panel, set **Transform → Location**:
   - X: **0**
   - Y: **0**
   - Z: **100** (standing height)
4. **Save level** (Ctrl+S)

### Step 9: Verify

Run: `python Game/verify_project_state.py`

Should show all components present!

---

## Option 2: Use Default VR Template Pawn

### If you have VR Template installed:

1. File → New Level → **VR Template** (if available)
2. Find the VR Pawn blueprint in the template content
3. Copy it to `/Game/ColdStart/Blueprints/`
4. Rename to **BP_VRPawn_HandTracking**
5. Place in level at (0, 0, 100)

---

## Expected Component Hierarchy

When done correctly, your blueprint should look like this:

```
BP_VRPawn_HandTracking (Pawn)
├─ DefaultSceneRoot (SceneComponent)
├─ Camera (CameraComponent)
├─ MotionController_Left (MotionControllerComponent)
│  └─ OculusXRHand_Left (OculusXRHandComponent)
└─ MotionController_Right (MotionControllerComponent)
   └─ OculusXRHand_Right (OculusXRHandComponent)
```

---

## Verification Checklist

After adding the VR pawn:

- [ ] Blueprint compiles without errors
- [ ] Pawn placed in level at (0, 0, 100)
- [ ] Camera component present
- [ ] 2 Motion Controllers (Left/Right)
- [ ] 2 OculusXRHand components (Left/Right)
- [ ] Run `verify_project_state.py` - passes

---

## Troubleshooting

### Can't find "OculusXR Hand Component"
- Try searching for just "Hand"
- Or try "Meta Hand Component"
- Make sure MetaXR plugin is enabled (Edit → Plugins → MetaXR)

### Components won't add
- Make sure you selected the parent component first
- Make sure blueprint is not in read-only mode

### Blueprint won't compile
- Check for errors in **Compiler Results** panel
- Make sure all components have valid properties set

---

## Quick Test

After setup, test VR Preview:

1. Click **⋮** next to Play button
2. Select **"VR Preview"**
3. Put on Quest 3 (with Link/Air Link active)
4. You should see the level
5. Set controllers down → hands should appear after 2-3 seconds

---

**Estimated Time:** 10 minutes (first time), 5 minutes (once you know the steps)

**Once working:** Project is ready for development!
