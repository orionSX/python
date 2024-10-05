import re
#task1
def euclid(x,y):
    while y!=0:
        x,y=y,x%y
    return x

def coprimes_amount(n):
    return len([x for x in range(1,n) if euclid(x,n)==1])

def sum_of_d(n):
    return sum([int(x) for x in str(n) if int(x)%3==0])

def divisor_copr_w_dig(n):
    divisors=[x for x in range(2,n+1) if n%x==0]
    digits=[int(x) for x in str(n)]
    k=[0]*len(divisors)
   
    for x in divisors:  
        c=0      
        for y in digits:
            if y!=0:
                if euclid(x,y)==1:
                    c+=1
        k[divisors.index(x)]=c
    
    return max(k),divisors[k.index(max(k))]


#task2
def check_sort(st):
    st=st.lower()
    return sorted(st)==list(st)

def check_A(st):
    return st.count("A")

def check_path(st):
    if not '/' in st:
        return "Wrong input"
    st=st.split('/')
    return st[-1].split('.')[0]




#task3
def reg(st):

    pattern = r'\b([0-2]?[0-9]|3[01])\s(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s(\d{4})\b'
    
    return re.findall(pattern, st)

#task4

def check_low(st):
    pattern = r'[a-z]'
    
    return re.findall(pattern, st)

def check_amount(st):
    pattern=r'[a-zA-z]'
    return len(set(re.findall(pattern, st)))

#task9
def sortlen():
    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
    mst.sort(key=lambda x:len(x))
    return mst
def sortwordlen():
    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
    mst.sort(key=lambda x:len(x.split(' ')))
    return mst

def sortascii():
    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
    mst.sort(key=lambda x:sum([ord(v) for v in x.split('')])/len(x))
    return mst

def sortqlen():
    def average_ascii_value(s):
    
        return sum(ord(char) for char in s) / len(s)

    def quadratic_deviation(val1, val2):
    
        return (val1 - val2) ** 2

    def sort_by_quadratic_deviation(strings):
        if len(strings) == 0:
            return []
        
    
        avg_ascii_first = average_ascii_value(strings[0])
        
    
        sorted_strings = sorted(strings, key=lambda s: quadratic_deviation(average_ascii_value(s), avg_ascii_first))
        
        return sorted_strings
    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
  
    return sort_by_quadratic_deviation(mst)
def sortqlentrip():
    def get_mirror_triples(s):
        count = []
       
        for i in range(len(s) - 2):
            if s[i] == s[i + 2]:
                count.append([s[i]+s[i+1]+s[i+2]])
        return max([average_ascii_value(x) for x in count])/len(count)

    def average_ascii_value(s):    
        return sum(ord(char) for char in s) / len(s)

    def quadratic_deviation(val1, val2):   
        return (val1 - val2) ** 2
    def sort_by_magic(strings):     
        sorted_strings = sorted(strings, key=lambda s: quadratic_deviation(average_ascii_value(s),get_mirror_triples(s)))
        return sorted_strings
    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
  
    return sort_by_magic(mst)

def sorttriplen():
    def count_mirror_triples(s):
        count = 0
       
        for i in range(len(s) - 2):
            if s[i] == s[i + 2]:
                count += 1
        return count

    def sort_by_mirror_triples(strings):
     
        sorted_strings = sorted(strings, key=lambda s: count_mirror_triples(s))
        return sorted_strings

    mst=[]
    st=input('Enter strings type exit when finished: ')
    while st!="exit":
        mst.append(st)
        st=input('Enter strings type exit when finished: ')
  
    return sort_by_mirror_triples(mst)
#lasttask

def indexes(arr):
    min1_idx = arr.index(min(arr))
    
   
    arr[min1_idx]=max(arr)+1
   
    min2_idx = arr.index(min(arr))
    
    return min1_idx, min2_idx

    
def lost(arr):
    a=min(arr)
    b=max(arr)
    ans=[]
    for i in range(a,b):
        if i not in arr:
            ans.append(i)
            
    return ans
def locmax(arr):
    count = 0
    n = len(arr)

    
    if n > 0 and (n == 1 or arr[0] > arr[1]):
        count += 1  

    if n > 1 and arr[n - 1] > arr[n - 2]:
        count += 1 


    for i in range(1, n - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            count += 1

    return count

def chered(arr):
    


    is_int = isinstance(arr[0], int)

    for i in range(1, len(arr)):
       
        current_is_int = isinstance(arr[i], int)

      
        if current_is_int == is_int:
            return False

        
        is_int = current_is_int

    return True


def last(arr):
    def is_prime(n):
        for i in range(2,n):
            if n%i==0:
                return False
            
        return True
    primes=[x for x in arr if is_prime(x)]
    srar_prime=sum(primes)/len(primes)
    ans=[x for x in arr if not is_prime(x) and x>srar_prime]
    return sum(ans)/len(ans)



if __name__=="__main__":
    number=int(input('Enter taskNumber: '))
    if number==1:
        x=int(input('Enter the number: '))
        print(coprimes_amount(x))
        print(sum_of_d(x))
        print(divisor_copr_w_dig(x))
    elif number==2:
        x=(input('Enter the string: '))
        print(check_sort(x))
        print(check_A(x))
        print(check_path(x))
    elif number==5:
        x=(input('Enter the string: '))
        print(reg(x))
    elif number==6:
        x=(input('Enter the string: '))
        print(check_low(x))
        print(check_amount(x))
        print(check_path(x))
    elif number==9:
        print(sortlen())
    elif number==10:
        print(sortwordlen())
    elif number==11:
        print(sortascii())
        print(sortqlentrip())
        print(sortqlen())
        print(sorttriplen())
    elif number==15:
        st=input('Enter array: ').split(' ')
        x=[int(y) for y in st if '.' not in y]
        print(indexes(x))
        print(lost(x))
        print(locmax(x))       
        
        xi=[int(z) for z in st if '.' not in z]
        xf=[float(z) for z in st if '.'  in z]
        x=xi+xf
        print(x)
        print(chered(x))
        print(last(x))
