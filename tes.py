
with open('name.txt','r') as f:
    with open('res.txt',"r") as fr:
        dat = f.read()
        for i in range(0,len(dat)):
            if f[i] != fr[i]:
                print("eror")