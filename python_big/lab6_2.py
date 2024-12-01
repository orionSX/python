import simpy
import numpy as np


NUM_CARS = 1000
MEAN_ARRIVAL_TIME = 0.1
MEAN_SERVICE_TIME = 0.5
QUEUE_LIMIT = 5


lost_customers = 0
total_time_in_station = []
departure_intervals = []
queue_lengths1 = []
queue_lengths2 = []


def congruent_method(N, a=561233, c=33312342, m=2**21, seed=123245):
    sequence = []
    x = seed
    for _ in range(N):
        x = (a * x + c) % m
        sequence.append(x / m)  
    return sequence


def exponential_distribution(N, lam):
    uniform_numbers = congruent_method(N)
    return [-(1 / lam) * np.log(u) for u in uniform_numbers]


def normal_distribution(N, mu, sigma):
    uniform_numbers = congruent_method(N * 2)  
    results = []
    for i in range(0, len(uniform_numbers), 2):
        u1, u2 = uniform_numbers[i], uniform_numbers[i + 1]
        z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
        results.append(mu + z0 * sigma)
        results.append(mu + z1 * sigma)
    return results[:N]


class GasStation:
    def __init__(self, env):
        self.env = env
        self.pump1_queue = simpy.Store(env, capacity=QUEUE_LIMIT)
        self.pump2_queue = simpy.Store(env, capacity=QUEUE_LIMIT)
        self.pump1 = simpy.Resource(env, capacity=1)
        self.pump2 = simpy.Resource(env, capacity=1)

    def choose_pump(self):
        if len(self.pump2_queue.items) < len(self.pump1_queue.items):
            return self.pump2, self.pump2_queue
        return self.pump1, self.pump1_queue


def customer(env, name, gas_station, service_times, last_departure_time):
    global lost_customers
    arrival_time = env.now

    pump, queue = gas_station.choose_pump()
    if len(queue.items) == QUEUE_LIMIT:
        lost_customers += 1
        return

    queue_lengths1.append(len(gas_station.pump1_queue.items))
    queue_lengths2.append(len(gas_station.pump2_queue.items))

    queue.put(name)

    with pump.request() as request:
        yield request
        yield queue.get()
        service_time = service_times.pop(0)
        yield env.timeout(service_time)

    departure_time = env.now
    total_time_in_station.append(departure_time - arrival_time)

    if last_departure_time[0] is not None: 
        departure_intervals.append(departure_time - last_departure_time[0])
    last_departure_time[0] = departure_time  



def generate_customers(env, gas_station, arrival_times, service_times):
    last_departure_time = [None]  
    for i in range(NUM_CARS):
        inter_arrival_time = arrival_times.pop(0)
        yield env.timeout(inter_arrival_time)
        env.process(customer(env, f'Customer_{i}', gas_station, service_times, last_departure_time))



arrival_times = exponential_distribution(NUM_CARS, 1 / MEAN_ARRIVAL_TIME)
service_times = exponential_distribution(NUM_CARS, 1 / MEAN_SERVICE_TIME)

env = simpy.Environment()
gas_station = GasStation(env)
env.process(generate_customers(env, gas_station, arrival_times, service_times))
env.run()

# Анализ результатов
avg_queue1 = sum(queue_lengths1) / len(queue_lengths1) if queue_lengths1 else 0
avg_queue2 = sum(queue_lengths2) / len(queue_lengths2) if queue_lengths2 else 0
rejection_rate = (lost_customers / NUM_CARS) * 100
avg_departure_interval = sum(departure_intervals) / len(departure_intervals) if departure_intervals else 0
avg_time_in_station = sum(total_time_in_station) / len(total_time_in_station) if total_time_in_station else 0

# Вывод результатов
print(f"1.1 Среднее число клиентов в 1 очереди: {np.round(avg_queue1,2)}")
print(f"1.2  Среднее число клиентов во 2 очереди:: {np.round(avg_queue2,2)}")
print(f"2. Процент клиентов, которые отказались от обслуживания {np.round(rejection_rate,2)}%")
print(f"3. Средний интервал времени между отъездами клиентов: {np.round(avg_departure_interval,2)} единиц времени")
print(f"4. Среднее время пребывания клиента на заправке: {np.round(avg_time_in_station,2)} единиц времени ")