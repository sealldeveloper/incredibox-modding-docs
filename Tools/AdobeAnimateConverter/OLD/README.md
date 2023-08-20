# Conversion of Adobe Animate Animations (FLA's) to working Polos
This will convert an exported symbols spritesheet and JSON from Adobe Animate to a working polo spritesheet and JSON.

> **Note**
> These animations rely on all motion being **inside** a 164 x 380 box, otherwise risking offcenter animations.

## Requirements
- Python 3.11 or higher

## How to use:
### Windows
1. Download this entire repository, more convinient downloads for individual tools will be provided in future.
2. Direct to this folder, go to `Tools`, then `AdobeAnimateConverter`.
3. Start by opening the `#install.bat` file and installing all required packages.
4. Then open `#start-converter.bat`, a folder called `input` should appear.
5. Put in the appropriate files:
  - `anime.json` for your animation
  - `anime-hd.png` for your HD spritesheet (required for the HD sheet)
  - `anime.png` for your non-HD spritesheet (required for the non-HD sheet)
6. Re-run the renderer by opening `#start-render.bat`, type in whether the JSON was an HD or Non-HD version (when exporting from animate, is your animate document the size of a normal polo or an HD one).
7. Your output will be in the output folder, under the hd and no-hd folders.
8. You have to finish the spritesheet by manually adding a default pose, headless pose, and a silouette pose.

## How to export the Spritesheet and JSON from Animate
1. After you've finished your symbol, right click on it and select the 'Generate Sprite Sheet...' button.
2. A menu will appear, the follow settings should be set:
- Image Dimensions: Auto size
- Image format: PNG 32 bit
- Background Color: Transparent
- Algorithm: Basic
- Data format: JSON
- Rotate: Disabled
- Trim: Disabled
- Stack frames: Enabled
- Border padding: 0px
- Shape padding: 0px




