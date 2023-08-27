import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
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
except Exception as e:
    print(f'[bright_red]ERROR: Packages have failed to install, please try reinstalling them.\n{str(e)}')
    sys.exit()

def jsfix(path,os,target,snd):
    with open(path) as f:
        d=jsmin(f.read())
    with open(path,'w') as f:
        try:
            p1 = d.split(',target="',1)[0]
            p2 = d.split(',target="',1)[1].split('"',1)[1]
            d = p1 + f',target="{target}"' + p2
            p1 = d.split(',osname="')[0]
            p2 = d.split(',osname="',1)[1].split('"',1)[1]
            d = p1 + f',osname="{os}"' + p2
            p1 = d.split(',sndtype="')[0]
            p2 = d.split(',sndtype="',1)[1].split('"',1)[1]
            d = p1 + f',sndtype="{snd}"' + p2
        except Exception as e:
            path=path.split('/')
            print(f'[bright_yellow]WARNING: {path[len(path)-1]} is likely obfuscated or a weird version, sizing and buttons may be weird or incorrect depending on platform.\n{str(e)}')
            PrintException()
        f.write(d)

def webapp_format_conversion():
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
                            print(f'{x} - {f} -> {x} - {newname}')
                        except Exception as e:
                            print(f'{x} - {f} -> [bright_red]ERROR! Couldn\'t convert...\n{str(e)}')
                shutil.rmtree(f'{path}/ogg')
            print('Converting all bonuses to MP4\'s...')
            path=f'temp/webapp/{x}/video'
            if not os.path.exists(path):
                os.makedirs(path)
            for y in os.listdir(path):
                if os.path.isfile(f'{path}/{y}') and not y.endswith('mp4'):
                    newname=y.split('.')[0]
                    video = VideoFileClip(f'{path}/{y}')
                    video.write_videofile(f'{path}/{newname}.mp4')
                    os.remove(f'{path}/{y}')
    return assetversions

def webapp_css_html_setup(version,assetversions):
    print('Patching files for your icon count...')
    icon="""
    <div class='icon hoverLocked' id='replaceiconid'>
        <div class='img'></div>
        <div class='txt'></div>
        <div class='bul'>
            <svg class='icn-svg'>
            <use xlink:href='#ic-check'></use>
            </svg>
        </div>
        <div class='ic-locked'>
            <svg class='icn-svg'>
            <use xlink:href='#ic-lock'></use>
            </svg>
        </div>
    </div>
    """
    versionhtml=f"<div class='text mini'>{version}</div>"
    icons=[]
    for i in assetversions:
        icons.append(icon.replace('replaceiconid',f'icon{i}'))
    iconhtml="\n".join(icons)
    newdata=[]
    with open('temp/webapp/app.html','r') as f:
        data=f.readlines()
        for l in data:
            if 'iconsreplaceme' in l:
                newdata.append(iconhtml)
            elif 'versionreplaceme' in l:
                newdata.append(versionhtml)
            else:
                newdata.append(l)
        with open('temp/webapp/newapp.html','w') as w:
            finaldata="<!-- Compiled using sealldevelopers source to webapp compiler -->\n"+"\n".join(newdata)
            w.write(finaldata)
            w.close()
        f.close()
    os.remove('temp/webapp/app.html')
    os.rename('temp/webapp/newapp.html','temp/webapp/app.html')
    newdata=[]
    with open('temp/webapp/index.html','r') as f:
        data=f.readlines()
        for l in data:
            if 'iconsreplaceme' in l:
                newdata.append(iconhtml)
            elif 'versionreplaceme' in l:
                newdata.append(versionhtml)
            else:
                newdata.append(l)
        with open('temp/webapp/newindex.html','w') as w:
            finaldata="<!-- Compiled using sealldevelopers source to webapp compiler -->\n"+"\n".join(newdata)
            w.write(finaldata)
            w.close()
        f.close()
    os.remove('temp/webapp/index.html')
    os.rename('temp/webapp/newindex.html','temp/webapp/index.html')
    print('Patching css...')
    count=0
    csses=['\n\n/* CSS Made with sealldeveloper webapp converter */']
    for i in assetversions:
        css="""
        #page-splash .centered #sp-select .icon#icon"""+str(i)+""".tweenUp{
            -webkit-animation:g .5s cubic-bezier(.165,.84,.44,1) ."""+str(18+(count*5))+"""s forwards;
            animation:g .5s cubic-bezier(.165,.84,.44,1) ."""+str(18+(count*5))+"""s forwards
        }
        #sp-select .icon#icon"""+str(i)+""" .img{
            background-position:-"""+str(130*(int(i)-1))+"""px 0
        }
        #sp-select .icon#icon"""+str(i)+""" .txt{
            background-position:-"""+str(130*(int(i)-1))+"""px -126px
        }
        #sp-select .icon#icon"""+str(i)+""" .bul{
            background-color:#000000
        }"""
        csses.append(css)
        count+=1
    with open('temp/webapp/css/style.min.css','a') as f:
        f.write("\n".join(csses))
        f.close()

