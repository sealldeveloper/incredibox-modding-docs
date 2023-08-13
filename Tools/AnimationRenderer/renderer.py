import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.progress import track
    import rich
    from PIL import Image
    from pydub import AudioSegment
    import json,shutil,os,imageio
    from moviepy.editor import *
except:
    print('Packages have failed to install, please try reinstalling them.')
    sys.exit()

def filechecks():
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    if not os.path.exists('input/anime.json'):
        print('[bright_red]ERROR: Make sure theres an \'anime.json\' file in the \'input\' folder.')
        sys.exit()
    if not os.path.exists('input/anime.png'):
        print('[bright_red]ERROR: Make sure theres an \'anime.png\' file in the \'input\' folder.')
        sys.exit()
    if os.path.exists('input/anime_a.ogg'):
        if not os.path.exists('input/anime_b.ogg'):
            print('[bright_yellow]WARNING: No \'anime_b.ogg\' found in the \'input\' folder, will not use an A and B track for audio in the MP4.')
    else:
        print('[bright_yellow]WARNING: No \'anime_a.ogg\' found in the \'input\' folder, will not make an MP4.')

def pathoverride(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def audio_merge(name1,name2):
    try:
        audioa=AudioSegment.from_ogg(name1)
    except:
        print(f'[bright_red]ERROR: The file \'{name1.replace("input","")}\' is an invalid OGG file. Please run it through a program like Audacity and re-export it as an OGG. Then retry.')
    try:
        audiob=AudioSegment.from_ogg(name2)
    except:
        print(f'[bright_red]ERROR: The file \'{name2.replace("input","")}\' is an invalid OGG file. Please run it through a program like Audacity and re-export it as an OGG. Then retry.')
    
    audiocombine=audioa+audiob
    audiocombine.export('output/anime.ogg',format="ogg")
    print('Audio merged, adding audio to MP4...')
    return AudioFileClip('output/anime.ogg')

if __name__ == "__main__":
    print(Panel("[orange_red1]Incredibox Animation Renderer\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    
    filechecks()
    
    f=open('input/anime.json')
    try:
        data=json.load(f)
        height=int(data['height'])
        width=int(data['width'])
        headHeight=int(data['headHeight'])
        animation_frames=data['arrayFrame']
        name=data['animeName']
    except:
        print('Not a valid JSON file!')
        sys.exit()

    pathoverride(f'output/{name}/normal/files')
    pathoverride(f'output/{name}/normal/internal')
    pathoverride(f'output/{name}/normal/gifframes')
    pathoverride(f'output/{name}/normal/output')

    img = Image.open("input/anime.png")
    imgwidth, imgheight = img.size
    print('Extracting bodies...')
    default=img.crop((0,0,width,height))
    default.save(f'output/{name}/normal/files/default.png')

    headless=img.crop((width,0,width*2,height))
    headless.save(f'output/{name}/normal/files/headless.png')

    silhouette=img.crop((width*2,0,width*3,height))
    silhouette.save(f'output/{name}/normal/files/silhouette.png')

    heads=img.crop((0,height,imgwidth,imgheight))
    headswidth,headsheight=heads.size
    headrows=int(headsheight/headHeight)+1
    headcolumns=int(headswidth/width)+1
    count=0
    print(f'Extracting heads... (~{headrows*headcolumns})')
    headcount=0
    for j in range(0,headcolumns):
        for i in track(range(0,headrows), description=f"Counting heads in row {j+1}"):
            temphead=heads.crop((j*width,i*headHeight,(j+1)*width,(i+1)*headHeight))
            if temphead.getbbox():
                headcount+=1
                temphead.save(f'output/{name}/normal/files/head{count}.png')
                temphead.save(f'output/{name}/normal/internal/{j*width}-{i*headHeight+height}.png')
                count+=1
    print(f'Found a total of {headcount} valid heads!')

    print('Creating the silhouette check...')
    silhouettecheck=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    default=Image.open(f'output/{name}/normal/files/default.png')
    silhouettecheck.paste(default,(0,0),default)
    silhouette=Image.open(f'output/{name}/normal/files/silhouette.png')
    datas = silhouette.getdata()
    newdata=[]
    for i in track(datas, description="Fixing silouette pixel transparency..."):
        if not i[3] == 0:
            newdata.append((i[0],i[1],i[2],210))
        else:
            newdata.append(i)
    silhouette.putdata(newdata)
    silhouettecheck.paste(silhouette,(0,0),silhouette)
    silhouettecheck.save(f'output/{name}/normal/output/silhouette-check.png')
    print('Finishing silhouette check!')
    gifframes=[]

    framecount=0
    for frame in track(animation_frames, description="Creating GIF frames..."):
        framecount+=1
        #print(f'Making gif frames: {framecount}/{len(animation_frames)}...')
        frame=frame['prop'].split(',')
        try:
            temphead=Image.open(f'output/{name}/normal/internal/{int(frame[0])}-{int(frame[1])}.png')
        except:
            print(f'ERROR: [bright_red]A frame in your animation is selecting an invalid head ({int(frame[0])},{int(frame[1])}), or your heads are seperated unevenly in your sprite sheet. (Animation frame {framecount})')
            sys.exit()
        tempheadless=Image.open(f'output/{name}/normal/files/headless.png')
        background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
        background.paste(tempheadless,(0,0),tempheadless)
        background.paste(temphead, (round(float(frame[2])),round(float(frame[3]))), temphead)
        background.save(f'output/{name}/normal/gifframes/{framecount}.png')
        gifframes.append(imageio.v3.imread(f'output/{name}/normal/gifframes/{framecount}.png', plugin="pillow", mode="RGBA"))

    print('Creating default vs checkframe...')
    background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    tempbody=Image.open(f'output/{name}/normal/files/default.png')
    background.paste(tempbody,(0,0),tempbody)
    background.save(f'output/{name}/normal/internal/checkframe1.png')
    background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    tempbody=Image.open(f'output/{name}/normal/gifframes/1.png')
    background.paste(tempbody,(0,0),tempbody)
    background.save(f'output/{name}/normal/internal/checkframe2.png')
    defaultcheckframes=[imageio.v3.imread(f'output/{name}/normal/internal/checkframe1.png', plugin="pillow", mode="RGBA"),imageio.v3.imread(f'output/{name}/normal/internal/checkframe2.png', plugin="pillow", mode="RGBA")]

    print('Compiling GIFs...')
    imageio.v3.imwrite(f'output/{name}/normal/output/anime.gif',gifframes,duration=int(1/24*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
    imageio.v3.imwrite(f'output/{name}/normal/output/default-pose-compared-to-first-frame.gif',defaultcheckframes,duration=int(1/1*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
    print('GIFs finished!')

    if os.path.exists('input/anime_a.ogg'):
        print('Compiling MP4...')
        imageio.v2.mimwrite('output/anime-hd.mp4',gifframes,fps=24)
        video=VideoFileClip('output/anime-hd.mp4')
        print('Compiled MP4, merging audio tracks..')
        if os.path.exists('input/anime_b.ogg'):
            audio=audio_merge('input/anime_a.ogg','input/anime_b.ogg')
        else:
            audio=audio_merge('input/anime_a.ogg','input/anime_a.ogg')
        final=video.set_audio(audio)
        final.write_videofile(f'output/{name}/normal/output/anime-with-audio.mp4')

    if os.path.exists('output/anime-hd.mp4'):
        os.remove('output/anime-hd.mp4')
    if os.path.exists('output/anime.ogg'):
        os.remove('output/anime.ogg')
    print('[bright_green]Compiled! Cleaning up...')
    if os.path.exists(f'output/{name}/normal/internal'):
        shutil.rmtree(f'output/{name}/normal/internal')