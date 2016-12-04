
import itertools
import importlib
#used for os.listdir and the block copied off stackoverflow
import os
#used for the block copied off stackoverflow
import sys, inspect

#create an empty list to contain plugin module names
plugName = []
#create an empty dictionary to contain plugin module objects
plugDict = {}
#create an empty list to contain the plugin manifests
privmsgUnchained = []

#taken from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
#not sure how it works, its here to allow me to import from subfolders
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"plugins")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

#retrieve a list of files in plugin folder and add .py files to the list plugName
for fn in os.listdir('plugins'):
    if fn[0:2] != '__':
        if fn[-3:] == '.py':
           plugName.append(fn[0:-3])


#iterate over list of modules names importing them and assigning them to a dictionary
#the name of the module is the key
#add manifests as modules are imported
for k in plugName:
    plugDict[k] = importlib.import_module(k)
#add manifest for privmsg
    try:
        privmsgUnchained.append(plugDict[k].privmsg)
#exception for when a plugin contains no privmsg manifest, because no privmsg functions
    except AttributeError as err:
        print('%s plugin missing privmsg functions %s' % (k, err))

#chain the manifest lists into a single list
privmsgFunc = list(itertools.chain.from_iterable(privmsgUnchained))


#add on launch notifications
#add function statistics to manifest of plugin files
tempint = 42
for p in plugName:
    print('Loaded %s plugin with %i functions' % (p, tempint))
#add checks for success or failiure here
print('pluginLoader finished importing, %i plugins with %i functions were collected' % (len(plugName), tempint))
