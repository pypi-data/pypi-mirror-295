import os
import zipfile
import tempfile
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload
from girder import logger

print("Zip Extractor module imported")
logger.debug("Zip Extractor module imported")

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        print('Zip Extractor plugin load method called')
        logger.debug('Zip Extractor plugin load method called')
        events.bind('model.file.finalizeUpload.after', 'zip_extractor', self._extract_zip)
        print('Zip Extractor event bound')
        logger.debug('Zip Extractor event bound')

    def _extract_zip(self, event):
        print("_extract_zip method called")
        logger.debug("_extract_zip method called")
        file = event.info['file']
        print(f"Processing file: {file['name']}")
        logger.debug(f"Processing file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            print(f"Skipping non-zip file: {file['name']}")
            logger.debug(f"Skipping non-zip file: {file['name']}")
            return

        try:
            assetstore = File().getAssetstoreAdapter(file)
            file_path = assetstore.fullPath(file)
            print(f"Zip file path: {file_path}")
            logger.debug(f"Zip file path: {file_path}")

            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                logger.error(f"File not found: {file_path}")
                return

            parent_folder = Folder().load(file['folderId'], force=True)
            print(f"Parent folder: {parent_folder['name']} ({parent_folder['_id']})")
            logger.debug(f"Parent folder: {parent_folder['name']} ({parent_folder['_id']})")

            with tempfile.TemporaryDirectory() as tmpdirname:
                print(f"Created temporary directory: {tmpdirname}")
                logger.debug(f"Created temporary directory: {tmpdirname}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    print(f"Extracted zip contents to: {tmpdirname}")
                    logger.debug(f"Extracted zip contents to: {tmpdirname}")

                for root, dirs, files in os.walk(tmpdirname):
                    for name in files:
                        file_path = os.path.join(root, name)
                        relative_path = os.path.relpath(file_path, tmpdirname)
                        print(f"Processing extracted file: {relative_path}")
                        logger.debug(f"Processing extracted file: {relative_path}")

                        # Create Girder folder structure
                        current_folder = parent_folder
                        path_parts = os.path.dirname(relative_path).split(os.sep)
                        for part in path_parts:
                            if part:
                                current_folder = Folder().createFolder(
                                    current_folder, part, creator=file['creatorId'],
                                    reuseExisting=True)
                                print(f"Created/found folder: {part} in {current_folder['name']}")
                                logger.debug(f"Created/found folder: {part} in {current_folder['name']}")

                        # Create Girder item and file
                        item = Item().createItem(
                            name=os.path.basename(relative_path),
                            creator=file['creatorId'],
                            folder=current_folder
                        )
                        print(f"Created item: {item['name']} in folder: {current_folder['name']}")
                        logger.debug(f"Created item: {item['name']} in folder: {current_folder['name']}")

                        with open(file_path, 'rb') as f:
                            uploaded_file = Upload().uploadFromFile(
                                f, size=os.path.getsize(file_path),
                                name=os.path.basename(relative_path),
                                parentType='item',
                                parent=item,
                                user=file['creatorId'],
                                assetstore=file['assetstoreId']
                            )
                            print(f"Uploaded file: {uploaded_file['name']} to item: {item['name']}")
                            logger.debug(f"Uploaded file: {uploaded_file['name']} to item: {item['name']}")

            print(f"Zip extraction completed for: {file['name']}")
            logger.debug(f"Zip extraction completed for: {file['name']}")

        except Exception as e:
            print(f"Error extracting zip file: {file['name']}. Error: {str(e)}")
            logger.exception(f"Error extracting zip file: {file['name']}. Error: {str(e)}")

        print("Zip extraction process finished")
        logger.debug("Zip extraction process finished")

print("Zip Extractor module fully loaded")
logger.debug("Zip Extractor module fully loaded")
