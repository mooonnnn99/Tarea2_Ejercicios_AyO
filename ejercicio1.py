import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt

def estimate_pi(seed: int, samples: int = 1_000_000) -> float:
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == "__main__":
    processes_list = [1, 2, 4, 8]
    speedups = []
    seeds = list(range(8))
    
    t0 = time.perf_counter()
    [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0

    for p in processes_list:
        t0 = time.perf_counter()
        with mp.Pool(processes=p) as pool:
            pool.map(estimate_pi, seeds)
        t_par = time.perf_counter() - t0
        speedups.append(t_seq / t_par)

    plt.plot(processes_list, speedups, marker='o', label='Speedup Observado')
    plt.plot(processes_list, processes_list, linestyle='--', label='Speedup Ideal')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Aceleración (Speedup)')
    plt.title('Aceleración Paralela vs Ideal')
    plt.legend()
    plt.grid(True)
    plt.savefig('ejercicio1_speedup.png')
    plt.show()