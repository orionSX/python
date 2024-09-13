import math

print("#1")

ROAD_LENGTH=109
speed=int(input('Enter speed'))
time=int(input('Enter hours'))

if speed>0:
	print(speed*time%ROAD_LENGTH)
else:
	print(abs(ROAD_LENGTH-abs(speed*time))%ROAD_LENGTH)

print("#2")

n1=int(input('Enter number of pupils in 1st class'))
n2=int(input('Enter number of pupils in 2nd class'))
n3=int(input('Enter number of pupils in 3rd class'))
print(math.ceil(n1/2)+math.ceil(n2/2)+math.ceil(n3/2))

print('#3')

n=int(input('Enter n: '))
m=int(input('Enter m: '))
print(math.ceil(m/n))



print('#4')

n=int(input('Enter n: '))
m=int(input('Enter m: '))

min_ = m * (n//m*(n//m-1)/2) + n%m*(n//m)
max_ = (n-m+1)*(n-m)/2

print(min_,max_,sep="\t")

print('#5')

n = int(input('Enter n'))
k = int(input('Enter k'))

sad_students = (n - (k % n))%n
print(sad_students)


print('#6')


int_number = int(input('Enter number'))
print(math.floor(int_number / 2 + 1) * 2)


print('#8')
def ans(K1, M, K2, P2, N2):
	#kv_v_podezd=etaj*kv_etaj
	#kv_na_etaj=kv_v_podezd/etaj
    for kv_etaj in range(1, 1001):  
        kv_podezd = K2 - ((P2 - 1) * (M * kv_etaj) + (N2 - 1) * kv_etaj + 1)
        if kv_podezd <= 0 or kv_podezd % M != 0:
            continue
        
        kv_podezd //= M  
        if kv_podezd < 1 or kv_podezd > 1000:
            continue

        
        if K1 < 1 or K1 > (P2 - 1) * kv_podezd + (N2 - 1) * kv_etaj + 1000:
            continue

        
        P1 = (K1 - 1) // kv_podezd + 1
        N1 = ((K1 - 1) % kv_podezd) // kv_etaj + 1
        
        if K1 == (P1 - 1) * kv_podezd + (N1 - 1) * kv_etaj + 1:
            return P1, N1
    
    return -1, -1  

# Ввод данных
K1, M, K2, P2, N2 = map(int, input('Enter k1 m k2 p2 n2 split by space').split())

# Нахождение результата
P1, N1 = ans(K1, M, K2, P2, N2)

# Вывод результата
print(P1, N1)



print('#9')



# Пример использования
N = int(input("Введите количество кусочков: "))
cuts = n/2 if n%2==0 else n if n!=1 else 0
print(cuts)



print('#10')
N,M,x,y=map(float,input('Enter N,M,x,y: ').split())
temp1=min(N,M)
temp2=max(N,M)
N=temp1
M=temp2

print(min(x,M-x,y,N-y))