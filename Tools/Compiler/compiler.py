import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    import rich
    import os,sys,shutil,linecache
    from distutils.dir_util import copy_tree
    from asarPy import pack_asar,extract_asar
    from pydub import AudioSegment
    from moviepy.editor import VideoFileClip
    from jsmin import jsmin
    import hashlib
    import requests
    import zipfile
    import http.server
    import socketserver
except Exception as e:
    print(f'[bright_red]ERROR: Packages have failed to install, please try reinstalling them.\n{str(e)}')
    sys.exit()

def file_selection(ftype):
    files=[]
    table = Table()
    table.add_column("File Options", style="magenta")
    for f in os.listdir('input'):
        if f.endswith(f'.{ftype}') and os.path.isfile(f'input/{f}'):
            files.append(f)
            table.add_row(f)
    print(table)
    selected = Prompt.ask('Which file do you want to use?', choices=files, show_choices=False)
    return selected

def folder_selection():
    folders=[]
    table = Table()
    table.add_column("Folder Options", style="magenta")
    for f in os.listdir('input'):
        if os.path.isdir(f'input/{f}') and '.' not in f:
            folders.append(f)
            table.add_row(f)
    print(table)
    selected = Prompt.ask('Which folder do you want to use?', choices=folders, show_choices=False)
    return selected

def webapp_localhost(name):
    try:
        localhost = Prompt.ask("Do you want to start the webapp on localhost?",choices=['y','n'])
        if localhost == 'y':
            DIRECTORY = 'output/webapp/'
            if not os.path.exists(DIRECTORY):
                os.mkdir(DIRECTORY)
            shutil.unpack_archive(name,DIRECTORY,'zip')
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=DIRECTORY, **kwargs)
                def log_message(self, format, *args):
                    no_logging_lol=""
            with socketserver.TCPServer(("", 8000), Handler) as httpd:
                try:
                    print('Press CTRL+C to stop! Hosting on http://localhost:8000/')
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    pass
                finally:
                    httpd.server_close()
    except:
        PrintException()



def jsfix(path,os,target,snd):
    try:
        fname = path.split('/')[len(path.split('/'))-1]
        with open(path, encoding='utf-8', errors='surrogateescape') as f:
            d=jsmin(f.read(), quote_chars="'\"`")
            f.close()
        with open(path,'w', encoding='utf-8') as f:
            try:
                p1 = d.split(',target="',1)[0]
                p2 = d.split(',target="',1)[1].split('"',1)[1]
                d = p1 + f',target="{target}"' + p2
                try:
                    p3 = d.split(',osname="')[0]
                    p4 = d.split(',osname="',1)[1].split('"',1)[1]
                    d = p3 + f',osname="{os}"' + p4
                except Exception as e:
                    print(f'{fname}: No \'osname\' found, no biggie!')
                p5 = d.split(',sndtype="')[0]
                p6 = d.split(',sndtype="',1)[1].split('"',1)[1]
                d = p5 + f',sndtype="{snd}"' + p6
                try:
                    p7 = d.split('checkAudioFormat("')[0]
                    p8 = d.split('checkAudioFormat("',1)[1].split(':sndtype',1)[1]
                    d = p7 + f'checkAudioFormat("{snd}")?"{snd}":sndtype' + p8
                except Exception as e:
                    print(f'{fname}: No \'checkAudioFormat\' found, potentially issues with loading MP3\'s...')
                
            except Exception as e:
                path=path.split('/')
                print(f'[bright_yellow]WARNING: {path[len(path)-1]} is likely obfuscated or a weird version, sizing and buttons may be weird or incorrect depending on platform, may also not load or encounter errors.\n{str(e)}')
                PrintException()
            f.write(d)
            f.close()
    except:
        PrintException()

