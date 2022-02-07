import os
import sys
import click
import pyicloud_ipd

"""
Tries to read the credentials (email & password)
If the expected file could not be found, it gets created and an exception is raised
"""
def readCredentials():

    # Check if the file exists. If not, create it and raise an exception
    if not os.path.isfile("credentials.txt"):
        with open("credentials.txt", "w") as credentialsFile:
            credentialsFile.write("email\n")
            credentialsFile.write("password")
        raise RuntimeError("Could not find 'credentials.txt' with email and password")

    # If found, open the file, read the data and return it
    with open("credentials.txt", "r") as credentialsFile:
        email = credentialsFile.readline().replace("\n", "")
        password = credentialsFile.readline().replace("\n", "")
    return (email, password)



"""
Uses an email and password to authenticate access
If two step authentication is needed for the account, the function for this case
gets called
"""
def authenticate(email, password):

    # Get an object to access the icloud api
    try:
        apiObject = pyicloud_ipd.PyiCloudService(
            email,
            password
        )

    # Something went wrong with authentication
    except Exception as exception:
        print("Oh no! The following exception occured!")
        print(exception)
        sys.exit(1)

    # In case 2SA is required...
    if apiObject.requires_2sa:
        twoStepAuthentication(apiObject)



"""
Method in case two factor authentication is needed
Based on the documentation from:
https://github.com/icloud-photos-downloader/pyicloud/tree/pyicloud-ipd
"""
def twoStepAuthentication(apiObject):
    print("Two step authentication needed!")

    trustedDevices = apiObject.trusted_devices
    for index, device in enumerate(trustedDevices):
        print("  %s: %s" % (index, device.get('deviceName', "SMS to %s" % device.get('phoneNumber'))))

    selectedDevice = click.prompt("Select a device for two step authentication!")
    selectedDevice = trustedDevices[int(selectedDevice)]

    if not apiObject.send_verification_code(selectedDevice):
        print("Could not send verification code!")
        sys.exit(1)
    
    verificationCode = click.prompt("Please enter the verification code!")
    if not apiObject.validate_verification_code(selectedDevice, verificationCode):
        print("Could not verify code!")
        sys.exit(1)
    


if __name__ == "__main__":
    print("hello")
    
    authenticate(
        readCredentials()[0],
        readCredentials()[1]
    )