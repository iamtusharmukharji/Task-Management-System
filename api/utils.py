
import json

# modular class for loading required credentials from credentials.json file
class CredentialLoader():
    def __init__(self):

        credential_file = "api/credentials/credentials.json"

        with open(credential_file, "r") as creds_file:
            credentials = json.load(creds_file)
        
        # storing database credentials
        self.database = credentials['database']
        

creds = CredentialLoader()
        