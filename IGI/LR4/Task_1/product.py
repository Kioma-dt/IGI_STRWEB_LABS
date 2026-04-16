class Product:
    """Class Containing Information About Product"""
    def __init__(self, name: str, export_country: str, amount: int):
        self.name = name
        self.export_country = export_country
        self.amount = amount

    def to_list(self):
        return [self.name, self.export_country, self.amount]

    def __str__(self) -> str:
        return  f"Product Name: {self.name}, Exports into Country: {self.export_country}, Amount: {self.amount}"   
    
class ProductAnalyzer:
    @staticmethod
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

    @staticmethod
    def sort_by_amount(products : list[Product]) -> list[Product]:
        """Sorting Products By Amount.
            
            Args:
                products: List of Products

            Returns:
                list: Sorted Products
        """

        return sorted(products, key=lambda k: k.amount)