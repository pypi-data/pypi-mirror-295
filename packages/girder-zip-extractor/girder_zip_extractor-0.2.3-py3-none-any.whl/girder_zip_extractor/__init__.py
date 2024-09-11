import os
import zipfile
import tempfile
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload
from girder import logger

# Add this line at the module level
print("Zip Extractor module imported")

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def __init__(self):
        super().__init__()
        print("Zip Extractor plugin initialized")

    def load(self, info):
        print('Zip Extractor plugin load method called')
        logger.info('Zip Extractor plugin loaded')
        events.bind('model.upload.finalize', 'zip_extractor', self._extract_zip)

    def _extract_zip(self, event):
        file = event.info['file']
        print(f"Zip extractor triggered for file: {file['name']}")
        logger.info(f"Zip extractor triggered for file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            print(f"Skipping non-zip file: {file['name']}")
            logger.info(f"Skipping non-zip file: {file['name']}")
            return

        try:
            assetstore = File().getAssetstoreAdapter(file)
            file_path = assetstore.fullPath(file)
            print(f"Zip file path: {file_path}")
            logger.info(f"Zip file path: {file_path}")

            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                logger.error(f"File not found: {file_path}")
                return

            parent_folder = Folder().load(file['folderId'], force=True)
            print(f"Parent folder: {parent_folder['name']} ({parent_folder['_id']})")
            logger.info(f"Parent folder: {parent_folder['name']} ({parent_folder['_id']})")

            with tempfile.TemporaryDirectory() as tmpdirname:
                print(f"Created temporary directory: {tmpdirname}")
                logger.info(f"Created temporary directory: {tmpdirname}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    print(f"Extracted zip contents to: {tmpdirname}")
                    logger.info(f"Extracted zip contents to: {tmpdirname}")

                for root, dirs, files in os.walk(tmpdirname):
                    for name in files:
                        file_path = os.path.join(root, name)
                        relative_path = os.path.relpath(file_path, tmpdirname)
                        print(f"Processing file: {relative_path}")
                        logger.info(f"Processing file: {relative_path}")

                        # Create Girder folder structure
                        current_folder = parent_folder
                        path_parts = os.path.dirname(relative_path).split(os.sep)
                        for part in path_parts:
                            if part:
                                current_folder = Folder().createFolder(
                                    current_folder, part, creator=file['creatorId'],
                                    reuseExisting=True)
                                print(f"Created/found folder: {part} in {current_folder['name']}")
                                logger.info(f"Created/found folder: {part} in {current_folder['name']}")

                        # Create Girder item and file
                        item = Item().createItem(
                            name=os.path.basename(relative_path),
                            creator=file['creatorId'],
                            folder=current_folder
                        )
                        print(f"Created item: {item['name']} in folder: {current_folder['name']}")
                        logger.info(f"Created item: {item['name']} in folder: {current_folder['name']}")

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
                            logger.info(f"Uploaded file: {uploaded_file['name']} to item: {item['name']}")

            print(f"Zip extraction completed for: {file['name']}")
            logger.info(f"Zip extraction completed for: {file['name']}")

            # Comment out this line if you want to keep the original zip file
            # File().remove(file)
            # print(f"Removed original zip file: {file['name']}")
            # logger.info(f"Removed original zip file: {file['name']}")

        except Exception as e:
            print(f"Error extracting zip file: {file['name']}. Error: {str(e)}")
            logger.exception(f"Error extracting zip file: {file['name']}. Error: {str(e)}")

        print("Zip extraction process finished")
        logger.info("Zip extraction process finished")

# Add this line at the module level
print("Zip Extractor module fully loaded")
