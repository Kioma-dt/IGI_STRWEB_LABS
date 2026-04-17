"""
Program to work with regexes
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 15-04-2026
"""

from string_service import Analyzer
from file_service import ZipFileService
from user_input import FilesUserInput
from os import system

def menu() -> None:
    """
    Menu for Task_2
    """
    
    while True:
        try:
            system("clear")

            print("Program to work with regexes")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 15-04-2026")
            print()

            input_filename = FilesUserInput.get_file_name("Input Input File Name: ", "txt")

            output_filename = FilesUserInput.get_file_name("Input Output File Name: ", "txt")
            
            zip_filename = FilesUserInput.get_file_name("Input Zip File Name: ", "zip")

            file_service = ZipFileService(input_filename, output_filename, zip_filename)

            text = file_service.read()
            print("Text Read Successfully!")
            print(text)
            print()

            analyzer = Analyzer(text)
            print("\nResult:")
            print(analyzer)
            print()

            file_service.write(analyzer.__str__())
            print("Result Write Successfully!")


            file_service.zip_file()
            print("Result Zipped Successfully!")
            print()

            print("Zip Info: ")
            print(file_service.zipped_file_info())

        except IOError as e:
            print(f"Input Output Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not FilesUserInput.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break
        

# If module is executing run it
if __name__ == "__main__":
    menu()