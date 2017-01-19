class plugin():

    def __init__(self, bot):

        commands = [
            self.flexcommands,
            self.help

        ]
        commandDictionary = {func.__name__:func for func in commands}
        triggerManifest = set(commandDictionary.keys())

        self.bot = bot
        self.bot.registerCommands('Utilities', commandDictionary, triggerManifest)

    def flexcommands(self, user, channel, message, arguments):
        cmdlist = list(self.bot.liveFunctionDictionary.keys())
        cmdlist.sort()
        phrase = 'There are {0} commands loaded: {1}'.format(len(cmdlist), cmdlist)
        self.bot.say(channel, phrase)
        self.bot.tempPrint(channel, phrase)

    def help(self, user, channel, message, arguments):
        phrase = 'Work in progress'
        self.bot.say(channel, phrase)
        self.bot.tempPrint(channel, phrase)
