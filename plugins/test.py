class plugin():

    def __init__(self, bot):

        commands = [
            self.eosin,
            self.bkbspin

        ]
        commandDictionary = {func.__name__:func for func in commands}
        triggerManifest = set(commandDictionary.keys())

        self.bot = bot
        self.bot.registerCommands('eosinMemes', commandDictionary, triggerManifest)


    def eosin(self, user, channel, message, arguments):
        phrase = 'http://i.imgur.com/NxVy4LE.png'
        self.bot.say(channel, phrase)
        self.bot.tempPrint(channel, phrase)

    def bkbspin(self, user, channel, message, arguments):
        phrase = 'to be added when beaches isnt a retard'
        self.bot.say(channel, phrase)
        self.bot.tempPrint(channel, phrase)

#learn decorators tomorrow
