
import itertools
import importlib
#used for os.listdir and the block copied off stackoverflow
import os
#used for the block copied off stackoverflow
import sys, inspect

#variable definitions
#create an empty list to contain plugin module names
plugName = []
#create an empty dictionary to contain plugin module objects
plugDict = {}
#create an empty dictionary to contain the trigger keywords for privmsg functions
privmsgcmdTrigger = {}
#create an empty set to store trigger keys to prevent adding duplicates
loadedTriggers = set()
#variable for sum of all functions
fnSum = 0
#create a n empty dictionary to store skipped functions, plugin name is the key and skipped functions are stored as lists
modifiedPlugins = {}


#taken from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
#not sure how it works, its here to allow me to import from subfolders
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"plugins")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

#default functions
#loadedCommands function, made sense to have this here instead of in a plugin to access complete manifests
def loadedCommands(user, channel, message, arguments=None):
    cmdlist = list(privmsgcmdTrigger.keys())
    cmdlist.sort()
    return 'There are {} commands loaded: {}'.format(len(cmdlist), cmdlist)

privmsgcmdTrigger['!commandsflex'] = loadedCommands

#amount of default functions
defaultFunctions = len(privmsgcmdTrigger.keys())
#function logging output to console
print('\nLoaded {} default functions'.format(defaultFunctions))

#retrieve a list of files in plugin folder and add .py files to the list plugName
plugName = [
    fn[0:-3] for fn in os.listdir('plugins') 
    if not fn.startswith('__') and fn.startswith('off.') and fn.endswith('.py')

]

#import modules in plugins folder, assign them to plugDict dictionary, assign command triggers to privmsgcmdTrigger
for p in plugName:
    #import module
    plugDict[p] = importlib.import_module(p)
    #add triggers to privmsgcmdTrigger
    try:
        #check for duplicate command triggers, if there are rename dupicates
        if loadedTriggers & plugDict[p].triggerManifest != set():
            #duplicate triggers detected
            #assign the trigger manifest for the plugin to a temporary dictionary and rename duplicates
            tmpDict = plugDict[p].privmsgcmdTrigger
            #create a dictionary entry in the modifiedPlugins dictionary using the plugin name as a key
            modifiedPlugins[p] = []
            #assign the value of the duplicate key to a new key, log actions
            for t in loadedTriggers & plugDict[p].triggerManifest:
                #iterate from 1 to 10 attempting to rename duplicate command trigger
                for i in range(1, 10):
                    #assign modified name to a temporary variable
                    newTriggerName = t + str(i)
                    #test if new trigger is already in use
                    if not(newTriggerName in loadedTriggers):
                        #new trigger is not in use, assigning the command function to the new trigger
                        tmpDict[newTriggerName] = tmpDict[t]
                        #delete the old trigger key
                        del tmpDict[t]
                        break
                #just in case there are 9 other commands with the same trigger, JUST IN CASE
                else:
                    print('Failed to reassign trigger after 10 tries, giving up')
                    #delete the key and value from the dictionary to be merged so there are no overwritten triggers
                    del tmpDict[t]
                    #change the newTriggerName value to None to specify the command was skipped from the load
                    newTriggerName = None
                #add keys that were renamed to a list in a dictionary keeping track of what was skipped, the dictionary key is the plugin name
                #add the renamed key, and its new name as a list, first index the original name, second index the new name
                #if the key is not renamed, newTriggerName will = None
                modifiedPlugins[p].append([t, newTriggerName])
            
            #merge modified plugin triggerManifest set with loadedTriggers set
            loadedTriggers.update(tmpDict.keys())
            #merge modified plugin dictionary to the loaded dictionary after duplicates have been stripped
            privmsgcmdTrigger.update(tmpDict)

            #logging relevant operations, output to console
            c = len(tmpDict)
            fnSum = fnSum + c
            print('Loaded {} functions from {} plugin : {} were renamed'.format(c, p, len(modifiedPlugins[p])))

        #no duplicate commands detected, merge dictionaries, add triggers to the loadedTriggers set, output logs
        else:
            #merge plugin triggerManifest set with loadedTriggers set
            loadedTriggers.update(plugDict[p].triggerManifest)
            #merge the trigger manifest from the plugin into the compiled trigger manifest dictionary
            privmsgcmdTrigger.update(plugDict[p].privmsgcmdTrigger)

            #logging relevent operations, output to console
            c = len(plugDict[p].privmsgcmdTrigger) #consider replacing this with metadata from the module
            fnSum = fnSum + c
            print('Loaded {} functions from {} plugin'.format(c, p))

    #exception for when a plugin lacks a triggerManifest
    except AttributeError as err:
        print('{} plugin missing privmsg functions {}'.format(p, err))


totalRenamedFunctions = 0
for p in modifiedPlugins:
    totalRenamedFunctions = totalRenamedFunctions + len(modifiedPlugins[p])


#add checks for success or failiure here
print('\n#####################################')
print('pluginLoader finished importing')
print('Loaded {} functions from {} plugins'.format(fnSum, len(plugName)))
if modifiedPlugins != 0:
    print('Renamed {} functions in {} plugins'.format(totalRenamedFunctions, len(modifiedPlugins)))
print('#####################################\n')
commandList = list(privmsgcmdTrigger.keys())
commandList.sort()
print('enabled commands: {}\n'.format(commandList))
