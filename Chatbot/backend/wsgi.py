# from backend import app

# import sys
# import os

# # Add the parent directory of 'backend' to the system path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app import app  

if __name__ == "__main__":
    app.run()