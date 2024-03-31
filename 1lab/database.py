import psycopg2


class ConnectDataBase:
    def __init__(self, name, user, password, host):
        self.name = name
        self.user = user
        self.password = password
        self.host = host

    def connect_to_database(self):
        try:
            return psycopg2.connect(dbname=self.name, user=self.user, password=self.password, host=self.host)
        except:
            print('Can`t establish connection to database')
