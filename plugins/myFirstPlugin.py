import random

class plugin():

    def __init__(self, bot):

        commands = [
            self.minglee,
            self.flame

        ]
        commandDictionary = {func.__name__:func for func in commands}
        triggerManifest = set(commandDictionary.keys())

        self.bot = bot
        self.bot.registerCommands('myFirstPlugin', commandDictionary, triggerManifest)

    def flame(self, user, channel, message, arguments):
        if arguments == []:
            target = user
        else:
            target = arguments[0]

        phrase = [
            '{0} is a retard',
            '{0} is a potato',
            '{0} is a monkey'

        ]
        random.shuffle(phrase)

        self.bot.say(channel, phrase[0].format(target))
        self.bot.tempPrint(channel, phrase[0].format(target))

    def minglee(self, user, channel, message, arguments):
        phrase = 'MingLee'

        self.bot.say(channel, phrase)
        self.bot.tempPrint(channel, phrase)
