from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
#currently used for fetching viewer lists from https://tmi.twitch.tv/group/user/%channelname%/chatters
import urllib.request
import json
#my plugin loader module
import pluginLoader

#config
#add exception for formatting error in configuration file
try:
    with open('config.txt', 'r') as config:
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

    def __init__(self):
        self.pluginDict = {}
        self.liveFunctionDictionary = {}
        self.liveTriggerManifest = set()
        self.viewerDict = {}

        #automatically load the userInfo.json and userPrivlege files
        self.loadUserInfo()
        self.loadUserPrivilege()

        #load plugins
        pluginLoader.importPlugins(pluginLoader.fetchPlugins(), self.pluginDict)
        #import commands
        for p in self.pluginDict:
            self.pluginDict[p].plugin(self)


    def signedOn(self):
        self.join(self.factory.channel)

        self.say(self.factory.channel, 'Hi!')

    def joined(self, channel):
        print('joined {}'.format(channel))

    def privmsg(self, user, channel, message):
        username = user.split('!', 1)[0]
        print('{} - {}: {}'.format(channel, username, message))

        if message[0] == '!':
            if not(username in self.userInfo.get('userPrivilege', {}).get('blacklist', [])):
                splitmessage = message.split(' ')
                command = splitmessage[0][1:]
                arguments = splitmessage[1:]

                chatCommand = self.liveFunctionDictionary.get(command)
                if chatCommand != None:
                    if arguments == []:
                        chatCommand(username, channel, message, arguments)
                    else:
                        #basic input sanitization
                        for a in arguments:
                            if a[0] in ('!', '/', '.'):
                                print('Caught malicious input')
                                self.say(channel, 'Please don\'t :(')
                                break
                        else:
                            chatCommand(username, channel, message, arguments)

    def fetchViewers(self, channel):
        req = urllib.request.Request('https://tmi.twitch.tv/group/user/{}/chatters'.format(channel))
        with urllib.request.urlopen(req) as response:
            viewersJSON = response.read()
    
        viewersUnparsed = json.loads(viewersJSON.decode('utf-8'))

        self.viewerDict['count'] = viewersUnparsed.get('chatter_count')
        self.viewerDict['staff'] = viewersUnparsed.get('chatters', {}).get('staff', [])
        self.viewerDict['mods'] = viewersUnparsed.get('chatters', {}).get('moderators', [])
        self.viewerDict['normal'] = viewersUnparsed.get('chatters', {}).get('viewers', [])

        self.viewerDict['total'] = self.viewerDict['staff'] + self.viewerDict['mods'] + self.viewerDict['normal']
        #debug, remove later
        print(self.viewerDict['total'])
        print(self.viewerDict['count'])

    def loadPlugins(self):
        """placeholder"""
        pass

    def registerCommands(self, name, commandDict, triggerMani):
        print(pluginLoader.importExCommand(name, commandDict, triggerMani, self.liveFunctionDictionary, self.liveTriggerManifest)[3])

    def sendMsg(self, channel, phrase):
        self.say(channel, phrase)
        print('{0} - flexb0t: {1}'.format(channel, phrase))

    def loadUserInfo(self):
        """load user specific command info and permissions json"""
        try:
            with open('userInfo.json','r') as f:
                self.userInfo = json.load(f)
                #debug
                print(self.userInfo)
        #no such file userInfo.json...
        except OSError as err:
            print('\nuserInfo.json was not found: {0}\n\nCustom parameters will not be available.\n'.format(err))
            self.userInfo = {}

    def  loadUserPrivilege(self):
        """load user power levels"""
        try:
            with open('userPrivilege.json','r') as f:
                self.userPower = json.load(f)
                #debug
                print(self.userPower)
        #no such file userInfo.json...
        except OSError as err:
            print('\nuserPrivilege.json was not found: {0}\n\nAdded waffl3x to admin user group as default\n'.format(err))
            self.userPower = {'admin':['waffl3x']}


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

