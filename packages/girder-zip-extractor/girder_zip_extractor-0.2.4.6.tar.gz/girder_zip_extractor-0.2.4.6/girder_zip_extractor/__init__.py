import os
import zipfile
import tempfile
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload

print("Zip Extractor module imported")

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        print('Zip Extractor plugin load method called')
        events.bind('data.process', 'zip_extractor', self._extract_zip)
        print('Zip Extractor event bound to data.process')

    def _extract_zip(self, event):
        print("_extract_zip method called")
        
        # Print the entire event object for debugging
        print(f"Event info: {event.info}")

        # Check if 'file' is in event.info
        if 'file' not in event.info:
            print("No 'file' in event.info")
            return

        file = event.info['file']
        
        # Print file object details
        print(f"File object: {file}")

        # Check if 'name' is in file object
        if 'name' not in file:
            print("No 'name' in file object")
            return

        print(f"Processing file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            print(f"Skipping non-zip file: {file['name']}")
            return

        try:
            assetstore = File().getAssetstoreAdapter(file)
            file_path = assetstore.fullPath(file)
            print(f"Zip file path: {file_path}")

            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                return

            # Check for 'itemId' instead of 'folderId'
            if 'itemId' in file:
                parent_item = Item().load(file['itemId'], force=True)
                parent_folder = Folder().load(parent_item['folderId'], force=True)
            elif 'folderId' in file:
                parent_folder = Folder().load(file['folderId'], force=True)
            else:
                print("No 'itemId' or 'folderId' in file object")
                return

            print(f"Parent folder: {parent_folder['name']} ({parent_folder['_id']})")

            with tempfile.TemporaryDirectory() as tmpdirname:
                print(f"Created temporary directory: {tmpdirname}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    print(f"Extracted zip contents to: {tmpdirname}")

                for root, dirs, files in os.walk(tmpdirname):
                    for name in files:
                        file_path = os.path.join(root, name)
                        relative_path = os.path.relpath(file_path, tmpdirname)
                        print(f"Processing extracted file: {relative_path}")

                        # Create Girder folder structure
                        current_folder = parent_folder
                        path_parts = os.path.dirname(relative_path).split(os.sep)
                        for part in path_parts:
                            if part:
                                current_folder = Folder().createFolder(
                                    current_folder, part, creator=file['creatorId'],
                                    reuseExisting=True)
                                print(f"Created/found folder: {part} in {current_folder['name']}")

                        # Create Girder item and file
                        item = Item().createItem(
                            name=os.path.basename(relative_path),
                            creator=file['creatorId'],
                            folder=current_folder
                        )
                        print(f"Created item: {item['name']} in folder: {current_folder['name']}")

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

            print(f"Zip extraction completed for: {file['name']}")

        except Exception as e:
            print(f"Error extracting zip file: {file['name']}. Error: {str(e)}")

        print("Zip extraction process finished")

print("Zip Extractor module fully loaded")
