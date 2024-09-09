from PIL import Image
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from numpy import array

def resizeImage(url_bytes, target_size=None):
    image = Image.open(url_bytes)
    # Convert the image to grayscale
    gray_image = image.convert('L')
    # Threshold the grayscale image to create a binary mask of white spaces
    threshold_value = 250
    binary_mask = gray_image.point(lambda p: p < threshold_value  )
    bbox = binary_mask.getbbox()
    # Crop the image to fit the contents tightly
    image = image.crop(bbox)
    # fill unblaned image size with white spae to square it 
    if image.size[0] != image.size[1]:
        background = Image.new('RGBA', (max(image.size), max(image.size)), 'white')
        position = ((background.width - image.width) // 2, (background.height - image.height) // 2)
        # Paste the original image at the center of the white background
        background.paste(image, position)
        image= background
        #set white backgound for png
    if target_size and image.width > target_size[0]:
        image= image.resize(target_size,  Image.LANCZOS)
    elif target_size:
        background = Image.new('RGBA', target_size, 'white')
        position = ((background.width - image.width) // 2, (background.height - image.height) // 2)
        background.paste(image, position)
        image= background
    # Create a new white background image with dimensions 150x150
    return image

def generate_image_hash(url_bytes):
    try:
        img= Image.open(url_bytes).convert('L')
        img = img.resize((256, 256), Image.ANTIALIAS)
        # Convert the image to a numpy array
        img_array = array(img)
        # Flatten the array to 1D
        flattened_array = img_array.flatten()
        # Convert pixel values to bytes
        byte_array = flattened_array.tobytes()
        # Calculate SHA-256 hash based on the processed image data
        hash_obj = hashlib.md5()
        hash_obj.update(byte_array)
        image_hash = hash_obj.hexdigest()
        return image_hash
    except:
        None

def getExcludedHashCodes(path):
    images_pathes= Path(path).glob('*')
    with ThreadPoolExecutor() as excuter:
        result= tuple(set(excuter.map(generate_image_hash, images_pathes)))  
        return result