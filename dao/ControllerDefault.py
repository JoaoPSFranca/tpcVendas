from dao.DatabasePyMySql import Database

class Controller:
    def __init__(self):
        self.db = Database()
        self.db.setting(ho="177.190.74.69",
                        db="tpc07",
                        us="trabtpc",
                        se="trabtpc",
                        po=65004)

    def insert(self, object):
        try:
            self.db.openConnection()
            sql = f"insert into {object.table} "
            sql += f"({object.attributes})"
            sql += f" values ({object.dataInsert})"
            self.db.execute(sql)
            self.db.save()
        except Exception as e:
            print(f"Insert Error: {e}")
            self.db.discard()

    def update(self, object, id):
        try:
            self.db.openConnection()
            sql = f"update {object.table} " + object.dataUpdate
            sql += f"where {object.pkey} = {id}"
            self.db.execute(sql)
            self.db.save()
        except Exception as e:
            print(f"Update Error: {e}")
            self.db.discard()

    def delete(self, object):
        try:
            self.db.openConnection()
            sql = f"delete from {object.table}"
            sql += f"{object.dataDelete}"
            self.db.execute(sql)
            self.db.save()
        except Exception as e:
            print(f"Delete Error: {e}")
            self.db.discard()

    def search(self, object=None, query=None):
        self.db.openConnection()
        if query is None:
            data = self.db.selectQuery(object.dataSearch)
            return object.convert(data[0]) if data else None
        else:
            return self.db.selectQuery(query)

    def search_all(self, object):
        self.db.openConnection()
        sql = f"select * from {object.table}"
        objects = self.db.selectQuery(sql)
        if objects:
            objects = [object.convert(obj) if obj else None for obj in objects]
        return objects

    def max_code(self, object):
        try:
            self.db.openConnection()
            sql = f"select {object.pkey} from {object.table} order by {object.pkey} desc limit 1"
            code = self.db.selectQuery(sql)
            return code
        except Exception as e:
            print(f"Max Code Error: {e}")
            self.db.discard()

    def search_sale_client(self, sale):
        self.db.openConnection()
        sql = f"select * from {sale.table} where idclient = {sale.client.idclient}"
        objects = self.db.selectQuery(sql)
        return objects