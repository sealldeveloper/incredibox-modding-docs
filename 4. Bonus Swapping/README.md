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
2. Open it up again, then select the 'pack' tab.
3. Inside your `app.asar.unpack` folder, select all the files then drag and drop them onto the blank box on the left side of the window.
4. Then, press pack.
5. After its done a file should appear in the `app.asar.unpack` folder called `app.asar`.
6. Move this to the folder where the app.asar originally was and replace it with this one, this will use your new compiled version in the game.
