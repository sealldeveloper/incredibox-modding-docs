from PIL import Image, ImageDraw, ImageFont
import math,os,json,sys
iconcount=int(input('Amount of Icons: '))
template=Image.new('RGBA',(iconcount*130-10,152), (255, 255, 255, 0))
draw=ImageDraw.Draw(template)
for i in range(0,iconcount):
        draw.rectangle((i*130,0,(i+1)*130-10,120), fill=(255,0,0))
        draw.text((i*130,0),f"Icon {i+1}",fill=(0,0,0))
        draw.rectangle((i*130,126,(i+1)*130-10,152), fill=(0,255,0))
        draw.text((i*130,126),f"Text {i+1}",fill=(0,0,0))
template.save(f'icons_template.png')