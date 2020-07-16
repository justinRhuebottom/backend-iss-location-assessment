#!/usr/bin/env python

import sys
import requests
import turtle
import time

__author__ = 'Justin Rhuebottom'

def getAstronauts():
    r = requests.get('http://api.open-notify.org/astros.json')
    if r.status_code != 200:
        sys.exit("Could not retrieve astronaut data")
    
    astronauts = r.json()["people"]

    print("There are " + str(len(astronauts)) + " astronauts currently in space.")
    for astronaut in astronauts:
        print(astronaut['name'] + ": " + astronaut['craft'])

def obtainGeo():
    r = requests.get('http://api.open-notify.org/iss-now.json')
    if r.status_code != 200:
        sys.exit("Could not retrieve geographic data")
    timestamp = r.json()["timestamp"]
    position = r.json()["iss_position"]
    
    return timestamp, position

def worldMap(geo_info):

    # Get passover time for Indianapolis and decode the response to a readable format

    r = requests.get('http://api.open-notify.org/iss-pass.json', params={"lat": 39.7684, "lon": -86.1581})
    passoverTime = time.ctime(r.json()["response"][0]['risetime'])

    # Register screen and turtle
    ts = turtle.Screen()
    ts.register_shape("iss.gif")
    ts.setup(720,360)
    ts.setworldcoordinates(-180,-80,180,80)
    ts.bgpic("map.gif")
    shelly = turtle.Turtle(shape="iss.gif")
    shelly.color("yellow")
    shelly.penup()

    # Make a dot over Indianapolis

    shelly.goto(-86.1581, 39.7684 )
    shelly.dot(size=8)
    shelly.write(passoverTime)


    # Stop drawing and move the turtle to the ISS Location
    shelly.goto(float(geo_info[1]['longitude']), float(geo_info[1]['latitude']))

    ts.mainloop()
    pass

def main():
    getAstronauts()
    geo_info = obtainGeo()
    worldMap(geo_info)


if __name__ == '__main__':
    main()
