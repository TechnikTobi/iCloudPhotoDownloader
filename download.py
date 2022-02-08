from lib2to3.pytree import convert
import os
import pyicloud_ipd
from datetime import datetime, timezone

"""
Lists to store iCloud object identifiers for different use cases
"""
allImageIDs = []
downloadedImages = []
failedImages = []

"""
Methods for reading and creating the CSV of all identfiers in iCloud
"""
def _readAllCSV(apiObject):
    if not os.path.isfile("allImageIDs.csv"):
        _createAllCSV(apiObject)

    with open("allImageIDs.csv", "r") as allFile:
        for line in allFile:
            allImageIDs.append(line.replace("\n", ""))
    
def _createAllCSV(apiObject):
    with open("allImageIDs.csv", "w") as allFile:
        for photo in apiObject.photos.all:
            allFile.write(photo.id + "\n")




"""
Methods for reading and writing the CSV containing the identifiers of images that 
were successfully downloaded
"""
def _readDownloadedCSV():
    if not os.path.isfile("downloadedImageIDs.csv"):
        open("downloadedImageIDs.csv", "a").close()
    
    with open("downloadedImageIDs.csv", "r") as downloadedFile:
        for line in downloadedFile:
            downloadedImages.append(line.replace("\n", ""))

def _writeDownloadedCSV():
    if not os.path.isfile("downloadedImageIDs.csv"):
        open("downloadedImageIDs.csv", "a").close()
    
    with open("downloadedImageIDs.csv", "w") as downloadedFile:
        for id in downloadedImages:
            downloadedFile.write(id + "\n")



"""
Methods for reading and writing the CSV containing the identifiers of images that 
could not be downloaded for now
"""
def _readFailedCSV():
    if not os.path.isfile("failedImageIDs.csv"):
        open("failedImageIDs.csv", "a").close()
    
    with open("failedImageIDs.csv", "r") as failedFile:
        for line in failedFile:
            failedImages.append(line.replace("\n", ""))

def _writeFailedCSV():
    if not os.path.isfile("failedImageIDs.csv"):
        open("failedImageIDs.csv", "a").close()
    
    with open("failedImageIDs.csv", "w") as failedFile:
        for id in failedImages:
            failedFile.write(id + "\n")



"""
Simply downloads a photo and stores it on disk with a new name
"""
def _simpleDownload(photo):

    assetDate = photo.asset_date

    # For adjusting the timezone from UTC to local
    # Not sure if this is a good idea though...
    # assetDate = assetDate.replace(tzinfo=timezone.utc).astimezone(tz=None)

    newFileName = str(assetDate.year)
    newFileName = newFileName + "-" + str(assetDate.strftime("%m"))
    newFileName = newFileName + "-" + str(assetDate.strftime("%d"))
    newFileName = newFileName + " " + str(assetDate.strftime("%H"))
    newFileName = newFileName + "-" + str(assetDate.strftime("%M"))
    newFileName = newFileName + "-" + str(assetDate.strftime("%S"))
    newFileName = newFileName + "-" + str(assetDate.strftime("%f"))
    newFileName = newFileName + "." + photo.filename.rsplit(".", 1)[-1]

    success = False

    # Try to download the image and store it under the newly created file name
    try:
        photoDownload = photo.download()
        with open(newFileName, "wb") as photoFile:
            photoFile.write(photoDownload.raw.read())
            success = True
    except Exception as e:
        print("Oh no! Something bad happend while downloading the image with name '" + photo.filename + "' (id: " + photo.id + ")")
        print(e)
        print("I will add the ID of this object to another list to try out later!")
        failedImages.append(photo.id)
        _writeFailedCSV()
    finally:
        return success



"""
Downloads all objects from iCloud photo that are
- in the list 'allImageIDs'
- NOT in the list 'downloadedImages'
"""
def downloadAll(apiObject):

    try:
        os.mkdir("data")
    except FileExistsError as e:
        pass

    os.chdir("data/")
    if allImageIDs == []:
        _readAllCSV(apiObject)
        _readDownloadedCSV()
        _readFailedCSV()

    for photo in apiObject.photos.all:
        if str(photo.id) in allImageIDs and photo.id not in downloadedImages:
            print("Trying to download image with name '" + photo.filename + "' (id: " + photo.id + ")")

            downloadSuccess = _simpleDownload(photo)
            
            # In case the download was successful, store the ID as 'downloaded'
            if downloadSuccess:
                print("Success!")

                downloadedImages.append(photo.id)
                _writeDownloadedCSV()
                
    _writeDownloadedCSV()
    _writeFailedCSV()
    os.chdir("..")