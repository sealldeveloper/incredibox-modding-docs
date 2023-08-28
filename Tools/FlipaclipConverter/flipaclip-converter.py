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

if __name__ == "__main__":
    print(Panel("[orange_red1]Flipaclip to Polo\n[dodger_blue1]by [salmon1]sealldeveloper", title="[green1]Welcome![bright_white]"))
    if os.path.exists('.temp.py'):
        os.remove('.temp.py')
    try:
        print('Checking for updates...')
        h1 = hashlib.sha256()
        with open('flipaclip-converter.py','rb') as f:
            data=f.read()
            h1.update(data)
        h2 = hashlib.sha256()
        r = requests.get('https://raw.githubusercontent.com/sealldeveloper/incredibox-modding-docs/main/Tools/FlipaclipConverter/flipaclip-converter.py')
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
    if not os.path.exists('input'):
        os.makedirs('input')
        print('[bright_red]ERROR: Please put your files in the \'input\' folder!')
        sys.exit()
    if not os.path.exists('input/files.zip'):
        print('[bright_red]ERROR: File \'files.zip\' does not exist in the input folder!')
        sys.exit()
    hd = Prompt.ask('HD?',choices=['y','n'])
    name=Prompt.ask('Name')
    
    files=[]
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.makedirs('temp')
    shutil.unpack_archive('input/files.zip','temp/','zip')
    for f in os.listdir('temp'):
        if f.endswith('.png'):
            files.append(f)
    allimages=[]
    frames=[]
    polishedframes={}
    count = 0
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    for f in track(files, description="Ignoring duplicates..."):
        vals=[]
        framechoice=0
        count+=1
        im = Image.open(f'temp/{f}')
        bw = 164
        if hd == 'y':
            bw=bw*2
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
    rowcount=0
    currentheight=380
    currentwidth=0
    arrayFrame=[]
    count=len(files)
    height=380*(math.ceil(len(allimages)/5)+1)
    width=164*5
    if hd == 'y':
        height=height*2
        currentheight=currentheight*2
        width=width*2
    
    template=Image.new('RGBA',(width,height), (255, 255, 255, 0))

    pasted_indexes={}
    for i in track(range(0,count)):
        imindex=polishedframes[i]
        if not imindex in list(pasted_indexes.keys()):
            rowcount+=1
            im = allimages[imindex]
            template.paste(im, (currentwidth,currentheight))
            arrayFrame.append({'prop':f'{int(currentwidth)/2},{int(currentheight)/2},0,0'})
            pasted_indexes[imindex] = {'prop':f'{int(currentwidth)/2},{int(currentheight)/2},0,0'}
            if rowcount%5 == 0:
                if hd == 'y':
                    currentheight+=380*2
                else:
                    currentheight+=380
                currentwidth=0
            else:
                if hd == 'y':
                    currentwidth+=164*2
                else:
                    currentwidth+=164
        else:
            arrayFrame.append(pasted_indexes[imindex])
    if not os.path.exists(f'output/{name}'):
        os.makedirs(f'output/{name}') 
    if hd == 'y':
        template.save(f'output/{name}/anime-hd.png')
    else:
        template.save(f'output/{name}/anime.png')
    data={}
    data['animeName']=name
    data['percentageMax']=str(0.2)
    data['totalFrame']=count
    data['width']=164
    data['height']=380
    data['headHeight']=380
    data['arrayFrame']=arrayFrame
    if hd == 'y':
        f=open(f'output/{name}/anime-hd.json','w')
        json.dump(data,f,indent=6)
        f.close()
    else:
        f=open(f'output/{name}/anime.json','w')
        json.dump(data,f,indent=6)
        f.close()
    if os.path.exists('temp'):
        shutil.rmtree('temp')