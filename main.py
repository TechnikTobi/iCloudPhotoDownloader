import os

"""
Tries to read the credentials (email & password)
If the expected file could not be found, it gets created and an exception is raised
"""
def readCredentials():

    if not os.path.isfile("credentials.txt"):
        with open("credentials.txt", "w") as credentialsFile:
            credentialsFile.write("email\n")
            credentialsFile.write("password")
        raise RuntimeError("Could not find 'credentials.txt' with email and password")

    with open("credentials.txt", "r") as credentialsFile:
        email = credentialsFile.readline().replace("\n", "")
        password = credentialsFile.readline().replace("\n", "")
    return (email, password)

if __name__ == "__main__":
    print("hello")
    print(readCredentials())