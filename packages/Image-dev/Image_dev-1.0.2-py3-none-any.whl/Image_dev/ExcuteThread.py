
from .SendRequests import UrlBytes
from .Resize_HashCode_Exclude import resizeImage, generate_image_hash, getExcludedHashCodes
from concurrent.futures import ThreadPoolExecutor

class ExcuteThread():

    def __init__(self, urls_and_names , l_path, s_path, o_path, down_path, exclude_path=None):
        self.s_path= s_path
        self.l_path= l_path
        self.o_path= o_path
        self.down_path= down_path
        self.exclude_path= exclude_path
        self.urls_and_names= set(urls_and_names)
        #run exclude
        if exclude_path:
            self.ExcludeImages()
            
        
    def saveOrignalDownload(self, response, image_name):
        with open(rf"{self.down_path}\{image_name}.jpg", 'wb') as file:
            file.write(response.getvalue())

    def saveResize(self, response, image_name):
        resizeImage(response, (150,150)).save(rf"{self.l_path}\{image_name}.jpg", 'png')
        resizeImage(response, (70,70)).save(rf"{self.s_path}\{image_name}.jpg", 'png')
        resizeImage(response, ).save(rf"{self.o_path}\{image_name}.jpg", 'png')

    def ExcludeImages(self):
        exclude_hashes= getExcludedHashCodes(self.exclude_path)
        self.exclude_hashes= exclude_hashes
        print('Excluded Images Included.')

    def threadFunc(self, url, image_name):
        
        status, response= UrlBytes(url).getImageBytes()
        if status:
            #get hash code
            hash_code= generate_image_hash(response)
            if self.exclude_path and hash_code in self.exclude_hashes:
                return {image_name : ('EXCLUDE', hash_code)}
            #download image to path
            self.saveOrignalDownload(response, image_name)
            #excute resize step
            self.saveResize(response, image_name)
            return {image_name : ('DONE', hash_code)}
        else:
            return {image_name : (response, None)}
    def Excute(self):
        with ThreadPoolExecutor() as excuter:
            result= list(excuter.map(lambda args: self.threadFunc(*args), self.urls_and_names))
            return result
        
    
    


            



    