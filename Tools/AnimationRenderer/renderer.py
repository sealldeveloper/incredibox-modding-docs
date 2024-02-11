import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import track
    import rich
    from PIL import Image, ImageDraw
    from pydub import AudioSegment
    import json,shutil,os,imageio
    from moviepy.editor import *
    import math
    import requests
    import hashlib
except Exception as e:
    print(f'[bright_red]ERROR: Packages have failed to install, please try reinstalling them.\n{str(e)}')
    sys.exit()

def filechecks(render_choice,filename):
    if not os.path.exists(f'input/{filename}.json'):
        print(f'[bright_red]ERROR: Make sure theres an \'{filename}.json\' file in the \'input\' folder.')
        sys.exit()
    else:
        print(f'[green]Found \'{filename}.json\'!')
    if render_choice == 'no-hd' or render_choice == 'both':
        if not os.path.exists(f'input/{filename}.png'):
            print(f'[bright_red]ERROR: Make sure theres an \'{filename}.png\' file in the \'input\' folder.')
            sys.exit()
        else:
            print(f'[green]Found \'{filename}.png\'!')
    if render_choice == 'hd' or render_choice == 'both':
        if not os.path.exists(f'input/{filename}-hd.png'):
            print(f'[bright_red]ERROR: Make sure theres an \'{filename}-hd.png\' file in the \'input\' folder.')
            sys.exit()
        else:
            print(f'[green]Found \'{filename}-hd.png\'!')
    if not os.path.exists(f'input/{filename}_combined.ogg'):
        print(f'[bright_yellow]No \'{filename}_combined.ogg\' found in \'input\', checking for \'{filename}_a.ogg\'...')
        if os.path.exists(f'input/{filename}_a.ogg'):
            print(f'[green]Found \'{filename}_a.ogg\'!')
            if not os.path.exists(f'input/{filename}_b.ogg'):
                print(f'[bright_yellow]WARNING: No \'{filename}_b.ogg\' found in the \'input\' folder, will not use an A and B track for audio in the MP4.')
            else:
                print(f'[green]Found \'{filename}_b.ogg\'!')
        else:
            print(f'[bright_yellow]WARNING: No \'{filename}_a.ogg\' found in the \'input\' folder, will not make an MP4.')
    else:
            print(f'[green]Found \'{filename}_combined.ogg\'!')

def file_selection():
    files=[]
    table = Table()
    table.add_column("Render Options", style="magenta")
    for f in os.listdir('input'):
        if f.endswith(f'.json') and os.path.isfile(f'input/{f}'):
            name=f.split('.json')[0]
            if os.path.isfile(f'input/{name}.png') or os.path.isfile(f'input/{name}-hd.png'):
                files.append(name)
                table.add_row(name)
    print(table)
    print("[dodger_blue1]Note: If your not seeing your files make sure the spritesheets do not contain \'-sprite\', the names for the JSON and spritesheet should be the same!")
    selected = Prompt.ask('Which file do you want to use?', choices=files, show_choices=False)
    return selected

def pathoverride(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f'[bright_red]ERROR: Can\'t delete \'{path}\'! Most likely you have something already using this folder. Please close the programs open in this folder!\n\n{str(e)}')
            sys.exit()
    os.makedirs(path)

def extract_bodies(width,height,name,v):
    global selected_file_name
    if v == "hd":
        img = Image.open(f"input/{selected_file_name}-hd.png")
    else:
        img = Image.open(f"input/{selected_file_name}.png")
    imgwidth, imgheight = img.size
    print(f'({v}) Extracting bodies...')
    default=img.crop((0,0,width,height))
    default.save(f'output/{name}/{v}/files/default.png')

    headless=img.crop((width,0,width*2,height))
    headless.save(f'output/{name}/{v}/files/headless.png')

    silhouette=img.crop((width*2,0,width*3,height))
    silhouette.save(f'output/{name}/{v}/files/silhouette.png')
    return imgwidth,imgheight,img

def extract_heads(height,imgwidth,imgheight,v,img, headHeight, width,name):
    heads=img.crop((0,height,imgwidth,imgheight))
    headswidth,headsheight=heads.size
    headrows=int(headsheight/headHeight)+1
    headcolumns=int(headswidth/width)+1
    print(f'({v}) Extracting heads... (~{headrows*headcolumns})')
    headcount=0
    for j in range(0,headcolumns):
        for i in track(range(0,headrows), description=f"({v}) Counting heads in column {j+1}"):
            temphead=heads.crop((j*width,i*headHeight,(j+1)*width,(i+1)*headHeight))
            if temphead.getbbox():
                headcount+=1
                temphead.save(f'output/{name}/{v}/files/head{headcount-1}.png')
                temphead.save(f'output/{name}/{v}/internal/{j*width}-{i*headHeight+height}.png')
    print(f'({v}) Found a total of {headcount} valid heads!')
    return headswidth,headsheight,headcount

