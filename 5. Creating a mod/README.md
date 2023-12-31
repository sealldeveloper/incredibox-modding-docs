# 5. Creating a mod
> **Warning**
> This is not a 'quick' or 'easy' process. Good mods take work.

## Step 1: A mod skeleton
Starting with a mod skeleton helps with starting, I recommend starting with something like Travis. It contains only one pack and is easily modifyable. The Travis Files are here in the 'ModTemplate' folder.
1. Download it and get familiar with the contents of the folders. You can generally ignore everything outside of the `app` folder.

## Step 2: The structure of an Incredibox Mod
### The contents of the `app` folder
| File/Folder         | Purpose/Contents                               |
|---------------------|------------------------------------------------|
| asset-v1            | Contents of the first pack.                    |
| css                 | Style sheets, generally can be left alone.     |
| font                | Font files, generally can be left alone.       |
| img                 | Menu images and tutorial images.               |
| js                  | Javascript files, generally can be left alone. |
| lang                | Language files and different translations.     |
| snd                 | Sound test file.                               |
| app.html/index.html | Website file to run Incredibox.                |

### The contents of the `asset-v1` folder
| File/Folder | Purpose/Contents                                                                          |
|-------------|-------------------------------------------------------------------------------------------|
| anime       | Animation files and sprite sheets.                                                        |
| img         | Menu items, default polo sheets, backgrounds and other GUI images.                        |
| sound/ogg   | Music files, bonus audio and bonus aspire audios.                                         |
| splash      | Home screen images.                                                                       |
| video       | Bonus videos.                                                                             |
| app.js      | All technical customization of character file names, source folder, colors, bpm and more. |

### `app.js`: broken down
`app.js` is a JavaScript file that controls the settings of the pack.
> **Note**
> I have made a generator for this, which vastly simplifies this process, take a look [here](https://sealldeveloper.github.io/boogoxseal.xyz/tools/appjs)

| Variable           | Purpose                                                                                |
|--------------------|----------------------------------------------------------------------------------------|
| this.name          | The name of the pack, keep inside double quotes.                                       |
| this.version       | Versioning, keep as is generally, change if your updating, v1, v2, etc.                |
| this.date          | The date of release, just the year generally.                                          |
| this.folder        | The folder its stored in, if the pack is in `assets-v2` change this to `"assets-v2/"`. |
| this.looptime      | The time it take to loop.                                                              |
| this.bpm           | The beats per minute.  (Purely visual)                                                 |
| this.totalframe    | The amount of frames per character per loop. This can be calculated from the looptime, steps listed below.|
| this.nbpolo        | The amount of polos in the game.                                                       |
| this.nbloopbonus   | The amount of loops for the bonus.                                                     |
| this.bonusloopA    | Can't determine an ingame change, leave as `!0`.                                       |
| this.bonusendloopA | Determines if a bonus should start at the start of loop A always. `!1` to enable.      |
| this.recmaxloop    | The maximum amount of loops for a recording.                                           |
| this.recminloop    | The minimum amount of loops for a recording.                                           |
| this.recmintime    | A math function to determine the minimum amount of time for a recording (don't change) |
| this.spritepolo    | The name of the file for the blank polo.                                               |
| this.spritepicto   | The name of the file for the icons in the pack.                                        |
| this.colBck        | A reserve colour for if the background image fails to render or to fill in transparent pixels of the rendered background image.|
| this.col0          | Text colour.                                                                           |
| this.col1          | Button background colour.                                                              |
| this.col2          | Unhovered button background colour (visible in the Playlist menu).                     |
| this.col3          | Loading bar, unselected menu tab background colour and hoverred button colour.         |
| this.col4          | Selected menu button icon colour. (visible in Playlist when selecting 'My Mix').       |
| this.animearray    | Contains the characters, expanded on below.                                            |
| this.bonusarray    | Contains the bonuses, expanded on below.                                               |

#### totalframe calculation from looptime
> **Note**
> This is automated in the [appjs generator tool](https://sealldeveloper.github.io/boogoxseal.xyz/tools/appjs), putting the length of one loop in the field labelled "The length of one loop (in milliseconds)" it is outputted to the "How many frames will the Polos have in their animation? (Based off 'Loop Time')"

`totalframe` is calculated from the following steps:
1. Multiply the `looptime` by `0.024`.
2. Round the number given down to the nearest whole number, eg. `1.7` goes to `1`.
3. Multiply the rounded number by `2`.
This is the amount of frames needed!

#### `animearray`
| Variable | Purpose                                                                                            |
|----------|----------------------------------------------------------------------------------------------------|
| name     | Name of the animation files in the anime folder.                                                   |
| color    | Color that appears on the bonus wheel when the character is placed.                                |
| uniqsnd  | If set to `!1` this character has an 'a' and a 'b' track, if set to `!0` it only has an 'a' track. |

#### `bonusarray`
| Variable | Purpose                                                     |
|----------|-------------------------------------------------------------|
| name     | Name of the bonus.                                          |
| src      | Name of the source video file in the video folder.          |
| code     | Numbers of the polo's to be selected to activate the bonus. |
| sound    | Name of the sound file for the bonus.                       |
| aspire   | Name of the sound file for the aspire.                      |

## Step 3: Building it and utilising previous skills!
Using the guides in steps 2, 3, and 4, you know how to swap out all these files, you can continue to do the same with your mod, take a look around and don't be afraid to experiment and break things. Learnings about mistakes. Good luck!

### Making a sprite
To start with making a sprite from scratch, a template it best. Use [the tool provided](https://sealldeveloper.github.io/boogoxseal.xyz/tools/polotemplate) to make a template to the dimensions you see fit. A JSON is generated alongside the template and coordinates with the empty frames.

A cool sprite example is the 8th character in the Void pack. It uses a headHeight of 380 (the same height of the character by default) to make the whole body change, at the disadvantage of each head having to contain movements, rather than moving it in a JSON.

#### Making a face
A face drawing guide for polos exists, made by Rem! A download is available [here](https://github.com/sealldeveloper/incredibox-modding-docs/files/12028660/polo_faces.zip).

A mouth example guide also exists, from Rem's discord! A download is available [here](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/799febcd-0ce6-4ae3-a359-5d240827f466).

#### Making a body
A sample body sprite exists, downloadable at the following links:
- [Normal Body Sprite Sheet](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/d6ec4001-e5ce-4305-ab7f-160e1a3ab62f)
- [HD Body Sprite Sheet](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/28c509e9-98b3-4c94-989f-e10b7f1b6818)

These files were in the Void pack and in Rem's Discord, so thanks to Rem once more!

## Step 4: Compiling your files.
### [Windows](https://github.com/sealldeveloper/incredibox-modding-docs/blob/main/1.%20Decompilation/README.md#step-2-compilation)
