from urllib.parse import *

def transcode(srcFile):
    try:
        from pathlib import Path
        from PIL import Image
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
            image = Image.open(srcFile, "r")
            format = image.format
            if format.lower() != "webp":
                fname = Path(srcFile).name
                newFile = srcFile.replace(fname[fname.index("."):], ".webp")
                image.save(newFile, "webp", quality=90)
                image.close()
                return True, newFile
    except Exception as e:
        pass
    return False, srcFile

def additionalUrl(srcFile, ossUrl):
    from pathlib import Path
    from PIL import Image
    try:
        file_name = Path(srcFile).name
        ext = file_name[file_name.index("."):].lower()
        params = {}
        if ext in [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".gif"]:
            img = Image.open(srcFile)
            params["width"] = img.width
            params["height"] = img.height
        elif ext in [".mp4",".mov",".avi",".wmv",".mpg",".mpeg",".rm",".ram",".flv",".swf",".ts"]:
            params = {}
        elif ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
            params = {}
        else:
            params = {}
        parsed_url = urlparse(ossUrl)
        updated_query_string = urlencode(params, doseq=True)
        final_url = parsed_url._replace(query=updated_query_string).geturl()
        return final_url
    except:
        return ossUrl

def upload(src, taskUUID=None, timeout=300, needTranscode=True):
    import os
    from pathlib import Path
    from ryry import taskUtils
    if os.path.exists(src) == False:
        raise Exception(f"upload file not found")
    if taskUUID == None or len(taskUUID) <= 0:
        taskUUID = taskUtils.taskInfoWithFirstTask()
    targetDomain = taskUtils.taskDomainWithUUID(taskUUID)

    if needTranscode:
        needDeleteSrc, newSrc = transcode(src)
    else:
        needDeleteSrc = False
        newSrc = src
    support_subdomain = getSubdomain(targetDomain)
    if support_subdomain:
        import uuid
        file_name = Path(newSrc).name
        ext = os.path.splitext(file_name)[-1][1:]
        new_file_name = ''.join(str(uuid.uuid4()).split('-'))
        ossurl = ftpUpload(newSrc, f"{new_file_name}.{ext}", support_subdomain)
    else:
        from ryry import ryry_webapi
        file_name = Path(newSrc).name
        ossurl = ryry_webapi.upload(newSrc, os.path.splitext(file_name)[-1][1:])
        
    ossurl = additionalUrl(newSrc, ossurl)
    if needDeleteSrc:
        os.remove(newSrc)
    return ossurl

def deepFtpUpload(file, new_file_name, ftp, writepath, readpath):
    import ftplib, os
    try:
        ftp.cwd(writepath)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            ftp.mkd(writepath)
            ftp.cwd(writepath)
            
    with open(file, 'rb') as f:
        ftp.storbinary(f'STOR {new_file_name}', f)
    return f"{readpath}/{new_file_name}"

def ftpUpload(file, new_file_name, subdomain):
    ip = subdomain["host"]
    username = subdomain["username"]
    password = subdomain["password"]
    writepath = subdomain["writepath"]
    readpath = subdomain["readpath"]
    import ftplib
    ftp = ftplib.FTP(ip, timeout=3)
    ftp.login(username, password)

    s = deepFtpUpload(file, new_file_name, ftp, writepath, readpath)
    ftp.quit()
    return s
    
def _can_connect_ftp(ip, username, password, writepath):  
    import ftplib
    try:  
        ftp = ftplib.FTP(ip, timeout=3)
        ftp.login(username, password)
        try:
            ftp.cwd(writepath)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                ftp.mkd(writepath)
                ftp.cwd(writepath)
        ftp.quit()
        return True
    except Exception as e:  
        print(f"Failed to connect to FTP server {ip}:{writepath} {e}")  
        return False 
    
SUBDOMAIN = {
    "192.168.3.220": {
        "host": "192.168.3.220",
        "username" : "xinyu100",
        "password" : "xinyu100.com",
        "writepath" : "1TB01/data/cache/",
        # "readpath" : "http://192.168.3.220/01/cache"
        "readpath" : "ftp://192.168.3.220/1TB01/data/cache"
    },
    "192.168.50.113": {
        "host" : "192.168.50.113",
        "username" : "ftpuser",
        "password" : "ftpuser",
        "writepath" : "cache/",
        "readpath" : "ftp://192.168.50.113/cache"
    }
}
def getSubdomain(targetDomain):
    if len(targetDomain) <= 0:
        return None
    for ip in SUBDOMAIN.keys():
        if targetDomain == SUBDOMAIN[ip]["readpath"]:
            if _can_connect_ftp(ip, SUBDOMAIN[ip]["username"], SUBDOMAIN[ip]["password"], SUBDOMAIN[ip]["writepath"]):
                return SUBDOMAIN[ip]
    return None

