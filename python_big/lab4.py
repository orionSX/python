import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import math
import random
import numpy


def congruent_method(N, a=561233, c=33312342, m=2**21, seed=12345):
    sequence = []
    x = seed
    for i in range(N):
        x = (a * x + c) % m
        sequence.append(x / m) 
    
    return sequence


def uniform_distribution(N, a, b):
    
    return [(b - a) * x + a for x in congruent_method(N) ]


def exponential_distribution(N, lam):
   
    return [-(1/lam)*numpy.log(x) for x in congruent_method(N)]


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


# Функция для вычисления математического ожидания и дисперсии
def calculate_statistics(sample):
    mean = sum(sample) / len(sample)
    variance = sum((x - mean) ** 2 for x in sample) / len(sample)
    return mean, variance

# Функция для расчета относительной погрешности
def relative_error(estimated_value, true_value):
    return abs((estimated_value - true_value) / true_value) * 100

# Функция для построения графиков погрешностей
def plot_error_graphs(uniform_errors, exp_errors, norm_errors, sample_sizes):
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))

    # График погрешности математического ожидания для равномерного распределения
    axs[0, 0].plot(sample_sizes, uniform_errors['mean'], marker='o', label='Mean Error')
    axs[0, 0].set_title('Равномерное распределение - Погрешность мат. ожидания')
    axs[0, 0].set_xlabel('Размер выборки')
    axs[0, 0].set_ylabel('Относительная погрешность (%)')

    # График погрешности дисперсии для равномерного распределения
    axs[1, 0].plot(sample_sizes, uniform_errors['var'], marker='o', label='Variance Error')
    axs[1, 0].set_title('Равномерное распределение - Погрешность дисперсии')
    axs[1, 0].set_xlabel('Размер выборки')
    axs[1, 0].set_ylabel('Относительная погрешность (%)')

    # График погрешности математического ожидания для экспоненциального распределения
    axs[0, 1].plot(sample_sizes, exp_errors['mean'], marker='o', label='Mean Error')
    axs[0, 1].set_title('Экспоненциальное распределение - Погрешность мат. ожидания')
    axs[0, 1].set_xlabel('Размер выборки')
    axs[0, 1].set_ylabel('Относительная погрешность (%)')

    # График погрешности дисперсии для экспоненциального распределения
    axs[1, 1].plot(sample_sizes, exp_errors['var'], marker='o', label='Variance Error')
    axs[1, 1].set_title('Экспоненциальное распределение - Погрешность дисперсии')
    axs[1, 1].set_xlabel('Размер выборки')
    axs[1, 1].set_ylabel('Относительная погрешность (%)')

    # График погрешности математического ожидания для нормального распределения
    axs[0, 2].plot(sample_sizes, norm_errors['mean'], marker='o', label='Mean Error')
    axs[0, 2].set_title('Нормальное распределение - Погрешность мат. ожидания')
    axs[0, 2].set_xlabel('Размер выборки')
    axs[0, 2].set_ylabel('Относительная погрешность (%)')

    # График погрешности дисперсии для нормального распределения
    axs[1, 2].plot(sample_sizes, norm_errors['var'], marker='o', label='Variance Error')
    axs[1, 2].set_title('Нормальное распределение - Погрешность дисперсии')
    axs[1, 2].set_xlabel('Размер выборки')
    axs[1, 2].set_ylabel('Относительная погрешность (%)')

    plt.tight_layout()
    plt.show()

# Построение гистограммы и диаграммы накопленных частот
def plot_histogram_and_cdf(sample, title):
    # Гистограмма
    plt.figure(figsize=(8, 4))
    plt.hist(sample, bins=10, alpha=0.7, edgecolor='black', density=True)
    plt.title(f'Гистограмма {title}')
    plt.show()

    # Диаграмма накопленных частот
    sorted_sample = sorted(sample)
    cumulative_freq = [i / len(sample) for i in range(1, len(sample) + 1)]

    plt.figure(figsize=(8, 4))
    plt.step(sorted_sample, cumulative_freq, where='post', color='blue')
    plt.title(f'Диаграмма накопленных частот {title}')
    plt.xlabel('Значение')
    plt.ylabel('Накопленная частота')
    plt.grid(True)
    plt.show()



