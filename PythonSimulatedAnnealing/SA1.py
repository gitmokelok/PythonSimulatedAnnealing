# -*- coding: utf-8 -*-

import math
import random

from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral11

def euc_2d(c1, c2):
    result = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    return result

def cost(permutation, cities):
    distance = 0.0
    for i in range(len(permutation)-1):
        c1 = permutation[i]
        c2 = permutation[i+1]
        distance += euc_2d(cities[c1], cities[c2])
    return distance

def random_permutation(numberOfCities):
    perm = range(numberOfCities)
    random.shuffle(perm)
    return perm

def stochastic_two_opt(route):
    tempRoute = list(route)
    c1 = random.choice(tempRoute)
    tempRoute.remove(c1)
    c2 = random.choice(tempRoute)
    c1Index = route.index(c1)
    c2Index = route.index(c2)
    if c1Index > c2Index:
        c1Index, c2Index = c2Index, c1Index
    tempRouteSlice = list(route[c1Index:c2Index])
    tempRouteSlice.reverse()
    route[c1Index:c2Index] = tempRouteSlice

def create_neighbor(current, cities):
    currentCost = cost(current, cities)
    candidate = list(current)
    stochastic_two_opt(candidate)
    return candidate


def should_accept(candidate, current, temp, cities):
    candidateCost = cost(candidate, cities)
    currentCost = cost(current, cities)
    if candidateCost <= currentCost:
        return True
    else:
        return math.exp((currentCost - candidateCost) / temp) > random.random()


#def search(cities, max_iter, max_temp, temp_change):
#    current = random_permutation(len(cities))
    
#    currentCost = cost(current, cities)
#    temp, best = max_temp, current
#    i = 0
#    while (temp > 0.000001):
#        i += 1 
#        candidate = create_neighbor(current, cities)
#        temp = temp *  (1 - temp_change)
#        #temp = max_temp / (1 + temp_change*i)  #temp_change = 0.001 ilgai skaiciauoja, bet randa geriausia 8127
#        #temp = max_temp / (1 + math.log(1+i))
#        if should_accept(candidate, current, temp, cities):
#            current = candidate
#        if cost(candidate, cities) < cost(best, cities):
#            best = candidate
#        if (i + 1) % 100 == 0:
#            print i+1, temp , cost(best, cities)
#    return best
def splitTspRoute(permutation_woDepo, truckCapacity, demandList_woDepo, cities_woDepo):
    result = list()
    new_route = list()
    new_routeCapacity = 0 
    for customer in permutation_woDepo:
        customerDemand = demandList_woDepo[customer]
        if customer != permutation_woDepo[-1]:
            if (new_routeCapacity + customerDemand) <= truckCapacity:
                new_routeCapacity += customerDemand
                new_route.append(customer)
            else:
                result.append(new_route)
                new_route = list()
                new_routeCapacity = 0
                new_routeCapacity += customerDemand
                new_route.append(customer)
        else:
            if (new_routeCapacity + customerDemand) <= truckCapacity:
                new_route.append(customer)
                result.append(new_route)
            else:
                result.append(new_route)
                new_route = list()
                new_routeCapacity = 0
                new_route.append(customer)
                result.append(new_route)
            
        #if capacity_counter <= truckCapacity:
        #    capacity_counter += demandList_woDepo[customer]
        #    if capacity_counter <= En22k4Capacity:
        #        new_route.append(customer)
        #    else:
        #        capacity_counter = 0
        #        capacity_counter += demandList_woDepo[customer]
        #        result.append(new_route)
        #        new_route = [customer]
        #if customer == permutation_woDepo[-1]:
        #    result.append(new_route)        
    return result

def normalize_route(tspRoute):
    result = list()
    for customer in tspRoute:
        result.append(customer+1)
    return result

def calculateVrpDistance(vrpRoutes, cities_withDepo):
    totalDistance = 0
    for route in vrpRoutes:
        temp = route
        if (temp[-1] != 0 and temp[0] != 0):
            temp.append(0)
            temp.insert(0,0)
        totalDistance += cost(temp, cities_withDepo)
    return totalDistance

