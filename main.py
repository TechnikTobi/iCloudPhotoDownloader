from authentication import getAPIobject
from download import downloadAll

if __name__ == "__main__":
    apiObject = getAPIobject(False)
    downloadAll(apiObject)