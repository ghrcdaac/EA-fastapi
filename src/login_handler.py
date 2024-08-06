import earthaccess as ea
from dotenv import load_dotenv

def login_handler():
    # For .netrc to load environment variables from .env file
    load_dotenv()
    auth = ea.login(strategy="environment", persist=True)

    # Check if the authentication is an instance of ea.Auth and if it's authenticated
    if isinstance(auth, ea.Auth) and auth.authenticated:   
        print("Login successful")
    else:
        raise Exception("Login failed. Check if valid credentials are provided")
