import os,sys,shutil
from asarPy import extract_asar
from distutils.dir_util import copy_tree
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
if not os.path.exists('app.zip'):
    print('Please move your mod zip in the folder and name it \'app.zip\'!')
    sys.exit()
if os.path.exists('temp/'):
    shutil.rmtree('temp/')
if os.path.exists('output/'):
    shutil.rmtree('output/')
os.makedirs('output/')
os.makedirs('temp/windows/')
print('Unpacking app...')
shutil.unpack_archive('app.zip','temp/windows/','zip')
print('Unpacking asar...')
extract_asar('temp/windows/app/resources/app.asar','temp/source/')
print('Packing source...')
shutil.make_archive('output/windows-to-source-packed','zip','temp/source/')
print('Packed as \'windows-to-source-packed.apk\'! Cleaning up...')
if os.path.exists('temp/'):
    shutil.rmtree('temp/')