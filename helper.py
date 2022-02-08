import os
import click

"""
Asks the user to specify a directory where the program should perform its operations
"""
def getWorkingDirectory():
    newWorkingPath = None
    pathExists = False

    while(not pathExists):
        try:
            newWorkingPath = click.prompt("Working Directory").replace("'", "").replace('"', '')
            pathExists = os.path.exists(newWorkingPath)
        except:
            pass

    return newWorkingPath
