"""
Program to work with regexes
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 15-04-2026
"""

from string_service import Analyzer
from file_service import FileService
import user_input
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

            print("Input Text File Name: ")
            text_filename = input()

            text = FileService.read(text_filename)
            print("Text Read Successfully!")
            print(text)
            print()

            analyzer = Analyzer(text)
            print("\nResult:")
            print(analyzer)
            print()

            print("Input Output File Name: ")
            output_filename = input()
            FileService.write(output_filename, analyzer.__str__())
            print("Result Write Successfully!")

            print("Input Zip File Name: ")
            zip_filename = input()

            FileService.zip_file(zip_filename, output_filename)
            print("Result Zipped Successfully!")
            print()

            print("Zip Info: ")
            print(FileService.zipped_file_info(zip_filename, output_filename))

        except IOError as e:
            print(f"Input Output Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not user_input.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break
        

# If module is executing run it
if __name__ == "__main__":
    menu()