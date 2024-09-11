from girder import events
from girder.models.file import File
from girder.models.folder import Folder
from girder.plugin import GirderPlugin
import os
import zipfile

class ZipExtractorPlugin(GirderPlugin):
    DISPLAY_NAME = 'ZIP Extractor'
    
    def load(self, info):
        events.bind('model.file.finalizeUpload.after', 'zipExtractor', self.extractZipFile)

    @staticmethod
    def extractZipFile(event):
        file = event.info['file']
        
        if not zipfile.is_zipfile(File().getLocalFilePath(file)):
            return
        
        fileLocalPath = File().getLocalFilePath(file)
        parentFolder = Folder().load(file['folderId'], force=True)
        
        with zipfile.ZipFile(fileLocalPath, 'r') as zip_ref:
            extractDir = os.path.join(os.path.dirname(fileLocalPath), file['name'][:-4])
            os.makedirs(extractDir, exist_ok=True)
            zip_ref.extractall(extractDir)
        
        for root, dirs, files in os.walk(extractDir):
            for filename in files:
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f:
                    newFile = File().createFile(
                        name=filename,
                        creator=file['creatorId'],
                        item=None,
                        saveFile=True,
                        folder=parentFolder,
                        reuseExisting=True
                    )
                    newFile = File().filter(newFile, file['creatorId'])
                    File().setContent(newFile, f)

        os.remove(fileLocalPath)
        File().remove(file)
