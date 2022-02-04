from src.api.app import api
from . import upload, analysis

api.add_resource(analysis.AnalysisResource, "/analysis")
api.add_resource(upload.UploadResource, "/upload")
