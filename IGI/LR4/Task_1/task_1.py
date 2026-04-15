"""
Program to work with files
Lab Work 4
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 15-04-2026
"""

import user_input
from product import Product
import file_service
from os import system

def get_product_info(products : list[Product], product_name: str) -> tuple[list[str], int]:
    """Getting Product Info By Name.
        
        Args:
            products: List of Products
            product_name: Name of Searching Product

        Returns:
            tuple: (List of Export Countries, Total Export Amount)
    """
    countries = []
    total_amount = 0

    for product in products:
        if product.name == product_name:
            countries.append(product.export_country)
            total_amount += product.amount

    return countries, total_amount

def sort_by_amount(products : list[Product]) -> list[Product]:
    """Sorting Products By Amount.
        
        Args:
            products: List of Products

        Returns:
            list: Sorted Products
    """

    return sorted(products, key=lambda k: k.amount)


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

            print("Input Saving File Name: ")
            filename = input()
            print()

            print("Save Options: ")
            print("1. CSV")
            print("2. Pickle")

            answer = input()

            match answer:
                case "1":
                    file_service.CsvService.save(products, filename)
                case "2":
                    file_service.PickleService.save(products, filename)
                case _:
                    raise Exception("Wrong Option Format")
                
            print("Saved Successfully!\n")

            print("Input Loading File Name: ")
            filename = input()
            print()

            print("Load Options: ")
            print("1. CSV")
            print("2. Pickle")

            loaded_products = None
            answer = input()


            match answer:
                case "1":
                    loaded_products = file_service.CsvService.load(filename)
                case "2":
                    loaded_products = file_service.PickleService.load(filename)
                case _:
                    raise Exception("Wrong Option Format")
                
            print("Loaded Successfully!\n")

            if(user_input.get_yes_or_no("Would You Like to Sort by Amount? (yes / no)")):
                loaded_products = sort_by_amount(products)

            print()

            for product in loaded_products:
                print(product)

            print()

            print("Input Product Name: ")
            product_name = input()

            countries, amount = get_product_info(loaded_products, product_name)

            print("Countries: ", end='')
            print(*countries, sep=', ')
            print(f"Total Amount: {amount}")


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