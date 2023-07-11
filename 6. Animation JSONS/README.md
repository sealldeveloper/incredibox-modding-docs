# 6. Animation JSONs
> **Note**
> There currently is no other way to make animations other than manually programming them.

## Step 1: How do they work?
JSON or JavaScript Object Notation is a format of storing information, and in this case for Incredibox, stores the polo's sprite dimensions and animation frames.

### JSON format
| Variable      | Purpose                                                      |
|---------------|--------------------------------------------------------------|
| animeName     | Name of the polo files.                                      |
| percentageMax | Seems to generally be 0.2, unknown purpose.                  |
| totalFrame    | Amount of animation frames for the polo, set in app.js.      |
| width         | Width of the sprite, both the head and the main body sprite. |
| height        | Height of the main body sprite.                              |
| headHeight    | Height of the head sprite.                                   |
| arrayFrame    | List of each frame of animation, explained below.            |

### `arrayFrame`
Each value is seperated by a comma in the `prop` variable.

The values explained are **in-order** and must be **set in the correct order**.

Let's use the first frame of `1_kick` from the Travis mod as an example: `328,380,0,3.8`

The first two values indicate the head frame being selected, on the sprite sheet lets look at pixel `328,380`:
![image](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/10442ce1-29df-489d-be51-8f630cfeeb6c)

That small red pixel is that pixel, now lets use the `headHeight` and `width` set earlier and draw a box.
![image](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/60e50daa-07a4-40f1-9c27-6dc57082866d)

We can see a perfect box around the head, so thats the head frame being selected. The pixel indicates the **top left corner** of the box being drawn.

Now, the remaining two values, indicate the heads movement ingame in terms of x and y! (The first value being x, second being y).

If we modify the value to be `328,380,5,5` adn recompile we should see the head move to the bottom right ingame.

![image](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/87346a7a-eaf0-471b-bfa7-07cbf9129361)

There we go!
So heres each value broken down:
- `328` : Top left corner of the head sprite, x value
- `380` : Top left corner of the head sprite, y value
- `0` : X movement of the head, positive numbers being right, negative numbers being left
- `3.8` : Y movement of the head, positive numbers being down, negative numbers being up

## Step 2: Making an animation
> **Warning**
> Making animation are not for the feint of heart, they take **alot** of time.

> **Note**
> I plan to make a renderer for the animations in Python or the like to avoid booting the game every time to test an animation.

1. Start with an existing JSON, that helps alot with the formatting existing already.
2. With your finished sprite sheet, make sure the JSON is named correctly, same as the `animeName` and the sprite sheet.
3. Begin modifying your animation frames, this takes a long time to perfect and to make sure its working you have to boot up Incredibox to check.
> **Note**
> Some people like to use Adobe Animate to plan their animation to the music they are using, animations by guessing can appear wonky, or out of time and planning them makes it alot easier.
4. After lots of effort, you should have a working animation.'

## Step 3: Compiling your animation into the game
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