def search(citiesNoDepo, max_temp, temp_change, citiesWithDepo, truckCapacity, customerDemands):
    current = random_permutation(len(citiesNoDepo))
    normalizedCurrent = normalize_route(current)
    currentVrp = splitTspRoute(normalizedCurrent, truckCapacity, customerDemands, citiesWithDepo)
    currentVRPCost = calculateVrpDistance(currentVrp, citiesWithDepo)
    currentCost = cost(current, citiesNoDepo)
    temp, best = max_temp, current
    bestVrp = currentVrp
    i = 0
    while (temp > 0.000001):
        i += 1 
        candidate = create_neighbor(current, citiesNoDepo)
        normalizedCandidate = normalize_route(current)
        candidateVrp = splitTspRoute(normalizedCandidate, truckCapacity, customerDemands, citiesWithDepo)
        currentVRPCost = calculateVrpDistance(candidateVrp, citiesWithDepo)
        temp = temp *  (1 - temp_change)
        #temp = max_temp / (1 + temp_change*i)  #temp_change = 0.001 ilgai skaiciauoja, bet randa geriausia 8127
        #temp = max_temp / (1 + math.log(1+i))
        if should_accept(candidate, current, temp, citiesNoDepo):
            current = candidate
            currentVrp = candidateVrp
        if cost(candidate, citiesNoDepo) < cost(best, citiesNoDepo):
            best = candidate
        if calculateVrpDistance(candidateVrp, citiesWithDepo) < calculateVrpDistance(bestVrp, citiesWithDepo):
            bestVrp = candidateVrp

        if (i + 1) % 100 == 0:
            print i+1, temp , calculateVrpDistance(bestVrp, citiesWithDepo)
    return bestVrp

def splitVRProuteIntoTruckDroneRoute(vrpRoute, citiesWithDepo):
    result = dict()
    totalCost = 0
    totalDroneCost = 0
    totalTruckCost = 0
    for truckRoute in vrpRoute:
        route1 = truckRoute[0::2]
        route2 = truckRoute[1::2]
        if route1[-1] != 0:
            route1.append(0)
        if route2[0] != 0:
            route2.insert(0,0)
        if route2[-1] != 0:
            route2.append(0)
        route1cost = cost(route1, citiesWithDepo) 
        route2cost = cost(route2, citiesWithDepo)
        if route1cost > route2cost:
            result['drone{}'.format(vrpRoute.index(truckRoute))] = truckRoute
            result['truck{}'.format(vrpRoute.index(truckRoute))] = route2          
            result['droneRouteCost{}'.format(vrpRoute.index(truckRoute))] = route1cost
            result['truckRouteCost{}'.format(vrpRoute.index(truckRoute))] = route2cost 
            tempDroneRoute = list()
            for city in truckRoute:
                if city not in route2:
                    tempDroneRoute.append(city)
            #totalCost += route2cost
            totalDroneCost += cost(tempDroneRoute, citiesWithDepo)
            totalTruckCost += route2cost
            totalCost += route2cost + cost(tempDroneRoute, citiesWithDepo)
        else:
            result['drone{}'.format(vrpRoute.index(truckRoute))] = truckRoute
            result['truck{}'.format(vrpRoute.index(truckRoute))] = route1
            result['droneRouteCost{}'.format(vrpRoute.index(truckRoute))] = route2cost
            result['truckRouteCost{}'.format(vrpRoute.index(truckRoute))] = route1cost
            tempDroneRoute = list()
            for city in truckRoute:
                if city not in route1:
                    tempDroneRoute.append(city)            
            totalCost += route1cost + cost(tempDroneRoute, citiesWithDepo)
            totalDroneCost += cost(tempDroneRoute, citiesWithDepo)
            totalTruckCost += route1cost
    result['totalVRPDCost'] = totalCost
    result['totalDroneCost'] = totalDroneCost
    result['totalTruckCost'] = totalTruckCost
    return result 

def splitXYcoords(cities):
    xCoords = list()
    yCoords = list()
    for city in cities:
        xCoords.append(city[0])
        yCoords.append(city[1])
    return xCoords, yCoords



