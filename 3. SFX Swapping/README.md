# 3. SFX Swapping
## Step 1: Changing a SFX
1. In your decompiled files, go to the app folder.
2. Depending if your using a normal incredibox install with multiple packs, or a mod with just one (such as Travis), you will see multiple "asset" folders, named asset-v1, asset-v2, etc.
3. Open the asset folder you want to edit (usually asset-v1) and then open the sound folder, then the ogg folder, then each ogg file matches to each character.
4. There will be two for each 'character' `_a` and `_b`, `_a` accords to the first bar, `_b` being the second bar. Keep an eye on the length, your going to want the SFX your replacing to be the same duration.
5. Once you've changed your SFX, its time to recompile.

## Step 2: Recompiling your files
### Windows
1. If you haven't already, follow steps 1 and 2 from [here](https://github.com/sealldeveloper/incredibox-modding-docs/tree/main/1.%20Decompilation#step-2-the-slightly-harder-part)
2. Whereever your decompiled files are, the folder **outside** of it should have the .bat file.
3. Make a new text document and change its entire name to `modded.asar`.
4. Make sure the folder where your modding environment is stored is named `modded.asar_DECOMPILED`
5. Open the .bat and do the following commands **in order**:
- `select modded.asar`
- `compile`
6. Close the window, a new file should appear: `modded.asar_COMPILED`.
7. Move this file to your Incredibox install, and rename the existing `app.asar` with `app-backup.asar` and rename `modded.asar` to `app.asar`.
8. Boot Incredibox and your changes should be visible.
