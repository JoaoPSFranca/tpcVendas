from model.Product import Product

class SaleItem:
    def __init__(self, idsale=0, product=None, quantity=0, value=0.0):
        self.__idsale = idsale
        self.__product = product if product else Product()
        self.__quantity = quantity
        self.__value = value
        self.__table = "item_venda"
        self.__attributes = "codvenda, codproduto, qtde, valor"
        self.__pkey = "codvenda, codproduto"

    @staticmethod
    def convert(data):
        return SaleItem(data[0], Product(data[1]), data[2], data[3])

    @property
    def dataInsert(self):
        return f"{self.idsale}, {self.product.idproduct}, {self.quantity}, {self.value}"

    @property
    def dataSearch(self):
        return f"SELECT * FROM {self.table} WHERE codvenda = {self.idsale} AND codproduto = {self.product.idproduct}"

    @property
    def dataUpdate(self):
        return f"SET qtde = {self.quantity}, valor = {self.value} "

    @property
    def dataDelete(self):
        return f" WHERE codvenda = {self.idsale} AND codproduto = {self.product.idproduct}"

    @property
    def idsale(self):
        return self.__idsale
    @idsale.setter
    def idsale(self, value):
        self.__idsale = value

    @property
    def product(self):
        return self.__product
    @product.setter
    def product(self, value):
        if isinstance(value, Product):
            self.__product = value
        else:
            raise ValueError("Product must be an instance of Product class.")

    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def table(self):
        return self.__table

    @property
    def attributes(self):
        return self.__attributes

    @property
    def pkey(self):
        return self.__pkey
