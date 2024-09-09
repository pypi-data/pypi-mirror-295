from .ExcuteThread import ExcuteThread
from .ExcuteAmphenol import ExcuteAmphenol
from .ExtractImageName import unifyImageName, extractImageName

class runAll():
    def __init__(self, df, output_path, orignal_dwonload_path, exclude_path= None, amphenol=False):
        small_path= rf"{output_path}\Small"
        large_path= rf"{output_path}\Large"
        orignal_path= rf"{output_path}\Orignal"
        dict_image_names= {url:name 
                           for url, name in 
                           zip(df['Original_Image_UP'].drop_duplicates(),
                                unifyImageName(
                                    df['Original_Image_UP'].drop_duplicates().apply(extractImageName))) }
        df['Image_Name']= df['Original_Image_UP'].map(dict_image_names)
        print('Image Name Set Successfully.')
        if amphenol:
            results= ExcuteAmphenol(zip(df['Original_Image_UP'], df['Image_Name']),
               large_path ,small_path, orignal_path, orignal_dwonload_path,
                exclude_path=exclude_path)
            status_results = results.Excute()
        else:
            results= ExcuteThread(zip(df['Original_Image_UP'], df['Image_Name']),
                large_path ,small_path, orignal_path, orignal_dwonload_path,
                   exclude_path=exclude_path)
            status_results = results.Excute()
        print('Download And Reszie Done.')

        df['Status']= df['Image_Name'].map({k: v[0] for d in status_results for k, v in d.items()})
        df['HashCode']= df['Image_Name'].map({k: v[1] for d in status_results for k, v in d.items()})

        df['L']= df['Image_Name'][df['Status']=='DONE'].apply(lambda x: f"{large_path}\\{x}.jpg")
        df['S']= df['Image_Name'][df['Status']=='DONE'].apply(lambda x: f"{small_path}\\{x}.jpg")
        df['O']= df['Image_Name'][df['Status']=='DONE'].apply(lambda x: f"{orignal_path}\\{x}.jpg")
        df['OR']= df['Image_Name'][df['Status']=='DONE'].apply(lambda x: f"{orignal_dwonload_path}\\{x}.jpg")

        self.df= df
 
    def get_df(self):
        return self.df
    

