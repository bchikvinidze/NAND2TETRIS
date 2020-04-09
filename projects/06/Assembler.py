import sys
import os
filename = sys.argv[1]
outFilename = filename[0:(len(filename)-4)] + '.hack'
fileIn = open(filename,'r') 
fileOut = open(outFilename,'w')
rows = fileIn.readlines()
userLabelDict = {}
sp = 0
for line in rows:
    if line.strip() != '' and line[0:2] != '//':
        line=line.replace(" ", "")
        if (line.startswith("(")):
            symbol = line[1:len(line)-2]
            userLabelDict[symbol] = sp
        else:
            sp = sp+1
            
compDict = {'0':'0101010',
            '1':'0111111',
            '-1':'0111010',
            'D':'0001100',
            'A':'0110000',
            '!D':'0001101',
            '!A':'0110001',
            '-D':'0001111', 
            '-A':'0110011',
            'D+1':'0011111',
            'A+1':'0110111',
            'D-1':'0001110',    
            'A-1':'0110010',
            'D+A':'0000010',
            'D-A':'0010011',
            'A-D':'0000111',
            'D&A':'0000000',
            'D|A':'0010101',
            'M':'1110000',
            '!M':'1110001',
            '-M':'1110011',
            'M+1':'1110111',
            'M-1':'1110010',
            'D+M':'1000010',
            'D-M':'1010011',
            'M-D':'1000111',
            'D&M':'1000000',
            'D|M':'1010101'}

destDict = { "":'000',
            'M':'001',
            'D':'010',
            'MD':'011',
            'A':'100',
            'AM':'101',
            'AD':'110',
            'AMD':'111'}

jumpDict = {"":'000',    
            "JGT":'001',  
            "JEQ":'010',
            "JGE":'011',
            "JLT":'100',
            "JNE":'101',
            "JLE":'110',
            "JMP":'111'}

labelDict = {'SP':0,
            'LCL':1,
            'ARG':2,
            'THIS':3,
            'THAT':4,
            'R0':0,
            'R1':1,
            'R2':2,
            'R3':3,
            'R4':4,
            'R5':5,
            'R6':6,
            'R7':7,
            'R8':8,
            'R9':9,
            'R10':10,
            'R11':11,
            'R12':12,
            'R13':13,
            'R14':14,
            'R15':15,
            'SCREEN':16384,
            'KBD': 24576 }

fileIn = open(filename,'r') 
rows = fileIn.readlines()
nextRam = 16
usedRAMs = list(userLabelDict.values())
for line in rows:
    if line.strip() != '' and line[0:2] != '//':
        line=line.replace(" ", "")
        line=line.split('//')[0] # before comment
        line=line.split('\n')[0] # before newline
        if line.startswith("@"):
            ramAddr = ""
            inp = line[1:len(line)]
            if(inp in labelDict):
                ramAddr = labelDict[inp]
            elif(inp in userLabelDict):
                ramAddr = userLabelDict[inp]
            if(ramAddr == ""):
                if(not inp.isdigit()):
                    symbol = line[1:len(line)]
                    #while(nextRam in usedRAMs):
                        #nextRam = nextRam + 1
                    userLabelDict[symbol] = nextRam
                    #usedRAMs.append(nextRam)
                    v = list(('{0:b}'.format(nextRam).zfill(16)))
                    nextRam = nextRam + 1
                else:    
                    v = list(('{0:b}'.format(int(inp)).zfill(16)))
                    #usedRAMs.append(int(inp))
            else:
                v = list(('{0:b}'.format(ramAddr)).zfill(16))
            #print("A inst: "+"".join(str(a) for a in v)+", ramAddr: "+str(ramAddr))
        elif line.startswith("("):
            continue
        else:
            dest = ""
            jump = ""
            comp = ""
            if('=' in line):
                lst = line.split('=')
                dest = lst[0]
                comp = lst[1].split(';')[0]                
            if(';' in line):
                lst = line.split(';')
                jump = lst[len(lst)-1]
                if comp == "":
                    comp = lst[0]
            comp = comp.strip('\n')
            jump = jump.strip('\n')
            v=list('1110000000000000')
            v[3:10] = compDict[comp]
            v[10:13] = destDict[dest]
            v[13:16] = jumpDict[jump]                
            tmp="".join(str(a) for a in v)
            #print("C inst: v = "+tmp+", dest = "+dest+", comp: "+comp+", jump: "+jump)
        fileOut.write("".join(str(a) for a in v)+"\n")
        sp = sp + 1
fileOut.close()
fileIn.close()
