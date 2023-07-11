# 3. Music Swapping
## Step 1: Changing the music
1. In your decompiled files, go to the app folder.
2. Depending if your using a normal incredibox install with multiple packs, or a mod with just one (such as Travis), you will see multiple "asset" folders, named asset-v1, asset-v2, etc.
3. Open the asset folder you want to edit (usually asset-v1) and then open the sound folder, then the ogg folder, then each ogg file matches to each character.
4. There will be two for each 'character' `_a` and `_b`, `_a` accords to the first bar, `_b` being the second bar. Keep an eye on the length, your going to want the music your replacing to be the same duration.
5. Once you've changed your music, its time to recompile.

## Step 2: Recompiling your files
### Windows
1. If you haven't already, follow steps 1 and 2 from [here](https://github.com/sealldeveloper/incredibox-modding-docs/tree/main/1.%20Decompilation#step-2-the-slightly-harder-part)
2. Open it up again, then select the 'pack' tab.
3. Inside your `app.asar.unpack` folder, select all the files then drag and drop them onto the blank box on the left side of the window.
4. Then, press pack.
5. After its done a file should appear in the `app.asar.unpack` folder called `app.asar`.
6. Move this to the folder where the app.asar originally was and replace it with this one, this will use your new compiled version in the game.
