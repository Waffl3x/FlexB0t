import importlib
import os
import sys, inspect

#taken from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
#not sure how it works, its here to allow me to import from subfolders
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"plugins")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

def fetchPlugins():
    plugNames = [fn[0:-3] for fn in os.listdir('plugins') 
    if not (fn.startswith('__') or fn.startswith('off.')) and fn.endswith('.py')]
    return plugNames

#requires names of plugins (can be derrived from fetchPlugins()) and a dictionary to store refrences
def importPlugins(pluginList, moduDictionary):
    for p in pluginList:
        moduDictionary[p] = importlib.import_module(p)
        #this feels weak, I dont know why yet



#add exclamation mark command(s) to specified dictionary renaming duplicate keys
def importExCommand(sourceName, sourceDict, sourceTriggerMani, liveDictionary, liveTriggerMani):
    """to be documented"""

    #stats
    cmdCount = len(sourceDict)
    deletedCount = 0

    #test for duplicate triggers
    if liveTriggerMani & sourceTriggerMani != set():
        #tested true for duplicate triggers
        #list to keep track of renamed commands
        renamedCommands = []
        #temporary dictionary so the source dictionary is not touched
        tempDict = sourceDict
        #attempt to append 1 to 9 on the trigger to avoid duplicates
        for t in liveTriggerMani & sourceTriggerMani:
            for i in range(1, 10):
                nameCandidate = t + str(i)
                #test if trigger is suitable
                if not(nameCandidate in liveTriggerMani):
                    #found suitable trigger, assign function to new key and delete the old key
                    tempDict[nameCandidate] = tempDict[t]
                    del tempDict[t]
                    #log changes in renamedCommands list
                    renamedCommands.append([sourceName, t, nameCandidate])
                    break
            #no suitable name found after 10 tries, delete the entry
            else:
                #log action in renamedCommands list
                renamedCommands.append([sourceName, t, 'Failed to rename'])
                del tempDict[t]
                deletedCount -= 1

        #there are no more duplicate triggers, merge to live dictionary and manifest
        liveTriggerMani.update(tempDict.keys())
        liveDictionary.update(tempDict)
        del tempDict

        return [
            sourceName,
            cmdCount,
            renamedCommands,
            'Loaded {0} functions from {1} plugin : {2} were renamed'.format((cmdCount - deletedCount), sourceName, len(renamedCommands))

        ]

    #test shows no duplicate keys, update live dictionary and manifest
    else:
        liveTriggerMani.update(sourceTriggerMani)
        liveDictionary.update(sourceDict)

        return [
            sourceName,
            cmdCount,
            None,
            'Loaded {0} functions from {1} plugin'.format(cmdCount, sourceName)

        ]
