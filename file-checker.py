import os
import hashlib
import csv
import time
import datetime
import shutil

def SHAeur(path, rename):
    result = []
    if(os.path.isdir(path)):
        arrayToDo = []
        elements = os.listdir(path)
        #print(elements)
        for oneElement in elements:
            newPath = path+oneElement
            print(newPath)
            if os.path.isdir(newPath):
                arrayToDo.append(newPath + '/')
            else:
                if checkIfImg(newPath):
                    pass
                try:
                    nameOfFile = os.path.basename(newPath)
                    dateOfFile = os.path.getctime(newPath)
                    dateOfFile = str(datetime.datetime.fromtimestamp(dateOfFile)).replace(' ', '_')
                    dateOfFileModify = os.path.getmtime(newPath)
                    dateOfFileModify = str(datetime.datetime.fromtimestamp(dateOfFileModify)).replace(' ', '_')
                    nameGood, nameError = correctName(nameOfFile, dateOfFile) 
                    if not nameGood:
                        if rename :
                            newPath = changeName(nameError, newPath, nameOfFile, dateOfFile)
                    shaOfFile = SHAmulti(newPath)
                    result.append([newPath, nameOfFile,  dateOfFile, dateOfFileModify, shaOfFile])
                except Exception as e:
                    print(e.__class__.__name__)
                    print(e)
        for oneDirectory in arrayToDo:
            newTab = SHAeur(oneDirectory, rename)
            for miniTab in newTab:
                result.append(miniTab)
        return result
    else:
        try:
            shaOfFile = SHAmulti(path)
            nameOfFile = os.path.basename(path)
            dateOfFile = os.path.getctime(path)  
            dateOfFile = str(datetime.datetime.fromtimestamp(dateOfFile)).replace(' ', '_')
            dateOfFileModify = os.path.getmtime(path)
            dateOfFileModify = str(datetime.datetime.fromtimestamp(dateOfFileModify)).replace(' ', '_')
            result.append([path, nameOfFile,  dateOfFile, dateOfFileModify, shaOfFile])
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
        return result

def checkIfImg(path):
    extension = os.path.splitext(path)[1]
    extension = extension.lower()
    extensionPhotos = ['.png', '.raw', '.jpg', '.gif', '.svg']
    for oneExtension in extensionPhotos:
        if oneExtension == extension:
            return True

def SHAsimple(newPath):
    f = open(newPath, 'rb')
    allBytes = f.read()
    hashage = hashlib.sha256(allBytes)
    readable_hash = hashage.hexdigest()
    return readable_hash

def SHAmulti(newPath):
    f = open(newPath, 'rb')
    hasheur = hashlib.sha256()
    for byte_block in iter(lambda: f.read(4096),b""):
        hasheur.update(byte_block)
    return hasheur.hexdigest()

def readFile(nameOfFile):
    #"C:\\Users\\Nextsourcia\\Desktop\\github\\tests\\python\\test.txt"
    file = open(nameOfFile, "r")
    fileRead = csv.reader(file, delimiter='#')
    for row in fileRead:
        print(row)
    file.close()

def writeFile(nameOfFile, tabToWrite):
    #"C:\\Users\\Nextsourcia\\Desktop\\github\\tests\\python\\test.txt"
    file = open(nameOfFile, "a", newline="", encoding='utf-8')
    fileWrite = csv.writer(file, delimiter='#')
    double = []
    for row in tabToWrite:
        if row[4] not in allHash:
            fileWrite.writerow(row)
            allHash.append(row[4])
        else :
            double.append(row)
    file.close()
    return double

def getAllHash(nameOfFile):
    file = open(nameOfFile, "r")
    fileRead = csv.reader(file, delimiter='#')
    allHash = []
    for row in fileRead:
        allHash.append(row[4])
    file.close()
    return allHash

def checkHash(allHash, hashFile):
    if hashFile in allHash:
        return True
    else:
        return False

