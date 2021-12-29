from os import mkdir, stat, listdir, remove
from os.path import basename, dirname, isdir, join, splitext
from shutil import copy2, rmtree
from PIL import Image

Image.MAX_IMAGE_PIXELS = 933120000


def crawler(originPath):
    result = []
    if isdir(originPath) is True:
        fileNameList = listdir(originPath)
        for i in fileNameList:
            result = result + crawler(join(originPath, i))
    else:
        if basename(originPath) != '.DS_Store':
            result.append(originPath)
        else:
            pass
    return result


def resizer(fileName, dest, sizeRatio, quality):
    originFileName = fileName
    fileName = basename(originFileName)
    folderName = basename(dirname(originFileName))
    if not isdir(join(dest, folderName)):
        try:
            mkdir(join(dest, folderName))
        except FileExistsError:
            pass
    root, extension = splitext(originFileName)
    try:
        img = Image.open(originFileName)
        if extension == '.png':
            img_jpg = img.convert('RGB')
            img_jpg.resize((int(img_jpg.width * sizeRatio), int(img_jpg.height * sizeRatio)), Image.ANTIALIAS)
            img_jpg.save(join(dest, folderName, basename(root)) + '.jpg', optimize=True, quality=quality)
        else:
            img = img.resize((int(img.width * sizeRatio), int(img.height * sizeRatio)), Image.ANTIALIAS)
            img.save(join(dest, folderName, fileName), optimize=True, quality=quality)
    except Exception:
        copy2(originFileName, join(dest, folderName, fileName))


def resizeWorker(dest, counter, totalCount, fileName):
    try:
        originFileName = fileName
        fileName = basename(originFileName)
        folderName = basename(dirname(originFileName))
        root, extension = splitext(originFileName)
        fileSize = stat(originFileName).st_size
        if fileSize > 5000000:
            resizer(originFileName, dest, 0.5, 60)
        elif fileSize > 1000000:
            resizer(originFileName, dest, 0.6, 65)
        elif fileSize > 500000:
            resizer(originFileName, dest, 0.6, 70)
        elif fileSize > 300000:
            resizer(originFileName, dest, 0.7, 75)
        elif fileSize > 100000:
            resizer(originFileName, dest, 0.7, 80)
        else:
            resizer(originFileName, dest, 0.8, 85)
        counter[0] += 1
        print(str(counter[0]) + ' / ' + str(totalCount) + ' - ' + str(fileSize) + ' -> ' +
              str(stat(join(dest, folderName, basename(root)) + '.jpg').st_size) + ' - ' + fileName)
    except Exception:
        pass
    else:
        try:
            remove(originFileName)
        except Exception as e:
            print('Fail to remove original file')
            print(e)
