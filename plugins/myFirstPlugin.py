import random
#This will kind of serve as a template for plugin modules

#manifest of amount of functions
#do this sometime

#function trigger dictionary


#privmsg commands require (user, channel, message, arguments) the final parameter is a list

#exclamation mark triggered privmsg commands
#function manifest named by function triggers
privmsgcmdTrigger = {}

#!flame
#!flame target
def flameUser(user, channel, message, arguments):
	if arguments == []:
		target = user
	else:
		target = arguments[0]

	return '{} is a retard'.format(target)

privmsgcmdTrigger['!flame'] = flameUser

#!gaydar
#!gayday target
def gaydar(user, channel, message, arguments):
	if arguments == []:
		target = user
	else:
		target = arguments[0]

	return '{} is {}% KappaPride'.format(target, random.randrange(0,100,1))

privmsgcmdTrigger['!gaydar'] = gaydar

#!startfight fighter1 fighter2
def startfight(user, channel, message, arguments):
	encounter = [
	'{0} knocked {1} on their ass!',
	'{0} hits {1} right in the face. {1} goes flying!',
	'{0} blows in {1}\'s general direction. {1} falls over!']
	target = arguments[0:2]
	random.shuffle(target)
	random.shuffle(encounter)
	return encounter[0].format(target[0], target[1])

privmsgcmdTrigger['!startfight'] = startfight

#!fight target
def fight(user, channel, message, arguments):
	encounter = [
	'{0} knocked {1} on their ass!',
	'{0} hits {1} right in the face. {1} goes flying!',
	'{0} blows in {1}\'s general direction. {1} falls over!']
	target = [arguments[0], user]
	random.shuffle(target)
	random.shuffle(encounter)
	return encounter[0].format(target[0], target[1])

privmsgcmdTrigger['!fight'] = fight

#!compliment target
def compliment(user, channel, message, arguments):
	target = arguments[0]
	return '{} is not a retard'.format(target)

privmsgcmdTrigger['!compliment'] = compliment



triggerManifest = set(privmsgcmdTrigger.keys())