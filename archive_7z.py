import subprocess
from os import listdir, chdir
from os.path import basename, abspath, join, isdir, isfile
from shutil import rmtree

pathOf7z = 'C:\\Program Files\\7-Zip'

def makeCompList(root):
    abRoot = abspath(root)
    toCompDirList = []
    toCompFileList = []
    for fileName in listdir(abRoot):
        abFileName = join(abRoot, fileName)
        if isdir(abFileName):
            toCompDirList.append(abFileName)
        else:
            toCompFileList.append(abFileName)

    return {'dirList': toCompDirList, 'fileList': toCompFileList}


def zipWorker(targetPath, origin):
    dirName = basename(origin)
    if isfile(join(targetPath, dirName) + '.7z') is True:
        print('같은 이름의 압축파일이 존재합니다!')
        return
    chdir(pathOf7z)
    subprocess.call(['7z.exe', 'a', join(targetPath, dirName) + '.7z', origin])
    rmtree(origin)
