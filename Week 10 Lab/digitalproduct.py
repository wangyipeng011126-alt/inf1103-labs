from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                stock: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"  Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data