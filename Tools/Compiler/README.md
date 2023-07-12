# Compiler
Compiling with dodgey GUIs no more! Compile from APK, or source to a windows EXE!

## Requirements
- Python 3.11 or higher

## How to use:
### 1. Setup
Run this.
```
python -m pip install -r requirements.txt
```
### 2. Source Compilation
1. Run the following command:
```
python source-to-windows.py
```
2. A 'source' folder will appear, once you've put your mod folders it should look like the following:

![image](https://github.com/sealldeveloper/incredibox-modding-docs/assets/120470330/0bea00d6-6947-4f5f-a084-1b5f8658102f)

3. Then run this:
```
python source-to-windows.py
```
4. This will compile the source to a working zip in the `output` folder.

### 2. Android to Windows
1. Place the APK file in the folder with the python file, rename it to `app.apk`
2. Run the following command:
```
python android-to-windows.py
```
3. This will reformat the APK to a zip for windows, its in the `output` folder.
