import os.path
import sys

#from kivy.garden import iconfonts

targetFilename = os.path.basename(sys.argv[1])
if targetFilename.endswith('.css'):
    targetFilename = targetFilename[:-4]
targetFilename = targetFilename + '.fontd'

#iconfonts.create_fontdict_file(sys.argv[1], targetFilename)
