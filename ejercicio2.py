import matplotlib.pyplot as plt

def knapsack_greedy(items, W, mode="ratio"):
    if mode == "ratio":
        sorted_items = sorted(items, key=lambda x: x['v']/x['w'], reverse=True)
    else: 
        sorted_items = sorted(items, key=lambda x: x['w'])
        
    weight, value, chosen = 0, 0, []
    for item in sorted_items:
        if weight + item['w'] <= W:
            chosen.append(item['id'])
            weight += item['w']
            value += item['v']
    return value, weight, chosen

items = [
    {'id': 'A', 'v': 1, 'w': 1},
    {'id': 'B', 'v': 1000, 'w': 50}
]
W = 50

val_ratio, w_ratio, c_ratio = knapsack_greedy(items, W, "ratio")
val_peso, w_peso, c_peso = knapsack_greedy(items, W, "peso")

print(f"Criterio Valor/Peso: Valor={val_ratio}, Capacidad Usada={w_ratio}, Objetos={c_ratio}")
print(f"Criterio Menor Peso: Valor={val_peso}, Capacidad Usada={w_peso}, Objetos={c_peso}")

fig, ax = plt.subplots()
ax.bar(['Valor/Peso', 'Menor Peso'], [val_ratio, val_peso], color=['blue', 'red'])
ax.set_ylabel('Valor Total Obtenido')
plt.title('Comparación de Criterios Greedy')
plt.savefig('ejercicio2_knapsack.png')
plt.show()