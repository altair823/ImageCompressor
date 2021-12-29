import subprocess
from os import listdir, chdir
from os.path import basename, abspath, join, isdir, isfile
from shutil import rmtree, copytree

archivePath = 'C:\\Users\\rlaxo\\Desktop\\hitomiArchive'


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


def zipWorker(targetPath, archiving, origin):
    dirName = basename(origin)
    if isfile(join(targetPath, dirName) + '.7z') is True:
        print('같은 이름의 압축파일이 존재합니다!')
        return
    subprocess.call(['7z', 'a', '-mx=9', '-t7z', join(targetPath, dirName) + '.7z', origin])
    try:
        if archiving is True:
            copytree(origin, join(archivePath, dirName))
            print('Move the data to archive folder.')
    except Exception as why:
        print('같은 이름의 파일이 저장소에 존재합니다! error: ', why)
    else:
        rmtree(origin)