def android_unpack(names):
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

def android_to_source(names):
    os.makedirs('temp/android/')
    os.makedirs('temp/asar/')
    print('Unpacking template...')
    shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
    print('Unpacking app...')
    shutil.unpack_archive('input/app.apk','temp/android/','zip')
    print('Organising new folder...')
    android_unpack(names)
    print('Packing source...')
    shutil.make_archive('output/apk-to-source-packed','zip','temp/asar/')
    print('Packed as \'apk-to-source-packed.zip\'! Cleaning up...')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    return True


def android_to_webapp(names,js_input):
    try:
        version=Prompt.ask('Pack Version to be displayed (eg. 1.0.0)')
        print('Importing libraries...')
        os.makedirs('temp/asar/')
        os.makedirs('temp/webapp/')
        print('Unpacking templates...')
        shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
        shutil.unpack_archive('templates/webapp.zip','temp/webapp/','zip')
        print('Unpacking app...')
        shutil.unpack_archive('input/app.apk','temp/android/','zip')
        print('Organising new folder...')
        android_unpack(names)
        print('Duplicating source to webapp...')
        for x in os.listdir('temp/asar/app'):
            if os.path.isdir(f'temp/asar/app/{x}'):
                if not x in ['css']:
                    copy_tree(f'temp/asar/app/{x}',f'temp/webapp/{x}')
        assetversions = webapp_format_conversion()
        webapp_css_html_setup(version,assetversions)
        if js_input == 'modify':
            jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
            jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
        print('Packing up webapp...')
        shutil.make_archive('output/apk-to-webapp-packed','zip','temp/webapp/')
        print('Packed as \'apk-to-webapp-packed.zip\'! Cleaning up...')
        if os.path.exists('temp/'):
            shutil.rmtree('temp/')
        return True
    except:
        PrintException()


def android_to_windows(names,js_input):
    os.makedirs('temp/windows/')
    os.makedirs('temp/android/')
    os.makedirs('temp/asar/')
    print('Unpacking template(s)...')
    shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
    shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
    print('Unpacking app...')
    shutil.unpack_archive('input/app.apk','temp/android/','zip')
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
    if not os.path.exists('input/app.apk'):
        print('[bright_red]ERROR: Please move your Incredibox Mod .apk file into the \'input\' folder and name it \'app.apk\'!')
        return False
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'source':
        val = android_to_source(names)
    elif output == 'webapp':
        val = android_to_webapp(names,jsinput)
    elif output == 'windows':
        val = android_to_windows(names,jsinput)
    return val


def source_to_webapp(js_input):
    names = [
        'css'
    ]
    version=Prompt.ask('Pack Version to be displayed (eg. 1.0.0)')
    os.makedirs('temp/webapp/')
    print('Unpacking template...')
    shutil.unpack_archive('templates/webapp.zip','temp/webapp/','zip')
    print('Duplicating source to webapp...')
    for x in os.listdir('input/source/app'):
        if os.path.isdir(f'input/source/app/{x}'):
            if not x in names:
                copy_tree(f'input/source/app/{x}',f'temp/webapp/{x}')
    assetversions = webapp_format_conversion()
    webapp_css_html_setup(version,assetversions)
    if js_input == 'modify':
        jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
        jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
    print('Packing up webapp...')
    shutil.make_archive('output/webapp-packed','zip','temp/webapp/')
    print('Packed as \'webapp-packed.zip\'! Cleaning up...')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    return True


