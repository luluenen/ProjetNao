import sys

PATH = sys.path[0].replace("\\","/")
PATH_DB = '/'.join(PATH.split("/")[:-1])+"/data"

PATH_LIST = [PATH, PATH+'/modules',
             PATH+'/search',
             PATH+'/search/music',
             PATH+'/search/information',
             PATH+'/search/news',
             PATH+'/search/tv',
             PATH+'/search/story',
             PATH_DB,
             PATH_DB+'/musicfile',
             PATH_DB+ '/storyfile'] 

def addPaths():
    for path in PATH_LIST:
        sys.path.insert(0, path)
       
