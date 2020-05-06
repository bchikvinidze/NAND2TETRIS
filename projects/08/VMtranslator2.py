import sys
import os

path = sys.argv[1]
isFile = os.path.isfile(path)
fileList = []
outFileName = ""
eqLab, ltLab, gtLab, nextLab = 0, 0, 0, 0
sysintencountered = False

#files to cover
if isFile:
    fileList.append(path)
    outFileName = path[0:(len(path)-3)] + '.asm'
else:
    for filename in os.listdir(path):
        if filename.endswith(".vm"):
            fileList.append(path+"/"+filename)
            if outFileName == "":
                pathFolders = path.split("/")
                outFileName = path + "/" + pathFolders[len(pathFolders)-1] + '.asm'
        else:
            continue

#one output file will be used            
fileOut = open(outFileName,'w') 

index = 0
#iterate files. Big part of the code is copied from my previous assignment
for filename in fileList:
    fileIn = open(filename,'r') 
    filename_elems = filename.split("/")
    cnt_folders = len(filename_elems)
    filename_without_path = filename_elems[cnt_folders-1]
    rows = fileIn.readlines()
    for line in rows:
        if line.strip() != '' and line[0:2] != '//':
            #line=line.split(" ")
            line=' '.join(line.split())
            line=line.split(" ")
            for elem in line:
                elem = elem.rstrip()
            asm = ""
            #for elem in line:
            #    print(elem)
            #print("\n")
            if line[0] == "push":
                if line[1] == "constant":    
                    const = line[2]
                    asm += "@" + const + "\n"
                    asm += "D=A\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "local":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@LCL\n"
                    asm += "A=M+D\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"                
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "argument":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@ARG\n"
                    asm += "A=M+D\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"              
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "this":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@THIS\n"
                    asm += "A=M+D\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"              
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "that":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@THAT\n"
                    asm += "A=M+D\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"              
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "static":
                    asm += "@"+filename_without_path+"."+str(line[2])+ "\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "temp":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@5\n" 
                    asm += "A=A+D\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"              
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[1] == "pointer":
                    if line[2] == "0": #THIS
                        asm += "@THIS\n"
                        asm += "D=M\n"
                        asm += "@SP\n"
                        asm += "A=M\n"
                        asm += "M=D\n"
                        asm += "@SP\n"
                        asm += "M=M+1\n"
                    elif line[2] == "1": #THAT
                        asm += "@THAT\n"
                        asm += "D=M\n"
                        asm += "@SP\n"
                        asm += "A=M\n"
                        asm += "M=D\n"
                        asm += "@SP\n"
                        asm += "M=M+1\n"
            elif line[0] == "pop":
                if line[1] == "local":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@LCL\n"
                    asm += "D=M+D\n"
                    asm += "@R15\n"
                    asm += "M=D\n" 
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@R15\n"
                    asm += "A=M\n"
                    asm += "M=D\n"              
                elif line[1] == "argument":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@ARG\n" #same as lcl, only this part is changed
                    asm += "D=M+D\n" 
                    asm += "@R15\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@R15\n"
                    asm += "A=M\n"
                    asm += "M=D\n"       
                elif line[1] == "this":
                    const = line[2]
                    asm += "@" + const + "\n"
                    asm += "D=A\n"
                    asm += "@THIS\n" #same as lcl, only this part is changed
                    asm += "D=M+D\n" 
                    asm += "@R15\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@R15\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                elif line[1] == "that":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@THAT\n" #same as lcl, only this part is changed
                    asm += "D=M+D\n" 
                    asm += "@R15\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@R15\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                elif line[1] == "static":
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@"+filename_without_path+"."+str(line[2])+ "\n"
                    asm += "M=D\n"
                elif line[1] == "temp":
                    const = line[2]
                    asm += "@" + const+ "\n"
                    asm += "D=A\n"
                    asm += "@5\n" #same as lcl, only this part is changed
                    asm += "D=A+D\n" #change only M to A (difference from lcl implementation)
                    asm += "@R15\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@R15\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                elif line[1] == "pointer":
                    if line[2] == "0": #THIS
                        asm += "@SP\n"
                        asm += "M=M-1\n"
                        asm += "A=M\n"
                        asm += "D=M\n"
                        asm += "@THIS\n"
                        asm += "M=D\n"
                    elif line[2] == "1": #THAT
                        asm += "@SP\n"
                        asm += "M=M-1\n"
                        asm += "A=M\n"
                        asm += "D=M\n"
                        asm += "@THAT\n"
                        asm += "M=D\n"
            elif line[0] == "add":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "D=D+M\n"
                asm += "M=D\n"
            elif line[0] == "neg":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "M=-M\n"
                asm += "@SP\n"
                asm += "M=M+1\n"
            elif line[0] == "sub":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "D=M-D\n"
                asm += "M=D\n"
            elif line[0] == "eq":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "D=D-M\n"
                asm += "M=0\n"
                asm += "@EQ"+str(eqLab)+"\n"
                asm += "D;JEQ\n"
                asm += "@NEXT"+str(nextLab)+"\n"
                asm += "0;JMP\n"
                asm += "(EQ"+str(eqLab)+")\n"
                asm += "@SP\n"
                asm += "A=M-1\n"
                asm += "M=-1\n"
                asm += "(NEXT"+str(nextLab)+")\n"
                eqLab += 1
                nextLab += 1
            elif line[0] == "gt":  
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "D=D-M\n"
                asm += "M=-1\n"
                asm += "@GT"+str(gtLab)+"\n"
                asm += "D;JGE\n"
                asm += "@NEXT"+str(nextLab)+"\n"
                asm += "0;JMP\n"
                asm += "(GT"+str(gtLab)+")\n"
                asm += "@SP\n"
                asm += "A=M-1\n"
                asm += "M=0\n"
                asm += "(NEXT"+str(nextLab)+")\n"
                gtLab += 1
                nextLab += 1
            elif line[0] == "lt":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "D=D-M\n"
                asm += "M=-1\n"
                asm += "@LT"+str(ltLab)+"\n"
                asm += "D;JLE\n"
                asm += "@NEXT"+str(nextLab)+"\n"
                asm += "0;JMP\n"
                asm += "(LT"+str(ltLab)+")\n"
                asm += "@SP\n"
                asm += "A=M-1\n"
                asm += "M=0\n"
                asm += "(NEXT"+str(nextLab)+")\n"
                ltLab += 1
                nextLab += 1
            elif line[0] == "and":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "M=M&D\n"
            elif line[0] == "or":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "A=A-1\n"
                asm += "M=M|D\n"
            elif line[0] == "not":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "M=!M\n"
                asm += "@SP\n"
                asm += "M=M+1\n"
            elif line[0] == "label":
                asm += "("+line[1] + filename_without_path + ")\n"
            elif line[0] == "goto":
                asm += "@"+line[1] + filename_without_path+ "\n"
                asm += "0;JMP\n"
            elif line[0] == "if-goto":
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                #asm += "M=0\n"
                asm += "@"+line[1]+filename_without_path+"\n"
                asm += "D;JNE\n"
            elif line[0] == "function":
                if line[1] == "Sys.init" and not sysintencountered:
                    sysintencountered = True
                funcName = line[1]
                asm += "("+funcName+")\n"
                asm += "@" + line[2]+"\n"
                asm += "D=A\n"
                asm += "@COUNTER_" + funcName + "\n"
                asm += "M=D\n"
                asm += "(LOOP_"+ funcName + ")\n"
                asm += "@COUNTER_" + funcName + "\n"
                asm += "D=M\n"
                asm += "@LOOPEND_"+ funcName + "\n"
                asm += "D;JEQ\n"
                asm += "@COUNTER_" + funcName + "\n"
                asm += "M=M-1\n" #from now on pushing begins:
                asm += "@0\n"
                asm += "D=A\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" 
                asm += "@LOOP_"+ funcName + "\n"
                asm += "0;JMP\n"
                asm += "(LOOPEND_"+ funcName + ")\n"
            elif line[0] == "return":
                asm += "@LCL\n"
                asm += "D=M\n"
                asm += "@ENDFRAME\n"
                asm += "M=D\n" #endFrame = LCL ends here
                asm += "D=M\n"
                asm += "@5\n"
                asm += "D=D-A\n"
                asm += "A=D\n"
                asm += "D=M\n"
                asm += "@RetAddr"+str(index)+"\n"
                asm += "M=D\n" #retAddr = *(endFrame – 5) ends here
                asm += "@ARG\n" 
                asm += "D=M\n"
                #
                asm += "@IND"+str(index)+"\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M-1\n"
                asm += "A=M\n"
                asm += "D=M\n"
                asm += "@IND"+str(index)+"\n"
                #
                asm += "A=M\n"
                asm += "M=D\n" #*ARG = pop() ends here
                asm += "@ARG\n"
                asm += "D=M+1\n"
                asm += "@SP\n"
                asm += "M=D\n" #SP = ARG + 1 ends here (same as pop argument 0)
                asm += "@ENDFRAME\n"
                asm += "D=M-1\n"
                asm += "A=D\n"
                asm += "D=M\n"
                asm += "@THAT\n"
                asm += "M=D\n" #THAT = *(endFrame – 1) ends here
                asm += "@2\n"
                asm += "D=A\n"
                asm += "@ENDFRAME\n"
                asm += "D=M-D\n"
                asm += "A=D\n"
                asm += "D=M\n"
                asm += "@THIS\n"
                asm += "M=D\n" #THIS = *(endFrame – 2) ends here
                asm += "@3\n"
                asm += "D=A\n"
                asm += "@ENDFRAME\n"
                asm += "D=M-D\n"
                asm += "A=D\n"
                asm += "D=M\n"
                asm += "@ARG\n"
                asm += "M=D\n" #ARG = *(endFrame – 3) ends here
                asm += "@4\n"
                asm += "D=A\n"
                asm += "@ENDFRAME\n"
                asm += "D=M-D\n"
                asm += "A=D\n"
                asm += "D=M\n"
                asm += "@LCL\n"
                asm += "M=D\n" #LCL = *(endFrame – 4) ends here
                asm += "@RetAddr"+str(index)+"\n"
                asm += "A=M\n" #I forgot this
                asm += "0;JMP\n" #goto *retAddr ends here
            elif line[0] == "call":
                asm += "@RetAddrLabel_"+ line[1] +str(index)+"\n"
                asm += "D=A\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" #push retAddrLabel ends here
                asm += "@LCL\n"
                asm += "D=M\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" #push LCL ends here
                asm += "@ARG\n"
                asm += "D=M\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" #push ARG ends here
                asm += "@THIS\n"
                asm += "D=M\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" #push THIS ends here
                asm += "@THAT\n"
                asm += "D=M\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n" #push THAT ends here
                asm += "@SP\n"
                asm += "D=M\n"
                asm += "@5\n"
                asm += "D=D-A\n"
                asm += "@"+line[2]+"\n"
                asm += "D=D-A\n"
                asm += "@ARG\n"
                asm += "M=D\n" #ARG = SP-5-nArgs ends here 
                asm += "@SP\n"
                asm += "D=M\n"
                asm += "@LCL\n"
                asm += "M=D\n" #LCL = SP ends heere
                asm += "@"+line[1].rstrip()+"\n"
                asm += "0;JMP\n" #goto functionName ends here
                asm += "(RetAddrLabel_"+line[1]+str(index)+")\n"
                index = index + 1
            fileOut.write(asm) 
            
