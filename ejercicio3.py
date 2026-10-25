import math
import random
import matplotlib.pyplot as plt

def tour_length(points, route):
    return sum(math.dist(points[route[i]], points[route[(i+1)%len(route)]]) for i in range(len(route)))

def nearest_neighbour(points, start):
    unvisited = set(range(len(points)))
    unvisited.remove(start)
    route = [start]
    current = start
    while unvisited:
        next_city = min(unvisited, key=lambda city: math.dist(points[current], points[city]))
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return route

def two_opt(points, route):
    best_route = list(route)
    improved = True
    improvements = 0
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route)):
                if k - i == 1: continue 
                new_route = best_route[:i] + best_route[i:k+1][::-1] + best_route[k+1:]
                if tour_length(points, new_route) < tour_length(points, best_route):
                    best_route = new_route
                    improved = True
                    improvements += 1
        if not improved: break
    return best_route, improvements

random.seed(42)
points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(30)]

rand_route = list(range(len(points)))
random.shuffle(rand_route)
rand_opt, rand_imps = two_opt(points, rand_route)

nn_route = nearest_neighbour(points, random.choice(range(len(points))))
nn_opt, nn_imps = two_opt(points, nn_route)

plt.bar(['Aleatorio', 'Vecino Más Cercano'], [rand_imps, nn_imps], color=['purple', 'orange'])
plt.ylabel('Número de Mejoras (Iteraciones)')
plt.title('Mejoras necesarias para alcanzar el óptimo local (2-opt)')
plt.savefig('ejercicio3_2opt.png')
plt.show()