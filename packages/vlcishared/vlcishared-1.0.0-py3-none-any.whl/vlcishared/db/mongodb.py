from pymongo import MongoClient, errors
import logging


class MongoDBConnector():
    def __init__(self, host: str, port: str, auth_source: str, user: str, password: str):
        self.uri = (
            f"mongodb://{user}:{password}@"
            f"{host}:{port}/"
            f"{auth_source}?authSource={auth_source}"
        )
        self.host = host
        self.port = port
        self.auth_source = auth_source
        self.user = user
        self.password = password
        self.client = None
        self.log = logging.getLogger()

    def get_db_connection(self):
        """Función que se conecta a la base de datos de MongoDB
            definida en el constructor"""
        try:
            self.log.info('Conectando a MongoDB')
            self.client = MongoClient(self.uri)
            return self.client.get_database()
        except errors.ConnectionFailure as e:
            raise ConnectionError(f"Error de conexión a MongoDB: {e}")

    def disconnect(self):
        if self.client:
            self.log.info('Desconectando de MongoDB')
            self.client.close()
