"""
Plan
- Replace the points in the HTML files with the appropriate code.
- Make sure MP3's are created.
- Export
"""
names = [
    'css',
    'js'
]
version=input('Pack Version to be displayed (eg. 1.0.0): ')
import os,sys,shutil
from distutils.dir_util import copy_tree
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
if not os.path.exists('source/'):
    print('Please move your mod source code into the \'source\' folder!')
    os.makedirs('source/')
    sys.exit()
if os.path.exists('temp/'):
    shutil.rmtree('temp/')
if os.path.exists('output/'):
    shutil.rmtree('output/')
os.makedirs('output/')
os.makedirs('temp/webapp/')
print('Unpacking template...')
shutil.unpack_archive('templates/webapp.zip','temp/webapp/','zip')
print('Duplicating source to webapp...')
for x in os.listdir('source/app'):
    if os.path.isdir(f'source/app/{x}'):
        if not x in names:
            copy_tree(f'source/app/{x}',f'temp/webapp/{x}')

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
                        print(f'{x}/sound/ogg/{f} -> {x}/sound/mp3/{newname}')
                    except Exception as e:
                        print(f'ogg/{f} -> ERROR! Couldn\'t convert... ({str(e)})')
                        print(e)
            shutil.rmtree(f'{path}/ogg')
        print('Converting all bonuses to MP4\'s...')
        path=f'temp/webapp/{x}/video'
        for y in os.listdir(path):
            if os.path.isfile(f'{path}/{y}') and not y.endswith('mp4'):
                newname=y.split('.')[0]
                video = VideoFileClip(f'{path}/{y}')
                video.write_videofile(f'{path}/{newname}.mp4')
                os.remove(f'{path}/{y}')


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

print('Packing up webapp...')
shutil.make_archive('output/webapp-packed','zip','temp/webapp/')
print('Packed as \'webapp-packed.zip\'! Cleaning up...')
if os.path.exists('temp/'):
    shutil.rmtree('temp/')