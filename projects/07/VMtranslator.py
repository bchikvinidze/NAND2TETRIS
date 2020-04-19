import sys
import os

filename = sys.argv[1]
outFilename = filename[0:(len(filename)-3)] + '.asm'
fileIn = open(filename,'r') 
fileOut = open(outFilename,'w')
rows = fileIn.readlines()
eqLab, ltLab, gtLab, nextLab = 0, 0, 0, 0

filename_elems = filename.split("/")
cnt_folders = len(filename_elems)
filename_without_path = filename_elems[cnt_folders-1]

for line in rows:
    if line.strip() != '' and line[0:2] != '//':
        line=line.split(" ")
        asm = ""
        if line[0] == "push":
            if line[1] == "constant":    
                const = line[2]
                asm += "@" + const
                asm += "D=A\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n"
            elif line[1] == "local":
                const = line[2]
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@"+filename_without_path+"."+str(line[2])
                asm += "D=M\n"
                asm += "@SP\n"
                asm += "A=M\n"
                asm += "M=D\n"
                asm += "@SP\n"
                asm += "M=M+1\n"
            elif line[1] == "temp":
                const = line[2]
                asm += "@" + const
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
                if line[2] == "0\n": #THIS
                    asm += "@THIS\n"
                    asm += "D=M\n"
                    asm += "@SP\n"
                    asm += "A=M\n"
                    asm += "M=D\n"
                    asm += "@SP\n"
                    asm += "M=M+1\n"
                elif line[2] == "1\n": #THAT
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
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@" + const
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
                asm += "@"+filename_without_path+"."+str(line[2])
                asm += "M=D\n"
            elif line[1] == "temp":
                const = line[2]
                asm += "@" + const
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
                if line[2] == "0\n": #THIS
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@THIS\n"
                    asm += "M=D\n"
                elif line[2] == "1\n": #THAT
                    asm += "@SP\n"
                    asm += "M=M-1\n"
                    asm += "A=M\n"
                    asm += "D=M\n"
                    asm += "@THAT\n"
                    asm += "M=D\n"
        elif line[0] == "add\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=D+M\n"
            asm += "M=D\n"
        elif line[0] == "neg\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "M=-M\n"
            asm += "@SP\n"
            asm += "M=M+1\n"
        elif line[0] == "sub\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "D=M-D\n"
            asm += "M=D\n"
        elif line[0] == "eq\n":
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
        elif line[0] == "gt\n":  
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
        elif line[0] == "lt\n":
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
        elif line[0] == "and\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "M=M&D\n"
        elif line[0] == "or\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "D=M\n"
            asm += "A=A-1\n"
            asm += "M=M|D\n"
        elif line[0] == "not\n":
            asm += "@SP\n"
            asm += "M=M-1\n"
            asm += "A=M\n"
            asm += "M=!M\n"
            asm += "@SP\n"
            asm += "M=M+1\n"
        fileOut.write(asm)
fileOut.close()
fileIn.close()
