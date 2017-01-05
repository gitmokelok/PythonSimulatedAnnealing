import math
import random

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
    capacity_counter = 0
    for customer in permutation_woDepo:
        if capacity_counter <= truckCapacity:
            capacity_counter += demandList_woDepo[customer]
            if capacity_counter <= En22k4Capacity:
                new_route.append(customer)
            else:
                capacity_counter = 0
                capacity_counter += demandList_woDepo[customer]
                result.append(new_route)
                new_route = [customer]
        if customer == permutation_woDepo[-1]:
            result.append(new_route)        
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

# problem configuration

En22k4_withDepo = [[145,215],[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
En22k4_noDepo = [[151,264],[159,261],[130,254],[128,252],[163,247],[146,246],[161,242],[142,239],[163,236],[148,232],[128,231],[156,217],[129,214],[146,208],[164,208],[141,206],[147,193],[164,193],[129,189],[155,185],[139,182]]
En22k4Demand = [0,1100,700,800,1400,2100,400,800,100,500,600,1200,1300,1300,300,900,2100,1000,900,2500,1800,700]
En22k4Capacity = 6000


En30k3 = [[162,354],[218,382],[218,358],[201,370],[214,371],[224,370],[210,382],[104,354],[126,338],[119,340],[129,349],[126,347],[125,346],[116,355],[126,335],[125,355],[119,357],[115,341],[153,351],[175,363],[180,360],[159,331],[188,357],[152,349],[215,389],[212,394],[188,393],[207,406],[184,410],[207,392]]
En51k5 = [[30,40],[37,52],[49,49],[52,64],[20,26],[40,30],[21,47],[17,63],[31,62],[52,33],[51,21],[42,41],[31,32],[5,25],[12,42],[36,16],[52,41],[27,23],[17,33],[13,13],[57,58],[62,42],[42,57],[16,57],[8,52],[7,38],[27,68],[30,48],[43,67],[58,48],[58,27],[37,69],[38,46],[46,10],[61,33],[62,63],[63,69],[32,22],[45,35],[59,15],[5,6],[10,17],[21,10],[5,64],[30,15],[39,10],[32,39],[25,32],[25,55],[48,28],[56,37]]

# algorithm configuration
max_iterations = 10000
max_temp = 100000.0
temp_change = 0.003
# execute the algorithm
best1 = search(En22k4_noDepo, max_temp, temp_change, En22k4_withDepo, En22k4Capacity, En22k4Demand)
#best2 = search(En30k3, max_iterations, max_temp, temp_change)
#best3 = search(En51k5, max_iterations, max_temp, temp_change)

print "Done. Best Solution: c=#{}, v=#{}".format(calculateVrpDistance(best1, En22k4_withDepo), best1)
#print "Done. Best Solution: c=#{}, v=#{}".format(cost(best2, En30k3), best2)
#print "Done. Best Solution: c=#{}, v=#{}".format(cost(best3, En51k5), best3)


#NAME : E-n22-k4
#COMMENT : (Christophides and Eilon, Min no of trucks: 4, Optimal value: 375)
#TYPE : CVRP
#DIMENSION : 22
#EDGE_WEIGHT_TYPE : EUC_2D
#CAPACITY : 6000


def splitTspRoute(permutation_woDepo, truckCapacity, demandList_woDepo, cities_woDepo):
    result = list()
    new_route = list()
    capacity_counter = 0
    for customer in permutation_woDepo:
        if capacity_counter <= truckCapacity:
            capacity_counter += demandList_woDepo[customer]
            if capacity_counter <= En22k4Capacity:
                new_route.append(customer)
            else:
                capacity_counter = 0
                capacity_counter += demandList_woDepo[customer]
                result.append(new_route)
                new_route = [customer]
        if customer == permutation_woDepo[-1]:
            result.append(new_route)        
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
        temp.append(0)
        temp.insert(0,0)
        totalDistance += cost(temp, cities_withDepo)
    return totalDistance
                
best1 = normalize_route(best1)
best_Optimal = [[17, 20, 18, 15, 12],[16, 19, 21, 14], [13, 11, 4, 3, 8, 10],[9, 7, 5, 2, 1, 6]] #COST 375
vrp1routes =  splitTspRoute(best1, En22k4Capacity, En22k4Demand, En22k4_withDepo)

print calculateVrpDistance(vrp1routes, En22k4_withDepo), vrp1routes

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