# problem configuration
En22k4_withDepo = [[145,215],[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
En22k4_noDepo = [[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
En22k4Demand = [0,1100,700,800,1400,2100,400,800,100,500,600,1200,1300,1300,300,900,2100,1000,900,2500,1800,700]
En22k4Capacity = 6000

'''
Plotting VRP instance methods
'''
def plotDepo(p, cities):
    p.circle(cities[0][0], cities[0][1], legend="Depo", fill_color="red", line_color="red", size=6)

def plotCustomers(p, cities): 
    customersX = list()
    customersY = list()
    for city in cities[1:]:
        customersX.append(city[0])
        customersY.append(city[1])
    p.circle(customersX, customersY, legend="Customers", fill_color="white", line_color="black", size=6) 

def createPlot(nameOfPlot_string):
    output_file("{}_VRP_plot.html".format(nameOfPlot_string))    
    p = figure(
            #tools="pan,box_zoom,reset,save",
            title="{}".format(nameOfPlot_string), 
            x_axis_label='X coordinates', 
            y_axis_label='Y coordinates', 
            plot_width=1024, plot_height=800
            )
    return p

def createPlotWithoutRoutes(nameOfPlot_string,vrpInstanceCities):
    p= createPlot(nameOfPlot_string)
    plotDepo(p, vrpInstanceCities)
    plotCustomers(p, vrpInstanceCities)
    show(p)
   
def plotVRPRoutes(p, Vrpsolution, vrpInstanceCities):
    numberOfRoutes = len(Vrpsolution)
    myPallete = Spectral11[0:numberOfRoutes]
    myPallete2 = Spectral11[numberOfRoutes:numberOfRoutes*2]
    for route in Vrpsolution:
        routeX = list()
        routeY = list()
        for city in route:
            routeX.append(vrpInstanceCities[city][0])
            routeY.append(vrpInstanceCities[city][1])
        p.line(routeX, routeY, line_width=2, line_color=myPallete[Vrpsolution.index(route)])
        p.line(routeX[:2], routeY[:2], line_width=5, line_color=myPallete2[Vrpsolution.index(route)], line_dash="4 4")

def plotVRPTruckDroneRoutes(p, TruckDroneVRPRoutesDictionary, vrpInstanceCities, vrpSolution):
    numberOfRoutes = len(vrpSolution)
    myPallete = Spectral11[0:numberOfRoutes]
    for route in vrpSolution:
        routeIndex = vrpSolution.index(route)
        truckRoute = TruckDroneVRPRoutesDictionary['truck{}'.format(routeIndex)]
        droneRoute = TruckDroneVRPRoutesDictionary['drone{}'.format(routeIndex)]
        routeX = list()
        routeY = list()
        for city in truckRoute:
            routeX.append(vrpInstanceCities[city][0])
            routeY.append(vrpInstanceCities[city][1])
        p.line(routeX, routeY, line_width=2, line_color=myPallete[routeIndex], legend = "Truck{} route".format(routeIndex))
        routeX = list()
        routeY = list()
        for city in droneRoute:
           routeX.append(vrpInstanceCities[city][0])
           routeY.append(vrpInstanceCities[city][1])
        p.line(routeX, routeY, line_width=5, line_color=myPallete[routeIndex], line_dash="4 4", legend = "Drone{} route".format(routeIndex))

def createPlotWithRoutes(nameOfPlot_string,vrpInstanceCities, VRPsolution):
    p = createPlot(nameOfPlot_string)
    plotDepo(p, vrpInstanceCities)
    plotCustomers(p, vrpInstanceCities)
    plotVRPRoutes(p, VRPsolution, vrpInstanceCities)
    show(p)

def createPlotWithTruckDroneRoutes(nameOfPlot_string,vrpInstanceCities, VRPsolution, TruckDroneVRPRoutesDictionary):
    p = createPlot(nameOfPlot_string)
    plotDepo(p, vrpInstanceCities)
    plotCustomers(p, vrpInstanceCities)
    plotVRPTruckDroneRoutes(p, TruckDroneVRPRoutesDictionary, vrpInstanceCities, VRPsolution)
    show(p)

# add some renderers
#p.line(x1, y1, line_width=1, line_color="orange")
#p.line(x2, y2, line_width=1, line_color="green")
#p.line(x3, y3, line_width=1, line_color="yellow")

#p.circle(depoX, depoY, legend="Depo", fill_color="red", line_color="red", size=6 )
#p.circle(x, y, legend="Customers", fill_color="white", line_color="black", size=6)

#p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")
#customers = createCustomers(p, En22k4_withDepo)
#createDepo(p, En22k4_withDepo)
#createCustomers(p, En22k4_withDepo)

# show the results
#show(p)


#En22vrpbestfounfVRPSolution = [[0, 9, 7, 5, 2, 1, 6, 0], [0, 10, 8, 3, 4, 11, 13, 0], [0, 16, 14, 12, 15, 18, 0], [0, 20, 17, 21, 19, 0]]
#createPlotWithRoutes('En22k4 - Instance. Vehicle Routing Problem with Truck only Solution', En22k4_withDepo, En22vrpbestfounfVRPSolution)

#En22k4 = [[145,215],[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
#En22k4noDepo = [[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
#En22k4Demand = [0,1100,700,800,1400,2100,400,800,100,500,600,1200,1300,1300,300,900,2100,1000,900,2500,1800,700]
#En22k4Capacity = 6000

#En23k3 = [[266,235],[295,272],[301,258],[309,260],[217,274],[218,278],[282,267],[242,249],[230,262],[249,268],[256,267],[265,257],[267,242],[259,265],[315,233],[329,252],[318,252],[329,224],[267,213],[275,192],[303,201],[208,217],[326,181]]
#En23k3noDepo = [[295,272],[301,258],[309,260],[217,274],[218,278],[282,267],[242,249],[230,262],[249,268],[256,267],[265,257],[267,242],[259,265],[315,233],[329,252],[318,252],[329,224],[267,213],[275,192],[303,201],[208,217],[326,181]]
#En23k3Demand = [0, 125, 84, 60, 500, 300, 175, 350, 150, 1100, 4100, 225, 300, 250, 500, 150, 100, 250, 120, 600, 500, 175, 75]
#En23k3Capacity = 4500

#En30k3 = [[162,354],[218,382],[218,358],[201,370],[214,371],[224,370],[210,382],[104,354],[126,338],[119,340],[129,349],[126,347],[125,346],[116,355],[126,335],[125,355],[119,357],[115,341],[153,351],[175,363],[180,360],[159,331],[188,357],[152,349],[215,389],[212,394],[188,393],[207,406],[184,410],[207,392]]
#En30k3noDepo = [[218,382],[218,358],[201,370],[214,371],[224,370],[210,382],[104,354],[126,338],[119,340],[129,349],[126,347],[125,346],[116,355],[126,335],[125,355],[119,357],[115,341],[153,351],[175,363],[180,360],[159,331],[188,357],[152,349],[215,389],[212,394],[188,393],[207,406],[184,410],[207,392]]
#En30k3Demand = [0,300,3100,125,100,200,150,150,450,300,100,950,125,150,150,550,150,100,150,400,300,1500,100,300,500,800,300,100,150,1000]
#En30k3Capacity = 4500

#En33k4 = [[292,495],[298,427],[309,445],[307,464],[336,475],[320,439],[321,437],[322,437],[323,433],[324,433],[323,429],[314,435],[311,442],[304,427],[293,421],[296,418],[261,384],[297,410],[315,407],[314,406],[321,391],[321,398],[314,394],[313,378],[304,382],[295,402],[283,406],[279,399],[271,401],[264,414],[277,439],[290,434],[319,433]]
#En33k4noDepo = [[298,427],[309,445],[307,464],[336,475],[320,439],[321,437],[322,437],[323,433],[324,433],[323,429],[314,435],[311,442],[304,427],[293,421],[296,418],[261,384],[297,410],[315,407],[314,406],[321,391],[321,398],[314,394],[313,378],[304,382],[295,402],[283,406],[279,399],[271,401],[264,414],[277,439],[290,434],[319,433]]
#En33k4Demand = [0,700,400,400,1200,40,80,2000,900,600,750,1500,150,250,1600,450,700,550,650,200,400,300,1300,700,750,1400,4000,600,1000,500,2500,1700,1100]
#En33k4Capacity = 8000

#En51k5 = [[30,40],[37,52],[49,49],[52,64],[20,26],[40,30],[21,47],[17,63],[31,62],[52,33],[51,21],[42,41],[31,32],[5,25],[12,42],[36,16],[52,41],[27,23],[17,33],[13,13],[57,58],[62,42],[42,57],[16,57],[8,52],[7,38],[27,68],[30,48],[43,67],[58,48],[58,27],[37,69],[38,46],[46,10],[61,33],[62,63],[63,69],[32,22],[45,35],[59,15],[5,6],[10,17],[21,10],[5,64],[30,15],[39,10],[32,39],[25,32],[25,55],[48,28],[56,37]]
#En51k5noDepo = [[37,52],[49,49],[52,64],[20,26],[40,30],[21,47],[17,63],[31,62],[52,33],[51,21],[42,41],[31,32],[5,25],[12,42],[36,16],[52,41],[27,23],[17,33],[13,13],[57,58],[62,42],[42,57],[16,57],[8,52],[7,38],[27,68],[30,48],[43,67],[58,48],[58,27],[37,69],[38,46],[46,10],[61,33],[62,63],[63,69],[32,22],[45,35],[59,15],[5,6],[10,17],[21,10],[5,64],[30,15],[39,10],[32,39],[25,32],[25,55],[48,28],[56,37]]
#En51k5Demand = [0,7,30,16,9,21,15,19,23,11,5,19,29,23,21,10,15,3,41,9,28,8,8,16,10,28,7,15,14,6,19,11,12,23,26,17,6,9,15,14,7,27,13,11,16,10,5,25,17,18,10]
#En51k5Capacity = 160

En76k7=[[40,40],[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k7noDepo = [[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k7Demand = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]
En76k7Capacity = 220

En76k8 = [[40,40],[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k8noDepo = [[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k8Demand = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]
En76k8Capacity = 180

En76k10 = [[40,40],[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k10noDepo = [[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k10Demand = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]
En76k10Capacity = 140

En76k14 = [[40,40],[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k14noDepo = [[22,22],[36,26],[21,45],[45,35],[55,20],[33,34],[50,50],[55,45],[26,59],[40,66],[55,65],[35,51],[62,35],[62,57],[62,24],[21,36],[33,44],[9,56],[62,48],[66,14],[44,13],[26,13],[11,28],[7,43],[17,64],[41,46],[55,34],[35,16],[52,26],[43,26],[31,76],[22,53],[26,29],[50,40],[55,50],[54,10],[60,15],[47,66],[30,60],[30,50],[12,17],[15,14],[16,19],[21,48],[50,30],[51,42],[50,15],[48,21],[12,38],[15,56],[29,39],[54,38],[55,57],[67,41],[10,70],[6,25],[65,27],[40,60],[70,64],[64,4],[36,6],[30,20],[20,30],[15,5],[50,70],[57,72],[45,42],[38,33],[50,4],[66,8],[59,5],[35,60],[27,24],[40,20],[40,37]]
En76k14Demand = [0,18,26,11,30,21,19,15,16,29,26,37,16,12,31,8,19,20,13,15,22,28,12,6,27,14,18,17,29,13,22,25,28,27,19,10,12,14,24,16,33,15,11,18,17,21,27,19,20,5,22,12,19,22,16,7,26,14,21,24,13,15,18,11,28,9,37,30,10,8,11,3,1,6,10,20]
En76k14Capacity = 100

En101k8 = [[35,35],[41,49],[35,17],[55,45],[55,20],[15,30],[25,30],[20,50],[10,43],[55,60],[30,60],[20,65],[50,35],[30,25],[15,10],[30,5],[10,20],[5,30],[20,40],[15,60],[45,65],[45,20],[45,10],[55,5],[65,35],[65,20],[45,30],[35,40],[41,37],[64,42],[40,60],[31,52],[35,69],[53,52],[65,55],[63,65],[2,60],[20,20],[5,5],[60,12],[40,25],[42,7],[24,12],[23,3],[11,14],[6,38],[2,48],[8,56],[13,52],[6,68],[47,47],[49,58],[27,43],[37,31],[57,29],[63,23],[53,12],[32,12],[36,26],[21,24],[17,34],[12,24],[24,58],[27,69],[15,77],[62,77],[49,73],[67,5],[56,39],[37,47],[37,56],[57,68],[47,16],[44,17],[46,13],[49,11],[49,42],[53,43],[61,52],[57,48],[56,37],[55,54],[15,47],[14,37],[11,31],[16,22],[4,18],[28,18],[26,52],[26,35],[31,67],[15,19],[22,22],[18,24],[26,27],[25,24],[22,27],[25,21],[19,21],[20,26],[18,18]]
En101k8noDepo = [[41,49],[35,17],[55,45],[55,20],[15,30],[25,30],[20,50],[10,43],[55,60],[30,60],[20,65],[50,35],[30,25],[15,10],[30,5],[10,20],[5,30],[20,40],[15,60],[45,65],[45,20],[45,10],[55,5],[65,35],[65,20],[45,30],[35,40],[41,37],[64,42],[40,60],[31,52],[35,69],[53,52],[65,55],[63,65],[2,60],[20,20],[5,5],[60,12],[40,25],[42,7],[24,12],[23,3],[11,14],[6,38],[2,48],[8,56],[13,52],[6,68],[47,47],[49,58],[27,43],[37,31],[57,29],[63,23],[53,12],[32,12],[36,26],[21,24],[17,34],[12,24],[24,58],[27,69],[15,77],[62,77],[49,73],[67,5],[56,39],[37,47],[37,56],[57,68],[47,16],[44,17],[46,13],[49,11],[49,42],[53,43],[61,52],[57,48],[56,37],[55,54],[15,47],[14,37],[11,31],[16,22],[4,18],[28,18],[26,52],[26,35],[31,67],[15,19],[22,22],[18,24],[26,27],[25,24],[22,27],[25,21],[19,21],[20,26],[18,18]]
En101k8Demand = [0,10,7,13,19,26,3,5,9,16,16,12,19,23,20,8,19,2,12,17,9,11,18,29,3,6,17,16,16,9,21,27,23,11,14,8,5,8,16,31,9,5,5,7,18,16,1,27,36,30,13,10,9,14,18,2,6,7,18,28,3,13,19,10,9,20,25,25,36,6,5,15,25,9,8,18,13,14,3,23,6,26,16,11,7,41,35,26,9,15,3,1,2,22,27,20,11,12,10,9,17]
En101k8Capacity = 200

En101k14 = [[35,35],[41,49],[35,17],[55,45],[55,20],[15,30],[25,30],[20,50],[10,43],[55,60],[30,60],[20,65],[50,35],[30,25],[15,10],[30,5],[10,20],[5,30],[20,40],[15,60],[45,65],[45,20],[45,10],[55,5],[65,35],[65,20],[45,30],[35,40],[41,37],[64,42],[40,60],[31,52],[35,69],[53,52],[65,55],[63,65],[2,60],[20,20],[5,5],[60,12],[40,25],[42,7],[24,12],[23,3],[11,14],[6,38],[2,48],[8,56],[13,52],[6,68],[47,47],[49,58],[27,43],[37,31],[57,29],[63,23],[53,12],[32,12],[36,26],[21,24],[17,34],[12,24],[24,58],[27,69],[15,77],[62,77],[49,73],[67,5],[56,39],[37,47],[37,56],[57,68],[47,16],[44,17],[46,13],[49,11],[49,42],[53,43],[61,52],[57,48],[56,37],[55,54],[15,47],[14,37],[11,31],[16,22],[4,18],[28,18],[26,52],[26,35],[31,67],[15,19],[22,22],[18,24],[26,27],[25,24],[22,27],[25,21],[19,21],[20,26],[18,18]]
En101k14noDepo = [[41,49],[35,17],[55,45],[55,20],[15,30],[25,30],[20,50],[10,43],[55,60],[30,60],[20,65],[50,35],[30,25],[15,10],[30,5],[10,20],[5,30],[20,40],[15,60],[45,65],[45,20],[45,10],[55,5],[65,35],[65,20],[45,30],[35,40],[41,37],[64,42],[40,60],[31,52],[35,69],[53,52],[65,55],[63,65],[2,60],[20,20],[5,5],[60,12],[40,25],[42,7],[24,12],[23,3],[11,14],[6,38],[2,48],[8,56],[13,52],[6,68],[47,47],[49,58],[27,43],[37,31],[57,29],[63,23],[53,12],[32,12],[36,26],[21,24],[17,34],[12,24],[24,58],[27,69],[15,77],[62,77],[49,73],[67,5],[56,39],[37,47],[37,56],[57,68],[47,16],[44,17],[46,13],[49,11],[49,42],[53,43],[61,52],[57,48],[56,37],[55,54],[15,47],[14,37],[11,31],[16,22],[4,18],[28,18],[26,52],[26,35],[31,67],[15,19],[22,22],[18,24],[26,27],[25,24],[22,27],[25,21],[19,21],[20,26],[18,18]]
En101k14Demand = [0,10,7,13,19,26,3,5,9,16,16,12,19,23,20,8,19,2,12,17,9,11,18,29,3,6,17,16,16,9,21,27,23,11,14,8,5,8,16,31,9,5,5,7,18,16,1,27,36,30,13,10,9,14,18,2,6,7,18,28,3,13,19,10,9,20,25,25,36,6,5,15,25,9,8,18,13,14,3,23,6,26,16,11,7,41,35,26,9,15,3,1,2,22,27,20,11,12,10,9,17]
En101k14Capacity = 112




class VrpInstance:
    def __init__(self, InstanceName, VrpCities, VrpCitiesNoDepo, Demand, Capacity):
        self.instanceName = InstanceName
        self.cities = VrpCities
        self.citiesNoDepo = VrpCitiesNoDepo
        self.demand = Demand
        self.capacity = Capacity
        
        
#vrpInstance = VrpInstance("E-n22-k4", En22k4, En22k4noDepo, En22k4Demand, En22k4Capacity)
#vrpInstance = VrpInstance("E-n23-k3", En23k3, En23k3noDepo, En23k3Demand, En23k3Capacity)
#vrpInstance = VrpInstance("E-n30-k3", En30k3, En30k3noDepo, En30k3Demand, En30k3Capacity)
#vrpInstance = VrpInstance("E-n33-k4", En33k4, En33k4noDepo, En33k4Demand, En33k4Capacity)
#vrpInstance = VrpInstance("E-n51-k5", En51k5, En51k5noDepo, En51k5Demand, En51k5Capacity)
vrpInstance = VrpInstance("E-n76-k7", En76k7, En76k7noDepo, En76k7Demand, En76k7Capacity)
#vrpInstance = VrpInstance("E-n76-k8", En76k8, En76k8noDepo, En76k8Demand, En76k8Capacity)
#vrpInstance = VrpInstance("E-n76-k10", En76k10, En76k10noDepo, En76k10Demand, En76k10Capacity)
#vrpInstance = VrpInstance("E-n76-k14", En76k14, En76k14noDepo, En76k14Demand, En76k14Capacity)
#vrpInstance = VrpInstance("E-n101-k8", En101k8, En101k8noDepo, En101k8Demand, En101k8Capacity)
#vrpInstance = VrpInstance("E-n101-k14", En101k14, En101k14noDepo, En101k14Demand, En101k14Capacity)



# algorithm configuration
max_iterations = 10000000
max_temp = 1000000000.0
temp_change = 0.003
# execute the algorithm
bestForAllListCost = 1000
bestSolution = list()
#for i in range(100):
#    best1 = search(En22k4_noDepo, max_temp, temp_change, En22k4_withDepo, En22k4Capacity, En22k4Demand)
#    bestResult = calculateVrpDistance(best1, En22k4_withDepo)
#    if bestResult < bestForAllListCost:
#        bestFroAllListCost = bestResult
#        bestSolution = best1
#    i += 1
vidutineReiksme = 0
numberOfRepeatitions = 100
for i in range(numberOfRepeatitions):
    best1 = search(vrpInstance.citiesNoDepo, max_temp, temp_change, vrpInstance.cities, vrpInstance.capacity, vrpInstance.demand)
    bestResult = calculateVrpDistance(best1, vrpInstance.cities)
    vidutineReiksme += bestResult
    if bestResult < bestForAllListCost:
        bestForAllListCost = bestResult
        bestSolution = best1
    i += 1  
#best2 = search(En30k3noDepo, max_temp, temp_change, En30k3, En30k3Capacity, En30k3Demand)
#best3 = search(En51k5noDepo, max_temp, temp_change, En51k5, En51k5Capacity, En51k5Demand)
vidutineReiksme = vidutineReiksme/numberOfRepeatitions
best1 = bestSolution
print "\n************{} VRP Solution********\n".format(vrpInstance.instanceName)

print "Vidutine VRP reiksme:{}; Best Solution: c={}, \nv={}, \nnumber of trucks:{}".format(vidutineReiksme,calculateVrpDistance(best1, vrpInstance.cities), best1, len(best1))
createPlotWithRoutes('{} - testinio pavyzdžio VRP sprendinys'.format(vrpInstance.instanceName), vrpInstance.cities, best1)
vrpDict = splitVRProuteIntoTruckDroneRoute(best1, vrpInstance.cities)
print "\n************{} VRP Solution********\n".format(vrpInstance.instanceName)

print "\n************{} VRP-D Solution********\n".format(vrpInstance.instanceName)
for k,v in vrpDict.items():
    print "{} : {}".format(k, v)
print "\n************{} VRP-D Solution********\n".format(vrpInstance.instanceName)    
createPlotWithTruckDroneRoutes('{} - testinio pavyzdžio VRP-D sprendinys'.format(vrpInstance.instanceName),vrpInstance.cities, best1, vrpDict)

#print "Done. Best Solution: c=#{}, v=#{}, number of trucks:{}".format(calculateVrpDistance(best2, En30k3), best2, len(best2))
#print "Done. Best Solution: c=#{}, v=#{}, number of trucks:{}".format(calculateVrpDistance(best3, En51k5), best3, len(best3))
#createPlotWithRoutes("firstTest",En22k4_withDepo,best1)



#NAME : E-n22-k4
#COMMENT : (Christophides and Eilon, Min no of trucks: 4, Optimal value: 375)
#TYPE : CVRP
#DIMENSION : 22
#EDGE_WEIGHT_TYPE : EUC_2D
#CAPACITY : 6000


#NAME : E-n30-k3
#COMMENT : (Christophides and Eilon, Min no of trucks: 3, Optimal value: 534)
#TYPE : CVRP
#DIMENSION : 30
#EDGE_WEIGHT_TYPE : EUC_2D
#CAPACITY : 4500

#NAME : E-n51-k5
#COMMENT : (Christophides and Eilon, Min no of trucks: 5, Optimal value: 521)
#TYPE : CVRP
#DIMENSION : 51
#EDGE_WEIGHT_TYPE : EUC_2D
#CAPACITY : 160




#def splitTspRoute(permutation_woDepo, truckCapacity, demandList_woDepo, cities_woDepo):
#    result = list()
#    new_route = list()
#    capacity_counter = 0
#    for customer in permutation_woDepo:
#        if capacity_counter <= truckCapacity:
#            capacity_counter += demandList_woDepo[customer]
#            if capacity_counter <= En22k4Capacity:
#                new_route.append(customer)
#            else:
#                capacity_counter = 0
#                capacity_counter += demandList_woDepo[customer]
#                result.append(new_route)
#                new_route = [customer]
#        if customer == permutation_woDepo[-1]:
#            result.append(new_route)        
#    return result

#def normalize_route(tspRoute):
#    result = list()
#    for customer in tspRoute:
#        result.append(customer+1)
#    return result

#def calculateVrpDistance(vrpRoutes, cities_withDepo):
#    totalDistance = 0
#    for route in vrpRoutes:
#        temp = route
#        temp.append(0)
#        temp.insert(0,0)
#        totalDistance += cost(temp, cities_withDepo)
#    return totalDistance
                
#best1 = normalize_route(best1)
#best_Optimal = [[17, 20, 18, 15, 12],[16, 19, 21, 14], [13, 11, 4, 3, 8, 10],[9, 7, 5, 2, 1, 6]] #COST 375
#vrp1routes =  splitTspRoute(best1, En22k4Capacity, En22k4Demand, En22k4_withDepo)

#print calculateVrpDistance(vrp1routes, En22k4_withDepo), vrp1routes

#for route in best_Optimal:
#    temp = route
#    temp.append(0)
#    temp.insert(0,0)
#    totalDistance += cost(temp, En22k4_withDepo)
    

#  c1, c2 = rand(perm.size), rand(perm.size)
#  exclude = [c1]
#  exclude << ((c1==0) ? perm.size-1 : c1-1)
#  exclude << ((c1==perm.size-1) ? 0 : c1+1)
#  c2 = rand(perm.size) while exclude.include?(c2)
#  c1, c2 = c2, c1 if c2 < c1
#  perm[c1...c2] = perm[c1...c2].reverse
#  return perm
# end

'''Best instance E-n22-k4 Results Start
#Best instance E-n22-k4 Results Start

#Done. Best Solution: c=#398.82218147, 
#v=#[[0, 9, 7, 5, 2, 1, 6, 0], 
#[0, 10, 8, 3, 4, 11, 13, 0], 
#[0, 16, 14, 12, 15, 18, 0], 
#[0, 20, 17, 21, 19, 0]], number of trucks:4
#{'totalDroneCost': 149.10489795390905, 
#'truck1': [0, 10, 3, 11, 0], 
#'truck0': [0, 7, 2, 6, 0], 
#'truck3': [0, 17, 19, 0], 
#'truck2': [0, 14, 15, 0], 
#'truckRouteCost2': 45.31952454318206, 
#'truckRouteCost3': 71.0584859939078, 
#'truckRouteCost0': 101.35524090731407, 
#'truckRouteCost1': 92.12004512982375, 
#'droneRouteCost3': 81.44261686028034, 
#'totalVRPDCost': 458.9581945281367, 
#'drone3': [0, 20, 17, 21, 19, 0], 
#'drone0': [0, 9, 7, 5, 2, 1, 6, 0], 
#'drone1': [0, 10, 8, 3, 4, 11, 13, 0], 
#'drone2': [0, 16, 14, 12, 15, 18, 0], 
#'droneRouteCost2': 82.81703802837868, 'droneRouteCost1': 97.33612157881626, 
#'totalTruckCost': 309.85329657422767, 'droneRouteCost0': 108.83326560735341}
'''
'''Best instance E-n30-k4 Results Start
c=555.704050543, 
v=[[0, 26, 28, 27, 29, 25, 24, 1, 5, 0], 
[0, 2, 4, 6, 3, 22, 20, 19, 18, 0], 
[0, 23, 10, 15, 16, 13, 7, 17, 9, 11, 12, 8, 14, 0], 
[0, 21, 0]], number of trucks:4
{'totalDroneCost': 199.84389141103657, 
'truck1': [0, 4, 3, 20, 18, 0], 
'truck0': [0, 26, 27, 25, 1, 0], 
'truck3': [0, 0], 
'truck2': [0, 23, 15, 13, 17, 11, 8, 0], 
'truckRouteCost2': 122.8000374003219, 'truckRouteCost3': 0.0, 
'truckRouteCost0': 158.92020668246738, 'truckRouteCost1': 128.9534608980116, 
'droneRouteCost3': 46.389654018972806, 'totalVRPDCost': 610.5175963918374, 
'drone3': [0, 21, 0], 
'drone0': [0, 26, 28, 27, 29, 25, 24, 1, 5, 0], 
'drone1': [0, 2, 4, 6, 3, 22, 20, 19, 18, 0], 
'drone2': [0, 23, 10, 15, 16, 13, 7, 17, 9, 11, 12, 8, 14, 0], 
'droneRouteCost2': 142.2351373464056, 'droneRouteCost1': 144.8717576466315, 
'totalTruckCost': 410.6737049808009, 'droneRouteCost0': 182.97164172026044}
'''

''' En51k5 instance best result
Done. Best Solution: c=596.536215517, 
v=[[0, 45, 33, 39, 30, 34, 21, 16, 50, 9, 10, 49, 0], 
[0, 38, 5, 37, 17, 15, 44, 42, 19, 40, 41, 13, 0], 
[0, 25, 14, 18, 4, 47, 12, 46, 0], 
[0, 6, 24, 43, 23, 7, 26, 8, 48, 27, 11, 0], 
[0, 32, 1, 22, 31, 28, 3, 36, 35, 20, 2, 29, 0]], number of trucks:5
{'totalVRPDCost': 735.5488964377674, 
'truck4': [0, 1, 31, 3, 35, 2, 0], 
'truck1': [0, 5, 17, 44, 19, 41, 0], 
'truck0': [0, 45, 39, 34, 16, 9, 49, 0], 
'truck3': [0, 6, 43, 7, 8, 27, 0], 
'truck2': [0, 25, 18, 47, 46, 0], 
'truckRouteCost2': 54.464953311139354, 'truckRouteCost3': 82.85992158487757, 
'truckRouteCost0': 118.12524440010388, 'truckRouteCost1': 90.04770650616192, 
'truckRouteCost4': 96.88247712758404, 'droneRouteCost4': 103.55460603846691, 
'droneRouteCost1': 122.20994356072077, 'droneRouteCost0': 123.22573555010429, 
'droneRouteCost3': 97.26751505274743, 'droneRouteCost2': 56.59153593071337, 
'totalDroneCost': 293.1685935079007, 
'drone4': [0, 32, 1, 22, 31, 28, 3, 36, 35, 20, 2, 29, 0], 
'drone0': [0, 45, 33, 39, 30, 34, 21, 16, 50, 9, 10, 49, 0], 
'drone1': [0, 38, 5, 37, 17, 15, 44, 42, 19, 40, 41, 13, 0], 
'drone2': [0, 25, 14, 18, 4, 47, 12, 46, 0], 
'drone3': [0, 6, 24, 43, 23, 7, 26, 8, 48, 27, 11, 0], 
'totalTruckCost': 442.38030292986673}
'''