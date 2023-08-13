# Animation Renderer
Instead of booting the game everytime to check an animation, use this! It also checks for pixel misalignment on the first frame, or in the silouette. No need to boot the game when animating, just build your animation with this.

> **Note**
> These animations are not perfect, decimal pixel changes are not accounted for and are rounded, for example `-4.95` becomes `-5` and `1.25` becomes `1`.

## Requirements
- Python 3.11 or higher

## How to use:
### Windows
1. Download this entire repository, more convinient downloads for individual tools will be provided in future.
2. Direct to this folder, go to `Tools`, then `AnimationRenderer`.
3. Start by opening the `#install.bat` file and installing all required packages.
4. Then open `#start-render.bat`, a folder called `input` should appear.
5. Put in the appropriate files:
  - `anime.json` for your animation
  - `anime-hd.png` for your HD spritesheet (required for the HD render)
  - `anime.png` for your non-HD spritesheet (required for the non-HD render)
  - `anime_a.ogg` **optional**, your A track for your polo, if you have only one track only include the A track
  - `anime_b.ogg` **optional**, your B track for your polo, only if you have two tracks
6. Re-run the renderer by opening `#start-render.bat`, type in the option you want, and it will render!
7. Your output will be in the output folder, under the characters name provided in the animation JSON.

## Examples (Travis Euphoria - HD Renderer)

![anime](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/bff7e720-fc0c-4436-a383-b83fe7b9df4e)
![default-pose-compared-to-first-frame](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/fc9991d2-2665-4f9c-8f0d-d86d8d6b150a)
![silhouette-check](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/7a5855d5-d722-41c9-a638-86c9490d0e06)



https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/d39a7507-0e97-4683-8733-89e4c1495a49



