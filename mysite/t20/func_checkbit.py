#coding:utf-8
def checkbit(id):
    sum=0
    id='{:0>20}'.format(id)
    for i in range(0,20):
        a=i+1
        b=id[20 - a:21 - a]
        c=2 if i%2==0 else 1
        d=c*int(b)
        e=d if d<10 else int(d/10)+d%10
        sum+=e
    checkbit = 0 if sum % 10 == 0 else 10 - sum % 10
    return checkbit
if __name__ == "__main__":
    pass