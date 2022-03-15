from functools import partial
from multiprocessing import Manager, Pool
from shutil import rmtree
from os import mkdir, listdir, rmdir
from os.path import isdir, abspath, join
from sys import argv
from resize import crawler, resizeWorker
from archive_7z import makeCompList, zipWorker


if __name__ == '__main__':

    originDir = ''
    resizedDestDir = abspath('temp')
    compressedDestDir = ''

        if len(argv) < 2:
            print('Wrong origin argument!')
            print('Wrong destination argument!')
            exit(1)
        elif len(argv) < 3:
            print('Wrong destination argument!')
            exit(1)
        if argv[1] != '':
            originDir = abspath(argv[1])
        if argv[2] != '':
            compressedDestDir = abspath(argv[2])

    if isdir(resizedDestDir) is False:
        mkdir(resizedDestDir)
    if isdir(compressedDestDir) is False:
        mkdir(compressedDestDir)

    waitingFiles = crawler(originDir)

    m = Manager()
    counter = m.list([0])

    worker_counter = partial(resizeWorker, resizedDestDir, counter, len(waitingFiles))

    print('전체 파일 개수: ' + str(len(waitingFiles)))
    with Pool(processes=12) as pool:
        pool.map(func=worker_counter, iterable=waitingFiles)

    temp = makeCompList(resizedDestDir)
    CompDirList = temp['dirList']
    CompFileList = temp['fileList']

    if argv[1] == 'true' or (len(argv) == 4 and argv[3] == 'true'):
        workerComp = partial(zipWorker, compressedDestDir, True)
    else:
        workerComp = partial(zipWorker, compressedDestDir, False)

    print('다음 파일들이 압축될 것입니다. ')
    print('폴더 : ', len(CompDirList), '개')
    print('기타 파일 : ', len(CompFileList), '개')

    with Pool(processes=12) as pool:
        pool.map(func=workerComp, iterable=CompDirList)

    rmtree(resizedDestDir)

    for file in listdir(originDir):
        try:
            rmdir(join(originDir, file))
        except Exception as e:
            print("Cannot delete original folder named as ", file)
            print(e)
