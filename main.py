import discord
import requests
import time
import random
import csv
from discord.ext import commands

# response = [{'flight_date': '2021-06-12', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '9', 'delay': 10, 'scheduled': '2021-06-12T08:55:00+00:00', 'estimated': '2021-06-12T08:55:00+00:00', 'actual': '2021-06-12T09:04:00+00:00', 'estimated_runway': '2021-06-12T09:04:00+00:00', 'actual_runway': '2021-06-12T09:04:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '5', 'baggage': None, 'delay': None, 'scheduled': '2021-06-12T10:45:00+00:00', 'estimated': '2021-06-12T10:45:00+00:00', 'actual': '2021-06-12T10:33:00+00:00', 'estimated_runway': '2021-06-12T10:33:00+00:00', 'actual_runway': '2021-06-12T10:33:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '123', 'iata': 'NZ123', 'icao': 'ANZ123', 'codeshared': None}, 'aircraft': None, 'live': None}, {'flight_date': '2021-06-12', 'flight_status': 'cancelled', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '1', 'delay': None, 'scheduled': '2021-06-12T18:30:00+00:00', 'estimated': '2021-06-12T18:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': None, 'baggage': None, 'delay': None, 'scheduled': '2021-06-12T20:30:00+00:00', 'estimated': '2021-06-12T20:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '129', 'iata': 'NZ129', 'icao': 'ANZ129', 'codeshared': None}, 'aircraft': None, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '4C', 'delay': 34, 'scheduled': '2021-06-11T08:55:00+00:00', 'estimated': '2021-06-11T08:55:00+00:00', 'actual': '2021-06-11T09:28:00+00:00', 'estimated_runway': '2021-06-11T09:28:00+00:00', 'actual_runway': '2021-06-11T09:28:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '7', 'baggage': None, 'delay': 6, 'scheduled': '2021-06-11T10:45:00+00:00', 'estimated': '2021-06-11T10:45:00+00:00', 'actual': '2021-06-11T10:44:00+00:00', 'estimated_runway': '2021-06-11T10:44:00+00:00', 'actual_runway': '2021-06-11T10:44:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '123', 'iata': 'NZ123', 'icao': 'ANZ123', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZQ', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C82741'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'landed', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '3', 'delay': 15, 'scheduled': '2021-06-11T15:40:00+00:00', 'estimated': '2021-06-11T15:40:00+00:00', 'actual': '2021-06-11T15:54:00+00:00', 'estimated_runway': '2021-06-11T15:54:00+00:00', 'actual_runway': '2021-06-11T15:54:00+00:00'}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '3', 'baggage': None, 'delay': None, 'scheduled': '2021-06-11T17:30:00+00:00', 'estimated': '2021-06-11T17:30:00+00:00', 'actual': '2021-06-11T17:29:00+00:00', 'estimated_runway': '2021-06-11T17:29:00+00:00', 'actual_runway': '2021-06-11T17:29:00+00:00'}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '125', 'iata': 'NZ125', 'icao': 'ANZ125', 'codeshared': None}, 'aircraft': {'registration': 'ZK-NZK', 'iata': 'B789', 'icao': 'B789', 'icao24': 'C8236E'}, 'live': None}, {'flight_date': '2021-06-11', 'flight_status': 'cancelled', 'departure': {'airport': 'Auckland International', 'timezone': 'Pacific/Auckland', 'iata': 'AKL', 'icao': 'NZAA', 'terminal': 'I', 'gate': '4', 'delay': None, 'scheduled': '2021-06-11T18:30:00+00:00', 'estimated': '2021-06-11T18:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'arrival': {'airport': 'Tullamarine', 'timezone': 'Australia/Melbourne', 'iata': 'MEL', 'icao': 'YMML', 'terminal': '2', 'gate': '7', 'baggage': None, 'delay': None, 'scheduled': '2021-06-11T20:30:00+00:00', 'estimated': '2021-06-11T20:30:00+00:00', 'actual': None, 'estimated_runway': None, 'actual_runway': None}, 'airline': {'name': 'Air New Zealand', 'iata': 'NZ', 'icao': 'ANZ'}, 'flight': {'number': '129', 'iata': 'NZ129', 'icao': 'ANZ129', 'codeshared': None}, 'aircraft': None, 'live': None}]

bot = commands.Bot(command_prefix='$')

TOKEN = 'ODUzMDk4MTc1MDQzNjAwNDA0.YMQblg.e2dd7DP28hs-I8HH3oy7dZeWORA'


def get_code(city):
    with open('airports.csv', newline='', encoding='UTF8') as airports:
        reader = csv.reader(airports, delimiter=',')
        for row in reader:
            if row[10] == city and row[2] == 'large_airport':
                return (row[13])


def print_full_flights(response, botResponse, userResponse):
    for i in botResponse:
        if i[0] == userResponse:
            flight = i

    flightNo = (flight.rpartition(" ")[0]).partition(" ")[2]

    botResponse = ['```']
    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]
        print(accessVar)
        if accessVar['flight']['icao'] == flightNo:
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
                         + ' Aircraft: ' + aircraft + ' ' + rego + '\n' +
                         'Status: ' + status + ' ' + arrTime + '\n']

            botResponse = botResponse + newFlight
            botResponse = botResponse + ['```']
            botResponse = "".join(botResponse)
            return botResponse


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
    query = {'access_key': 'c4223304f131787d840025bdc3570a46'}
    url = "http://api.aviationstack.com/v1/"
    if len(args) == 3:
        if len(args[1]) == 3 and len(args[2]) == 3:
            if not args[0][0].isupper():
                query['airline_name'] = args[0]
            query['dep_iata'] = args[1].upper()
            query['arr_iata'] = args[2].upper()
        if len(args[1]) > 3:
            if not args[0][0].isupper():
                query['airline_name'] = args[0]
            query['dep_iata'] = get_code(args[1].capitalize())
            query['arr_iata'] = get_code(args[2].capitalize())

    response = requests.get(url + "flights", params=query)
    flight_numbers = []
    botResponse = []
    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]
        flightNo = accessVar['flight']['icao']
        if flightNo in flight_numbers:
            continue
        if accessVar['airline']['name'] != args[0]:
            continue
        flight_numbers.append(flightNo)
        depTime = accessVar['departure']['scheduled'][11:][:5]
        newFlight = [str(flight_numbers.index(flightNo) + 1) + '. ' + flightNo + ' ' + depTime + '\n']
        botResponse = botResponse + newFlight
    numberOfFlights = len(flight_numbers)

    botResponse = ['```' + 'There are ' + str(
        numberOfFlights) + ' flights with your parameters today: ' + '\n'] + botResponse + [
                      "Respond with the number of a flight for more information. E.g. 1 ```"]
    unjoinedBotResponse = botResponse
    botResponse = "".join(botResponse)
    await ctx.send(botResponse)

    userResponse = await bot.wait_for('message')
    await ctx.send(print_full_flights(response, unjoinedBotResponse, userResponse.content))


bot.run(TOKEN)
