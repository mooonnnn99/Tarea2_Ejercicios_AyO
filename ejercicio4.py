import math
import random
import time
import matplotlib.pyplot as plt

def tour_length(points, route):
    return sum(math.dist(points[route[i]], points[route[(i+1)%len(route)]]) for i in range(len(route)))

def random_2opt_move(route):
    i, k = sorted(random.sample(range(len(route)), 2))
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

def simulated_annealing(points, schedule_type, initial_temp=1000, iterations=5000):
    current_route = list(range(len(points)))
    random.shuffle(current_route)
    current_cost = tour_length(points, current_route)
    
    best_route, best_cost = current_route, current_cost
    history = []
    
    t0 = time.perf_counter()
    for t in range(1, iterations + 1):
        if schedule_type == 'linear':
            temp = max(0, initial_temp - (initial_temp / iterations) * t)
        else: # exponential
            temp = initial_temp * (0.995 ** t)
            
        if temp <= 0.01: break
            
        next_route = random_2opt_move(current_route)
        next_cost = tour_length(points, next_route)
        delta_e = current_cost - next_cost
        
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current_route, current_cost = next_route, next_cost
            if current_cost < best_cost:
                best_route, best_cost = current_route, current_cost
                
        history.append(current_cost)
        
    execution_time = time.perf_counter() - t0
    return history, best_cost, execution_time

random.seed(42)
points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(30)]

hist_lin, cost_lin, time_lin = simulated_annealing(points, 'linear')
hist_exp, cost_exp, time_exp = simulated_annealing(points, 'exponential')

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(hist_lin, label='Lineal')
plt.plot(hist_exp, label='Exponencial')
plt.xlabel('Iteraciones')
plt.ylabel('Costo (Longitud)')
plt.title('Curvas de Convergencia')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter([time_lin], [cost_lin], label='Lineal', color='blue', s=100)
plt.scatter([time_exp], [cost_exp], label='Exponencial', color='orange', s=100)
plt.xlabel('Tiempo de Ejecución (s)')
plt.ylabel('Calidad de la Solución (Costo)')
plt.title('Tiempo vs Calidad')
plt.legend()

plt.tight_layout()
plt.savefig('ejercicio4_sa.png')
plt.show()