def source_to_windows(js_input):
    os.makedirs('temp/windows/')
    print('Unpacking template...')
    shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
    copy_tree('input/source','temp/source')
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


def source(output,js_input):
    if not os.path.exists('input/source/'):
        print('[bright_red]ERROR: Please move your mod source code into the \'source\' folder, and then put the \'source\' folder in the \'input\' folder!')
        os.makedirs('source/')
        return False
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'webapp':
        val = source_to_webapp(js_input)
    elif output == 'windows':
        val = source_to_windows(js_input)
    return val


def windows_to_webapp(js_input):
    names = [
        'css'
    ]
    version=Prompt.ask('Pack Version to be displayed (eg. 1.0.0): ')    
    os.makedirs('temp/webapp/')
    os.makedirs('temp/windows/')
    print('Unpacking template and app...')
    shutil.unpack_archive('templates/webapp.zip','temp/webapp/','zip')
    shutil.unpack_archive('input/app.zip','temp/windows/','zip')
    print('Unpacking asar...')
    extract_asar('temp/windows/app/resources/app.asar','temp/source/')
    print('Duplicating source to webapp...')
    for x in os.listdir('temp/source/app'):
        if os.path.isdir(f'temp/source/app/{x}'):
            if not x in names:
                copy_tree(f'temp/source/app/{x}',f'temp/webapp/{x}')

    assetversions = webapp_format_conversion()
    webapp_css_html_setup(version,assetversions)
    if js_input == 'modify':
        jsfix('temp/webapp/js/main.min.js','ios','browser','mp3')
        jsfix('temp/webapp/js/index.min.js','ios','browser','mp3')
    print('Packing up webapp...')
    shutil.make_archive('output/windows-to-webapp-packed','zip','temp/webapp/')
    print('Packed as \'windows-to-webapp-packed.zip\'! Cleaning up...')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    return True


def windows_to_source():
    names = [
        'css',
        'font',
        'img',
        'js',
        'lang',
        'snd',
        'app.html',
        'index.html'
    ]
    os.makedirs('temp/windows/')
    print('Unpacking app...')
    shutil.unpack_archive('input/app.zip','temp/windows/','zip')
    print('Unpacking asar...')
    extract_asar('temp/windows/app/resources/app.asar','temp/source/')
    print('Packing source...')
    shutil.make_archive('output/windows-to-source-packed','zip','temp/source/')
    print('Packed as \'windows-to-source-packed.zip\'! Cleaning up...')
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    return True


def windows(output):
    if not os.path.exists('input/app.zip'):
        print('[bright_red]ERROR: Please move your mod zip into the \'input\' folder and name it \'app.zip\'!')
        return False
    if os.path.exists('temp/'):
        shutil.rmtree('temp/')
    if os.path.exists('output/'):
        shutil.rmtree('output/')
    os.makedirs('output/')
    val = False
    if output == 'webapp':
        val = windows_to_webapp(js_input)
    elif output == 'source':
        val = windows_to_source()
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
                sys.exit()
        else:
            if os.path.exists('.temp.py'):
                os.remove('.temp.py')
            print('[bright_green]Latest Version!')
    except Exception as e:
        print(f'[bright_red]ERROR: Failed to check for updates!\n{str(e)}')
        PrintException()
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    js_input = ""
    format_output = ""
    format_input = Prompt.ask("Enter the format you are importing",choices=['android','source','windows'])
    output_choices=[]
    if format_input == 'android':
        output_choices.extend(['source','webapp','windows'])
    elif format_input =='source':
        output_choices.extend(['webapp','windows'])
    elif format_input =='windows':
        output_choices.extend(['source','webapp'])
    format_output = Prompt.ask("Enter the format you are exporting",choices=output_choices)
    if not format_output == 'source':
        js_input = Prompt.ask("Do you want the JS files to modify the existing ones in your mod, or to use tested ones (v0.5.4) and replace yours?",choices=['replace','modify'])
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
            if not res:
                res_redo = Prompt.ask("The conversion failed, do you want to try again?",choices=['y','n'])
                if res_redo == 'n':
                    break
            if res:
                break
        except Exception:
            PrintException()
