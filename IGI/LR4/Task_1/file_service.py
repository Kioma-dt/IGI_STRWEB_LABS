from product import Product
import csv
import pickle
import re
from abc import ABC, abstractmethod

class FileService(ABC):
    """Abstract Class That Works with Files."""
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def save(products: list[Product]) -> None:
        """Abstract Method To Save To File"""
        pass

    @abstractmethod
    def load() -> list[Product]:
        """Abstract Method To Load From File"""
        pass
    

class CsvService(FileService):
    """Class That Works with CSV Files."""
    def __init__(self, filename):
        super().__init__(filename)


    def save(self, products : list[Product]) -> None:
        """Saving Products Info to CSV File.
        
        Args:
            products: List with Products

        Raises:
            IOError: File Saving Problems
        """
        try:
            if not re.search(r"\.csv$", self.filename):
                self.filename += '.csv'

            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "ExportCountry", "Amount"])
                for product in products:
                    writer.writerow(product.to_list())
        except IOError as ex:
            raise IOError(f"CSV File Write Error: {ex}")
        
    def load(self) -> list[Product]:
        """Loading Products from CSV File.
        
        Args:
            filename: Name of Loading File

        Returns:
            list: Loaded Products

        Raises:
            IOError: File Loading Problems"""
        products = []
        try:
            if not re.search(r"\.csv$", self.filename):
                self.filename += '.csv'

            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append(Product(row["Name"], row["ExportCountry"], int(row["Amount"])))

                return products
                
        except IOError as ex:
            raise IOError(f"CSV File Read Error: {ex}")
        

class PickleService(FileService):
    """Class That Works with Pickle Serialization."""

    def save(self, products : list[Product]) -> None:
        """Saving Products Info to File Using Pickle.
        
        Args:
            products: List with Products

        Raises:
            IOError: File Saving Problems
        """
        if not re.search(r"\.(pkl|pickle)$", self.filename):
                self.filename += '.pkl'
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(products, file)
        except IOError as ex:
            raise IOError(f"Pickle File Write Error: {ex}")

        
    def load(self) -> list[Product]:
        """Loading Products from File Using Pickle.
        Returns:
            list: Loaded Products

        Raises:
            IOError: File Loading Problems"""
        if not re.search(r"\.(pkl|pickle)$", self.filename):
                self.filename += '.pkl'
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except IOError as ex:
            raise IOError(f"Pickle File Read Error: {ex}")