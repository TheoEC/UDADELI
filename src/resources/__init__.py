from src.api.app import api
from . import clientes, pedidos, upload

api.add_resource(upload.UploadResource, "/upload")
api.add_resource(clientes.ClientesResource, "/clientes")
api.add_resource(pedidos.PedidosResource, "/pedidos")
