def solve1(v1):
    while True:
        
        temp = 2
        while temp * temp <= v1:
            if v1 % temp == 0:
                break 
            temp += 1 
            
        if temp * temp <= v1:
          
            v1 += 1
            continue
        
        else:
           
            return v1
def solve2(v2,total):
    while total!=0:
        temp=v2%total
        v2=total
        total=temp
    return v2



result1=1
v1=0
while result1 != 4271010253:
    v1+=1
    temp=solve1(v1)
    result1=temp*solve1(temp+128)
    

print(v1)
total=(solve1(solve1(v1)+128)-1)*(solve1(v1)-1)
v2=0
while True:
    result2=0
    
    v2+=1
    n2=v2
    while result2 !=1 or n2>=total:
            n2+=1
            result2=solve2(n2,total)
    if n2==201326609:
        
        break
print(v2)
