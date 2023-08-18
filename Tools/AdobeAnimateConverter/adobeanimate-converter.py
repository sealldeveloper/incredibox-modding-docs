import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.progress import track
    import rich
    from PIL import Image, ImageDraw
    from pydub import AudioSegment
    import json,shutil,os,imageio
    from moviepy.editor import *
    import math
    from shutil import copyfile
except:
    print('Packages have failed to install, please try reinstalling them.')
    sys.exit()

def filechecks(render_choice):
    if not os.path.exists('input/anime.json'):
        print('[bright_red]ERROR: Make sure theres an \'anime.json\' file in the \'input\' folder.')
        sys.exit()
    else:
        print('[green]Found \'anime.json\'!')
    if render_choice == 'no-hd' or render_choice == 'both':
        if not os.path.exists('input/anime.png'):
            print('[bright_red]ERROR: Make sure theres an \'anime.png\' file in the \'input\' folder.')
            sys.exit()
        else:
            print('[green]Found \'anime.png\'!')
    if render_choice == 'hd' or render_choice == 'both':
        if not os.path.exists('input/anime-hd.png'):
            print('[bright_red]ERROR: Make sure theres an \'anime-hd.png\' file in the \'input\' folder.')
            sys.exit()
        else:
            print('[green]Found \'anime-hd.png\'!')

def get_widthheight(frames):
    count=0
    width=0
    height=0
    for x in frames:
        if count == 0:
            width=int(frames[x]['sourceSize']['w'])
            height=int(frames[x]['sourceSize']['h'])
        count+=1
    return width,height

def pathoverride(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f'[bright_red]ERROR: Can\'t delete \'{path}\'! Most likely you have something already using this folder. Please close the programs open in this folder!\n\n{str(e)}')
            sys.exit()
    os.makedirs(path)

def extract_heads(width,height,img,v):
    headcount=0
    prev=[]
    newframes=[]
    headcoords=[]
    for x in track(frames, description=f"({v}) Extracting heads..."):
        x=frames[x]['frame']
        if not x in prev:
            headcount+=1
            prev.append(x)
            temphead=img.crop((int(x['x']),int(x['y']),width+int(x['x']),height+int(x['y'])))
            temphead.save(f'output/{v}/heads/{x["x"]},{x["y"]}_head.png')
            headcoords.append((int(x['x']),int(x['y'])))
        newframes.append({"prop":f"{x['x']},{x['y']},0,0"})
    return headcount, newframes, headcoords

def spritesheet_build(width,height,headcount,headcoords,newframes,v):
    count=0
    new=Image.new('RGBA',(width*5,height*(math.ceil(headcount/5)+1)), (255,255,255,0))
    currentx=0
    currenty=int(height)
    modified_indexes=[]
    for x in track(range(headcount), description=f"({v}) Forging sprite-sheet..."):
        count+=1
        x,y=headcoords[x]
        temphead=Image.open(f'output/{v}/heads/{x},{y}_head.png')
        copyfile(f'output/{v}/heads/{x},{y}_head.png',f'output/{v}/fixedheads/{currentx},{currenty}_head.png')
        new.paste(temphead,(currentx,currenty),temphead)
        fc=0
        for f in newframes:
            if f['prop'] == f"{x},{y},0,0" and fc not in modified_indexes:
                modified_indexes.append(fc)
                newframes[fc]['prop'] = f"{currentx},{currenty},0,0"
            fc+=1
        
        if count%5 == 0:
            currenty+=int(height)
            currentx=0
        else:
            currentx+=int(width)
    if v == 'hd':
        new.save(f'output/{v}/anime-hd.png')
    else:
        new.save(f'output/{v}/anime.png')
    fc=0
    for f in track(newframes, description=f"({v}) Checking all frames are valid..."):
        fc+=1
        x=f['prop'].split(',')[0]
        y=f['prop'].split(',')[1]
        if not os.path.isfile(f'output/{v}/fixedheads/{x},{y}_head.png'):
            print(f'[bright_red]ERROR: {fc} - {x},{y}')
    return newframes

def build_json(newframes,width,height,v):
    print(f"({v}) Building animation json...")
    fixedjson={"animeName":"generated-from-fla-using-sealldevelopers-tools","percentageMax":"0.2","totalFrame":f"{len(newframes)}","width":f"{width}","height":f"{height}","headHeight":f"{height}","arrayFrame":newframes}
    f=open('output/anime.json','w')
    json.dump(fixedjson,f)

def path_setup(v):
    try:
        pathoverride(f'output/{v}/heads')
        pathoverride(f'output/{v}/fixedheads')
        pathoverride(f'output/{v}/frames')
    except:
        print(f'[bright_red]ERROR ({v}): Failed to delete a folder, likely its in use. Please retry.')

if __name__ == "__main__":
    print(Panel("[purple3]Adobe Animate [deep_pink2]--> [medium_spring_green]Incredibox [pale_turquoise1]Conversion\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    input_choice = Prompt.ask("Are your sprite sheet(s) in HD, no-HD, or do both exist?",choices=['no-hd','hd','both'])
    json_choice = Prompt.ask("Is the JSON in an HD or non-hd format?",choices=['no-hd','hd'])
    filechecks(input_choice)
    
    f=open('input/anime.json', encoding='utf8')
    try:
        data=f.read()
        data=data[1:]
        jsondata=json.loads(data)
        frames=jsondata['frames']
    except Exception as e:
        print(f'[bright_red]ERROR: \'anime.json\' is not a valid animation Adobe Animate JSON file!\n\n{str(e)}')
        sys.exit()
    
    width,height = get_widthheight(frames)
    if not width%164 == 0:
        print(f'[bright_yellow]WARNING: The width is not a recommended value (a multiple of 164, currently its {width}). This may result in the polo being off-center.')
    if input_choice == 'no-hd' or input_choice == 'both':
        if json_choice == 'hd':
            width=width/2
            height=height/2
        path_setup('no-hd')
        img = Image.open('input/anime.png')
        headcount, newframes, headcoords = extract_heads(width,height,img,'no-hd')
        newframes = spritesheet_build(width,height,headcount,headcoords,newframes,'no-hd')
        build_json(newframes,width,height,'no-hd')
    if input_choice == 'hd' or input_choice == 'both':
        if json_choice == ' non-hd':
            width=width*2
            height=height*2
        path_setup('hd')
        img = Image.open('input/anime-hd.png')
        headcount, newframes, headcoords = extract_heads(width,height,img,'hd')
        newframes = spritesheet_build(width,height,headcount,headcoords,newframes,'hd')
        if input_choice == 'hd':
            build_json(newframes,width,height,'hd')