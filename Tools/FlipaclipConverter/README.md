# Conversion of Flipaclip PNG Sequences to working Polos
This will convert an exported PNG sequence from Flipaclip to a working polo spritesheet and JSON.

> **Note**
> These animations rely on all motion being **inside** a 164 x 380 (or HD equivilent) box, otherwise risking offcenter animations.

## Requirements
- Python 3.11 or higher (Make sure to select the `Add to PATH` option)

## How to use:
### Windows
1. Download this entire repository, more convinient downloads for individual tools will be provided in future.
2. Direct to this folder, go to `Tools`, then `FlipaclipConverter`.
3. Start by opening the `#install.bat` file and installing all required packages.
4. Then open `#start-converter.bat`, a folder called `input` should appear.
5. Put in the appropriate files:
  - Flipaclip can export a `zip` of your files, put this zip in the input folder.
  - If you are using your own PNG sequence, zip all the files.
  - Ensure the zip is called `files.zip`.
6. Re-run the converter by opening `#start-converter.bat`, type in whether the PNG sequence is HD or not, and the name (usually `number_name` for eg. `1_kick`).
7. Your output will be in the output folder, under the name of the polo you inputted.




