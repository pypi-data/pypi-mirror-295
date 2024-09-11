import os
import zipfile
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload
from girder import logger


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        events.bind('model.file.finalizeUpload.after', 'zip_extractor', self._extract_zip)

    def _extract_zip(self, event):
        file = event.info['file']
        logger.info(f"Zip extractor triggered for file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            return

        assetstore = File().getAssetstoreAdapter(file)
        file_path = assetstore.fullPath(file)

        if not os.path.isfile(file_path):
            logger.error(f"File not found: {file_path}")
            return

        parent_folder = Folder().load(file['folderId'], force=True)

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    if zip_info.is_dir():
                        continue  # Skip directories, we'll create them as needed

                    # Extract to a temporary location
                    extracted_path = zip_ref.extract(zip_info, '/tmp/zip_extract')
                    relative_path = os.path.relpath(extracted_path, '/tmp/zip_extract')

                    # Create Girder folder structure
                    current_folder = parent_folder
                    path_parts = os.path.dirname(relative_path).split(os.sep)
                    for part in path_parts:
                        if part:
                            current_folder = Folder().createFolder(
                                current_folder, part, creator=file['creatorId'],
                                reuseExisting=True)

                    # Create Girder item and file
                    item = Item().createItem(
                        name=os.path.basename(relative_path),
                        creator=file['creatorId'],
                        folder=current_folder
                    )

                    with open(extracted_path, 'rb') as f:
                        Upload().uploadFromFile(
                            f, size=os.path.getsize(extracted_path),
                            name=os.path.basename(relative_path),
                            parentType='item',
                            parent=item,
                            user=file['creatorId'],
                            assetstore=file['assetstoreId']
                        )

                    # Clean up temporary extracted file
                    os.remove(extracted_path)

            # Remove temporary extraction directory
            os.rmdir('/tmp/zip_extract')
            
            logger.info(f"Zip extraction completed for: {file['name']}")

            # Optionally, remove the original zip file after extraction
            File().remove(file)

        except Exception as e:
            logger.error(f"Error extracting zip file: {file['name']}. Error: {str(e)}")
