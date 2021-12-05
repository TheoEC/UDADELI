from src.server.instance import server
from src.resources.upload import Upload
from src.resources.data import Data

api = server.api
api.add_resource(Upload, '/upload_file')
api.add_resource(Data, '/data')

if __name__ == '__main__':
    server.run()
