class plugin():

    def __init__(self, bot):

        commands = [
            self.command1,
            self.command2

        ]
        commandDictionary = {func.__name__:func for func in commands}
        triggerManifest = set(commandDictionary.keys())

        self.bot = bot
        self.bot.registerCommands('template', commandDictionary, triggerManifest)


    def command1(self, user, channel, message, arguments):
        pass

    def command2(self, user, channel, message, arguments):
        pass
