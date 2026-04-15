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