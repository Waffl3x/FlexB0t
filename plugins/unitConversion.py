class plugin():

    def __init__(self, bot):

        commands = [
            self.convert,
            self.ctof,
            self.ftoc

        ]
        commandDictionary = {func.__name__:func for func in commands}
        triggerManifest = set(commandDictionary.keys())

        self.bot = bot
        self.bot.registerCommands('unitConversion', commandDictionary, triggerManifest)


    def convert(self, user, channel, message, arguments):
        unitConversion = self.bot.userInfo.get('unitConversion', {}).get('convert', {})

        phrase = '{0} {1} converted to {2} is {3}'

        value = float(arguments[0])
        c = unitConversion.get(arguments[1] + arguments[2])

        if c != None:
            convertedValue = value * c

            self.bot.sendMsg(channel, phrase.format(arguments[0], arguments[1], arguments[2], round(convertedValue, 2)))

        else:

            self.bot.sendMsg(channel, 'conversion information not found')


    def ctof(self, user, channel, message, arguments):
        value = float(arguments[0])
        convertedValue = value * 9 / 5 + 32

        phrase = '{0} Celcius converted to Fahrenheit is {1}'

        self.bot.sendMsg(channel, phrase.format(arguments[0], convertedValue))

    def ftoc(self, user, channel, message, arguments):
        value = float(arguments[0])
        convertedValue = (value - 32) * 5 / 9

        phrase = '{0} Fahrenheit converted to Celcius is {1}'

        self.bot.sendMsg(channel, phrase.format(arguments[0], round(convertedValue, 1)))
