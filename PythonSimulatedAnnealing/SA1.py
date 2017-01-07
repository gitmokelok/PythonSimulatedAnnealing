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
    for truckRoute in vrpRoute:
        route1 = truckRoute[0::2]
        route2 = truckRoute[1::2]
        if route1[-1] != 0:
            route1.append(0)
        if route2[0] != 0:
            route2.insert(0,0)
        if route2[-1] != 0:
            route2.append(0)
        if cost(route1, citiesWithDepo) > cost(route2, citiesWithDepo):
            result['drone{}'.format(vrpRoute.index(truckRoute))] = truckRoute
            result['truck{}'.format(vrpRoute.index(truckRoute))] = route2
        else:
            result['drone{}'.format(vrpRoute.index(truckRoute))] = truckRoute
            result['truck{}'.format(vrpRoute.index(truckRoute))] = route1
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
            tools="pan,box_zoom,reset,save",
            title="{}_Instance".format(nameOfPlot_string), 
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
        p.line(routeX, routeY, line_width=2, line_color=myPallete[routeIndex])
        routeX = list()
        routeY = list()
        for city in droneRoute:
           routeX.append(vrpInstanceCities[city][0])
           routeY.append(vrpInstanceCities[city][1])
        p.line(routeX, routeY, line_width=5, line_color=myPallete[routeIndex], line_dash="4 4")

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



En30k3 = [[162,354],[218,382],[218,358],[201,370],[214,371],[224,370],[210,382],[104,354],[126,338],[119,340],[129,349],[126,347],[125,346],[116,355],[126,335],[125,355],[119,357],[115,341],[153,351],[175,363],[180,360],[159,331],[188,357],[152,349],[215,389],[212,394],[188,393],[207,406],[184,410],[207,392]]
En30k3noDepo = [[218,382],[218,358],[201,370],[214,371],[224,370],[210,382],[104,354],[126,338],[119,340],[129,349],[126,347],[125,346],[116,355],[126,335],[125,355],[119,357],[115,341],[153,351],[175,363],[180,360],[159,331],[188,357],[152,349],[215,389],[212,394],[188,393],[207,406],[184,410],[207,392]]
En30k3Demand = [0,300,3100,125,100,200,150,150,450,300,100,950,125,150,150,550,150,100,150,400,300,1500,100,300,500,800,300,100,150,1000]
En30k3Capacity = 4500

En51k5 = [[30,40],[37,52],[49,49],[52,64],[20,26],[40,30],[21,47],[17,63],[31,62],[52,33],[51,21],[42,41],[31,32],[5,25],[12,42],[36,16],[52,41],[27,23],[17,33],[13,13],[57,58],[62,42],[42,57],[16,57],[8,52],[7,38],[27,68],[30,48],[43,67],[58,48],[58,27],[37,69],[38,46],[46,10],[61,33],[62,63],[63,69],[32,22],[45,35],[59,15],[5,6],[10,17],[21,10],[5,64],[30,15],[39,10],[32,39],[25,32],[25,55],[48,28],[56,37]]
En51k5noDepo = [[37,52],[49,49],[52,64],[20,26],[40,30],[21,47],[17,63],[31,62],[52,33],[51,21],[42,41],[31,32],[5,25],[12,42],[36,16],[52,41],[27,23],[17,33],[13,13],[57,58],[62,42],[42,57],[16,57],[8,52],[7,38],[27,68],[30,48],[43,67],[58,48],[58,27],[37,69],[38,46],[46,10],[61,33],[62,63],[63,69],[32,22],[45,35],[59,15],[5,6],[10,17],[21,10],[5,64],[30,15],[39,10],[32,39],[25,32],[25,55],[48,28],[56,37]]
En51k5Demand = [0,7,30,16,9,21,15,19,23,11,5,19,29,23,21,10,15,3,41,9,28,8,8,16,10,28,7,15,14,6,19,11,12,23,26,17,6,9,15,14,7,27,13,11,16,10,5,25,17,18,10]
En51k5Capacity = 160


# algorithm configuration
max_iterations = 10000
max_temp = 100000.0
temp_change = 0.003
# execute the algorithm
best1 = search(En22k4_noDepo, max_temp, temp_change, En22k4_withDepo, En22k4Capacity, En22k4Demand)
#best2 = search(En30k3noDepo, max_temp, temp_change, En30k3, En30k3Capacity, En30k3Demand)
#best3 = search(En51k5noDepo, max_temp, temp_change, En51k5, En51k5Capacity, En51k5Demand)

print "Done. Best Solution: c=#{}, v=#{}, number of trucks:{}".format(calculateVrpDistance(best1, En22k4_withDepo), best1, len(best1))
#print "Done. Best Solution: c=#{}, v=#{}, number of trucks:{}".format(calculateVrpDistance(best2, En30k3), best2, len(best2))
#print "Done. Best Solution: c=#{}, v=#{}, number of trucks:{}".format(calculateVrpDistance(best3, En51k5), best3, len(best3))
#createPlotWithRoutes("firstTest",En22k4_withDepo,best1)

vrpDict = splitVRProuteIntoTruckDroneRoute(best1, En22k4_withDepo)

createPlotWithTruckDroneRoutes('firstTest',En22k4_withDepo, best1, vrpDict)

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

