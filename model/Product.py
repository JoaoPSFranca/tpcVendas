class Product:
    def __init__(self, idproduct=0, name="", price=0.0):
        self.__idproduct = idproduct
        self.__name = name
        self.__price = price
        self.__table = "produto"
        self.__attributes = "codproduto, descricao, preco"
        self.__pkey = "codproduto"

    @staticmethod
    def convert(data):
        return Product(data[0], data[1], data[2])

    @property
    def dataInsert(self):
        return f"{self.idproduct}, '{self.name}', {self.price}"

    @property
    def dataSearch(self):
        return f"SELECT * FROM {self.table} WHERE {self.pkey} = {self.idproduct}"

    @property
    def dataUpdate(self):
        return f"SET descricao = '{self.name}', preco = {self.price} "

    @property
    def dataDelete(self):
        return f" WHERE {self.pkey} = {self.idproduct}"

    @property
    def idproduct(self):
        return self.__idproduct
    @idproduct.setter
    def idproduct(self, value):
        self.__idproduct = value

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def table(self):
        return self.__table

    @property
    def attributes(self):
        return self.__attributes

    @property
    def pkey(self):
        return self.__pkey
