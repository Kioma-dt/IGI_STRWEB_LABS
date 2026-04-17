"""
Program to work with files
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 15-04-2026
"""

from user_input import ProductUserInput
from product import Product, ProductAnalyzer
import file_service
from os import system


products = [
    Product("Wheat", "Germany", 34),
    Product("Wheat", "France", 5000),
    Product("Wheat", "Italy", 950),

    Product("Oil", "China", 800),
    Product("Oil", "India", 4200),
    Product("Oil", "USA", 1500),

    Product("Natural_Gas", "Germany", 3000),
    Product("Natural_Gas", "Poland", 12),

    Product("Cars", "USA", 1334),
    Product("Cars", "Canada", 134),
    Product("Cars", "UK", 12346)
]


def menu() -> None:
    """
    Menu for Task_1
    """
    
    while True:
        try:
            system("clear")

            print("Program to work with files")
            print("Lab Work 4")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 15-04-2026")
            print()

            file_ser = file_service.FileService
            print("Input File Name: ")
            filename = input()
            print()

            print("Save Options: ")
            print("1. CSV")
            print("2. Pickle")

            answer = input()

            match answer:
                case "1":
                    file_ser = file_service.CsvService(filename)
                case "2":
                    file_ser = file_service.PickleService(filename)
                case _:
                    raise Exception("Wrong Option Format")
                
            file_ser.save(products)
                
            print("Saved Successfully!\n")
            
            loaded_products = file_ser.load()
            print("Loaded Successfully!\n")

            if(ProductUserInput.get_yes_or_no("Would You Like to Sort by Amount? (yes / no)")):
                loaded_products = ProductAnalyzer.sort_by_amount(products)

            print()

            for product in loaded_products:
                print(product)

            print()

            product_name = ProductUserInput.get_product_name("Input Product Name: ", products)

            countries, amount = ProductAnalyzer.get_product_info(loaded_products, product_name)

            print("Countries: ", end='')
            print(*countries, sep=', ')
            print(f"Total Amount: {amount}")


        except IOError as e:
            print(f"Input Output Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if not ProductUserInput.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break
        

# If module is executing run it
if __name__ == "__main__":
    menu()