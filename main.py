from authentication import getAPIobject
from download import downloadAll
from helper import getWorkingDirectory
import os 

if __name__ == "__main__":
    os.chdir(getWorkingDirectory())
    downloadAll(getAPIobject(True))