from ftplib import FTP

class FileTransfer():
    # TODO Exceptions
    
    def __init__(self, pip):
        self.ftp = FTP(pip)

    def login(self, user, pwrd):
        self.ftp.login(user, pwrd)

    def getPath(self):
        return self.ftp.pwd()

    def setPath(self, path):
        self.ftp.cwd(path)

    def getListFiles(self, path=''):
        return self.ftp.nlst(path)

    def uploadFile(self, filename):
        f = open(filename, 'rb')
        self.ftp.storbinary('STOR %s' % filename, f)
        f.close()

    def downloadFile(self, filename):
        f = open(filename, 'wb')
        self.ftp.retrbinary('RETR %s' % filename, f.write)
        f.close()

    def createDirectory(self, dname):
        self.ftp.mkd(dname)

    def renameFile(oldname, newname):
        self.ftp.rename(oldname, newname)

    def deleteFile(self, filename):
        self.ftp.delete(filename)

    def close(self):
        self.ftp.close()

if __name__ == '__main__':
    port = 9559
    ip = "169.254.14.64"
    username = "nao"
    pwrd = "nao"
    
    ftp = FileTransfer(ip)
    ftp.login(username, pwrd)
    print ftp.getListFiles()
    ftp.uploadFile('D:\Uni\.PROJET S4\development\s4-projet-10-2016\data\musicfile\oiKj0Z_Xnjc.wav')
    ftp.close()