def checkIfInFile(nameOfFile, hashFile):
    file = open(nameOfFile, "r")
    fileRead = csv.reader(file, delimiter='#')
    for row in fileRead:
        if hashFile in row[4] :
            file.close()
            return True
    file.close()
    return False

def correctName(nameOfFile, dateOfFile):
    try:
        partOfTheName = nameOfFile.split('_')
        date = partOfTheName[0].split('-')
        if len(date) == 3:
            dateName = partOfTheName[0].split('-')
            partDateOfFile = dateOfFile.split('_')[0].split('-')
            if dateCoherent([dateName[0], dateName[1], dateName[2]], [partDateOfFile[0], partDateOfFile[1], partDateOfFile[2]]):
                return True
            else:
                return False, 'badDate'   
        else:
            return  False, 'noDateInName'
    except Exception as e:
        return False, 'badName'

def dateCoherent(dateNameOfFile, dateOfFile):
    if int(dateNameOfFile[0]) > int(dateOfFile[0]):
        return False
    else:
        if int(dateNameOfFile[1]) > int(dateOfFile[1]) :
            return False
        else :
            if int(dateNameOfFile[2]) > int(dateOfFile[2]):
                return False
            else :
                return True

def changeName(nameError, pathToFile, nameOfFile, dateOfFile):
    nameOfDirectory = pathToFile.replace(nameOfFile, '')
    dateOfFile = dateOfFile.split('_')[0].split('-')
    if nameError == 'badDate':
        #TODO change the date in name
        goodNameOfFile = 'caca'
    elif nameError == 'noDateInName':
        #TODO get the name And add Name
        goodNameOfFile = dateOfFile[0] + '-' + dateOfFile[1] + '-' + dateOfFile[2] + '_'
    elif nameError == 'badName':
        #TODO change the name
        #date + name + extension
        rawNameOfFile = '_'.join(nameOfFile.split('_')[1:])
        goodNameOfFile = dateOfFile[0] + '-' + dateOfFile[1] + '-' + dateOfFile[2] + '_'
    newPathToFile = nameOfDirectory + goodNameOfFile
    #os.rename(pathToFile, newPathToFile)
    #return newPathToFile
    return pathToFile

def displayIndex():
    count = 0
    for nb in allChoice :
        print(nb + '->' + textChoice[count])
        count = count + 1

def yesORno():
    print('1->Yes')
    print('2->No')
    choix = input()
    while choix != '1' and choix != '2':
        print('1->Yes')
        print('2->No')
        choix = input()
    if choix == '1':
        return True
    else :
        return False

def choice(index, text):
    count = 0
    for oneIndex in index:
        print(oneIndex + '->' + text[count])
        count = count + 1
    notCorrect = True
    choix = input()
    while notCorrect :
        for oneIndex in index:
            if oneIndex == choix :
                notCorrect = False
                break
        if notCorrect:
            count = 0
            for oneIndex in index:
                print(oneIndex + '->' + text[count])
                count = count + 1
            choix = input()
    return choix

def createIndex(dataFile, rename):
    global allHash
    tabToSave = SHAeur(pathToCheck, rename)
    doublons = writeFile(dataFile, tabToSave)
    for doublon in doublons:
        print(doublon)
    allHash = getAllHash(dataFile)

def allFileExist(pathToDataFile):
    result = []
    badHash =[]
    file = open(pathToDataFile, "r")
    fileRead = csv.reader(file, delimiter='#')
    for row in fileRead:
        if os.path.exists(row[0]) :
            if SHAmulti(row[0]) == row[4]:
                continue
            else :
                badHash.append([row])
        else:
            #result.append([row[0], row[1], row[2], row[3], row[4]])
            result.append([row])
    file.close()
    if len(result) == 0 and len(badHash) == 0 :
        return True, True
    else :
        return result, badHash


def getter(pathToDataFile, options):
    dataFile = open(pathToDataFile, "r")
    fileRead = csv.reader(dataFile, delimiter='#')
    if options[0] != '':
        parmas = [0]
        search = options[0]
    elif options[1] != '':
        parmas = [1]
        search = options[1]
    elif options[2] != '':
        parmas = [2, 3]
        search = options[2]
    elif options[3] != '':
        parmas = [4]
        search = options[3]
    res = []
    for row in fileRead:
        for param in parmas:
            if row[param] == search:
                res.append(row)
    dataFile.close()
    return res



