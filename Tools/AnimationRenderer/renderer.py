from PIL import Image
from pydub import AudioSegment
import json,shutil,os,imageio
from moviepy.editor import *
f=open('anime.json')
data=json.load(f)
height=int(data['height'])
width=int(data['width'])
headHeight=int(data['headHeight'])
animation_frames=data['arrayFrame']

if os.path.exists('files'):
    shutil.rmtree('files')
os.makedirs('files')
if os.path.exists('internal'):
    shutil.rmtree('internal')
os.makedirs('internal')
if os.path.exists('gifframes'):
    shutil.rmtree('gifframes')
os.makedirs('gifframes')
if os.path.exists('output'):
    shutil.rmtree('output')
os.makedirs('output')

img = Image.open("anime.png")
imgwidth, imgheight = img.size
print('Extracting bodies...')
default=img.crop((0,0,width,height))
default.save('files/default.png')

headless=img.crop((width,0,width*2,height))
headless.save('files/headless.png')

silhouette=img.crop((width*2,0,width*3,height))
silhouette.save('files/silhouette.png')

heads=img.crop((0,height,imgwidth,imgheight))
headswidth,headsheight=heads.size
headrows=int(headsheight/headHeight)+1
headcolumns=int(headswidth/width)+1
count=0
print(f'Extracting heads... (~{headrows*headcolumns})')
for j in range(0,headcolumns):
    for i in range(0,headrows):
        temphead=heads.crop((j*width,i*headHeight,(j+1)*width,(i+1)*headHeight))
        if temphead.getbbox():
            print(f'Found Head! {count+1}/~{headrows*headcolumns}')
            temphead.save(f'files/head{count}.png')
            temphead.save(f'internal/{j*width}-{i*headHeight+height}.png')
            count+=1


silhouettecheck=Image.new('RGBA',(width,height), (255, 255, 255, 0))
default=Image.open(f'files/default.png')
silhouettecheck.paste(default,(0,0),default)
silhouette=Image.open(f'files/silhouette.png')
datas = silhouette.getdata()
newdata=[]
for i in datas:
    if not i[3] == 0:
        newdata.append((i[0],i[1],i[2],210))
    else:
        newdata.append(i)
silhouette.putdata(newdata)
silhouettecheck.paste(silhouette,(0,0),silhouette)
silhouettecheck.save('output/silhouette-check.png')

gifframes=[]

framecount=0
for frame in animation_frames:
    framecount+=1
    print(f'Making gif frames: {framecount}/{len(animation_frames)}...')
    frame=frame['prop'].split(',')
    temphead=Image.open(f'internal/{frame[0]}-{frame[1]}.png')
    tempheadless=Image.open(f'files/headless.png')
    background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    background.paste(tempheadless,(0,0),tempheadless)
    background.paste(temphead, (round(float(frame[2])),round(float(frame[3]))), temphead)
    background.save(f'gifframes/{framecount}.png')
    gifframes.append(imageio.v3.imread(f'gifframes/{framecount}.png', plugin="pillow", mode="RGBA"))


background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
tempbody=Image.open(f'files/default.png')
background.paste(tempbody,(0,0),tempbody)
background.save('internal/checkframe1.png')
background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
tempbody=Image.open(f'gifframes/1.png')
background.paste(tempbody,(0,0),tempbody)
background.save('internal/checkframe2.png')
defaultcheckframes=[imageio.v3.imread(f'internal/checkframe1.png', plugin="pillow", mode="RGBA"),imageio.v3.imread(f'internal/checkframe2.png', plugin="pillow", mode="RGBA")]

def audio_merge(name1,name2):
    audioa=AudioSegment.from_ogg(name1)
    audiob=AudioSegment.from_ogg(name2)
    audiocombine=audioa+audiob
    audiocombine.export('anime.ogg',format="ogg")
    print('Audio merged, adding audio to MP4...')
    return AudioFileClip('anime.ogg')

print('Compiling GIFs...')
imageio.v3.imwrite('output/anime.gif',gifframes,duration=int(1/24*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
imageio.v3.imwrite('output/default-pose-compared-to-first-frame.gif',defaultcheckframes,duration=int(1/1*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)

if os.path.exists('anime_a.ogg'):
    print('Compiling MP4...')
    imageio.v2.mimwrite('anime.mp4',gifframes,fps=24)
    video=VideoFileClip('anime.mp4')
    print('Compiled MP4, merging audio tracks..')
    if os.path.exists('anime_b.ogg'):
        audio=audio_merge('anime_a.ogg','anime_b.ogg')
    else:
        audio=audio_merge('anime_a.ogg','anime_a.ogg')
    final=video.set_audio(audio)
    final.write_videofile('output/anime-with-audio.mp4')

if os.path.exists('anime.mp4'):
    os.remove('anime.mp4')
if os.path.exists('anime.ogg'):
    os.remove('anime.ogg')
print('Compiled! Cleaning up...')
if os.path.exists('internal'):
    shutil.rmtree('internal')