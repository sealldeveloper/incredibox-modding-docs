# 4. Bonus Swapping

## Step 1: Changing an existing bonus
1. In your decompiled files, go to the app folder.
2. Depending if your using a normal incredibox install with multiple packs, or a mod with just one (such as Travis), you will see multiple "asset" folders, named asset-v1, asset-v2, etc.
3. Open the asset folder you want to edit (usually asset-v1) and then open the video folder, this contains the video files for the bonuses.
4. The video dimensions are 1000 x 400. Replace the video with whatever video you wish, just conform to the dimensions.
5. Leave this folder, and go to the sound folder, then ogg. Down the bottom the bonus and aspire files will exist. `aspire` is the leadup to the bonus, `bonus` is the actual audio for the video.
6. After modifying the files you wish, its time to recompile.

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
