from model.Client import Client

class Sale:
    def __init__(self, idsale=0, date="", total_value=0.0, client=None):
        self.__idsale = idsale
        self.__date = date
        self.__total_value = total_value
        self.__client = client if client else Client()
        self.__table = "venda"
        self.__attributes = "codvenda, data, valor_total, codcliente"
        self.__pkey = "codvenda"

    @staticmethod
    def convert(data):
        return Sale(data[0], data[1], data[2], Client(data[3]))

    @property
    def dataInsert(self):
        return f"{self.idsale}, '{self.date}', {self.total_value}, {self.client.idclient}"

    @property
    def dataSearch(self):
        return f"SELECT * FROM {self.table} WHERE {self.pkey} = {self.idsale}"

    @property
    def dataUpdate(self):
        return f"SET data = '{self.date}', valor_total = {self.total_value}, codcliente = {self.client.idclient} "

    @property
    def dataDelete(self):
        return f" WHERE {self.pkey} = {self.idsale}"

    @property
    def idsale(self):
        return self.__idsale
    @idsale.setter
    def idsale(self, value):
        self.__idsale = value

    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def total_value(self):
        return self.__total_value
    @total_value.setter
    def total_value(self, value):
        self.__total_value = value

    @property
    def client(self):
        return self.__client
    @client.setter
    def client(self, value):
        self.__client = value

    @property
    def table(self):
        return self.__table

    @property
    def attributes(self):
        return self.__attributes

    @property
    def pkey(self):
        return self.__pkey
