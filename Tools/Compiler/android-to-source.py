import os,sys,shutil
from asarPy import pack_asar
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
if not os.path.exists('app.apk'):
    print('Please move your mod apk in the folder and name it \'app.apk\'!')
    sys.exit()
if os.path.exists('temp/'):
    shutil.rmtree('temp/')
if os.path.exists('output/'):
    shutil.rmtree('output/')
os.makedirs('output/')
os.makedirs('temp/android/')
os.makedirs('temp/asar/')
print('Unpacking template...')
shutil.unpack_archive('templates/asar.zip','temp/asar/','zip')
os.makedirs('temp/asar/app/')
print('Unpacking app...')
shutil.unpack_archive('app.apk','temp/android/','zip')
print('Organising new folder...')
for f in os.listdir('temp/android/assets/www/'):
    if f.startswith('asset-v'):
            if os.path.isfile(f'temp/android/assets/www/{f}'):
                shutil.copyfile(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
            elif os.path.isdir(f'temp/android/assets/www/{f}'):
                copy_tree(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
    for n in names:
        if f==n:
            if os.path.isfile(f'temp/android/assets/www/{f}'):
                shutil.copyfile(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
            elif os.path.isdir(f'temp/android/assets/www/{f}'):
                copy_tree(f'temp/android/assets/www/{f}',f'temp/asar/app/{f}')
print('Packing source...')
shutil.make_archive('output/apk-to-source-packed','zip','temp/asar/')
print('Packed as \'apk-to-source-packed.zip\'! Cleaning up...')
if os.path.exists('temp/'):
    shutil.rmtree('temp/')