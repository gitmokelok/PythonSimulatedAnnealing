import math
import itertools
import random

def euc_2d(c1, c2):
    result = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[2])**2)
    return int(round(result))

def cost(permutation, cities):
    distance = 0
    c2 = 0
    for c1 in permutation:
        if c1 == (permutation[-1]):
            c2 = permutation[0]
        else:
            c2 = permutation[permutation.index(c1)+1]
        distance += euc_2d(cities[c1], cities[c2])
    return distance

def random_permutation(numberOfCities):
    perm = range(numberOfCities)
    random.shuffle(perm)
    return perm

def stochastic_two_opt(route):
    tempRoute = route;    
    c1 = random.choice(tempRoute)
    tempRoute.remove(c1)
    c2 = random.choice(tempRoute)
    c1Index = route.index(c1);
    c2Index = route.index(c2);
    if c1Index > c2Index:
        c1Index, c2Index = c2Index, c1Index
    tempRouteSlice = list(route[c1Index:c2Index])
    tempRouteSlice.reverse()
    route[c1Index:c2Index] = tempRouteSlice    
    
    #exclude = [c1]
    #if c1 == 0:
    #    exclude.append(len(perm)-1)
    #else:
    #    exclude.append(c1-1)
    #if c1==(len(perm)-1):
    #    exclude.append(0)
    #else:
    #    exclude.append(c1+1)
    #while c2 in exclude:
    #    c2 = random.choice(perm)
    #if c2 < c1:
    #    c1,c2 = c2,c1
    #newPermSlice = list(reversed(perm[c1:c2]))
    #perm[c1:c2] = newPermSlice
    return route

def create_neighbor(current, cities):   
    candidate = list()
    candidate = stochastic_two_opt(current)
    return candidate

def should_accept(candidate, current, temp, cities):
    candidateCost = cost(candidate, cities)
    currentCost = cost(current, cities)
    if candidateCost <= currentCost:
        return true
    else:
        return math.exp((currentCost - candidateCost) / temp) > random.random()

def search(cities, max_iter, max_temp, temp_change):
    current = random_permutation(len(cities))
    currentCost = cost(current, cities)
    temp, best = max_temp, current
  
    for i in range(max_iter):
        candidate = create_neighbor(current, cities)
        temp = temp_max * temp_change
        if should_accept(candidate, current, temp):
            current = candidate
        if cost(candidate, cities) < cost(best, cities):
            best = candidate
        if (i+1) % 10 == 0:
            print " > iteration #{(iter+1)}, temp=#{temp}, best=#{best[:cost]}"
    return best

# problem configuration
berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
            [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
            [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
            [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
            [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
            [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
            [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
            [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
            [830,610],[605,625],[595,360],[1340,725],[1740,245]
           ]
#current = random_permutation(len(berlin52))
#print current 
#currentCost = cost(current, berlin52)
#print currentCost
# algorithm configuration
max_iterations = 2000
max_temp = 100000.0
temp_change = 0.098
# execute the algorithm
best = search(berlin52, max_iterations, max_temp, temp_change)
print "Done. Best Solution: c=#{best[:cost]}, v=#{best[:vector].inspect}"

#myList = random_permutation(10)
#print myList
#antoherList = stochastic_two_opt(myList)
#print antoherList
    
    

#  c1, c2 = rand(perm.size), rand(perm.size)
#  exclude = [c1]
#  exclude << ((c1==0) ? perm.size-1 : c1-1)
#  exclude << ((c1==perm.size-1) ? 0 : c1+1)
#  c2 = rand(perm.size) while exclude.include?(c2)
#  c1, c2 = c2, c1 if c2 < c1
#  perm[c1...c2] = perm[c1...c2].reverse
#  return perm
#end

