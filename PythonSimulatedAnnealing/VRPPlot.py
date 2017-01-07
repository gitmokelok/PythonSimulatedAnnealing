from bokeh.plotting import figure, output_file, show
import math
import random
import pandas




# best support is with data in a format that is table-like
# data = {
#     'sample': ['1st', '2nd', '1st', '2nd', '1st', '2nd'],
#     'x': ['python', 'python', 'pypy', 'pypy', 'jython', 'jython'],
#     'y': [-2, 5, 12, 40, 22, 30],
# }
def two_optSwap(route, i, k):
    new_route = list()
    if i ==0:
        new_route = []
    else:
        new_route += route[0:i-1]
    reversedRoute = list(reversed(route[i:k+1]))
    new_route += reversedRoute
    route2 = route[k+1:]
    new_route += route2
    return new_route

def euc_2d(c1, c2):
    result = math.sqrt(((c1[0] - c2[0]) ** 2) + ((c1[1] - c2[1]) ** 2))
    return result

def convert_coord_into_rad(coordinate):
    PI = 3.141592
    deg = int(coordinate)
    min = coordinate - deg;
    rad = PI * (deg + 5.0 * min/ 3.0) / 180.0;
    return rad

def geo_distance(c1, c2):
    RRR = 6378.388
    q1 = math.cos(convert_coord_into_rad(c1[0]) - convert_coord_into_rad(c2[0]))
    q2 = math.cos(convert_coord_into_rad(c1[1]) - convert_coord_into_rad(c2[1]))
    q3 = math.cos(convert_coord_into_rad(c1[1]) + convert_coord_into_rad(c2[1]))
    dij = int( RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
    return dij

def cost(permutation, cities):
    distance = 0.0
    c2 = 0
    for c1 in permutation:
        if c1 == (permutation[-1]):
            c2 = permutation[0]
        else:
            c2 = permutation[permutation.index(c1) + 1]
        distance += geo_distance(cities[c1], cities[c2])

        #distance += euc_2d(cities[c1], cities[c2])
    return distance


# prepare some data
# x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
# y0 = [i**2 for i in x]
# y1 = [10**i for i in x]
# y2 = [10**(i**2) for i in x]
#uly16.tsp plot coords start
x= [39.57, 40.56, 36.26,
    33.48, 37.56, 38.42, 37.52,
    41.23, 41.17, 36.08, 38.47,
    38.15, 37.51, 35.49, 39.36]
y= [26.15, 25.32, 23.12,
    10.54, 12.19, 13.11, 20.44,
    9.1,   13.05, -5.21, 15.13,
    15.35, 15.17, 14.32, 19.56]

depoX= 38.24
depoY= 20.42
#uly16.tsp plot coords end
uly16= [[38.24,20.42],[39.57,26.15],[40.56,25.32],[36.26,23.12],[33.48,10.54],[37.56,12.19],[38.42,13.11],[37.52,20.44],[41.23,9.1],[41.17,13.05],[36.08,-5.21],[38.47,15.13],[38.15,15.35],[37.51,15.17],[35.49,14.32],[39.36,19.56]]

cities = [[39.57,26.15],[40.56,25.32],[36.26,23.12],[33.48,10.54],[37.56,12.19],[38.42,13.11],[37.52,20.44],[41.23,9.1],[41.17,13.05],[36.08,-5.21],[38.47,15.13],[38.15,15.35],[37.51,15.17],[35.49,14.32],[39.36,19.56]]
'''
v=[10, 11, 14, 1, 0, 2, 6, 13, 3, 9, 7, 8, 5, 4, 12]
v=range(15)
random.shuffle(v)
best_distance = cost(v, cities)
best_route = list()
counter = 0
print best_distance, best_route
# while best_distance > 60:
#     for i in range(len(cities) -1):
#         for k in range(i+1, len(cities)-1 ):
#             new_route = two_optSwap(v, i, k)
#             new_distance = cost(new_route, cities)
#             counter += 1
#             if new_distance < best_distance:
#                 best_distance = new_distance
#                 best_route = new_route
#             if counter % 100000 == 0:
#                 print best_distance, best_route, new_distance, new_route

while best_distance > 60:
    i = random.randint(0, len(cities)-2)
    k = random.randint(1, len(cities)-1)
    while (k < i):
        k = random.randint(1, len(cities)-1)
    new_route = two_optSwap(v, i, k)
    new_distance = cost(new_route, cities)
    counter += 1
    if new_distance < best_distance:
        best_distance = new_distance
        best_route = new_route
    if counter % 100000 == 0:
        print best_distance, best_route, new_distance, new_route


print best_route, cost(best_route,cities), best_distance
'''
v=[4, 5, 10, 12, 11, 14, 1, 0, 2, 6, 13, 3, 9, 7, 8]
v=[10, 5, 4, 13, 3, 9, 7, 8, 14, 1, 0, 2, 6, 12, 11]
capacity = 5

best_optimal_solution = [9, 7, 8, 5, 4, 13, 12, 11, 10, 3, 2, 0, 1, 14, 6]
'''Route #1: 10 8 9 6 5
Route #2: 14 13 12 11 4
Route #3: 3 1 2 15 7'''
best_optimal_solution1 = [0,10, 8, 9, 6, 5,0]
best_optimal_solution2 = [0,14, 13, 12, 11, 4 ,0]
best_optimal_solution3 = [0,3,1, 2, 15, 7,0]
test = cost(best_optimal_solution1, uly16) + cost(best_optimal_solution2, uly16) + cost(best_optimal_solution3, uly16)
print cost(best_optimal_solution1, uly16)
print cost(best_optimal_solution2, uly16)
print cost(best_optimal_solution3, uly16)
print test

x1 = [depoX]
y1 = [depoY]

x2 = [depoX]
y2 = [depoY]

x3 = [depoX]
y3 = [depoY]

for index in best_optimal_solution[:capacity]:
   x1.append(x[index])
   y1.append(y[index])

#startEndCityIndex = v[0]

x1.append(depoX)
y1.append(depoY)

for index in best_optimal_solution[capacity:10]:
   x2.append(x[index])
   y2.append(y[index])

#startEndCityIndex = v[0]

x2.append(depoX)
y2.append(depoY)

for index in best_optimal_solution[10:]:
   x3.append(x[index])
   y3.append(y[index])

#startEndCityIndex = v[0]

x3.append(depoX)
y3.append(depoY)
# startEndCityX = x[startEndCityIndex]
# startEndCityY = y[startEndCityIndex]
'''
Route #1: 10 8 9 6 5
Route #2: 14 13 12 11 4
Route #3: 3 1 2 15 7
Cost 30492


'''
# output to static HTML file
output_file("log_lines.html")


# add some renderers
p.line(x1, y1, line_width=1, line_color="orange")
p.line(x2, y2, line_width=1, line_color="green")
p.line(x3, y3, line_width=1, line_color="yellow")

#p.line(x, y, legend="y=x^2", line_width=3)
#p.line(x, y1, legend="y=10^x", line_color="red")
p.circle(depoX, depoY, legend="Depo", fill_color="red", line_color="red", size=6, )
p.circle(x, y, legend="Customers", fill_color="white", line_color="black", size=6)

#p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

# show the results
show(p)