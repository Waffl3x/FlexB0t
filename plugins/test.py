class plugin():



	def __init__(self, bot):

		commands = [
			self.eosin,
			self.bkbspin

		]
		commandDictionary = {func.__name__:func for func in commands}
		triggerManifest = set(commandDictionary.keys())

		self.bot = bot
		self.bot.registerCommands('eosinMemes', self, commandDictionary, triggerManifest)


	def eosin(self, user, channel, message, arguments):
		self.bot.say(channel, 'http://i.imgur.com/NxVy4LE.png')

	def bkbspin(self, user, channel, message, arguments):
		self.bot.say(channel, 'to be added when beaches isnt a retard')
