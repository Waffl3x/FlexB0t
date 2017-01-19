# coding: UTF-8

import random
#add more commenting so this can be used as an example for plugins to be based off

#create a dictionary to contain function refrences with a their trigger as a key
privmsgcmdTrigger = {}

#create a dictionary to store the special rules when commands are used by/on users
riggedUser = {}
#load rules file into the dictionary
def reloadUserRules():
    u"""Reload's the file(s) defining specific user rules

    This will load any changes made to rules configuration since the bot was loaded
    """
    with open('plugins\\myFirstPlugin.gaydarInfo.txt', 'r') as f:
        for line in f:
            if line.startswith('\n'):
                break
            if line.startswith('#'):
                pass
            else:
                spline = line.split('%')
                a, b, c = spline[1], int(spline[3]), int(spline[5])
                riggedUser[a] = [b, c]

reloadUserRules()

#fairly temporary reload command
def forceReload(user, channel, message, arguments):
    if user == 'waffl3x':
        reloadUserRules()
        return 'Reload successful!'
    else:
        return 'You do not have permission to use this command.'

privmsgcmdTrigger['!reload'] = forceReload

#exclamation mark triggered privmsg commands

#!flame
#!flame target
def flameUser(user, channel, message, arguments):
    if arguments == []:
        target = user
    else:
        target = arguments[0]

    phrase = [
        '{0} is a retard',
        '{0} is a potato'

    ]
    random.shuffle(phrase)

    return phrase[0].format(target)

privmsgcmdTrigger['!flame'] = flameUser

#!compliment target
def compliment(user, channel, message, arguments):
    target = arguments[0]

    phrase = [
        '{0} is not a retard',
        '{0} is not a potato',
        '{0} is very nice'

    ]
    random.shuffle(phrase)

    return phrase[0].format(target)

privmsgcmdTrigger['!compliment'] = compliment

#!gaydar
#!gaydar target
def gaydar(user, channel, message, arguments):
    if arguments == []:
        target = user
    else:
        target = arguments[0]

    if target in riggedUser:
        pcntValue = random.randrange(riggedUser[target][0], riggedUser[target][1])
    else:
        pcntValue = random.randrange(0,100,1)

    return '{} is {}% KappaPride'.format(target, pcntValue)

privmsgcmdTrigger['!gaydar'] = gaydar

#!startfight fighter1 fighter2
def startfight(user, channel, message, arguments):
    encounter = [
        '{0} punches {1}, who falls over. {1} now has a sore ass.',
        '{0} hits {1} right in the face. {1} goes flying!',
        '{0} hits {1} with a fan. {1} flies a few feet off to the side.',
        '{0} blows in {1}\'s general direction. {1} falls over!'
    
    ]
    target = arguments[0:2]
    random.shuffle(target)
    random.shuffle(encounter)
    return encounter[0].format(target[0], target[1])

privmsgcmdTrigger['!startfight'] = startfight

#!fight target
def fight(user, channel, message, arguments):
    encounter = [
        '{0} punches {1}, who falls over. {1} now has a sore ass.',
        '{0} hits {1} right in the face. {1} goes flying!',
        '{0} hits {1} with a fan. {1} flies a few feet off to the side.',
        '{0} blows in {1}\'s general direction. {1} falls over!'

    ]
    target = [arguments[0], user]
    random.shuffle(target)
    random.shuffle(encounter)
    return encounter[0].format(target[0], target[1])

privmsgcmdTrigger['!fight'] = fight

#temporary list until I add a file or something
suggestionBlacklist = []
#!suggest suggestion
#save a suggestion for a command to a text file
def suggest(user, channel, message, arguments):
    if not(user in suggestionBlacklist):
        if (len(message) < 100):
            with open('suggestions.txt', 'a') as t:
                t.write('{0} in {1} suggested: {2}\n'.format(user, channel, message[9:]))
            return 'Thank you for the suggestion!'
        else:
            return 'Suggestion was too long, please enter a shorter one.'

privmsgcmdTrigger['!suggest'] = suggest


def mingleeEmote(user, channel, message, arguments):
    return 'MingLee'

privmsgcmdTrigger['!minglee'] = mingleeEmote


triggerManifest = set(privmsgcmdTrigger.keys())