def silhouette_check(width,height,name,v):
    print(f'({v}) Creating the silhouette check...')
    silhouettecheck=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    default=Image.open(f'output/{name}/{v}/files/default.png')
    silhouettecheck.paste(default,(0,0),default)
    silhouette=Image.open(f'output/{name}/{v}/files/silhouette.png')
    datas = silhouette.getdata()
    newdata=[]
    for i in track(datas, description=f"({v}) Fixing silouette pixel transparency..."):
        if not i[3] == 0:
            newdata.append((i[0],i[1],i[2],210))
        else:
            newdata.append(i)
    silhouette.putdata(newdata)
    silhouettecheck.paste(silhouette,(0,0),silhouette)
    silhouettecheck.save(f'output/{name}/{v}/output/silhouette-check.png')
    print(f'({v}) Finishing silhouette check!')

def gif_frames(name,v):
    gifframes=[]
    gifframestext=[]

    framecount=0
    for frame in track(animation_frames, description=f"({v}) Creating GIF frames..."):
        framecount+=1
        try:
            oldframe=frame['prop']
            frame=frame['prop'].split(',')
        except:
            print(f'[bright_red]ERROR ({v}): A frame in your animation is missing the \'prop\' aspect at frame {framecount} ({frame})')
            sys.exit()
        try:
            x = frame[0]
            y = frame[1]
        except:
            print(f'[bright_red]ERROR ({v}): A frame in your animation is using an invalid head location that is either missing or not a number ({oldframe}) at frame {framecount}')
            sys.exit()
        try:
            if v == 'normal':
                temphead=Image.open(f'output/{name}/{v}/internal/{int(float(frame[0]))}-{int(float(frame[1]))}.png')
            else:
                temphead=Image.open(f'output/{name}/{v}/internal/{int(float(frame[0]))*2}-{int(float(frame[1]))*2}.png')
        except:
            if v == 'normal':
                print(f'[bright_red]ERROR ({v}): A frame in your animation is selecting an invalid head ({int(frame[0])},{int(frame[1])}), or your heads are seperated unevenly in your sprite sheet. (Animation frame {framecount})')
            else:
                print(f'[bright_red]ERROR ({v}): A frame in your animation is selecting an invalid head ({int(frame[0])},{int(frame[1])} or for HD sprite sheets {int(frame[0])*2},{int(frame[1])*2}), or your heads are seperated unevenly in your sprite sheet. (Animation frame {framecount})')
            sys.exit()
        tempheadless=Image.open(f'output/{name}/{v}/files/headless.png')
        background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
        background.paste(tempheadless,(0,0),tempheadless)
        try:
            m1 = round(float(frame[2]))
            m2 = round(float(frame[3]))
        except:
            print(f'[bright_red]ERROR ({v}): A frame in your animation is using an invalid movement ({int(frame[0])},{int(frame[1])},{frame[2]},{frame[3]}) at frame {framecount}')
            sys.exit()
        background.paste(temphead, (m1,m2), temphead)
        background.save(f'output/{name}/{v}/gifframes/{framecount}.png')
        backgroundDraw = ImageDraw.Draw(background)
        backgroundDraw.text((0,0), f"{framecount}",fill=(200,0,0))
        background.save(f'output/{name}/{v}/gifframes/text/{framecount}_text.png')
        gifframes.append(imageio.v3.imread(f'output/{name}/{v}/gifframes/{framecount}.png', plugin="pillow", mode="RGBA"))
        gifframestext.append(imageio.v3.imread(f'output/{name}/{v}/gifframes/text/{framecount}_text.png', plugin="pillow", mode="RGBA"))
    return gifframes,gifframestext

def def_vs_check(width,height,name,v):
    print(f'({v}) Creating default vs checkframe...')
    background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    tempbody=Image.open(f'output/{name}/{v}/files/default.png')
    background.paste(tempbody,(0,0),tempbody)
    background.save(f'output/{name}/{v}/internal/checkframe1.png')
    background=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    tempbody=Image.open(f'output/{name}/{v}/gifframes/1.png')
    background.paste(tempbody,(0,0),tempbody)
    background.save(f'output/{name}/{v}/internal/checkframe2.png')
    defaultcheckframes=[imageio.v3.imread(f'output/{name}/{v}/internal/checkframe1.png', plugin="pillow", mode="RGBA"),imageio.v3.imread(f'output/{name}/{v}/internal/checkframe2.png', plugin="pillow", mode="RGBA")]
    return defaultcheckframes