def run_simulation(a, b, lam, mu, sigma):
    sample_sizes = [10, 20, 50, 100, 1000]
    
    uniform_errors = {'mean': [], 'var': []}
    exp_errors = {'mean': [], 'var': []}
    norm_errors = {'mean': [], 'var': []}

    fig, axs = plt.subplots(len(sample_sizes), 3, figsize=(18, 20))

    for idx, N in enumerate(sample_sizes):
        # Равномерное распределение
        uniform_sample = uniform_distribution(N, a, b)
        uniform_mean, uniform_var = calculate_statistics(uniform_sample)
        uniform_errors['mean'].append(relative_error(uniform_mean, (a + b) / 2))
        uniform_errors['var'].append(relative_error(uniform_var, ((b - a) ** 2) / 12))

        # Оценка количества интервалов для равномерного распределения
        K = round(1 + 3.2 * math.log10(N))
        
        len_q_uni = (max(uniform_sample) - min(uniform_sample)) / K

        # Гистограмма накопленных частот для равномерного распределения
        axs[idx, 0].hist(uniform_sample, bins=N, alpha=0.7, edgecolor='black', density=True)
        axs[idx, 0].set_title(f'Равномерное распределение (N={N})')

        # Накопленные частоты по интервалам
        interval_edges = [min(uniform_sample) + i * len_q_uni for i in range(K + 1)]
        cumulative_freq = [0] * K
        for value in uniform_sample:
            for i in range(K):
                if interval_edges[i] <= value < interval_edges[i + 1]:
                    cumulative_freq[i] += 1

        # Накопление частот
        cumulative_freq = [sum(cumulative_freq[:i + 1]) / N for i in range(K)]
        
        
        cumulative_freq.insert(0,0)
        cumulative_freq[-1]=math.ceil(cumulative_freq[-1])
       
        # Построение накопленной кривой
        axs[idx, 0].step(interval_edges, cumulative_freq, where='post', color='blue')

        # Экспоненциальное распределение
        exp_sample = exponential_distribution(N, lam)
        
        exp_mean, exp_var = calculate_statistics(exp_sample)
        exp_errors['mean'].append(relative_error(exp_mean, 1 / lam))
        exp_errors['var'].append(relative_error(exp_var, 1 / lam ** 2))

        # Оценка количества интервалов для экспоненциального распределения
        K = round(1 + 3.2 * math.log10(N))
        len_q_exp = (max(exp_sample) - min(exp_sample)) / K

        # Гистограмма накопленных частот для экспоненциального распределения
        axs[idx, 1].hist(exp_sample, bins=N, alpha=0.7, edgecolor='black', density=True)
        axs[idx, 1].set_title(f'Экспоненциальное распределение (N={N})')

       
        interval_edges = [min(exp_sample) + i * len_q_exp for i in range(K + 1)]
        cumulative_freq = [0] * K
        for value in exp_sample:
            for i in range(K):
                if interval_edges[i] <= value < interval_edges[i + 1]:
                    cumulative_freq[i] += 1

        cumulative_freq = [sum(cumulative_freq[:i + 1]) / N for i in range(K)]
        
        
        cumulative_freq.insert(0,0)
        cumulative_freq[-1]=math.ceil(cumulative_freq[-1])

       
        axs[idx, 1].step(interval_edges, cumulative_freq, where='post', color='blue')

        norm_sample = normal_distribution(N, mu, sigma)
        norm_mean, norm_var = calculate_statistics(norm_sample)
        norm_errors['mean'].append(relative_error(norm_mean, mu))
        norm_errors['var'].append(relative_error(norm_var, sigma ** 2))

        K = round(1 + 3.2 * math.log10(N))
        len_q_norm = (max(norm_sample) - min(norm_sample)) / K


        axs[idx, 2].hist(norm_sample, bins=N, alpha=0.7, edgecolor='black', density=True)
        axs[idx, 2].set_title(f'Нормальное распределение (N={N})')

        interval_edges = [min(norm_sample) + i * len_q_norm for i in range(K + 1)]
        cumulative_freq = [0] * K
        for value in norm_sample:
            for i in range(K):
                if interval_edges[i] <= value < interval_edges[i + 1]:
                    cumulative_freq[i] += 1

        # Накопление частот
        cumulative_freq = [sum(cumulative_freq[:i + 1]) / N for i in range(K)]
        
        
        cumulative_freq.insert(0,0)
        cumulative_freq[-1]=math.ceil(cumulative_freq[-1])
       
        axs[idx, 2].step(interval_edges, cumulative_freq, where='post', color='blue')


    plt.tight_layout()
    plt.show()

    # Построение графиков погрешностей
    plot_error_graphs(uniform_errors, exp_errors, norm_errors, sample_sizes)



# GUI на tkinter
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Моделирование случайных чисел")
        self.geometry("400x300")

        self.label = tk.Label(self, text="Введите параметры:")
        self.label.pack(pady=10)

        self.a_label = tk.Label(self, text="a (для равномерного распределения):")
        self.a_label.pack()
        self.a_entry = ttk.Entry(self)
        self.a_entry.pack()

        self.b_label = tk.Label(self, text="b (для равномерного распределения):")
        self.b_label.pack()
        self.b_entry = ttk.Entry(self)
        self.b_entry.pack()

        self.lam_label = tk.Label(self, text="λ (для экспоненциального распределения):")
        self.lam_label.pack()
        self.lam_entry = ttk.Entry(self)
        self.lam_entry.pack()

        self.mu_label = tk.Label(self, text="μ (для нормального распределения):")
        self.mu_label.pack()
        self.mu_entry = ttk.Entry(self)
        self.mu_entry.pack()

        self.sigma_label = tk.Label(self, text="σ (для нормального распределения):")
        self.sigma_label.pack()
        self.sigma_entry = ttk.Entry(self)
        self.sigma_entry.pack()

        self.run_button = tk.Button(self, text="Запустить моделирование", command=self.run_simulation)
        self.run_button.pack(pady=20)

    def run_simulation(self):
        a = float(self.a_entry.get())
        b = float(self.b_entry.get())
        lam = float(self.lam_entry.get())
        mu = float(self.mu_entry.get())
        sigma = float(self.sigma_entry.get())
        run_simulation(a, b, lam, mu, sigma)

if __name__ == "__main__":
    app = App()
    app.mainloop()