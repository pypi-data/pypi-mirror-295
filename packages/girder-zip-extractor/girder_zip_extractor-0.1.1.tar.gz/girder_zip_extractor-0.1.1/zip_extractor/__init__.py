from girder import events, logger
from girder.models.file import File
from girder.models.folder import Folder
from girder.models.item import Item
from girder.plugin import GirderPlugin
import os
import zipfile
import shutil

class ZipExtractorPlugin(GirderPlugin):
    DISPLAY_NAME = 'ZIP Extractor'
    
    def load(self, info):
        events.bind('model.file.finalizeUpload.after', 'zipExtractor', self.extractZipFile)

    @staticmethod
    def extractZipFile(event):
        file = event.info['file']
        
        if not zipfile.is_zipfile(File().getLocalFilePath(file)):
            return
        
        try:
            fileLocalPath = File().getLocalFilePath(file)
            parentFolder = Folder().load(file['folderId'], force=True)
            
            with zipfile.ZipFile(fileLocalPath, 'r') as zip_ref:
                extractDir = os.path.join(os.path.dirname(fileLocalPath), file['name'][:-4])
                os.makedirs(extractDir, exist_ok=True)
                zip_ref.extractall(extractDir)
            
            ZipExtractorPlugin._processExtractedFolder(extractDir, parentFolder, file['creatorId'])
            
            shutil.rmtree(extractDir)
            os.remove(fileLocalPath)
            File().remove(file)
            
            logger.info(f"Successfully extracted and removed zip file: {file['name']}")
        except Exception as e:
            logger.error(f"Error processing zip file {file['name']}: {str(e)}")
            raise

    @staticmethod
    def _processExtractedFolder(path, parentFolder, creatorId):
        for entry in os.scandir(path):
            if entry.is_dir():
                newFolder = Folder().createFolder(
                    parent=parentFolder,
                    name=entry.name,
                    creator=creatorId,
                    reuseExisting=True
                )
                ZipExtractorPlugin._processExtractedFolder(entry.path, newFolder, creatorId)
            else:
                with open(entry.path, 'rb') as f:
                    item = Item().createItem(
                        name=entry.name,
                        creator=creatorId,
                        folder=parentFolder
                    )
                    newFile = File().createFile(
                        name=entry.name,
                        creator=creatorId,
                        item=item,
                        saveFile=True,
                        reuseExisting=False
                    )
                    newFile = File().filter(newFile, creatorId)
                    File().setContent(newFile, f)
