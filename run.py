from libs.Gyawn import Gyawn
from dotenv import load_dotenv
import os
load_dotenv()

Gyawn= Gyawn()

def main():
    tkn= os.getenv("tkn")

    Gyawn.run(tkn, log_level=0)
