from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
#my plugin loader module
import pluginLoader
pL = pluginLoader


#config

#add exception for formatting error in configuration file
try:
    with open('config.txt', 'r') as config
    for line in config:
        if line[0:7] == 'server~':
            server = line[11:line.rfind('\'')]
        elif line[0:7] == 'port~~~':
            port = int(line[11:line.rfind('\'')])
        elif line[0:7] == 'nick~~~':
            nick = line[11:line.rfind('\'')]
        elif line[0:7] == 'pword~~':
            pword = line[11:line.rfind('\'')]
        elif line[0:7] == 'channel':
            channel = line[11:line.rfind('\'')]
except OSError as err:
    print('Error opening configuration file: {}'.format(err))
except NameError as err:
    print('Configuration file missing: {}'.format(err))


class flexbot(irc.IRCClient):

    nickname = nick
    password = pword

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        print('joined {}'.format(channel))

    def privmsg(self, user, channel, message):
        self.username = user.split('!', 1)[0]
        print('{} - {}: {}'.format(channel, self.username, message))

        if message[0] == '!':
            self.command = message.split(' ')[0]
            self.arguments = message.split(' ')[1:]
            #retrieve a function from the trigger dictionary, .get() returns None if key is not found
            self.function = pL.privmsgcmdTrigger.get(self.command)
            if self.function != None:
                self.response = self.function(self.username, channel, message, self.arguments)
                if self.response != None:
                    self.say(channel, self.response)
                    print('{} - flexb0t: {}'.format(channel, self.response))

class flexFactory(protocol.ClientFactory):
    protocol = flexbot

    def __init__(self, channel):
        self.channel = channel

#It's possible this is far superiour to "protocol = flexbot"
#I already have confirmed that it does the same job, I just dont know the difference
#or how it works at all
#
#    def buildProtocol(self, addr):
#        p = flexbot()
#        p.factory = self
#        return p

    def clientConnectionLost(self, connector, reason):
        print('lost connection ({})'.format(reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed: {}'.format(reason))
        reactor.stop()


if __name__ == '__main__':
    ff = flexFactory(channel)
    reactor.connectTCP(server, port, ff)
    reactor.run()