def getFirstSupportSubdomain():
    for ip in SUBDOMAIN.keys():
        if _can_connect_ftp(ip, SUBDOMAIN[ip]["username"], SUBDOMAIN[ip]["password"], SUBDOMAIN[ip]["writepath"]):
            return SUBDOMAIN[ip]
    return None

def download(url, saveDir):
    import uuid, requests, os
    from urlparser import urlparser
    from fake_useragent import UserAgent
    if len(url) <= 0:
        return None
    try:
        name = ''.join(str(uuid.uuid4()).split('-'))
        
        if url.startswith("ftp"):
            import ftplib, random
            parsed_url = urlparse(url)  
            host = parsed_url.hostname
            if host in SUBDOMAIN:
                ip = SUBDOMAIN[host]["host"]
                username = SUBDOMAIN[host]["username"]
                password = SUBDOMAIN[host]["password"]
                writepath = SUBDOMAIN[host]["writepath"]
                readpath = SUBDOMAIN[host]["readpath"]
                ftp = ftplib.FTP(ip, timeout=3)  
                ftp.login(username, password)  
            
                remote_filepath = parsed_url.path[1:]
                if "." in urlparser.urlparse(url).path:
                    ext = urlparser.urlparse(url).path[urlparser.urlparse(url).path.index("."):]
                    savePath = os.path.join(saveDir, f"{name}{ext}")
                    with open(savePath, 'wb') as f:  
                        ftp.retrbinary(f'RETR {remote_filepath}', f.write)
                    return savePath
                else:
                    if remote_filepath[-1:] != "/":
                        remote_filepath += "/"
                    ftp.cwd(remote_filepath)
                    files = ftp.nlst()
                    if files:
                        random_file = random.choice(files)
                        savePath = os.path.join(saveDir, f"{name}_{random_file}")
                        with open(savePath, 'wb') as f:  
                            ftp.retrbinary(f'RETR {random_file}', f.write)  
                        return savePath
                ftp.quit()  
            else:
                print(f"download fail: domain {host} not support")
        elif url.startswith("http"):
            ua = UserAgent()
            ext = urlparser.urlparse(url).path[urlparser.urlparse(url).path.index("."):]
            savePath = os.path.join(saveDir, f"{name}{ext}")
            if os.path.exists(savePath):
                os.remove(savePath)
            retry = 0
            while retry < 2:
                file = requests.get(url, verify=False, headers={'User-Agent': ua.random}, timeout=30)
                with open(savePath, "wb") as c:
                    c.write(file.content)
                if os.path.exists(savePath) and os.stat(savePath).st_size > 100:
                    return savePath
                retry += 1
            print(f"download success but file not found")
        else:
            print(f"url {url} not support")
    except Exception as e:
        print(f"download fail: {e}")
    return None

def downloadDir(url, saveDir, useCount=-1, autoDelete=False):
    import uuid, os
    if len(url) <= 0:
        return None
    try:
        name = ''.join(str(uuid.uuid4()).split('-'))
        
        if url.startswith("ftp"):
            import ftplib, random
            parsed_url = urlparse(url)  
            host = parsed_url.hostname
            if host in SUBDOMAIN:
                ip = SUBDOMAIN[host]["host"]
                username = SUBDOMAIN[host]["username"]
                password = SUBDOMAIN[host]["password"]
                ftp = ftplib.FTP(ip, timeout=3)  
                ftp.login(username, password)  
            
                remote_filepath = parsed_url.path[1:]
                if remote_filepath[-1:] != "/":
                    remote_filepath += "/"
                ftp.cwd(remote_filepath)
                files = ftp.nlst()
                savePath = os.path.join(saveDir, f"{name}")
                if os.path.exists(savePath) == False:
                    os.makedirs(savePath)
                if useCount > 0 and useCount <= len(files):
                    files = random.sample(files, useCount)
                for file in files:
                    with open(os.path.join(savePath, file), 'wb') as f:  
                        ftp.retrbinary(f'RETR {file}', f.write)
                        if autoDelete:
                            try:
                                ftp.delete(file)
                            except Exception as e:
                                print(f"Error deleting file {file}: {e}")
                ftp.quit()  
                return savePath
            else:
                print(f"downloadDir fail: domain {host} not support")
        else:
            print(f"url {url} not support")
    except Exception as e:
        print(f"downloadDir fail: {e}")
    return None

# url = upload("D:\\0505.mp4", "111", 300)
# download("http://w.hs1921.com/skin/wywk/images/img_weixin.jpg", "C:\\Users\\123\\Downloads\\test")