from .ReadFile import read
import re
from pandas import merge
from . import OracelConnection

class AfterCreation():

    def __init__(self, input_file_path, after_creation_file_path):
        self.input_file_path= input_file_path
        self.after_creation_file_path= after_creation_file_path
        self.file_name= '.'.join(self.input_file_path.split('\\')[-1].split('.')[:-1])

    def createImporteFile(self):
        try:
            input_file= read(self.input_file_path)
            after_creation= read(self.after_creation_file_path)
        except Exception as e:
            input_file= self.input_file_path.copy()
            after_creation= self.after_creation_file_path.copy()
        #Select Target Columns.
        
        try:
            importer_df= input_file[['Part_Number', 'VENDOR', 'IMAGE_SOURCE', 'IMAGE_SOURCE_TYPE', 'PART_IMAGE_LEVEL']].copy()
        except KeyError as key:
            match= re.search("\'(?P<k>.+)\'", str(key)).group('k')
            print(f"{match} Missing from Columns")
            raise
        importer_df['Small']= merge(input_file, after_creation, how='left', left_on='S', right_on='File Path')['SE_URL'].values
        importer_df['large']= merge(input_file, after_creation, how='left', left_on='L', right_on='File Path')['SE_URL'].values
        importer_df['ORIGINAL_IMAGE']= merge(input_file, after_creation, how='left', left_on='O', right_on='File Path')['SE_URL'].values
        return importer_df

    def updateImageProgress(self):
        connection= OracelConnection.connectDB()
        cursor = connection.cursor()
        cursor.execute(f" UPDATE image_progress SET CREATION_STATUS = 'DONE'  WHERE FILE_NAME = '{self.file_name}'")
        connection.commit()
        connection.close()

