import sys
try:
    from rich import print
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.progress import track
    import rich
    from PIL import Image
    import json, shutil, os, imageio, math
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    from PIL import ImageChops
    import re
    import hashlib
    import requests
except Exception as e:
    print(f'[bright_red]ERROR: Packages have failed to install, please try reinstalling them. ({str(e)})')
    sys.exit()

def calcdiff(im1, im2):
    dif = ImageChops.difference(im1, im2)
    return np.mean(np.array(dif))

def update():
    if os.path.exists('.temp.py'):
        os.remove('.temp.py')
    try:
        print('Checking for updates...')
        h1 = hashlib.sha256()
        with open('flipaclip-converter.py','rb') as f:
            data=f.read()
            h1.update(data)
        h2 = hashlib.sha256()
        r = requests.get('https://raw.githubusercontent.com/sealldeveloper/incredibox-modding-docs/main/Tools/FlipaclipConverter/flipaclip-converter-heads.py')
        text = r.content
        with open('.temp.py','wb') as f:
            f.write(text)
        with open('.temp.py', 'rb') as f:
            data2 = f.read()
        h2.update(data2)
        if not h1.hexdigest() == h2.hexdigest():
            update = Prompt.ask('Out of date! Do you want to update?',choices=['y','n'])
            if update == 'y':
                r = requests.get('https://api.github.com/repos/sealldeveloper/incredibox-modding-docs/contents/Tools/FlipaclipConverter?ref=main')
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
        PrintException()

def boundingBoxes():
    global files
    boundingboxes=[]
    for f in track(files, description="Getting smallest head area..."):
        # get the bbox of all images
        im = Image.open(f'temp/{f}')
        boundingboxes.append(im.getbbox())
    left=boundingboxes[0][0]
    top=boundingboxes[0][1]
    right=boundingboxes[0][2]
    bottom=boundingboxes[0][3]
    for x in boundingboxes:
        # continually check for max size on each box
        if x is None:
            continue
        if x[0] < left:
            left=x[0]
        if x[1] < top:
            top=x[1]
        if x[2] > right:
            right=x[2]
        if x[3] > bottom:
            bottom=x[3]
    return left,top,right,bottom

if __name__ == "__main__":
    print(Panel("[orange_red1]Flipaclip (Heads) to Polo\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    update()
    #check files exist
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    if not os.path.exists('input/files.zip'):
        print('[bright_red]ERROR: File \'files.zip\' does not exist in the input folder!')
        sys.exit()
    #inputs
    hd = Prompt.ask('HD?',choices=['y','n'])
    name=Prompt.ask('Name')
    #cleanup
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.makedirs('temp')
    shutil.unpack_archive('input/files.zip','temp/','zip')
    #variable defenitions
    files=[]
    allimages=[]
    frames=[]
    polishedframes={}
    #files list
    for f in os.listdir('temp'):
        if f.endswith('.png'):
            files.append(f)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    #resize with bboxes
    left,top,right,bottom = boundingBoxes()
    for f in track(files, description="Re-exporting for smaller size..."):
        im = Image.open(f'temp/{f}')
        im2 = im.crop((left,top,right,bottom))
        im2.save(f'temp/{f}')
    #duplicate images ignore
    count=0
    for f in track(files, description="Ignoring duplicates..."):
        vals=[]
        framechoice=0
        count+=1
        im = Image.open(f'temp/{f}')
        # resize head to fit the 164 width if it doesnt by rescaling the height
        bw = 164*2 if hd == 'y' else 164
        wp = (bw/float(im.size[0]))
        hs = int((float(im.size[1])*float(wp)))
        im = im.resize((bw,hs))
        for x in allimages:
            vals.append(calcdiff(im,x))
        if not 0.0 in vals:
            allimages.append(im)
            framechoice=len(allimages)-1
        else:
            valscount=0
            for x in vals:
                if x == 0.0:
                    framechoice=valscount
                valscount+=1
        if len(allimages) == 0:
            allimages.append(im)
        polishedframes[count-1]=framechoice
    #variable setup for spritesheet and json creation
    rowcount=0
    currentwidth=0
    currentheight=380
    arrayFrame=[]
    count=len(files)
    height=(bottom-top)*(math.ceil(len(allimages)/5))
    widthadjust=164
    if hd == 'y':
        currentheight=currentheight*2
        height+=380*2
        widthadjust*=2
    else:
        height+=380
    width=widthadjust*5
    #create blank canvas
    template=Image.new('RGBA',(width,height), (255, 255, 255, 0))
    #starting of looping
    pasted_indexes={}
    for i in track(range(0,count)):
        imindex=polishedframes[i]
        if not imindex in list(pasted_indexes.keys()):
            rowcount+=1
            im = allimages[imindex]
            template.paste(im, (currentwidth,currentheight))
            val={'prop':f'{int(currentwidth)/2},{int(currentheight)/2},0,0'} if hd == 'y' else {'prop':f'{int(currentwidth)},{int(currentheight)},0,0'}
            arrayFrame.append(val)
            pasted_indexes[imindex] = val
            if rowcount%5 == 0:
                currentheight+=bottom-top
                currentwidth=0
            else:
                currentwidth+=widthadjust
        else:
            arrayFrame.append(pasted_indexes[imindex])
    #setup export folder
    if not os.path.exists(f'output/{name}'):
        os.makedirs(f'output/{name}') 
    #export spritesheets
    templatesavepath = f'output/{name}/'+('anime-hd.png' if hd == 'y' else 'anime.png')
    template.save(templatesavepath)
    if hd == 'y':
        tw,th=template.size
        nonhd=template.resize((int(tw/2),int(th/2)))
        nonhd.save(f'output/{name}/anime.png')
    #export json
    data={
        'animeName':name,
        'percentageMax':'0.2',
        'totalFrame':count,
        'width':164,
        'height':380,
        'headHeight':bottom-top,
        'arrayFrame':arrayFrame
    }
    f=open(f'output/{name}/anime.json','w')
    json.dump(data,f,indent=6)
    f.close()
    #remove temp dir
    if os.path.exists('temp'):
        shutil.rmtree('temp')