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
2. Open it up again, then select the 'pack' tab.
3. Inside your `app.asar.unpack` folder, select all the files then drag and drop them onto the blank box on the left side of the window.
4. Then, press pack.
5. After its done a file should appear in the `app.asar.unpack` folder called `app.asar`.
6. Move this to the folder where the app.asar originally was and replace it with this one, this will use your new compiled version in the game.
