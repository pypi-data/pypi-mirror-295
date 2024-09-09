import re
def extractImageName(url):
    illegal= re.escape(' \/:*?"<>|=')
    image_extensions = '|'.join(["JPEG", "JPG", "PNG", "GIF", "BMP", "TIFF",
                                "TIF", "SVG", "WEBP", "HEIC", "HEIF", "PSD", "AI",
                                "EPS", "RAW", "ICO", "PDF", "CR2", "NEF", "ORF",
                                "DNG", "ARW", "RW2"]).lower()
    # if link is a url
    filename='' 
    match= re.search(f"[\\\/](?P<k>[^\\\/]+)\.({image_extensions})", url, flags= re.IGNORECASE)
    if match:   
        filename= match.group('k')         
    if filename =='':
        filename= url.split('/')[-1]         
    if filename =='':
        filename= url.split('/')[-2]  
    #remove illegal cajrs form name  
    filename= re.sub(f"[{illegal}]", '',filename)
    return filename

def unifyImageName(series):
    dupl= series[series.duplicated()].unique()
    for name in dupl:
        for counter, index in enumerate(series[series==name].index[1:]):
            series[index]= f"{name}({counter+1})"
    return series
