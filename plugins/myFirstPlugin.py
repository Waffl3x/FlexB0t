import random

class plugin():

    def __init__(self, bot):

        commands = [
            self.flame,
            self.compliment,
            self.gaydar,
            self.fight,
            self.minglee

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

        self.bot.sendMsg(channel, phrase[0].format(target))

    def compliment(self, user, channel, message, arguments):
        if arguments == []:
            target = user
        else:
            target = arguments[0]

        phrase = [
            '{0} is not a retard',
            '{0} is not a potato',
            '{0} is very nice'

        ]
        random.shuffle(phrase)

        self.bot.sendMsg(channel, phrase[0].format(target))

    def gaydar(self, user, channel, message, arguments):
        customUser = self.bot.userInfo.get('myFirstPlugin', {}).get('gaydar', {})

        if arguments == []:
            target = user
        else:
            target = arguments[0]

        if target in customUser:
            amount = random.randrange(customUser[target][0], customUser[target][1])
        else:
            amount = random.randrange(0,100,1)

        phrase = '{} is {}% KappaPride'.format(target, amount)

        self.bot.sendMsg(channel, phrase)

    def fight(self, user, channel, message, arguments):
        if len(arguments) == 1:
            target = [user, arguments[0]]
        else:
            target = [arguments[0], arguments[1]]

        phrase = [
            '{0} punches {1}, who falls over. {1} now has a sore ass.',
            '{0} hits {1} right in the face. {1} goes flying!',
            '{0} hits {1} with a fan. {1} flies a few feet off to the side.',
            '{0} blows in {1}\'s general direction. {1} falls over!'

        ]
        random.shuffle(target)
        random.shuffle(phrase)

        self.bot.sendMsg(channel, phrase[0].format(target[0], target[1]))

    def minglee(self, user, channel, message, arguments):
        phrase = 'MingLee'

        self.bot.sendMsg(channel, phrase)
