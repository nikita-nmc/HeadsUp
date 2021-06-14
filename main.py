import discord
import requests
import random
import csv
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

TOKEN = 'ODUzMDk4MTc1MDQzNjAwNDA0.YMQblg.e2dd7DP28hs-I8HH3oy7dZeWORA'


def get_code(city):
    listOfAirports = []
    with open('airports.csv', newline='', encoding='UTF8') as airports:
        reader = csv.reader(airports, delimiter=',')
        for row in reader:
            if row[10] == city and row[2] == 'large_airport':
                listOfAirports.append([row[13], ' ', row[3]])
    return listOfAirports


def print_full_flights(response, botResponse, userResponse):

    for i in botResponse:
        if i[0] == userResponse:
            flight = i

    flightNo = (flight.rpartition(" ")[0]).partition(" ")[2]

    botResponse = ['```']
    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]
        if accessVar['flight']['icao'] == flightNo:
            airline = accessVar['airline']['name']
            depAirport = accessVar['departure']['airport']
            depTerminal = accessVar['departure']['terminal']
            depGate = accessVar['departure']['gate']
            depTime = accessVar['departure']['scheduled'][11:][:5]
            arrAirport = accessVar['arrival']['airport']
            arrTerminal = accessVar['arrival']['terminal']
            arrGate = accessVar['arrival']['gate']
            arrBags = accessVar['arrival']['baggage']
            make = 'Unknown'
            try:
                aircraft = accessVar['aircraft']['icao'][1:]
                rego = accessVar['aircraft']['registration']
                if aircraft[0] == 'B':
                    make = 'Boeing'
                elif aircraft[0] == 'A':
                    make = 'Airbus'
            except TypeError:
                aircraft = 'Unknown'
                rego = 'N/A'
            status = accessVar['flight_status']
            arrTime = accessVar['arrival']['scheduled'][11:][:5]

            newFlight = [
                "\nAirline: {} \nFlight Number: {} \nStatus: {} \n \nDEPARTURE \nDeparture: {} \nTerminal: {} \nGate: {} \nScheduled Time: {} \n \n".format(
                    airline, flightNo, status, depAirport, depTerminal, str(depGate).replace("None", "Unknown"), depTime)
                + "ARRIVAL \nArrival: {} \nTerminal: {} \nGate: {} \nBaggage Carousel: {} \nScheduled Time: {} \n \n".format(
                    arrAirport, str(arrTerminal).replace("None", "Unknown"), str(arrGate).replace("None", "Unknown"), str(arrBags).replace("None", "Unknown"), arrTime)
                + "AIRCRAFT \nMake: {} \nModel: {} \nRegistration: {}".format(make, aircraft, rego)]

            pictureLink = "https://www.jetphotos.com/photo/keyword/" + rego

            botResponse = botResponse + newFlight
            botResponse = botResponse + ['```']
            botResponse = "".join(botResponse)
            toReturn = [botResponse, pictureLink]
            return toReturn


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ooga(ctx):
    await ctx.send('Booga')

@bot.command()
async def hello(ctx):
    greetings = ["Hello!", "Hi!", "Hey!", "Hiya!", "Heya!"]
    await ctx.send(random.choice(greetings))

@bot.command()
async def flightHelp(ctx):
    text = ["```" + 'Welcome to Heads Up! The bot currently supports the following commands: \n' +
            '\n$flight Airline <IATA ORIGIN AIRPORT CODE E.G. AKL> <IATA DESTINATION AIRPORT CODE E.G. SYD> \n' +
            '\n$flight Airline <Origin City E.G. Auckland> <Destination City E.G. Sydney> \n' +
            '\n$flightAbout\n'
            '\nIf the airline name has several words, type it within speech marks E.G. "Air New Zealand" \n' +
            'To respond to the bot with an option selection, simply type the singular number E.G. 1 \n' +
            '\nKnown Issues: ' +
            '\n-The API returns some airlines in lowercase letters, some user searches may not be recognized as a result E.G. Jetstar is only recognised as jetstar```']
    await ctx.send(text[0])

@bot.command()
async def flightAbout(ctx):
    text = ["```" + 'Heads Up V0.1.1 2021\n' +
            '\nWritten By Nikita Roumiantsev in Auckland, New Zealand\n' +
            '\nPowered by Aviation Stack \n' + "```"]
    await ctx.send(text[0])

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
            depAirportList = get_code(args[1].capitalize())
            arrAirportList = get_code(args[2].capitalize())
            if len(depAirportList) != 1:
                await ctx.send("Please select the departure airport: ")
                toPrint = ['```']
                for i in range(len(depAirportList)):
                    toPrint = toPrint + [str(i+1)] + [". "] + depAirportList[i] + ["\n"]
                toPrint += ['```']
                await ctx.send("".join(toPrint))
                userResponse = await bot.wait_for('message')
                query['dep_iata'] = depAirportList[int(userResponse.content)-1][0]
            else:
                query['dep_iata'] = get_code(args[1].capitalize())[0][0]
            if len(arrAirportList) != 1:
                await ctx.send("Please select the arrival airport: ")
                toPrint = ['```']
                for i in range(len(arrAirportList)):
                    toPrint = toPrint + [str(i + 1)] + [". "] + arrAirportList[i] + ["\n"]
                toPrint += ['```']
                await ctx.send("".join(toPrint))
                userResponse = await bot.wait_for('message')
                query['arr_iata'] = arrAirportList[int(userResponse.content) - 1][0]
            else:
                query['arr_iata'] = get_code(args[2].capitalize())[0][0]
    print(query)
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
    if numberOfFlights == 0:
        botResponse = ['```' + 'There are no flights with your parameters today.' + '```']
    elif numberOfFlights == 1:
        botResponse = ['```' + 'There is ' + str(
            numberOfFlights) + ' flight with your parameters today: ' + '\n'] + botResponse + [
                        "Respond with the number of a flight for more information. E.g. 1 ```"]
    else:
        botResponse = ['```' + 'There are ' + str(
            numberOfFlights) + ' flights with your parameters today: ' + '\n'] + botResponse + [
                        "Respond with the number of the flight for more information. E.g. 1 ```"]
    unjoinedBotResponse = botResponse
    botResponse = "".join(botResponse)
    await ctx.send(botResponse)

    userResponse = await bot.wait_for('message')
    detailedFlight = print_full_flights(response, unjoinedBotResponse, userResponse.content)
    # print(detailedFlight[0])
    await ctx.send(detailedFlight[0])
    if detailedFlight[1][-3:] != 'N/A':
        await ctx.send(detailedFlight[1])


bot.run(TOKEN)
