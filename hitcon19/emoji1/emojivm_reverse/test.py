numd = {0: '😀', 1: '😁', 2: '😂', 3: '🤣', 4: '😜', 5: '😄', 6: '😅', 7: '😆', 8: '😉', 9: '😊', 10: '😍'}

def temp(x):
    a= []
    a.append(int((x/100)%10))
    a.append(int((x/10)%10))
    a.append(int(x%10))
    return a

def allocate():
    return "⏬😅⏬😍❌⏬😀➕🆕"

def char_load(num):
    a=temp(num)
    if(num<=10):
        return "⏬"+numd[num]
    elif(num>10  and num <100):
        return "⏬"+numd[a[1]]+"⏬😍❌"+"⏬"+numd[a[2]]+"➕"
    elif(num>=100):
        return "⏬"+numd[a[0]]+"⏬😍❌"+"⏬"+numd[a[1]]+"➕"+"⏬😍❌"+"⏬"+numd[a[2]]+"➕"

def load(num):
    i=0
    s=""
    while(i<num):
        s=s+"⏬"+numd[i]+"⏬😀📥"
        i=i+1
    return s

def _print():
    return "⏬😀📝"

def main():
    emoshell=""
    emoshell=emoshell+allocate()
    for i in range(1,10):
        ans = i*1
        emoshell=emoshell+ char_load(ord("\n"))+char_load(ord(str(int(ans%10))))+ char_load(ord(" "))  + char_load(ord("=")) + char_load(ord(" ")) + char_load(ord(str(i))) + char_load(ord(" ")) + char_load(ord("*"))+ char_load(ord(" ")) + char_load(ord("1"))
        emoshell=emoshell+ load(10)
        emoshell = emoshell+ _print()
    
    emoshell=emoshell+ "🛑"
    fp = open("lulz","w")
    fp.write(emoshell)
    fp.close()

main()

def hitcon():
    emoshell=""
    emoshell=emoshell+allocate()
    s = "hitcon"[::-1]
    for i in s:
        emoshell = emoshell + char_load(ord(i))
    emoshell=emoshell+load(6)
    emoshell = emoshell+ _print()
    emoshell=emoshell+ "🛑"
    return emoshell