allChoice = ['1', '2', '3', '4', '5', '6', '7', '42']
textChoice = ['Check if a file is in the index', 'Create Directory index', 'Check the index' , 'Use the getter', 'Add files', 'Change working directory', 'Change index file', 'Leave']
stop = False
dataFile = "C:\\Users\\Nextsourcia\\Desktop\\github\\tests\\python\\test.txt"
pathToCheck = "C:/Users/Nextsourcia/Desktop/DCIM/"
while not stop:
    print('--------------------')
    print('<-- Working directory : "' + pathToCheck + '" -->')
    print('<-- Index file : "' + dataFile + '" -->')
    choix = choice(allChoice, textChoice)
    global allHash
    if os.path.exists(dataFile) :
        allHash = getAllHash(dataFile)
        if len(allHash) == 0:
            print('not access to the dataFile')
            print('Do you want to generate it ?')
            if yesORno():
                createIndex(dataFile, pathToCheck, False)
            else :
                print('Index not generated')
    else :
        print('not access to the dataFile')
        print('Do you want to generate it ?')
        if yesORno():
            createIndex(dataFile, pathToCheck, False)
        else :
            print('Index not generated')
    if choix == '1':
        choixUser = choice(['1', '2'], ['Use a hash', 'Select a file'])
        if choixUser == '1':
            hashToCheck = input('Enter the Hash\n')
            hashToCheck = '8af932a8866c771f694fa1r5fb36a052cf663843339de305b236a7cbf0f12139'
            inDir = checkHash(allHash, hashToCheck)
            print(hashToCheck + ' is in dir ? -> ' + str(inDir))
        elif choixUser == '2':
            fileToCheck = input('Enter the path to the file\n')
            while not os.path.exists(fileToCheck) :
                fileToCheck = input('Enter the path to the file\n')
            hashToCheck = SHAmulti(fileToCheck)
            inDir = checkHash(allHash, hashToCheck)
            print(hashToCheck + ' is in dir ? -> ' + str(inDir))
    elif choix == '2':
        createIndex(dataFile, pathToCheck, True)
    elif choix == '3':
        res, badHash = allFileExist(dataFile)
        if res == True:
            print('-->> all Files are Correct')
        else:
            print(str(len(res)) + ' files are not found')
            for oneFile in res:
                print(oneFile)
            print(str(len(badHash)) + ' files hash are not correct')
            for oneFile in badHash:
                print(oneFile)
    elif choix == '4':
        listOfFiles = getter(dataFile, ['', '', '', '42c67427a5cf2bb564899ddc77aaa97094ff4111a660a9c5dcbb00a5d59f8d88'])
        for oneFile in listOfFiles:
            print(oneFile)
    elif choix == '5':
        dirToAdd = input('Put the name of the directory\n')
        while not os.path.exists(dirToAdd) :
            dirToAdd = input("Put the name of the directory\n")
        choixUser = choice(['1', '2'], ['Déplacer', 'Copier'])
        if choixUser == '1':
            print('Déplacement')
            shutil.move(dirToAdd, pathToCheck, copy_function = shutil.copytree)
        else :
            print('Copie')
            nameOfDir = os.path.basename(dirToAdd)
            shutil.copytree(dirToAdd, pathToCheck + nameOfDir)
    elif choix == '6':
        newPathDir = input('Put the name of the directory\n')
        while not os.path.exists(newPathDir) :
            newPathDir = input("Put the name of the directory\n")
        pathToCheck = newPathDir
    elif choix == '7':
        newPathData = input('Put the name of the new file index\n')
        while not os.path.exists(newPathData) :
            newPathData = input("Put the name of the new file index\n")
        dataFile = newPathData
    elif choix == '42':
        stop = True
        print('exited')
    









