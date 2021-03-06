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
            '{0} is a monkey',
            '{0} is a noob',
            '{0} is a moron'

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

        targetLow = target.lower()

        if targetLow in customUser:
            info = customUser[targetLow]
            #current types are range (R), literal (L), and custom string (S)
            if info[0] == 'R':
                amount = random.randrange(info[1], info[2])
                phrase = '{0} is {1}% KappaPride'.format(target, amount)
            elif info[0] == 'L':
                amount = info[1]
                phrase = '{0} is {1}% KappaPride'.format(target, amount)
            elif info[0] == 'S':
                phrase = info[1]
            else:
                print('#\nuser info formatted incorrectly: invalid flag at first index of list\n#')
        else:
            amount = random.randrange(0,100,1)
            phrase = '{0} is {1}% KappaPride'.format(target, amount)

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