def webapp_format_conversion():
    try:
        assetversions=[]
        for x in os.listdir('temp/webapp'):
            if x.startswith('asset-v') and os.path.isdir(f'temp/webapp/{x}'):
                assetversions.append(x.replace('asset-v',''))
                print('Converting OGG\'s to MP3\'s for better compatibility on devices...')
                path=f'temp/webapp/{x}/sound'
                if not os.path.exists(f'{path}/mp3/') and os.path.exists(f'{path}/ogg/'):
                    os.makedirs(f'{path}/mp3/')
                    for f in os.listdir(f'{path}/ogg'):
                        if os.path.isfile(f'{path}/ogg/{f}') and f.endswith('.ogg'):
                            newname=f.replace('.ogg','.mp3')
                            
                            try:
                                AudioSegment.from_ogg(f'{path}/ogg/{f}').export(f'{path}/mp3/{newname}')
                                print(f'[bright_blue]({x}) [default]{f} -> {newname}')
                            except Exception as e:
                                print(f'[bright_blue]({x}) [default]{f} -> [bright_red]ERROR! Couldn\'t convert...\n{str(e)}')
                    shutil.rmtree(f'{path}/ogg')
                print('Converting all bonuses to MP4\'s...')
                path=f'temp/webapp/{x}/video'
                if not os.path.exists(path):
                    os.makedirs(path)
                for y in os.listdir(path):
                    if os.path.isfile(f'{path}/{y}') and not y.endswith('mp4') and not y.endswith('png') and not y.endswith('jpg') and not y.endswith('jpeg'):
                        newname=y.split('.')[0]
                        video = VideoFileClip(f'{path}/{y}')
                        video.write_videofile(f'{path}/{newname}.mp4')
                        os.remove(f'{path}/{y}')
        return assetversions
    except:
        PrintException()

