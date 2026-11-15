# Qelem animation workspace: research and implementation

Qelem keeps its own dark/amber interface, Kotlin/Compose UI, Rust drawing engine, artwork
format and existing drawing tools. The animation workspace is an optional layout within an
existing artwork, not a destructive conversion or a copy of another app's visual assets.

## Design research

The official Procreate Dreams handbook describes a gallery (Theater), a Stage/canvas, a
Timeline with a playhead/ruler and content tracks, and a drawing-oriented Flipbook view.
It also describes separate Compose, Perform, and Keyframe modes, and a resizeable
stage/timeline split. These are workflow references, not features Qelem already has:

- [Interface overview](https://help.procreate.com/dreams/handbook/interface-and-gestures/interface)
- [Timeline and modes](https://help.procreate.com/dreams/handbook/interface-and-gestures/timeline)
- [Stage and canvas](https://help.procreate.com/dreams/handbook/interface-and-gestures/stage)
- [Timeline gestures](https://help.procreate.com/dreams/handbook/1.0/interface-and-gestures/timeline)

## Implemented so far

- Actions → Canvas → Animation Assist enables the existing frame/group animation; ▥ opens
  Qelem's expanded timeline and Compact returns to the original drawing-oriented layout.
- One actual drawing track, a synchronized time ruler, highlighted playhead, zoom and track
  height, previews and held-frame markers. Scroll the track horizontally; tap or drag the
  ruler to preview frames, then release to select. Cancelled scrubs restore the prior frame.
- Existing add, duplicate/split, exposure length, frame options, onion skin and playback
  controls work on the existing artwork. Undo and redo use the same artwork history.
- **Select** on the expanded timeline selects visible frame IDs (tap any held slot to
  toggle its whole frame, or use All/Clear). In selection mode, − Hold / + Hold change
  the selected frame durations together as one undoable operation; each duration clamps
  independently to 1–61 total slots. The selection is temporary and never selects layers
  in the Layers panel; Done returns to normal editing. The ruler is disabled while selecting.
- The timeline toolbar's ← Frame / Frame → move the selected visible frame one position,
  carrying its holds, mask or complete group; this is an undoable change to the existing
  document, and the selected held position follows the frame's stable ID. Pinned background
  and foreground frames cannot be moved or crossed. To prevent changing clipping bases, the
  action refuses documents with top-level clipping; hidden layers remain intact. This moves
  existing drawing frames, not independent movie clips or tracks.
- Qelem's gallery remains its gallery; existing layer and frame persistence and animated
  export paths are not replaced. The expanded timeline uses lazy composition and Rust slot
  expansion avoids a repeated frame search, but device speed has not been benchmarked.

## Remaining work

This is **not** yet Dreams' multitrack/movie format: no independent audio or video clips,
content tracks, non-destructive motion keyframes, Perform mode, or animation importer.
Adding those requires a versioned document schema, backwards-compatible save/reopen and
undo, synchronized rendering/playback/export, migration tests, and device verification.
Those controls should not be presented as working before the underlying model exists.

The Android preview is separately packaged and debug signed. It has no importer for old
Qelem artwork. Back up projects, keep the original app installed, and verify on a device;
there is no guarantee a differently signed preview can update a previous preview.

### Timeline interface refinement

The expanded drawing timeline now keeps undo, redo, timecode, transport, frame selection and add-frame controls visible in a compact header. Less frequent frame, playback, onion-skin and timeline sizing actions live in the scrollable **Tools** menu. Selection mode keeps its batch controls together; the compact Animation Assist view and underlying artwork remain unchanged. Buttons have descriptive accessibility labels and the tool menu is height-limited to leave room for the track on shorter screens. This is an incremental Qelem interface, not a complete Dreams workspace; check layout and touch targets on real devices.

### Windows and Android continuation

Windows Animation Assist now offers **Timeline** in its compact bar on windows at least 520 × 300 points. It opens a larger single drawing-track view with first/previous/play/next/last navigation, timecode, hold adjustment, safe frame reordering, settings and add-frame controls. Tap the current frame for its existing options; **Canvas** returns to compact mode. Small windows and Page Assist retain the compact view. Frame holds and moves use the same native undoable operations as Android; pinned frames and top-level clipping still block unsafe moves. The held offset follows the frame ID on reorder and undo. Android's expanded timeline Tools menu now includes jump-to-first and jump-to-last slot, including held slots. Neither interface creates independent tracks or changes the document format. The two UIs and native input still need testing on physical Windows and Android devices, including small screens and settings popovers.

### Batch frame selection across Windows and Android

In the Windows expanded Timeline, choose **Select** and click frames (including a held slot) to select their stable frame IDs. Drag the track to browse without changing the active drawing layer; use **All**, **Clear** or **Invert**, then **− Hold / + Hold** to adjust every selected duration in one native undo step. **Done** or Escape clears the temporary selection and returns to the drawing timeline. Returning to Canvas, closing the artwork, switching to Page Assist or resizing to the compact fallback also ends selection. Frames no longer visible are removed from the selection. Android's existing multi-frame selection now also offers **Invert** for the currently visible frame IDs. Selection is not saved and is not the Layers panel selection. It does not create clips or tracks; each frame remains clamped to 1–61 total slots. Keyboard/mouse/touch behavior and screen-reader support require physical verification.

### Gesture and timeline zoom increment

Dreams' [gesture guide](https://help.procreate.com/dreams/handbook/interface-and-gestures/gestures) describes pinch zoom and single-finger timeline panning. The Android expanded drawing track now supports a two-touch pinch between its existing two timeline zoom levels; the scale is visual only and does not change playback, frame duration or artwork. One-finger timeline scroll/tap, ruler scrub and stylus input continue to use their existing handlers. While two fingers touch the track the gesture owns those touches until release, preventing an accidental frame tap; it does not implement two-finger panning, tap-to-undo or other Dreams multi-touch gestures. The existing explicit zoom controls remain available. Windows expanded Timeline has separate −/+ zoom buttons, including during frame selection; compact/Page Assist stays at its original scale. The controls retain Qelem's colors and icons rather than copying another app's proprietary assets. Pointer arbitration, pinch cancellation, accessibility and small-screen layout still require physical-device testing. Multitrack, keyframes, Perform mode, media and other gesture families remain future work.

### Tutorial-informed onion controls

The supplied tutorial describes tapping the timecode to turn onion skins on and edit them while drawing frame by frame. In Qelem's expanded Android and Windows timelines, tap/click the timecode to open a small onion-skin popover. The switch uses the same underlying Animation Assist onion setting as the existing QuickMenu; toggling it back on restores the last nonzero frame count remembered in the current app session. **Edit playback & onions** opens the existing settings for frame count, opacity and before/after colors. This control is unavailable while batch-selecting frames; selecting, compact mode and Page Assist retain their existing behavior. These settings use the current document's Animation Assist model, not Dreams-style independent track onions, and the remembered toggle value is not promised across app restarts. Device layout, touch, rendering and save/reopen still need verification.

The tutorial also distinguishes artwork content from non-destructive keyframe tracks, describes Perform capture, per-property easing, masks, grouping, Backstage and media export. Qelem's present single-track frame/layer model cannot safely provide those as equivalent features: they require a versioned movie/track model and tested rendering, playback, export, persistence and migration before UI controls can truthfully expose them. The tutorial's described viewport-dependent looping and gestures are reference material, not behavior assumed or silently enabled in Qelem.

### Screenshot-guided timeline styling

Using the supplied tutorial screenshots as a visual reference, the expanded Qelem timeline on Android and Windows now uses a darker, flatter, wider workspace surface, quieter track/ruler contrast, a left-anchored Android timecode, and a visible playhead over the drawing track. Windows uses more available window width and shows thumbnails in held slots. The existing amber accent and Qelem's own controls remain, as do compact Animation Assist and Page Assist. The playhead is a visual overlay; the existing ruler/track interactions still own input. This restyles the existing single-track overlay; it does not introduce a separate stage, movie gallery, independent tracks, movie settings or keyframes shown in the reference. Real Android/Windows device checks are still needed for layout, color, scrolling, gestures, accessibility and screen sizes.
