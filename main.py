#TODO: ADD COMMENTS!

import datetime
import pycountry
import discord
import requests
import random
import csv
import pytz
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

TOKEN = 'REDACTED'


def get_code(city):
    listOfAirports = []
    with open('airports.csv', newline='', encoding='UTF8') as airports:
        reader = csv.reader(airports, delimiter=',')
        for row in reader:
            if row[10].lower() == city.lower() and (row[2] == 'large_airport' or row[2] == 'medium_airport'):
                listOfAirports.append([row[13], ' ', pycountry.countries.get(alpha_2=row[8]).name, ' ', row[3]])
    return listOfAirports


def get_progress(depTimeZone, arrTimeZone, estDep, estArr, delay):
    return


def print_full_flights(response, botResponse="", userResponse="", flight=0):
    for i in botResponse:
        if i[0] == userResponse:
            flight = i
    if botResponse != "":
        flightNo = (flight.rpartition(" ")[0]).partition(" ")[2]
    else:
        flightNo = flight.upper()

    botResponse = ['```']
    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]

        if accessVar['flight']['iata'] == flightNo:
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
                if accessVar['aircraft']['icao'][0] == 'B':
                    make = 'Boeing'
                elif accessVar['aircraft']['icao'][0] == 'A':
                    make = 'Airbus'
            except TypeError:
                aircraft = 'Unknown'
                rego = 'N/A'
            status = accessVar['flight_status']
            arrTime = accessVar['arrival']['scheduled'][11:][:5]
            depTimeZone = accessVar['departure']['timezone']
            arrTimeZone = accessVar['arrival']['timezone']
            estDep = accessVar['departure']['estimated'][11:][:5]
            estArr = accessVar['arrival']['estimated'][11:][:5]
            delay = accessVar['departure']['delay']

            if status == 'active':
                get_progress(depTimeZone, arrTimeZone, estDep, estArr, delay)

            newFlight = [
                "\nAirline: {} \nFlight Number: {} \nStatus: {} \n \nDEPARTURE \nDeparture: {} \nTerminal: {} \nGate: {} \nScheduled Time: {} \n \n".format(
                    airline, flightNo, status, depAirport, depTerminal, str(depGate).replace("None", "Unknown"),
                    depTime)
                + "ARRIVAL \nArrival: {} \nTerminal: {} \nGate: {} \nBaggage Carousel: {} \nScheduled Time: {} \n \n".format(
                    arrAirport, str(arrTerminal).replace("None", "Unknown"), str(arrGate).replace("None", "Unknown"),
                    str(arrBags).replace("None", "Unknown"), arrTime)
                + "AIRCRAFT \nMake: {} \nModel: {} \nRegistration: {}".format(make, aircraft, rego)]


            pictureLink = "https://www.jetphotos.com/photo/keyword/" + rego

            botResponse = botResponse + newFlight
            botResponse = botResponse + ['```']
            botResponse = "".join(botResponse)
            toReturn = [botResponse, pictureLink]
            print(toReturn)
            return toReturn


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
async def flightHelp(ctx):
    text = ["```" + 'Welcome to HeadsUp! The bot currently supports the following commands: \n' +
            '\n$flight Airline <IATA ORIGIN AIRPORT CODE E.G. AKL> <IATA DESTINATION AIRPORT CODE E.G. SYD> \n' +
            '\n$flight Airline <Origin City E.G. Auckland> <Destination City E.G. Sydney> \n' +
            '\n$flight <FLIGHT NUMBER> E.G. $flight AA1'
            '\n$flightAbout\n' +
            '\nIf a name has several words, type it within speech marks E.G. "Air New Zealand" "Los Angeles" \n' +
            'To respond to the bot with an option selection, simply type the singular number E.G. 1 \n' +
            '\nKnown Issues: ' +
            '\n-The API returns some airlines in an unnatural fashion, so some searches may not work E.G. Air China is returned as Air China LTD```']
    await ctx.send(text[0])


@bot.command()
async def flightAbout(ctx):
    text = ["```" + 'HeadsUp V0.1.2 2021\n' +
            '\nWritten By Nikita Roumiantsev in Auckland, New Zealand\n' +
            '\nPowered by Aviation Stack \n' + "```"]
    await ctx.send(text[0])


@bot.command()
async def flight(ctx, *args):
    query = {'access_key': 'REDACTED'}
    url = "http://api.aviationstack.com/v1/"
    if len(args) == 1:
        query['flight_iata'] = args[0].upper()
    elif len(args) == 3:
        if len(args[1]) == 3 and len(args[2]) == 3:
            if not args[0][0].isupper():
                query['airline_name'] = args[0]
            query['dep_iata'] = args[1].upper()
            query['arr_iata'] = args[2].upper()
        if len(args[1]) > 3:
            if not args[0][0].isupper():
                query['airline_name'] = args[0]
            depAirportList = get_code(args[1])
            arrAirportList = get_code(args[2])
            if len(depAirportList) != 1:
                await ctx.send("Please select the departure airport: ")
                toPrint = ['```']
                for i in range(len(depAirportList)):
                    toPrint = toPrint + [str(i + 1)] + [". "] + depAirportList[i] + ["\n"]
                toPrint += ['```']
                await ctx.send("".join(toPrint))
                userResponse = await bot.wait_for('message')
                query['dep_iata'] = depAirportList[int(userResponse.content) - 1][0]
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
    response = requests.get(url + "flights", params=query)
    if len(args) == 1:

        detailedFlight = print_full_flights(response, "", "", args[0])
        if detailedFlight == None:
            await ctx.send('```' + 'There are no flights with your parameters today.' + '```')
        await ctx.send(detailedFlight[0])
        if detailedFlight[1][-3:] != 'N/A':
            await ctx.send(detailedFlight[1])
        return


    flight_numbers = []
    botResponse = []
    for i in range(len(response.json()['data'])):
        accessVar = response.json()['data'][i]
        flightNo = accessVar['flight']['iata']
        if flightNo in flight_numbers:
            continue
        if accessVar['airline']['name'] != args[0] and len(args) != 1:
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
            numberOfFlights) + ' ' + args[0] + " flight from " + query['dep_iata'] + ' to ' + query[
                           'arr_iata'] + ' today: ' + '\n'] + botResponse + [
                          "Select it for more information.  ```"]
    else:
        botResponse = ['```' + 'There are ' + str(
            numberOfFlights) + ' ' + args[0] + " flights from " + query['dep_iata'] + ' to ' + query[
                           'arr_iata'] + ' today: ' + '\n'] + botResponse + [
                          "Select one for more information. ```"]
    unjoinedBotResponse = botResponse
    botResponse = "".join(botResponse)
    await ctx.send(botResponse)

    userResponse = await bot.wait_for('message')
    detailedFlight = print_full_flights(response, unjoinedBotResponse, userResponse.content)
    await ctx.send(detailedFlight[0])
    if detailedFlight[1][-3:] != 'N/A':
        await ctx.send(detailedFlight[1])


bot.run(TOKEN)
