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
os.makedirs('temp/android/')
print('Unpacking app...')
shutil.unpack_archive('app.zip','temp/windows/','zip')
print('Unpacking asar...')
extract_asar('temp/windows/app/resources/app.asar','temp/asar/')
print('Unpacking template...')
shutil.unpack_archive('templates/android.zip','temp/android/','zip')
print('Organising new apk folder...')
for f in os.listdir('temp/asar/app/'):
    if os.path.isfile(f'temp/asar/app/{f}'):
        shutil.copyfile(f'temp/asar/app/{f}',f'temp/android/assets/www/{f}')
    elif os.path.isdir(f'temp/asar/app/{f}'):
        copy_tree(f'temp/asar/app/{f}',f'temp/android/assets/www/{f}')
print('Repacking new version...')
shutil.make_archive('output/windows-to-apk-packed','zip','temp/android/')
os.rename('output/windows-to-apk-packed.zip','output/windows-to-apk-packed.apk')
print('Packed as \'windows-to-apk-packed.apk\'! Cleaning up...')
if os.path.exists('temp/'):
    shutil.rmtree('temp/')