def android_unpack(names):
    try:
        for f in os.listdir('temp/android/assets/www/'):
            if f.startswith('asset-v'):
                    if os.path.isfile(f'temp/android/assets/www/{f}'):
                        shutil.copyfile(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
                    elif os.path.isdir(f'temp/android/assets/www/{f}'):
                        copy_tree(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
            if f in names:
                if os.path.isfile(f'temp/android/assets/www/{f}'):
                    shutil.copyfile(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
                elif os.path.isdir(f'temp/android/assets/www/{f}'):
                    copy_tree(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
    except:
        PrintException()



def mac_to_webapp(js_input,file):
    try:
        os.makedirs('temp/webapp/')
        os.makedirs('temp/mac/')
        print('Unpacking template and app...')
        shutil.unpack_archive(f'input/{file}','temp/mac/','zip')
        print('Unpacking asar...')
        if not os.path.isfile('temp/mac/Incredibox.app/Contents/Resources/app.asar'):
            print('[bright_red]ERROR: The \'app.asar\' doesn\'t exist! Check the app is called \'Incredibox.app\', and the \'app.asar\' exists!')
            return False
        extract_asar('temp/mac/Incredibox.app/Contents/Resources/app.asar','temp/source/')
        shutil.unpack_archive('templates/webapp.zip','temp/source/app/','zip')
        print('Duplicating source to webapp...')
        for x in os.listdir('temp/source/app'):
            if os.path.isdir(f'temp/source/app/{x}'):
                copy_tree(f'temp/source/app/{x}',f'temp/webapp/{x}')
            elif os.path.isfile(f'temp/source/app/{x}'):
                shutil.copyfile(f'temp/source/app/{x}',f'temp/webapp/{x}')

        assetversions = webapp_format_conversion()
        if js_input == 'modify':
            jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
            jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
        print('Packing up webapp...')
        filename = 'output/mac-to-webapp-packed'
        shutil.make_archive(filename,'zip','temp/webapp/')
        print('Packed as \'mac-to-webapp-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        webapp_localhost(filename+'.zip')
        return True
    except:
        PrintException()

def mac_to_source(file):
    try:
        os.makedirs('temp/mac/')
        print('Unpacking app...')
        shutil.unpack_archive(f'input/{file}','temp/mac/','zip')
        print('Unpacking asar...')
        if not os.path.isfile('temp/mac/Incredibox.app/Contents/Resources/app.asar'):
            print('[bright_red]ERROR: The \'app.asar\' doesn\'t exist! Check the app is called \'Incredibox.app\', and the \'app.asar\' exists!')
            return False
        extract_asar('temp/mac/Incredibox.app/Contents/Resources/app.asar','temp/source/')
        print('Packing source...')
        shutil.make_archive('output/mac-to-source-packed','zip','temp/source/')
        print('Packed as \'mac-to-source-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()

def mac_to_windows(js_input,file):
    try:
        os.makedirs('temp/windows/')
        os.makedirs('temp/mac/')
        os.makedirs('temp/macasar/')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking template...')
        shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
        shutil.unpack_archive(f'input/{file}','temp/mac/','zip')
        shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
        print('Unpacking asar...')
        if not os.path.isfile('temp/mac/Incredibox.app/Contents/Resources/app.asar'):
            print('[bright_red]ERROR: The \'app.asar\' doesn\'t exist! Check the app is called \'Incredibox.app\', and the \'app.asar\' exists!')
            return False
        extract_asar('temp/mac/Incredibox.app/Contents/Resources/app.asar','temp/macasar/')
        """if js_input == 'modify':
            jsfix('temp/source/app/js/main.min.js','win','desktop','ogg')
            jsfix('temp/source/app/js/index.min.js','win','desktop','ogg')
        print('Packing asar...')
        pack_asar("temp/source",'temp/app.asar')
        print('Copying new asar...')
        shutil.copyfile('temp/app.asar','temp/windows/app/resources/app.asar')
        print('Repacking new version...')
        shutil.make_archive('output/windows-packed','zip','temp/windows/')
        print('Packed as \'windows-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')"""
        return True
    except:
        PrintException()

def mac(output,jsinput):
    file = file_selection('zip')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'webapp':
        val = mac_to_webapp(jsinput,file)
    elif output == 'source':
        val = mac_to_source(file)
    elif output == 'windows':
        val = mac_to_windows(jsinput,file)
    return val


def android_to_source(names,file):
    try:
        os.makedirs('temp/android/')
        os.makedirs('temp/asar/')
        print('Unpacking template...')
        shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
        print('Unpacking app...')
        shutil.unpack_archive(f'input/{file}','temp/android/','zip')
        print('Organising new folder...')
        android_unpack(names)
        print('Packing source...')
        shutil.make_archive('output/apk-to-source-packed','zip','temp/asar/')
        print('Packed as \'apk-to-source-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()

def android_to_webapp(names,js_input,file):
    try:
        print('Importing libraries...')
        os.makedirs('temp/asar/app/')
        os.makedirs('temp/webapp/')
        print('Unpacking templates...')
        print('Unpacking app...')
        shutil.unpack_archive(f'input/{file}','temp/android/','zip')
        print('Organising new folder...')
        android_unpack(names)
        shutil.unpack_archive('templates/webapp.zip','temp/asar/app/','zip')
        print('Duplicating source to webapp...')
        for x in os.listdir('temp/asar/app/'):
            if os.path.isdir(f'temp/asar/app/{x}'):
                copy_tree(f'temp/asar/app/{x}',f'temp/webapp/{x}')
            elif os.path.isfile(f'temp/asar/app/{x}'):
                shutil.copyfile(f'temp/asar/app/{x}',f'temp/webapp/{x}')
        assetversions = webapp_format_conversion()
        if js_input == 'modify':
            jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
            jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
        print('Packing up webapp...')
        filename = 'output/apk-to-webapp-packed'
        shutil.make_archive(filename,'zip','temp/webapp/')
        print('Packed as \'apk-to-webapp-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        webapp_localhost(filename+'.zip')
        return True
    except:
        PrintException()

def android_to_windows(names,js_input,file):
    try:
        os.makedirs('temp/windows/')
        os.makedirs('temp/android/')
        os.makedirs('temp/asar/')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking template(s)...')
        shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
        shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
        print('Unpacking app...')
        shutil.unpack_archive(f'input/{file}','temp/android/','zip')
        print('Organising new asar folder...')
        android_unpack(names)
        if js_input == 'modify':
            jsfix('temp/asar/app/js/main.min.js','win','desktop','ogg')
            jsfix('temp/asar/app/js/index.min.js','win','desktop','ogg')
        print('Packing asar...')
        pack_asar("temp/asar",'temp/app.asar')
        print('Copying new asar...')
        shutil.copyfile('temp/app.asar','temp/windows/app/resources/app.asar')
        print('Repacking new version...')
        shutil.make_archive('output/apk-to-windows-packed','zip','temp/windows/')
        print('Packed as \'apk-to-windows-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()

def android_to_mac(names,js_input,file):
    try:
        os.makedirs('temp/macasar/')
        os.makedirs('temp/mac/Incredibox.app')
        os.makedirs('temp/android/')
        os.makedirs('temp/windows/')
        os.makedirs('temp/asar/')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking app...')
        shutil.unpack_archive('templates/mac.zip','temp/mac/Incredibox.app/','zip')
        shutil.unpack_archive('templates/macasar.zip','temp/macasar/','zip')
        shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
        shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
        shutil.unpack_archive(f'input/{file}','temp/android/','zip')
        print('Formatting...')
        android_unpack(names)
        if js_input == 'modify':
            jsfix('temp/asar/app/js/main.min.js','mac','desktop','ogg')
            jsfix('temp/asar/app/js/index.min.js','mac','desktop','ogg')
        for f in os.listdir('temp/asar/app/'):
            if os.path.isfile(f'temp/asar/app/{f}'):
                shutil.copyfile(f'temp/asar/app/{f}',f'temp/macasar/app/{f}')
            elif os.path.isdir(f'temp/asar/app/{f}'):
                copy_tree(f'temp/asar/app/{f}',f'temp/macasar/app/{f}')
        print('Packing new asar...')
        pack_asar('temp/macasar/','temp/mac.asar')
        print('Moving asars...')
        shutil.copyfile('temp/mac.asar','temp/mac/Incredibox.app/Contents/Resources/app.asar')
        shutil.copyfile('temp/windows/app/resources/electron.asar','temp/mac/Incredibox.app/Contents/Resources/electron.asar')
        os.chmod('temp/mac/Incredibox.app/Contents/MacOS/Incredibox',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/PkgInfo',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/Frameworks/Incredibox Helper.app/Contents/MacOS/Incredibox Helper',0o755)
        for f in os.listdir('temp/mac/Incredibox.app/Contents/Frameworks/'):
            if os.path.isdir(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}') and f.endswith('.framework'):
                os.chmod(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}/{f.replace(".framework","")}',0o755)
        print('Packing Mac version...')
        shutil.make_archive('output/source-to-mac-packed','zip','temp/mac/')
        print('Packed as \'source-to-mac.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()


def android(output,jsinput):
    names = [
        'css',
        'font',
        'img',
        'lang',
        'snd',
        'app.html',
        'index.html'
    ]
    file = file_selection('apk')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'source':
        val = android_to_source(names,file)
    elif output == 'webapp':
        val = android_to_webapp(names,jsinput,file)
    elif output == 'windows':
        val = android_to_windows(names,jsinput,file)
    elif output == 'mac':
        val = android_to_mac(names,jsinput,file)
    return val


def source_to_webapp(js_input,folder):
    try:
        os.makedirs('temp/webapp/')
        print('Unpacking template...')
        print('Duplicating source to webapp...')
        for x in os.listdir(f'input/{folder}/app'):
            if os.path.isdir(f'input/{folder}/app/{x}'):
                copy_tree(f'input/{folder}/app/{x}',f'temp/webapp/{x}')
            elif os.path.isfile(f'input/{folder}/app/{x}'):
                shutil.copyfile(f'input/{folder}/app/{x}',f'temp/webapp/{x}')
        shutil.unpack_archive('templates/webapp.zip','temp/webapp/','zip')
        assetversions = webapp_format_conversion()
        if js_input == 'modify':
            jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
            jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
        print('Packing up webapp...')
        filename = 'output/webapp-packed'
        shutil.make_archive(filename,'zip','temp/webapp/')
        print('Packed as \'webapp-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        webapp_localhost(filename+'.zip')
        return True
    except:
        PrintException()

def source_to_windows(js_input,folder):
    try:
        os.makedirs('temp/windows/')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking template...')
        shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
        copy_tree(f'input/{folder}','temp/source')
        if js_input == 'modify':
            jsfix('temp/source/app/js/main.min.js','win','desktop','ogg')
            jsfix('temp/source/app/js/index.min.js','win','desktop','ogg')
        print('Packing asar...')
        pack_asar("temp/source",'temp/app.asar')
        print('Copying new asar...')
        shutil.copyfile('temp/app.asar','temp/windows/app/resources/app.asar')
        print('Repacking new version...')
        shutil.make_archive('output/windows-packed','zip','temp/windows/')
        print('Packed as \'windows-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()

def source_to_mac(js_input,folder):
    try:
        os.makedirs('temp/macasar/')
        os.makedirs('temp/windows/')
        os.makedirs('temp/mac/Incredibox.app')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking app...')
        shutil.unpack_archive('templates/mac.zip','temp/mac/Incredibox.app/','zip')
        shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
        shutil.unpack_archive('templates/macasar.zip','temp/macasar/','zip')
        copy_tree(f'input/{folder}','temp/source')
        print('Formatting...')
        for f in os.listdir('temp/source/app/'):
            if os.path.isfile(f'temp/source/app/{f}'):
                shutil.copyfile(f'temp/source/app/{f}',f'temp/macasar/app/{f}')
            elif os.path.isdir(f'temp/source/app/{f}'):
                copy_tree(f'temp/source/app/{f}',f'temp/macasar/app/{f}')
        if js_input == 'modify':
            jsfix('temp/macasar/app/js/main.min.js','mac','desktop','ogg')
            jsfix('temp/macasar/app/js/index.min.js','mac','desktop','ogg')
        print('Packing new asar...')
        pack_asar('temp/macasar/','temp/mac.asar')
        print('Moving asars...')
        shutil.copyfile('temp/mac.asar','temp/mac/Incredibox.app/Contents/Resources/app.asar')
        shutil.copyfile('temp/windows/app/resources/electron.asar','temp/mac/Incredibox.app/Contents/Resources/electron.asar')
        os.chmod('temp/mac/Incredibox.app/Contents/MacOS/Incredibox',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/PkgInfo',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/Frameworks/Incredibox Helper.app/Contents/MacOS/Incredibox Helper',0o755)
        for f in os.listdir('temp/mac/Incredibox.app/Contents/Frameworks/'):
            if os.path.isdir(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}') and f.endswith('.framework'):
                os.chmod(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}/{f.replace(".framework","")}',0o755)
        print('Packing Mac version...')
        shutil.make_archive('output/source-to-mac-packed','zip','temp/mac/')
        print('Packed as \'source-to-mac.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()


def source(output,js_input):
    folder=folder_selection()
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'webapp':
        val = source_to_webapp(js_input,folder)
    elif output == 'windows':
        val = source_to_windows(js_input,folder)
    elif output == 'mac':
        val = source_to_mac(js_input,folder)
    return val


def windows_to_webapp(js_input,file):
    try:
        os.makedirs('temp/webapp/')
        os.makedirs('temp/windows/')
        print('Unpacking template and app...')
        shutil.unpack_archive(f'input/{file}','temp/windows/','zip')
        print('Unpacking asar...')
        extract_asar('temp/windows/app/resources/app.asar','temp/source/')
        print('Duplicating source to webapp...')
        shutil.unpack_archive('templates/webapp.zip','temp/source/app/','zip')
        for x in os.listdir('temp/source/app'):
            if os.path.isdir(f'temp/source/app/{x}'):
                copy_tree(f'temp/source/app/{x}',f'temp/webapp/{x}')
            elif os.path.isfile(f'temp/source/app/{x}'):
                shutil.copyfile(f'temp/source/app/{x}',f'temp/webapp/{x}')
        assetversions = webapp_format_conversion()
        if js_input == 'modify':
            jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
            jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
        print('Packing up webapp...')
        filename = 'output/windows-to-webapp-packed'
        shutil.make_archive(filename,'zip','temp/webapp/')
        print('Packed as \'windows-to-webapp-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        webapp_localhost(filename+'.zip')
        return True
    except:
        PrintException()

def windows_to_source(file):
    try:
        os.makedirs('temp/windows/')
        print('Unpacking app...')
        shutil.unpack_archive(f'input/{file}','temp/windows/','zip')
        print('Unpacking asar...')
        extract_asar('temp/windows/app/resources/app.asar','temp/source/')
        print('Packing source...')
        shutil.make_archive('output/windows-to-source-packed','zip','temp/source/')
        print('Packed as \'windows-to-source-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()

def windows_to_mac(file):
    try:
        os.makedirs('temp/windows/')
        os.makedirs('temp/macasar/')
        os.makedirs('temp/mac/Incredibox.app')
        print('[bright_blue]NOTE: The version being uploaded SHOULD have JS files ≥ v1.1.5 otherwise you risk a black-screen error on Desktop platforms.')
        print('Unpacking app...')
        with zipfile.ZipFile(f'input/{file}', 'r') as zip_ref:
            zip_ref.extractall('temp/windows/')
        shutil.unpack_archive('templates/mac.zip','temp/mac/Incredibox.app/','zip')
        shutil.unpack_archive('templates/macasar.zip','temp/macasar/','zip')
        print('Unpacking asar...')
        extract_asar('temp/windows/app/resources/app.asar','temp/source/')
        print('Formatting new asar...')
        for f in os.listdir('temp/source/app/'):
            if os.path.isfile(f'temp/source/app/{f}'):
                shutil.copyfile(f'temp/source/app/{f}',f'temp/macasar/app/{f}')
            elif os.path.isdir(f'temp/source/app/{f}'):
                copy_tree(f'temp/source/app/{f}',f'temp/macasar/app/{f}')
        print('Packing new asar...')
        pack_asar('temp/macasar/','temp/mac.asar')
        print('Moving asars...')
        shutil.copyfile('temp/mac.asar','temp/mac/Incredibox.app/Contents/Resources/app.asar')
        shutil.copyfile('temp/windows/app/resources/electron.asar','temp/mac/Incredibox.app/Contents/Resources/electron.asar')
        os.chmod('temp/mac/Incredibox.app/Contents/MacOS/Incredibox',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/PkgInfo',0o755)
        os.chmod('temp/mac/Incredibox.app/Contents/Frameworks/Incredibox Helper.app/Contents/MacOS/Incredibox Helper',0o755)
        for f in os.listdir('temp/mac/Incredibox.app/Contents/Frameworks/'):
            if os.path.isdir(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}') and f.endswith('.framework'):
                os.chmod(f'temp/mac/Incredibox.app/Contents/Frameworks/{f}/{f.replace(".framework","")}',0o755)
        print('Packing source...')
        shutil.make_archive('output/windows-to-mac-packed','zip','temp/mac/')
        print('Packed as \'windows-to-mac.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()


def windows(output,js_input):
    file = file_selection('zip')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'webapp':
        val = windows_to_webapp(js_input,file)
    elif output == 'source':
        val = windows_to_source(file)
    elif output == 'mac':
        val = windows_to_mac(file)
    return val


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f"EXCEPTION IN ({filename}, LINE {lineno} \"{line.strip()}\"): {exc_obj}")


if __name__ == "__main__":
    print(Panel("[bright_cyan]Incredibox Mod Formatter\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    if os.path.exists('.temp.py'):
        os.remove('.temp.py')
    try:
        print('Checking for updates...')
        h1 = hashlib.sha256()
        with open('compiler.py','rb') as f:
            data=f.read()
            h1.update(data)
        h2 = hashlib.sha256()
        r = requests.get('https://raw.githubusercontent.com/sealldeveloper/incredibox-modding-docs/main/Tools/Compiler/compiler.py')
        text = r.content
        with open('.temp.py','wb') as f:
            f.write(text)
        with open('.temp.py', 'rb') as f:
            data2 = f.read()
        h2.update(data2)
        if not h1.hexdigest() == h2.hexdigest():
            update = Prompt.ask('Out of date! Do you want to update?',choices=['y','n'])
            if update == 'y':
                r = requests.get('https://api.github.com/repos/sealldeveloper/incredibox-modding-docs/contents/Tools/Compiler?ref=main')
                json = r.json()
                for x in track(json, description='Updating...'):
                    if not x['type'] == 'dir':
                        res = requests.get(x['download_url'])
                        data = res.content
                        with open(f'{x["name"]}','wb') as f:
                            f.write(data)
                    else:
                        r2 = requests.get(x['url'])
                        json2 = r2.json()
                        if os.path.exists(x['name']):
                            shutil.rmtree(x['name'])
                        os.makedirs(x['name'])
                        for y in json2:
                            if not y['type'] == 'dir':
                                res2 = requests.get(y['download_url'])
                                data2 = res2.content
                                with open(f'{x["name"]}/{y["name"]}','wb') as ff:
                                    ff.write(data2)
                print('Rerun the program, updated!')
                if os.path.exists('.temp.py'):
                    os.remove('.temp.py')
                sys.exit()
        else:
            print('[bright_green]Latest Version!')
        if os.path.exists('.temp.py'):
            os.remove('.temp.py')
    except Exception as e:
        print(f'[bright_red]ERROR: Failed to check for updates!\n{str(e)}')
        PrintException()
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    js_input = ""
    format_output = ""
    format_input = Prompt.ask("Enter the format you are importing",choices=['android','source','windows','mac'])
    output_choices=[]
    if format_input == 'android':
        output_choices.extend(['source','webapp','windows','mac'])
    elif format_input == 'source':
        output_choices.extend(['webapp','windows','mac'])
    elif format_input == 'windows':
        output_choices.extend(['source','webapp','mac'])
    elif format_input == 'mac':
        output_choices.extend(['source','webapp','windows'])
    format_output = Prompt.ask("Enter the format you are exporting",choices=output_choices)
    if not format_output == 'source':
        js_input = 'modify'
    else:
        js_input = 'replace'
    while True:
        try:
            res = ""
            if format_input == 'android':
                res = android(format_output,js_input)
            elif format_input == 'source':
                res = source(format_output,js_input)
            elif format_input == 'windows':
                res = windows(format_output,js_input)
            elif format_input == 'mac':
                res = mac(format_output,js_input)
            if not res:
                res_redo = Prompt.ask("The conversion failed, do you want to try again?",choices=['y','n'])
                if res_redo == 'n':
                    break
            if res:
                break
        except Exception:
            PrintException()
