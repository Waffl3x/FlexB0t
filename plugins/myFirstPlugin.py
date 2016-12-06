import random
#This will kind of serve as a template for plugin modules

#manifest of amount of functions
#do this sometime

#function trigger dictionary


#privmsg commands require (user, channel, message, arguments) the final parameter is a list

#exclamation mark triggered privmsg commands
#function manifest named by function triggers
privmsgcmdTrigger = {}

def flameUser(user, channel, message, arguments):
	return '{} is a retard'.format(arguments[0])

privmsgcmdTrigger['!flame'] = flameUser

def gaydar(user, channel, message, arguments):
		return '{} is {}% KappaPride'.format(arguments[0], random.randrange(0,100,1))

privmsgcmdTrigger['!gaydar'] = gaydar

#this is likely getting moved directly into the plugin loader
"""
def loadedCommands(user, channel, message, arguments=None):
	return 'There are {} commands loaded: {}'.format(pluginLoader.fnSum, pluginLoader.privmsgcmdTrigger.keys())

privmsgcmdTrigger['!commands'] = loadedCommands
"""

triggerManifest = set(privmsgcmdTrigger.keys())