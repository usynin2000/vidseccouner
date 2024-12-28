import os
from dotenv import load_dotenv

load_dotenv()

# got from MetaMask
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# got as API_KEY in https://developer.metamask.io/
INFURA_API_KEY = os.getenv('INFURA_API_KEY')