#adding bootstrap code:
if sysintencountered:
    temp = open(path+"/temp.asm",'w')
    bt = "@256\n"
    bt += "D=A\n"
    bt += "@SP\n"
    bt += "M=D\n"
    #After this, sys.init should be called:
    bt += "@RetAddrLabel_Sys.init\n"
    bt += "D=A\n"
    bt += "@SP\n"
    bt += "A=M\n"
    bt += "M=D\n"
    bt += "@SP\n"
    bt += "M=M+1\n" #push retAddrLabel ends here
    bt += "@LCL\n"
    bt += "D=M\n"
    bt += "@SP\n"
    bt += "A=M\n"
    bt += "M=D\n"
    bt += "@SP\n"
    bt += "M=M+1\n" #push LCL ends here
    bt += "@ARG\n"
    bt += "D=M\n"
    bt += "@SP\n"
    bt += "A=M\n"
    bt += "M=D\n"
    bt += "@SP\n"
    bt += "M=M+1\n" #push ARG ends here
    bt += "@THIS\n"
    bt += "D=M\n"
    bt += "@SP\n"
    bt += "A=M\n"
    bt += "M=D\n"
    bt += "@SP\n"
    bt += "M=M+1\n" #push THIS ends here
    bt += "@THAT\n"
    bt += "D=M\n"
    bt += "@SP\n"
    bt += "A=M\n"
    bt += "M=D\n"
    bt += "@SP\n"
    bt += "M=M+1\n" #push THAT ends here
    bt += "@SP\n"
    bt += "D=M\n"
    bt += "@5\n"
    bt += "D=D-A\n"
    bt += "@0\n"
    bt += "D=D-A\n"
    bt += "@ARG\n"
    bt += "M=D\n" #ARG = SP-5-nArgs ends here 
    bt += "@SP\n"
    bt += "D=M\n"
    bt += "@LCL\n"
    bt += "M=D\n" #LCL = SP ends heere
    bt += "@Sys.init\n"
    bt += "0;JMP\n" #goto functionName ends here
    bt += "(RetAddrLabel_Sys.init)\n"
    temp.write(bt)
    fileOut.close()
    fileOut = open(outFileName,'r')
    for line in fileOut:
        temp.write(line)
    temp.close()
    os.remove(outFileName)
    os.rename(path+"/temp.asm", outFileName)
else:    
    fileOut.close()
fileIn.close()
