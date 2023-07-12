# 1. Decompilation and Compilation

## Step 1: The easy part

> **Note**
> Generally though, instead of using an install, use a preexisting mod like Travis.

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
1. Download [this](https://github.com/aardio/WinAsar/raw/master/dist/WinAsar.7z) and extract the exe file. This will be marked as dangerous in some browsers, if your worried the VirusTotal scans of the zip and exe are linked at the end of this step.
2. Once opened, there is an 'extract' button on the left, click it.
3. Up the top press 'open', then direct to the 'app.asar' file and open it.
4. Press extract at the bottom.
5. A new folder called `app.asar.unpack` will appear. This will contain all the decompiled files needed! Congratulations.

- [VirusTotal Scan of 7Z](https://www.virustotal.com/gui/file/818200b7b5eff0c3afa29b467a00cf975faf0d7ec409b7946ae0fdce53ab457c)
- [VirusTotal Scan of EXE](https://www.virustotal.com/gui/file/15184a7ddf502c4e078eed4dfe41c8c74db31eb58f4fbf666c73b4249bc6235e)
> **Note**
> These are likely false positives, but if you are technically inclined there are other tools you can use to do this online.


## Step 3: Compilation
You have two options for compilation.
### GUI (easier, slower)
1. If you haven't already, follow points 1 and 2 from Step 2.
2. Open it up again, then select the 'pack' tab.
3. Inside your `app.asar.unpack` folder, select all the files then drag and drop them onto the blank box on the left side of the window.
4. Then, press pack.
5. After its done a file should appear in the `app.asar.unpack` folder called `app.asar`.
6. Move this to the folder where the app.asar originally was and replace it with this one, this will use your new compiled version in the game.

### Python Script (slightly harder, faster)
1. Download the following script(s): [Compiler](https://github.com/sealldeveloper/incredibox-modding-docs/tree/main/Tools/Compiler) and the steps are listed to compile from source!
