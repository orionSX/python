import numpy as np
import math

num_jobs = 500
job_arrival_rate = 1
setup_time_min, setup_time_max = 0.2, 0.5
process_time_mean, process_time_std = 0.5, 0.1
breakdown_interval_mean, breakdown_interval_std = 20, 2
repair_time_min, repair_time_max = 0.1, 0.5

def congruent_method(N, a=561233, c=33312342, m=2**21, seed=123245):
    sequence = []
    x = seed
    for i in range(N):
        x = (a * x + c) % m
        sequence.append(x / m) 
    
    return sequence


def uniform_distribution(N, a, b):
    
    return [(b - a) * x + a for x in congruent_method(N) ]


def exponential_distribution(N, lam):
   
    return [-(1/lam)*np.log(x) for x in congruent_method(N)]


def normal_distribution(N, mu, sigma):
    normal_sample = []
    u1 = congruent_method(N=N,seed=12365)    
    u2 = congruent_method(N=N,seed=12335)
    
    for i in range(N // 2):    
        
        z0 = math.sqrt(-2 * math.log(u1[i])) * math.cos(2 * math.pi * u2[i])
        z1 = math.sqrt(-2 * math.log(u1[i])) * math.sin(2 * math.pi * u2[i])
        normal_sample.append(mu + sigma * z0)
        normal_sample.append(mu + sigma * z1)
    return normal_sample[:N]


job_arrival_times = np.cumsum(exponential_distribution(num_jobs, job_arrival_rate))
job_start_times = np.zeros(num_jobs)
job_end_times = np.zeros(num_jobs)
breakdown_times = np.cumsum(normal_distribution(num_jobs,breakdown_interval_mean,breakdown_interval_std))


current_time = 0
total_idle_time = 0
breakdown_index = 0

for i in range(num_jobs):

    arrival_time = job_arrival_times[i]

   
    if current_time < arrival_time:
        total_idle_time += arrival_time - current_time
        current_time = arrival_time

    setup_time = uniform_distribution(num_jobs,setup_time_min,setup_time_max)[np.random.randint(10,400)]
    current_time += setup_time

    process_time = normal_distribution(num_jobs,process_time_mean, process_time_std)[np.random.randint(10,400)]

 
    while breakdown_index < len(breakdown_times) and breakdown_times[breakdown_index] < current_time + process_time:

        breakdown_time = breakdown_times[breakdown_index]
        repair_time=normal_distribution(num_jobs,repair_time_min,repair_time_max)[np.random.randint(10,400)]
       

        total_idle_time += breakdown_time - current_time
        current_time = breakdown_time + repair_time
        breakdown_index += 1
        current_time += normal_distribution(num_jobs,setup_time_min,setup_time_max)[np.random.randint(10,400)]
      

    job_start_times[i] = current_time - process_time
    job_end_times[i] = current_time
    current_time += process_time

total_processing_time = sum(job_end_times - job_arrival_times)
average_processing_time = sum(job_end_times - job_arrival_times) / len(job_end_times - job_arrival_times)
machine_utilization = (total_processing_time - total_idle_time) / total_processing_time

print(f"Среднее время выполнения задания: {np.round(average_processing_time,2)} часов")
print(f"Загрузка станка: {np.round(machine_utilization * 100,2)}%")