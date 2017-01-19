privmsgcmdTrigger = {}

unitConversion = {}
unitConversion['feetmeters'] = 0.3048
unitConversion['metersfeet'] = 3.28
unitConversion['antiplansalt'] = 1687
unitConversion['saltantiplan'] = 0.000592768
unitConversion['D_E_IIronTalons'] = 10.3

#!convert value startunit convertunit
def convert(user, channel, message, arguments):
    value = float(arguments[0])
    c = unitConversion.get(arguments[1] + arguments[2])
    if c != None:
        convertedValue = value * c
    else:
        return 'conversion information not found'
    return '{0} {1} converted to {2} is {3}'.format(arguments[0], arguments[1], arguments[2], round(convertedValue, 2))

privmsgcmdTrigger['!convert'] = convert

#!ctof value
def ctof(user, channel, message, arguments):
    value = float(arguments[0])
    convertedValue = value * 9 / 5 + 32
    return '{0} Celcius converted to Fahrenheit is {1}'.format(arguments[0], round(convertedValue, 1))

privmsgcmdTrigger['!ctof'] = ctof

#!ftoc value
def ftoc(user, channel, message, arguments):
    value = float(arguments[0])
    convertedValue = (value - 32) * 5 / 9
    return '{0} Fahrenheit converted to Celcius is {1}'.format(arguments[0], round(convertedValue, 1))

privmsgcmdTrigger['!ftoc'] = ftoc


triggerManifest = set(privmsgcmdTrigger.keys())
