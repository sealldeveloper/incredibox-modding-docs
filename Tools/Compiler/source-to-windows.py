import os,sys,shutil
from asarPy import pack_asar
if not os.path.exists('source/'):
    print('Please move your mod source code into the \'source\' folder!')
    os.makedirs('source/')
    sys.exit()
if os.path.exists('temp/'):
    shutil.rmtree('temp/')
if os.path.exists('output/'):
    shutil.rmtree('output/')
os.makedirs('output/')
os.makedirs('temp/windows/')
print('Unpacking template...')
shutil.unpack_archive('templates/windows.zip','temp/windows/','zip')
print('Packing asar...')
pack_asar("source",'temp/app.asar')
print('Copying new asar...')
shutil.copyfile('temp/app.asar','temp/windows/app/resources/app.asar')
print('Repacking new version...')
shutil.make_archive('output/windows-packed','zip','temp/windows/')
print('Packed as \'windows-packed.zip\'! Cleaning up...')
if os.path.exists('temp/'):
    shutil.rmtree('temp/')