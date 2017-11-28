# coding: utf8
import os
import fnmatch

class Story():
    fname=""
    def __init__(self, path): 
        self.path = '/'.join(path.split('/')[:-1])
        self.fname = path.split('/')[-1]

    def getContent(self):
        content = None
        if self.fname in os.listdir(self.path):
            myfile = open(self.path+'/'+self.fname,"r")
            content = ""
            lines = myfile.readlines()
            for line in lines:
                content = content + line.strip() + '. '
        return content

if __name__ == '__main__':
    fname = "/byujeaux.txt"
    st = Story(fname)
    text = st.getContent()
    print text
    




