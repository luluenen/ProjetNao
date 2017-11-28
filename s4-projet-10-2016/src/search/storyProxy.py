#coding: utf8
import sys
import os


PATH_PROXY = sys.path[0]

if __name__ == "__main__":
    sys.path.insert(0, sys.path[0]+'/story')

from storyd import *

class StoryProxy():
        """
            Proxy for stories:
            if you would rather create your own function, this class must be modified.
        """
        stories = {'beaux': 'beaux.txt',
                   'La cigale et la fourmi': 'la_cigale_et_la_fourmi.txt'}
        storyName =''

        def __init__(self):
            pass


        def getStory(self, storyName, path=PATH_PROXY, tool="story"):
            print 'getting story'
            content = None
            if tool == 'story':
                story = Story(path+'/'+self.stories[storyName])
                content = story.getContent()
            return content

if __name__ == '__main__':
        st = StoryProxy()
        print st.getStory('beaux')
        

