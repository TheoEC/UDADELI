from src.api.app import api
from . import file, analysis

api.add_resource(analysis.AnalysisResource, "/analysis")
api.add_resource(
    file.FileResource,
    "/planilhas",
    "/planilhas/<spreadsheet_id>"
)
