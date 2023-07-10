# 1. Decompilation

## Step 1: The easy part

### Windows
Firstly, go to the location of your Incredibox install, this can be found by doing the following:
1. Open Steam
2. Find Incredibox in your library
3. Right click it and go to Manage > Browse Local Files
4. The folder will open

Inside the folder will be one exe file, duplicate it and rename the file extension from .exe to .zip, then extract the zip.

You should now have a bunch of files, these are the 'source' code.

## Step 2: The slightly harder part

### Windows
1. Download [this repo](https://github.com/vlOd2/ASAREditor)
2. There is a specific file in it, `ASAR Editor.bat`, copy it into the `resources` folder of the Incredibox extract.
3. Double click it to open it, this should open a terminal window.
4. Type in the following two commands, **in order**:
- `select app.asar`
- `decompile`
5. You can then close the window, a new folder should appear called `app.asar_DECOMPILED`. This will contain all the decompiled files needed! Congratulations.
