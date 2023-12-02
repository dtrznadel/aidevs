from dotenv import load_dotenv, find_dotenv
import os

file_path = "empty_file.txt"
os.chdir("C:/projects/aidevs_repo/aidevs/")
# Open the file in write mode ('w') to create an empty file
with open(file_path, "w") as file:
    pass  # The file is created but remains empty
