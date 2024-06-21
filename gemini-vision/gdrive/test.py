from service import GoogleDriveService
from loader import GoogleDriveLoader

service = GoogleDriveService().build()
loader = GoogleDriveLoader(service)
all_files = loader.search_for_files() #returns a list of unqiue file ids and names 
# pdf_bytes = loader.download_file({some_id}) #returns bytes for that file