def compile_gifs(gifframes,defaultcheckframes,name,v,filename):
    print(f'({v}) Compiling GIFs...')
    imageio.v3.imwrite(f'output/{name}/{v}/output/default-pose-compared-to-first-frame.gif',defaultcheckframes,duration=int(1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
    if filename=='no-text':
        imageio.v3.imwrite(f'output/{name}/{v}/output/anime_{filename}.gif',gifframes,duration=int(1/24*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
    else:
        imageio.v3.imwrite(f'output/{name}/{v}/output/anime_{filename}.gif',gifframestext,duration=int(1/24*1000), plugin="pillow", mode="RGBA", loop=0, transparency=0, disposal=2)
    print(f'({v}) GIFs finished!')

def audio_merge(name1,name2,totalFrame,v):
    global selected_file_name
    sfxlength = math.floor((totalFrame/2)/0.024)
    try:
        audioa=AudioSegment.from_ogg(name1)
    except:
        print(f'[bright_red]ERROR ({v}): The file \'{name1.replace("input/","")}\' is an invalid OGG file. Please run it through a program like Audacity and re-export it as an OGG. Then retry.')
        sys.exit()
    try:
        audiob=AudioSegment.from_ogg(name2)
    except:
        print(f'[bright_red]ERROR ({v}): The file \'{name2.replace("input/","")}\' is an invalid OGG file. Please run it through a program like Audacity and re-export it as an OGG. Then retry.')
        sys.exit()
    try:
        if name1==name2:
            audioa = audioa[:sfxlength*2]
        else:
            audioa = audioa[:sfxlength]
            audiob = audiob[:sfxlength]
    except Exception as e:
        print(f'[bright_red]ERROR ({v}): Correcting the length of the SFX\'s failed...\n\n{str(e)}')
        sys.exit()
    if name1 == name2:
        audiocombine=audioa
    else:
        audiocombine=audioa+audiob
    audiocombine.export(f'output/{selected_file_name}.ogg',format="ogg")
    print(f'({v}) Audio merged, adding audio to MP4...')
    return AudioFileClip(f'output/{selected_file_name}.ogg')

def mp4_compile(gifframes,name,totalFrame,v,filename):
    if os.path.exists('input/anime_a.ogg') or os.path.exists('input/anime_combined.ogg'):
        print(f'({v}) Compiling MP4...')
        if filename == 'no-text':
            imageio.v2.mimwrite('output/anime-hd.mp4',gifframes,fps=24,macro_block_size=1)
        else:
            imageio.v2.mimwrite('output/anime-hd.mp4',gifframestext,fps=24,macro_block_size=1)
        video=VideoFileClip('output/anime-hd.mp4')
        print(f'({v}) Compiled MP4, processing audio tracks...')
        if os.path.exists('input/anime_combined.ogg'):
            try:
                audio = AudioFileClip('input/anime_combined.ogg')
            except Exception as e:
                PrintException()
        else:
            if os.path.exists('input/anime_b.ogg'):
                audio=audio_merge('input/anime_a.ogg','input/anime_b.ogg',totalFrame,v)
            else:
                audio=audio_merge('input/anime_a.ogg','input/anime_a.ogg',totalFrame,v)
        final=video.set_audio(audio)
        final.write_videofile(f'output/{name}/{v}/output/anime-with-audio_{filename}.mp4',logger=None)

def cleanup(name,v):
    if os.path.exists('output/anime-hd.mp4'):
        try:
            os.remove('output/anime-hd.mp4')
        except Exception as e:
            print(f'[bright_red]ERROR ({v}): Can\'t delete \'output/anime-hd.mp4\'! Most likely you have something already using this file. Please close the programs using this file!\n\n{str(e)}')
            sys.exit()
    if os.path.exists(f'output/{selected_file_name}.ogg'):
        try:
            os.remove(f'output/{selected_file_name}.ogg')
        except Exception as e:
            print(f'[bright_red]ERROR ({v}): Can\'t delete \'output/{selected_file_name}.ogg\'! Most likely you have something already using this file. Please close the programs using this file!\n\n{str(e)}')
            sys.exit()
    print(f'[bright_green]({v}) Compiled! Cleaning up...')
    if os.path.exists(f'output/{name}/{v}/internal'):
        try:
            shutil.rmtree(f'output/{name}/{v}/internal')
        except Exception as e:
            print(f'[bright_red]ERROR ({v}): Can\'t delete \'output/{name}/{v}/internal\'! Most likely you have something already using this folder. Please close the programs open in this folder!\n\n{str(e)}')
            sys.exit()

if __name__ == "__main__":
    print(Panel("[orange_red1]Incredibox Animation Renderer\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    if os.path.exists('.temp.py'):
        os.remove('.temp.py')
    try:
        print('Checking for updates...')
        h1 = hashlib.sha256()
        with open('renderer.py','rb') as f:
            data=f.read()
            h1.update(data)
        h2 = hashlib.sha256()
        r = requests.get('https://raw.githubusercontent.com/sealldeveloper/incredibox-modding-docs/main/Tools/AnimationRenderer/renderer.py')
        text = r.content
        with open('.temp.py','wb') as f:
            f.write(text)
        with open('.temp.py', 'rb') as f:
            data2 = f.read()
        h2.update(data2)
        if not h1.hexdigest() == h2.hexdigest():
            update = Prompt.ask('Out of date! Do you want to update?',choices=['y','n'])
            if update == 'y':
                r = requests.get('https://api.github.com/repos/sealldeveloper/incredibox-modding-docs/contents/Tools/AnimationRenderer?ref=main')
                json = r.json()
                for x in track(json, description="Updating..."):
                    res = requests.get(x['download_url'])
                    data = res.content
                    with open(f'{x["name"]}','wb') as f:
                        f.write(data)
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
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    selected_file_name = file_selection()
    render_choice = Prompt.ask("What render version do you want?",choices=['no-hd','hd','both'])
    no_text_choice = Prompt.ask("Do you want the frame counter?",choices=['y','n'])
    filechecks(render_choice,selected_file_name)
    
    f=open(f'input/{selected_file_name}.json')
    try:
        data=json.load(f)
        height=int(data['height'])
        width=int(data['width'])
        headHeight=int(data['headHeight'])
        totalFrame=int(data['totalFrame'])
        animation_frames=data['arrayFrame']
        name=data['animeName']
    except Exception as e:
        print(f'[bright_red]ERROR: \'{selected_file_name}.json\' is not a valid animation JSON file!\n\n{str(e)}')
        sys.exit()
    if not totalFrame == len(animation_frames):
        print(f'[bright_red]ERROR: The \'totalFrame\' ({totalFrame}) and the amount of frames in the \'arrayFrame\' ({len(animation_frames)}) are not the same in the JSON file! Please make them the same, by either adding more frames or updating the totalFrame.')
        sys.exit()
    if render_choice == 'no-hd' or render_choice == 'both':
        pathoverride(f'output/{name}/normal/files')
        pathoverride(f'output/{name}/normal/internal')
        pathoverride(f'output/{name}/normal/gifframes')
        pathoverride(f'output/{name}/normal/gifframes/text')
        pathoverride(f'output/{name}/normal/output')
        imgwidth,imgheight,img = extract_bodies(width,height,name,'normal')
        headswidth,headsheight,headcount = extract_heads(height,imgwidth,imgheight,'normal',img,headHeight,width,name)
        silhouette_check(width,height,name,'normal')
        gifframes,gifframestext = gif_frames(name,'normal')
        defaultcheckframes = def_vs_check(width,height,name,'normal')
        if no_text_choice == 'n':
            compile_gifs(gifframes,defaultcheckframes,name,'normal','no-text')
            mp4_compile(gifframes,name,len(animation_frames),'normal','no-text')
            cleanup(name,'normal')
        else:
            compile_gifs(gifframestext,defaultcheckframes,name,'normal','text')
            mp4_compile(gifframestext,name,len(animation_frames),'normal','text')
            cleanup(name,'normal')
    if render_choice == 'hd' or render_choice == 'both':
        height=height*2
        width=width*2
        headHeight=headHeight*2
        pathoverride(f'output/{name}/hd/files')
        pathoverride(f'output/{name}/hd/internal')
        pathoverride(f'output/{name}/hd/gifframes')
        pathoverride(f'output/{name}/hd/gifframes/text')
        pathoverride(f'output/{name}/hd/output')
        imgwidth,imgheight,img = extract_bodies(width,height,name,'hd')
        headswidth,headsheight,headcount = extract_heads(height,imgwidth,imgheight,'hd',img, headHeight, width,name)
        silhouette_check(width,height,name,'hd')
        gifframes,gifframestext = gif_frames(name,'hd')
        defaultcheckframes = def_vs_check(width,height,name,'hd')
        if no_text_choice == 'n':
            compile_gifs(gifframes,defaultcheckframes,name,'hd','no-text')
            mp4_compile(gifframes,name,len(animation_frames),'hd','no-text')
            cleanup(name,'hd')
        else:
            compile_gifs(gifframestext,defaultcheckframes,name,'hd','text')
            mp4_compile(gifframestext,name,len(animation_frames),'hd','text')
            cleanup(name,'hd')