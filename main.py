import discord
import requests
import time
import random
from discord.ext import commands

response = {'pagination': {'limit': 100, 'offset': 0, 'count': 4, 'total': 4}, 'data': [{'flight_date': '2021-06-12', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '6', 'delay': 20, 'scheduled': '2021-06-12T07:00:00+00:00', 'estimated': '2021-06-12T07:00:00+00:00', 'actual': '2021-06-12T07:19:00+00:00', 'estimated_runway': '2021-06-12T07:19:00+00:00', 'actual_runway': '2021-06-12T07:19:00+00:00'}, 'arrival': {'airport': 'Kingsford Smith', 'timezone': 'Australia/Sydney', 'iata': 'SYD', 'icao': 'YSSY', 'terminal': '1', 'gate': '8', 'baggage': '15', 'delay': None, 'scheduled': '2021-06-12T08:35:00+00:00', 'estimated': '2021-06-12T08:35:00+00:00', 'actual': '2021-06-12T08:29:00+00:00', 'estimated_runway': '2021-06-12T08:29:00+00:00', 'actual_runway': '2021-06-12T08:29:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '101', 'iata': 'NZ101', 'icao': 'ANZ101', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NNB', 'iata': 'A21N', 'icao': 'A21N', 'icao24': 'C8274F'}, 'live': None}, {'flight_date': '2021-06-12', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '5', 'delay': 22, 'scheduled': '2021-06-12T09:00:00+00:00', 'estimated': '2021-06-12T09:00:00+00:00', 'actual': '2021-06-12T09:21:00+00:00', 'estimated_runway': '2021-06-12T09:21:00+00:00', 'actual_runway': '2021-06-12T09:21:00+00:00'}, 'arrival': {'airport': 'Kingsford Smith', 'timezone': 'Australia/Sydney', 'iata': 'SYD', 'icao': 'YSSY', 'terminal': '1', 'gate': '25', 'baggage': '15', 'delay': 3, 'scheduled': '2021-06-12T10:20:00+00:00', 'estimated': '2021-06-12T10:20:00+00:00', 'actual': '2021-06-12T10:23:00+00:00', 'estimated_runway': '2021-06-12T10:23:00+00:00', 'actual_runway': '2021-06-12T10:23:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '103', 'iata': 'NZ103', 'icao': 'ANZ103', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZN', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C8273F'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '6', 'delay': 22, 'scheduled': '2021-06-11T09:00:00+00:00', 'estimated': '2021-06-11T09:00:00+00:00', 'actual': '2021-06-11T09:21:00+00:00', 'estimated_runway': '2021-06-11T09:21:00+00:00', 'actual_runway': '2021-06-11T09:21:00+00:00'}, 'arrival': {'airport': 'Kingsford Smith', 'timezone': 'Australia/Sydney', 'iata': 'SYD', 'icao': 'YSSY', 'terminal': '1', 'gate': '37', 'baggage': '15', 'delay': None, 'scheduled': '2021-06-11T10:20:00+00:00', 'estimated': '2021-06-11T10:20:00+00:00', 'actual': '2021-06-11T10:14:00+00:00', 'estimated_runway': '2021-06-11T10:14:00+00:00', 'actual_runway': '2021-06-11T10:14:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '103', 'iata': 'NZ103', 'icao': 'ANZ103', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZN', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C8273F'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '1', 'delay': 19, 'scheduled': '2021-06-11T16:00:00+00:00', 'estimated': '2021-06-11T16:00:00+00:00', 'actual': '2021-06-11T16:19:00+00:00', 'estimated_runway': '2021-06-11T16:19:00+00:00', 'actual_runway': '2021-06-11T16:19:00+00:00'}, 'arrival': {'airport': 'Kingsford Smith', 'timezone': 'Australia/Sydney', 'iata': 'SYD', 'icao': 'YSSY', 'terminal': '1', 'gate': '37', 'baggage': '15', 'delay': 2, 'scheduled': '2021-06-11T17:35:00+00:00', 'estimated': '2021-06-11T17:35:00+00:00', 'actual': '2021-06-11T17:37:00+00:00', 'estimated_runway': '2021-06-11T17:37:00+00:00', 'actual_runway': '2021-06-11T17:37:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '109', 'iata': 'NZ109', 'icao': 'ANZ109', 'codeshared': None}, 'aircraft': None, 'live': None}]}



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
    #query = {'access_key':'c4223304f131787d840025bdc3570a46'}
    #url = "http://api.aviationstack.com/v1/"
    #if len(args) == 3:
    #    query['airline_name'] = args[0]
    #    query['dep_iata'] = args[1]
    #    query['arr_iata'] = args[2]


    #response = requests.get(url+"flights", params=query)
    print(response['data'][0])
    botResponse = ['```' + 'There are ' + str(len(response['data'])) + ' flights with your parameters today.' + '\n']


    for i in range(len(response['data'])):
        accessVar = response['data'][i]


        newFlight = [accessVar['flight']['icao'] + ' ' + accessVar['departure']['airport'] + ' Terminal: ' + accessVar['departure']['terminal'] + ' Gate: '
                    + accessVar['departure']['gate'] + ' ' + accessVar['departure']['scheduled'][11:][:5] + ' ' ]


        botResponse = botResponse + newFlight










    await ctx.send(botResponse[0])


    #await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(TOKEN)
