from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
#my plugin loader module
import pluginLoader

#config
#investigate use of the with statement when opening files

#add exception for formatting error in configuration file

try:
    config = open('config.txt', 'r')
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
    config.close()
except OSError as err:
    print('Error opening configuration file: %s' % err)
except NameError as err:
    print('Configuration file missing: %s' % err)


class flexbot(irc.IRCClient):

    nickname = nick
    password = pword

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        print('joined %s' % channel)

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]
        print('%s - %s: %s' % (channel, user, message))

        if message[0] == '!':
            for f in pluginLoader.privmsgFunc:
                f(self, user, channel, message)

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
        print('lost connection (%s)' % reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed: %s' % reason)
        reactor.stop()


if __name__ == '__main__':
    ff = flexFactory(channel)
    reactor.connectTCP(server, port, ff)
    reactor.run()

