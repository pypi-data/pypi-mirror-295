import os
import zipfile
from pathlib import Path
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.upload import Upload
from girder.constants import AccessType


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        events.bind('model.file.finalizeUpload.after', 'zip_extractor', self._extract_zip)

    def _extract_zip(self, event):
        file = event.info['file']
        
        if not file['name'].lower().endswith('.zip'):
            return

        upload = event.info['upload']
        upload_path = Upload().getAbsolutePath(upload)
        file_path = Path(upload_path)

        if not file_path.is_file():
            return

        folder = Folder().load(file['folderId'], force=True)
        
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_file_list = zip_ref.infolist()
            total_extract = len(zip_file_list)
            for member_index, member in enumerate(zip_file_list):
                try:
                    extracted_path = zip_ref.extract(member, upload_path)
                    relative_path = os.path.relpath(extracted_path, upload_path)
                    
                    # Create folder structure if necessary
                    current_folder = folder
                    parts = os.path.dirname(relative_path).split(os.sep)
                    for part in parts:
                        if part:
                            current_folder = Folder().createFolder(
                                current_folder, part, creator=file['creator'],
                                reuseExisting=True)

                    # Upload extracted file to Girder
                    if os.path.isfile(extracted_path):
                        with open(extracted_path, 'rb') as f:
                            File().createFile(
                                name=os.path.basename(extracted_path),
                                creator=file['creator'],
                                item=None,
                                reuseExisting=False,
                                assetstore=file['assetstoreId'],
                                save=True,
                                parent=current_folder,
                                stream=f
                            )
                    
                    # TODO: Implement progress update using Girder's notification system
                    # as socketio is not directly available in Girder plugins
                    
                except zipfile.error as e:
                    print(f"Error extracting the zip file {e}")
                    pass

        # Remove the original zip file after extraction
        File().remove(file)
