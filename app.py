from src.server.instance import server

from src.resources.clientes import ClientesResource
from src.resources.pedidos import PedidosResource
from src.resources.data import Data
from src.resources.upload import Upload

api = server.api
api.add_resource(ClientesResource, '/clientes')
api.add_resource(PedidosResource, '/pedidos')
api.add_resource(Upload, '/upload_file')
api.add_resource(Data, '/data')

if __name__ == '__main__':
    server.run()
