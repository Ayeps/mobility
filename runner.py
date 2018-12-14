#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

import paho.mqtt.client as mqtt
import time
import json

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

global state
state = ""
global dataJson

def run():
    global mqttClient
    global traci
    global state
    """execute the TraCI control loop"""
    step = 0

# TAXI 1 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("279297476","279297476").edges
    print("route:::: ", route)
    traci.route.add("taxi1Start", route)
    traci.vehicle.add('taxi1', "taxi1Start")
    traci.vehicle.setColor('taxi1', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi1", "279297476", 5.0, flags=traci.constants.STOP_PARKING)

# TAXI 2 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("-167299074#1","66478404#2").edges
    traci.route.add("taxi2Start", route)
    traci.vehicle.add('taxi2', "taxi2Start")
    traci.vehicle.setColor('taxi2', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi2", "-167299074#1", 5.0, flags=traci.constants.STOP_PARKING)

# TAXI 3 ######
#   findRoute(self, fromEdge, toEdge, vType='', depart=-1.0, routingMode=0)
    route = traci.simulation.findRoute("270055655","66478404#2").edges
    traci.route.add("taxi3Start", route)
    traci.vehicle.add('taxi3', "taxi3Start")
    traci.vehicle.setColor('taxi3', (255,0,0))
    # setStop(self, vehID, edgeID, pos=1.0, laneIndex=0...)
    traci.vehicle.setStop("taxi3", "270055655", 5.0, flags=traci.constants.STOP_PARKING)


    
    cars = []

    while traci.simulation.getMinExpectedNumber() > 0:
#    while step < 1000:
        traci.simulationStep()
        print(step)
        vehs = traci.vehicle.getIDList()
#        print(vehs)
        pos = {}
#        for v in vehs:
        for name in ["taxi1"]:#, "taxi2", "taxi3"]:
            pos2D = traci.vehicle.getPosition(name)
            pos[name] = traci.simulation.convertGeo(pos2D[0], pos2D[1])
            #convertRoad(self, x, y, isGeo=False)
            topic = "pos/slovenia/ljubljana"
            payload = json.dumps({"id":name, "lon":pos[name][0], "lat":pos[name][1]})
            

#            edgeIDt1 = traci.simulation.convertRoad(14.48367, 46.04032, True)
#            print("::::::: ", edgeIDt1)
#            edgeIDt2 = traci.simulation.convertRoad(14.48507, 46.04064, True)
#            print("::::::: ", edgeIDt2)
#            edgeIDt3 = traci.simulation.convertRoad(14.49044, 46.04335, True)
#            print("::::::: ", edgeIDt3)
##            traci.vehicle.getAdaptedTraveltime("taxi1", time, edgeID)
#            print("traveltime", traci.vehicle.getAdaptedTraveltime("taxi1", 0, edgeIDt1[0]))
#            print("traveltime", traci.vehicle.getAdaptedTraveltime("taxi1", 0, edgeIDt2[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt1[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt2[0]))
#            print("adaptedTraveltime after adaption in interval (check time 0)", traci.edge.getTraveltime(edgeIDt3[0]))
#
#            route1 = traci.simulation.findRoute("279297476",edgeIDt1[0]).edges
#            route2 = traci.simulation.findRoute("279297476",edgeIDt2[0]).edges
#            print("kkkkk: ",route)
#            time = 0
#            for edge in route1 :
#               time += traci.edge.getTraveltime(edge)
#            print("time111: ",time)
#            time = 0
#            for edge in route2 :
#               time += traci.edge.getTraveltime(edge)
#            print("time2222: ",time)




#           print("convertGeo2D", traci.simulation.convertGeo(pos["taxi1"][0], pos["taxi1"][1], True))
            print("------------")
            print(payload)
            if(step%1 == 0):
                mqttClient.publish(topic, payload)
#            print(pos[v])
#        print(vehs)
#        if step == 40:
        if state == "request":
            state_ = state
            state = ""
            stateAction(state_)

#            for veh in ["taxi1"]:#, "taxi2", "taxi3"]:
 
            print("----------------------------------")
            print("We are in 40s")
            print("----------------------------------")
#            if traci.vehicle.getSpeed("right_0") == 0:
#                traci.vehicle.resume("right_0")
            # changeTarget(vehicleID, edgeID) - can make turns
#            traci.vehicle.changeTarget("right_0", "04")
            # setRoute(self, vehID, edgeList) ex:setRoute('1', ['1', '2', '4'])
#            traci.vehicle.setRoute("right_0", ["10", "03", "30"])
            # setRouteID(self, vehID, routeID)
#            traci.vehicle.setRouteID("right_0", "down")
#            newRoute = traci.simulation.findRoute("279297476", "39726119#0").edges
#            edgeID = traci.simulation.convertRoad(14.49634, 46.04794, True)
#            edgeID = traci.simulation.convertRoad(14.49278, 46.04561, True)
            edgeID = traci.simulation.convertRoad(14.47917, 46.04494, True)
#            newRoute = traci.simulation.findRoute("279297476", edgeID[0]).edges
            currentEdge = traci.vehicle.getRoadID("taxi1")
            print("ROAD:::", currentEdge)
##            newRoute = traci.simulation.findRoute(currentEdge, "66478404#2").edges
            newRoute = traci.simulation.findRoute(currentEdge, edgeID[0]).edges
            print("nova rutaaaaa: ", newRoute)
            traci.vehicle.setRoute("taxi1", newRoute)
            traci.vehicle.setStop("taxi1", edgeID[0], flags=traci.constants.STOP_PARKING)
###            traci.vehicle.setStop("taxi1", "66478404#2", flags=traci.constants.STOP_PARKING)
            if traci.vehicle.getSpeed("taxi1") == 0:
                traci.vehicle.resume("taxi1")
        step += 1
    mqttClient.disconnect()
    mqttClient.loop_stop()
    traci.close()
    sys.stdout.flush()

def stateAction(state):
    global dataJson
    if(state == "request"):
        print("ok")
        vehEdgeID = traci.vehicle.getRoadID("taxi1")
        edgeIDt1 = traci.simulation.convertRoad(dataJson["myLon"], dataJson["myLat"], True)
        print("::::::: ", edgeIDt1[0])
#        route1 = traci.simulation.findRoute("279297476",edgeIDt1[0]).edges
#        route2 = traci.simulation.findRoute("279297476",edgeIDt2[0]).edges
#        print("kkkkk: ",route)
#        time = 0
#        for edge in route1 :
#           time += traci.edge.getTraveltime(edge)
#        print("time111: ",time)

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("req/slovenia/#")
    print("Subscribed")

# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    global traci
    global state
    global dataJson
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    if msg.topic == "req/slovenia/ljubljana":
        dataJson = json.loads(msg.payload)
        state = "request"
#        vehs = traci.vehicle.getIDList()
#        for v in vehs:
#        for veh in ["taxi1"]:#, "taxi2", "taxi3"]:
#            pos2D = traci.vehicle.getPosition("taxi1")
#            print("POSSSS:",pos2D)
#            print("bbbbbbbbbbbbbbbb")
#            vehEdgeID = traci.vehicle.getRoadID("taxi1")
#            print("VEssssssss:",vehEdgeID)
#            topic = "pos/slovenia/ljubljana"
#            payload = json.dumps({"id":veh, "lon":pos[veh][0], "lat":pos[veh][1]})

    print("Topic: " + msg.topic)
    print("payload: " + msg.payload)
#    if traci.vehicle.getSpeed("right_0") == 0:
#        traci.vehicle.resume("right_0")
#    traci.vehicle.setRoute("right_0", ["10", "03", "30"])
#    traci.vehicle.setStop("right_0", "30", 400.0, flags=traci.constants.STOP_PARKING)


def main():
    global mqttClient
    mqttClient = mqtt.Client("mobiClient")
    mqttClient.on_connect = mqtt_on_connect
    mqttClient.on_message = mqtt_on_message

    mqttClient.connect("178.62.252.50", port=1883, keepalive=60)

    # Loop forever
    try:
#        mqttClient.loop_forever()
        mqttClient.loop_start()
        run()


    # Catches SigINT
    except KeyboardInterrupt:
        mqttClient.disconnect()
        print("Exiting main thread")
        time.sleep(2.0)



# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
#    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    global traci
    traci.start([sumoBinary, "-c", "data/cross.sumocfg", "--collision.check-junctions","true","--collision.action","teleport"])
#    run()
    main()
