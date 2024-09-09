
from .Resize_HashCode_Exclude import resizeImage, generate_image_hash, getExcludedHashCodes
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from io import BytesIO

class ExcuteAmphenol():
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

    def getSeleniumResponse(self, url):
        try:
            self.driver.get(url)
            time.sleep(4)
            image_element = self.driver.find_element(By.TAG_NAME, "img")
            response= BytesIO(image_element.screenshot_as_png)
            return True, response
        except Exception as e:
            return False, 'BROKEN 403'
        
    def threadFunc(self, url, image_name):
        status, response= self.getSeleniumResponse(url)
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
        # chrome_options = Options()
        # chrome_options.add_argument('-headless')
        self.driver = webdriver.Chrome()

        result=[]
        for url, name in self.urls_and_names:
            result.append(self.threadFunc(url, name))
            time.sleep(15)

        self.driver.quit()
        return result
        
    
    


            



    