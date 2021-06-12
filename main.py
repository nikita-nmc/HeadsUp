import discord
import requests
import time
import random
from discord.ext import commands

#response = [{'flight_date': '2021-06-12', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '9', 'delay': 10, 'scheduled': '2021-06-12T08:55:00+00:00', 'estimated': '2021-06-12T08:55:00+00:00', 'actual': '2021-06-12T09:04:00+00:00', 'estimated_runway': '2021-06-12T09:04:00+00:00', 'actual_runway': '2021-06-12T09:04:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '5', 'baggage': None, 'delay': None, 'scheduled': '2021-06-12T10:45:00+00:00', 'estimated': '2021-06-12T10:45:00+00:00', 'actual': '2021-06-12T10:33:00+00:00', 'estimated_runway': '2021-06-12T10:33:00+00:00', 'actual_runway': '2021-06-12T10:33:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '123', 'iata': 'NZ123', 'icao': 'ANZ123', 'codeshared': None}, 'aircraft': None, 'live': None}, {'flight_date': '2021-06-12', 'flight_status': 'cancelled', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '1', 'delay': None, 'scheduled': '2021-06-12T18:30:00+00:00', 'estimated': '2021-06-12T18:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': None, 'baggage': None, 'delay': None, 'scheduled': '2021-06-12T20:30:00+00:00', 'estimated': '2021-06-12T20:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '129', 'iata': 'NZ129', 'icao': 'ANZ129', 'codeshared': None}, 'aircraft': None, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '4C', 'delay': 34, 'scheduled': '2021-06-11T08:55:00+00:00', 'estimated': '2021-06-11T08:55:00+00:00', 'actual': '2021-06-11T09:28:00+00:00', 'estimated_runway': '2021-06-11T09:28:00+00:00', 'actual_runway': '2021-06-11T09:28:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '7', 'baggage': None, 'delay': 6, 'scheduled': '2021-06-11T10:45:00+00:00', 'estimated': '2021-06-11T10:45:00+00:00', 'actual': '2021-06-11T10:44:00+00:00', 'estimated_runway': '2021-06-11T10:44:00+00:00', 'actual_runway': '2021-06-11T10:44:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '123', 'iata': 'NZ123', 'icao': 'ANZ123', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZQ', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C82741'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '3', 'delay': 15, 'scheduled': '2021-06-11T15:40:00+00:00', 'estimated': '2021-06-11T15:40:00+00:00', 'actual': '2021-06-11T15:54:00+00:00', 'estimated_runway': '2021-06-11T15:54:00+00:00', 'actual_runway': '2021-06-11T15:54:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '3', 'baggage': None, 'delay': None, 'scheduled': '2021-06-11T17:30:00+00:00', 'estimated': '2021-06-11T17:30:00+00:00', 'actual': '2021-06-11T17:29:00+00:00', 'estimated_runway': '2021-06-11T17:29:00+00:00', 'actual_runway': '2021-06-11T17:29:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '125', 'iata': 'NZ125', 'icao': 'ANZ125', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZK', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C8236E'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'cancelled', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '4', 'delay': None, 'scheduled': '2021-06-11T18:30:00+00:00', 'estimated': '2021-06-11T18:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '7', 'baggage': None, 'delay': None, 'scheduled': '2021-06-11T20:30:00+00:00', 'estimated': '2021-06-11T20:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '129', 'iata': 'NZ129', 'icao': 'ANZ129', 'codeshared': None}, 'aircraft': None, 'live': None}]

bot = commands.Bot(command_prefix='$')

TOKEN = 'ODUzMDk4MTc1MDQzNjAwNDA0.YMQblg.e2dd7DP28hs-I8HH3oy7dZeWORA'

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def hello(ctx):
    greetings = ["Hello!", "Hi!", "Hey!", "Hiya!", "Heya!"]
    await ctx.send(random.choice(greetings))

@bot.command()
async def flight(ctx, *args):
    query = {'access_key':'c4223304f131787d840025bdc3570a46'}
    url = "http://api.aviationstack.com/v1/"
    if len(args) == 3:
        query['airline_name'] = args[0]
        query['dep_iata'] = args[1]
        query['arr_iata'] = args[2]

    response = requests.get(url+"flights", params=query)
    botResponse = ['```' + 'There are ' + str(len(response.json()['data'])) + ' flights with your parameters today:' + '\n']

    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]
        flightNo = accessVar['flight']['icao']
        depAirport = accessVar['departure']['airport']
        depTerminal = accessVar['departure']['terminal']
        depGate = accessVar['departure']['gate']
        depTime = accessVar['departure']['scheduled'][11:][:5]
        arrAirport = accessVar['arrival']['airport']
        arrTerminal = accessVar['arrival']['terminal']
        arrGate = accessVar['arrival']['gate']
        try:
            aircraft = accessVar['aircraft']['icao']
            rego = accessVar['aircraft']['registration']
        except TypeError:
            aircraft = 'Unknown'
            rego = 'N/A'
        status = accessVar['flight_status']
        arrTime = accessVar['arrival']['scheduled'][11:][:5]

        newFlight = ['\n' + flightNo + ' ' + depAirport + ' Terminal: ' + str(depTerminal) + ' Gate: '
                    + str(depGate) + ' Scheduled Departure: ' + depTime +
                    ' ' + arrAirport + ' Terminal: ' + str(arrTerminal) + ' Gate: ' + str(arrGate)
                    + ' Aircraft: ' + aircraft + ' ' + rego + '\n'+
                    'Status: ' + status + ' ' + arrTime + '\n']
        botResponse = botResponse + newFlight

    botResponse = botResponse + ['```']

    botResponse = "".join(botResponse)

    await ctx.send(botResponse)


    #await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(TOKEN)
