from product import Product
import csv
import pickle
import re

class CsvService:
    """Class That Works with CSV Files."""
    @staticmethod
    def save(products : list[Product], filename : str) -> None:
        """Saving Products Info to CSV File.
        
        Args:
            products: List with Products
            filename: Name of Saving File

        Raises:
            IOError: File Saving Problems
        """
        try:
            if not re.search(r"\.csv$", filename):
                filename += '.csv'

            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "ExportCountry", "Amount"])
                for product in products:
                    writer.writerow(product.to_list())
        except IOError as ex:
            raise IOError(f"CSV File Write Error: {ex}")
        
    @staticmethod
    def load(filename : str) -> list[Product]:
        """Loading Products from CSV File.
        
        Args:
            filename: Name of Loading File

        Returns:
            list: Loaded Products

        Raises:
            IOError: File Loading Problems"""
        products = []
        try:
            if not re.search(r"\.csv$", filename):
                filename += '.csv'

            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append(Product(row["Name"], row["ExportCountry"], int(row["Amount"])))

                return products
                
        except IOError as ex:
            raise IOError(f"CSV File Read Error: {ex}")
        

class PickleService:
    """Class That Works with Pickle Serialization."""

    @staticmethod
    def save(products : list[Product], filename : str) -> None:
        """Saving Products Info to File Using Pickle.
        
        Args:
            products: List with Products
            filename: Name of Saving File

        Raises:
            IOError: File Saving Problems
        """
        if not re.search(r"\.(pkl|pickle)$", filename):
                filename += '.pkl'
        try:
            with open(filename, 'wb') as file:
                pickle.dump(products, file)
        except IOError as ex:
            raise IOError(f"Pickle File Write Error: {ex}")

        
    @staticmethod
    def load(filename : str) -> list[Product]:
        """Loading Products from File Using Pickle.
        
        Args:
            filename: Name of Loading File

        Returns:
            list: Loaded Products

        Raises:
            IOError: File Loading Problems"""
        if not re.search(r"\.(pkl|pickle)$", filename):
                filename += '.pkl'
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except IOError as ex:
            raise IOError(f"Pickle File Read Error: {ex}")