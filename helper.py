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
            # Get path, remove ' and "
            newWorkingPath = click.prompt("Choose Working Directory").replace("'", "").replace('"', '')

            # Remove spaces at the end of the string
            while(newWorkingPath[-1] == " "):
                newWorkingPath = newWorkingPath[:-1]

            # Check if the path actually exists
            pathExists = os.path.exists(newWorkingPath)
        except:
            pass

    return newWorkingPath
