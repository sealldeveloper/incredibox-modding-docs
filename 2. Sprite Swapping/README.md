# 2. Sprite Swapping

## Step 1: Changing an existing sprite
1. In your decompiled files, go to the app folder.
2. Depending if your using a normal incredibox install with multiple packs, or a mod with just one (such as Travis), you will see multiple "asset" folders, named asset-v1, asset-v2, etc.
3. Open the asset folder you want to edit (usually asset-v1) and then open the anime folder, you will see all the sprite sheets and json files.
4. The JSON files depict the animations, (explained here) while the sprite sheets store the designs.
5. Open the sprite sheet you want to edit, and then begin your modifications. The size of the head or body modified should stay **within the range of the model your editing**, the game has values stored for where the sprite is, so try not to leave the boundries of the existing model too much as your sprite may get messed up. These dimensions can be changed but that will be explained later.
6. Once you've modified the sprite you wish to change, you have to recompile your files.

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
