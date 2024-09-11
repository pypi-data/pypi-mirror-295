import os
import zipfile
import tempfile
from girder import plugin, events
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.models.upload import Upload
from girder.exceptions import ValidationException
from bson import ObjectId

class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Girder Zip Extractor'

    def load(self, info):
        events.bind('data.process', 'zip_extractor', self._extract_zip)
        print('ZIP EXTRACTOR: Zip Extractor event bound to data.process')

    def _extract_zip(self, event):
        
        print(f"ZIP EXTRACTOR: Event info: {event.info}")

        if 'file' not in event.info:
            print("ZIP EXTRACTOR: No 'file' in event.info")
            return

        file = event.info['file']
        
        print(f"ZIP EXTRACTOR: File object: {file}")
        print(f"ZIP EXTRACTOR: File object type: {type(file)}")
        print(f"ZIP EXTRACTOR: File object attributes: {dir(file)}")

        if 'name' not in file:
            print("ZIP EXTRACTOR: No 'name' in file object")
            return

        print(f"ZIP EXTRACTOR: Processing file: {file['name']}")

        if not file['name'].lower().endswith('.zip'):
            print(f"ZIP EXTRACTOR: Skipping non-zip file: {file['name']}")
            return

        try:
            assetstore = File().getAssetstoreAdapter(file)
            file_path = assetstore.fullPath(file)
            print(f"ZIP EXTRACTOR: Zip file path: {file_path}")

            if not os.path.isfile(file_path):
                print(f"ZIP EXTRACTOR: File not found: {file_path}")
                return

            if 'itemId' in file:
                parent_item = Item().load(file['itemId'], force=True)
                parent_folder = Folder().load(parent_item['folderId'], force=True)
            elif 'folderId' in file:
                parent_folder = Folder().load(file['folderId'], force=True)
            else:
                print("ZIP EXTRACTOR: No 'itemId' or 'folderId' in file object")
                return

            print(f"ZIP EXTRACTOR: Parent folder: {parent_folder['name']} ({parent_folder['_id']})")

            with tempfile.TemporaryDirectory() as tmpdirname:
                print(f"ZIP EXTRACTOR: Created temporary directory: {tmpdirname}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    print(f"ZIP EXTRACTOR: Extracted zip contents to: {tmpdirname}")

                for root, dirs, files in os.walk(tmpdirname):
                    for name in files:
                        file_path = os.path.join(root, name)
                        relative_path = os.path.relpath(file_path, tmpdirname)
                        print(f"ZIP EXTRACTOR: Processing extracted file: {relative_path}")

                        # Create Girder folder structure
                        current_folder = parent_folder
                        path_parts = os.path.dirname(relative_path).split(os.sep)
                        print(f"ZIP EXTRACTOR: current_folder={current_folder}, path_parts={path_parts}")
                        for part in path_parts:
                            if part and part not in ['__MACOSX']:
                                try:
                                    new_folder = Folder().createFolder(
                                        parent=current_folder,
                                        parentType = "folder",
                                        name=part,
                                        # creator=ObjectId(file['creatorId']),
                                        creator=None,
                                        reuseExisting=True
                                    )
                                    current_folder = new_folder
                                    print(f"ZIP EXTRACTOR: Created/found folder: {part} in {current_folder['name']}")
                                except ValidationException as ve:
                                    print(f"ZIP EXTRACTOR: Error creating folder: {part}. Error: {str(ve)}")
                                    raise

                        # Create Girder item and file
                        try:
                            item = Item().createItem(
                                name=os.path.basename(relative_path),
                                creator=ObjectId(file['creatorId']),
                                folder=current_folder
                            )
                            print(f"ZIP EXTRACTOR: Created item: {item['name']} in folder: {current_folder['name']}")

                            with open(file_path, 'rb') as f:
                                uploaded_file = Upload().uploadFromFile(
                                    f, size=os.path.getsize(file_path),
                                    name=os.path.basename(relative_path),
                                    parentType='item',
                                    parent=item,
                                    user=ObjectId(file['creatorId']),
                                    assetstore=file['assetstoreId']
                                )
                                print(f"ZIP EXTRACTOR: Uploaded file: {uploaded_file['name']} to item: {item['name']}")
                        except ValidationException as ve:
                            print(f"ZIP EXTRACTOR: Error creating item or uploading file: {relative_path}. Error: {str(ve)}")
                            continue

            print(f"ZIP EXTRACTOR: Zip extraction completed for: {file['name']}")

        except Exception as e:
            print(f"ZIP EXTRACTOR: Error extracting zip file: {file['name']}. Error: {str(e)}")
            import traceback
            print(f"ZIP EXTRACTOR: Traceback: {traceback.format_exc()}")

        print("ZIP EXTRACTOR: Zip extraction process finished")

print("ZIP EXTRACTOR: Zip Extractor module fully loaded")
