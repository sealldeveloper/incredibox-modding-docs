from PIL import Image, ImageDraw, ImageFont
import math,os,json,sys
name=input('Name of Polo File: ')
totalframe=int(input('Total Animation Frames (can be changed later): '))
height=int(input('Height: '))
width=int(input('Width: '))
if width>164:
    print('The width cannot be greater than 164 pixels! Otherwise the body breaks')
    sys.exit()
headHeight=int(input('Head Height: '))
headscount=int(input('Head Count: '))
if os.path.exists(f'{name}_coordinates.txt'):
    os.remove(f'{name}_coordinates.txt')
if os.path.exists(f'{name}.txt'):
    os.remove(f'{name}.txt')
nearest5=5*math.ceil(headscount/5)
rows=nearest5/5
col=nearest5/rows
template=Image.new('RGBA',(int(width*col),int(height+(rows*headHeight))), (255, 255, 255, 0))
draw=ImageDraw.Draw(template)
draw.rectangle((0,0,164,height), fill=(255,0,0))
draw.text((164/2-164/10,height/2-height/20),"Default",fill=(0,0,0))
draw.rectangle((164,0,164*2,height), fill=(0,255,0))
draw.text((164+164/2-164/10,height/2-height/20),"Headless",fill=(0,0,0))
draw.rectangle((164*2,0,164*3,height), fill=(0,0,255))
draw.text((2*164+164/2-164/10,height/2-height/20),"Siloette",fill=(0,0,0))
draw.text((0,0),f"sealldeveloper's Template Generator\n{name},{totalframe},{height},{width},{headHeight},{headscount}",fill=(0,0,0))

heads=Image.new('RGBA',(int(width*col),int((rows*headHeight))), (255, 255, 255, 0))
headswidth=width*col
headsheight=rows*headHeight
draw2=ImageDraw.Draw(heads)
count=0
textcount=0
for i in range(0,int(rows)):
    for j in range(0,int(col)):
        count+=1
        textcount+=1
        if not textcount > headscount:
            if count%2 == 0:
                draw2.rectangle((j*width,i*headHeight,(j+1)*width,(i+1)*headHeight),fill=(255,255,0))
            else:
                draw2.rectangle((j*width,i*headHeight,(j+1)*width,(i+1)*headHeight),fill=(0,255,255))
            draw2.text((j*width,i*headHeight),f"Head {textcount}",fill=(0,0,0))
            with open(f'{name}_coordinates.txt','a') as f:
                f.write(f'Head {textcount} Coords: {j*width},{i*headHeight+height}\n')

template.paste(heads,(0,height),heads)
template.save(f'{name}_template.png')

arrayFrame=[]
for i in range (0,totalframe):
    arrayFrame.append({'prop':f'0,{height},0,0'})
data={}
data['animeName']=name
data['percentageMax']=str(0.2)
data['totalFrame']=str(totalframe)
data['width']=str(width)
data['height']=str(height)
data['headHeight']=str(headHeight)
data['arrayFrame']=arrayFrame
f=open(f'{name}.json','w')
json.dump(data,f,indent=6)
f.close()