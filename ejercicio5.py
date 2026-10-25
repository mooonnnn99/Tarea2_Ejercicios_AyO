import itertools
import math
import random
import matplotlib.pyplot as plt

def tour_length(points, route):
    return sum(math.dist(points[route[i]], points[route[(i+1)%len(route)]]) for i in range(len(route)))

def mst_prim(points):
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, len(points))}
    children = {v: [] for v in range(len(points))}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]: best[u] = (d, v)
    return children

def preorder(children, root=0):
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def two_opt(points, route):
    best_route = list(route)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route)):
                if k - i == 1: continue 
                new_route = best_route[:i] + best_route[i:k+1][::-1] + best_route[k+1:]
                if tour_length(points, new_route) < tour_length(points, best_route):
                    best_route = new_route
                    improved = True
        if not improved: break
    return best_route

ratios = []
mst_costs, mst_opt_costs = [], []

random.seed(123)
for _ in range(100):
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(9)]
    
    opt_route = min(itertools.permutations(range(9)), key=lambda t: tour_length(points, t))
    opt_cost = tour_length(points, opt_route)
    
    mst_route = preorder(mst_prim(points))
    mst_cost = tour_length(points, mst_route)
    
    mst_opt_route = two_opt(points, mst_route)
    mst_opt_cost = tour_length(points, mst_opt_route)
    
    ratios.append(mst_cost / opt_cost)
    mst_costs.append(mst_cost)
    mst_opt_costs.append(mst_opt_cost)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.hist(ratios, bins=15, color='teal', edgecolor='black')
plt.axvline(2, color='red', linestyle='dashed', linewidth=2, label='Límite Teórico (2)')
plt.xlabel('Razón de Aproximación (MST / Óptimo)')
plt.ylabel('Frecuencia')
plt.legend()

plt.subplot(1, 2, 2)
plt.boxplot([mst_costs, mst_opt_costs], labels=['MST Puro', 'MST + 2-opt'])
plt.ylabel('Costo del Tour')

plt.tight_layout()
plt.savefig('ejercicio5_mst.png')
plt.show()