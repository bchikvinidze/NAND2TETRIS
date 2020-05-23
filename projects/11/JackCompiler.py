import sys
import os
import re

path = sys.argv[1]
isFile = os.path.isfile(path)
fileList = []
outFileNames_vm = []
tokenIndex = 1
classSymbolTable = {}
classSymbolCounts = {'static':0,'this':0}

classname = ""
whileCounter = 0
ifCounter = 0
args = 0

dict_keywords = {'class':'keyword','constructor':'keyword','function':'keyword',
        'method':'keyword','field':'keyword','static':'keyword','var':'keyword','int':'keyword',
        'char':'keyword','boolean':'keyword','void':'keyword','true':'keyword','false':'keyword','null':'keyword',
        'this':'keyword','let':'keyword','do':'keyword','if':'keyword','else':'keyword',
        'while':'keyword','return':'keyword'}
        
symbol_keywords ={'{':'symbol','}':'symbol','(':'symbol',')':'symbol','[':'symbol',
        ']':'symbol','.':'symbol',',':'symbol',';':'symbol','+':'symbol',
        '-':'symbol','*':'symbol','/':'symbol','&':'symbol','|':'symbol',
        '<':'symbol','>':'symbol','=':'symbol','~':'symbol'}

specialCases = {'<':'&lt;','>':'&gt;','&':'&amp;'}

keyword = '(class|constructor|function|method|static|field|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)'
symbol = '[{}()[\].,;+\-*/&|<>=~]' #forgot escape for ]
integerConstant = '\d+'
stringConstant = '"[^"\n]*"'
identifier = '[\w]+'

#files to cover
if isFile:
    fileList.append(path)
    outFileNames_vm.append(path[0:(len(path)-5)] + '.vm')
else:
    for filename in os.listdir(path):
        if filename.endswith(".jack"):
            fileList.append(path+"/"+filename)
            outFileNames_vm.append(path + "/" + filename[0:len(filename)-5] + '.vm')
        else:
            continue

def removeComments(line):
    line = line.strip()
    if line == '' or line[0:2] == '//' or line[0:2] == "/*" or line[0] == "*":
        return ""
    result = line.split("//")
    return result[0]

def tokenizer(textToTokenize):
    regex = re.compile(symbol+"|"+identifier+"|"+stringConstant+"|"+integerConstant)
    elems = regex.findall(textToTokenize)
    return elems   

def makeTxml(tokens):
    txml = "<tokens>\n"
    for token in tokens:
        newLine = ""
        if token in dict_keywords:
            newLine = "<keyword> "+token+" </keyword>\n"
        elif token in symbol_keywords:
            if token in specialCases:
                newLine = "<symbol> "+specialCases.get(token)+" </symbol>\n"
            else:
                newLine = "<symbol> "+token+" </symbol>\n"
        elif re.match(integerConstant,token):
            newLine = "<integerConstant> "+token+" </integerConstant>\n"
        elif re.match(stringConstant,token):
            newLine = "<stringConstant> "+token.replace('"','')+" </stringConstant>\n"
        elif re.match(identifier,token):
            newLine = "<identifier> "+token+" </identifier>\n"
        txml = txml + newLine
    txml = txml + "</tokens>"
    return txml

def updateClassSymbolTable(name, typeof, kind):
    global classSymbolTable
    global classSymbolCounts
    if(kind == 'field'):
        kind = 'this'
    classSymbolTable[name] = (typeof, kind, classSymbolCounts[kind])
    classSymbolCounts[kind] = classSymbolCounts[kind] + 1
    
def compileClass(tokens, txml):
    global tokenIndex
    tokenIndex = tokenIndex+3
    result = ""
    while tokens[tokenIndex-1] == "field" or tokens[tokenIndex-1] == "static" :
        typeof = tokens[tokenIndex]
        kind = tokens[tokenIndex-1]
        updateClassSymbolTable(tokens[tokenIndex+1], typeof, kind)
        compileClassVarDec(txml, tokens, typeof, kind)
    while (tokens[tokenIndex-1] == "constructor" or tokens[tokenIndex-1] == "function" or tokens[tokenIndex-1] == "method"):
        result += compileSubroutineDec(txml, tokens, tokens[tokenIndex-1])
    return result

def compileClassVarDec(txml, tokens, typeof, kind):
    global tokenIndex
    while(tokens[tokenIndex-1] != ";"):
        if(tokens[tokenIndex] == ","):
            updateClassSymbolTable(tokens[tokenIndex+1], typeof, kind)
        tokenIndex = tokenIndex + 1
    tokenIndex = tokenIndex + 1

def compileSubroutineDec(txml, tokens, subroutineType):
    global tokenIndex
    global ifCounter
    result = ""
    expressionListCounter = 0
    paramListCounter = 0
    whileCounter = 0
    ifCounter = 0
    whileCounter = 0
    subroutineSymbolCounts = {'local':0,'argument':0}
    subroutineSymbolTable = {}
    if(subroutineType == "method"):
        subroutineSymbolTable['this'] = (classname, 'argument', 0)
        subroutineSymbolCounts['argument'] = 1       
    tokenIndex = tokenIndex + 2 #bypass return type, parameter name
    subroutineName = classname + "." + tokens[tokenIndex-1]
    tokenIndex = tokenIndex + 2
    compileParameterList(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    tokenIndex = tokenIndex + 2
    varcnt = 0
    while tokens[tokenIndex-1] == "var":
        compileVarDec(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    result += function(subroutineName, subroutineSymbolCounts['local'])
    if subroutineType == "constructor":
        result += push('constant', classSymbolCounts['this'])
        result += "call Memory.alloc 1\n"
        result += "pop pointer 0\n"
    elif subroutineType == "method":
        result += push('argument', 0)
        result += pop('pointer', 0)
    result += compileStatements(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts) 
    tokenIndex = tokenIndex+ 1
    return result;

def compileParameterList(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global paramListCounter
    paramListCounter = 0
    while(tokens[tokenIndex-1] != ")"):
        if "identifier" in txml[tokenIndex] and "identifier" not in txml[tokenIndex+1]:
            subroutineSymbolTable[tokens[tokenIndex-1]] = (tokens[tokenIndex-2], 'argument', subroutineSymbolCounts['argument'])
            subroutineSymbolCounts['argument'] = subroutineSymbolCounts['argument'] + 1
        tokenIndex = tokenIndex + 1
        paramListCounter += 1

def compileVarDec(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    tokenIndex = tokenIndex + 2
    typeof = ""
    while(tokens[tokenIndex-1] != ";"):
        if "identifier" in txml[tokenIndex]:
            if(typeof == ""):
                typeof = tokens[tokenIndex-2]
                subroutineSymbolTable[tokens[tokenIndex-1]] = (typeof, 'local', subroutineSymbolCounts['local'])
                subroutineSymbolCounts['local'] = subroutineSymbolCounts['local'] + 1
            else:    
                subroutineSymbolTable[tokens[tokenIndex-1]] = (typeof, 'local', subroutineSymbolCounts['local'])
                subroutineSymbolCounts['local'] = subroutineSymbolCounts['local'] + 1
        tokenIndex = tokenIndex + 1
    tokenIndex = tokenIndex + 1
    
def compileStatements(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    result = ""
    while tokens[tokenIndex-1] == "let" or tokens[tokenIndex-1] == "if" or tokens[tokenIndex-1] == "while" or tokens[tokenIndex-1] == "do" or tokens[tokenIndex-1] == "return":
        if tokens[tokenIndex-1] == "let":
            result += compileLet(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        elif tokens[tokenIndex-1] == "if":
            result += compileIf(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        elif tokens[tokenIndex-1] == "while":
            result += compileWhile(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        elif tokens[tokenIndex-1] == "do":
            result += compileDo(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        elif tokens[tokenIndex-1] == "return":
            result += compileReturn(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        tokenIndex = tokenIndex + 1
    return result

def compileLet(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global classSymbolTable
    global classSymbolCounts
    tokenIndex = tokenIndex + 1
    var = tokens[tokenIndex-1]
    kind = ""
    index = -1
    result = ""
    if var in classSymbolTable:
        kind = classSymbolTable[var][1] 
        index = classSymbolTable[var][2] 
    else:
        kind = subroutineSymbolTable[var][1]
        index = subroutineSymbolTable[var][2]
    tokenIndex = tokenIndex + 1
    if tokens[tokenIndex-1] == "[":
        tokenIndex = tokenIndex + 1
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        tokenIndex = tokenIndex + 1
        result += push(kind, index)
        result += "add\n" #arr[i] shift by i
        tokenIndex = tokenIndex + 1
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        result += "pop temp 0\n"
        result += "pop pointer 1\n"
        result += "push temp 0\n"
        result += "pop that 0\n"
    else:
        tokenIndex = tokenIndex + 1
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        if var in classSymbolTable:
            result += pop(classSymbolTable[var][1], classSymbolTable[var][2])
        else:
            result += pop(subroutineSymbolTable[var][1], subroutineSymbolTable[var][2])
    return result

def compileIf(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global ifCounter
    nthif = ifCounter
    ifCounter += 1
    tokenIndex = tokenIndex + 2
    result = compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    tokenIndex = tokenIndex + 2
    result += "not\n"
    result += "if-goto notif"+str(nthif)+"\n"
    result += compileStatements(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    tokenIndex = tokenIndex + 1
    result += "goto ifend" + str(nthif)+"\n"
    result += "label notif" + str(nthif)+"\n"
    if tokens[tokenIndex-1] == "else":
        tokenIndex = tokenIndex + 2
        result += compileStatements(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    else:
        tokenIndex =  tokenIndex - 1
    result += "label ifend"+ str(nthif)+"\n"
    return result


def compileWhile(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global whileCounter
    result = ""
    nthWhile = whileCounter
    whileCounter += 1
    result = "label while"+str(nthWhile)+"\n"
    tokenIndex = tokenIndex + 2
    result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    result += "not\n"
    result += "if-goto whileBreak"+str(nthWhile)+"\n"
    tokenIndex = tokenIndex + 2
    result += compileStatements(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    result += "goto while"+str(nthWhile)+"\n"
    result += "label whileBreak"+str(nthWhile)+"\n"
    return result

def compileDo(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    result = subroutineCall(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    result += "pop temp 0\n"
    tokenIndex = tokenIndex+1 
    return result


def compileReturn(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    tokenIndex = tokenIndex + 1
    result = ""
    if tokens[tokenIndex-1] != ";":
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    else:
        result += push('constant',0)
    #tokenIndex = tokenIndex + 1
    result += ret()
    return result

def compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    result = ""
    result += compileTerm(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    while tokens[tokenIndex-1] in ['+','-','*','/','&','|','<','>','=']:
        op = tokens[tokenIndex-1]
        tokenIndex = tokenIndex + 1
        result += compileTerm(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        result += calc(op)
    return result

def compileTerm(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global classSymbolTable
    result = ""
    if tokens[tokenIndex-1] == "(": #meaning its expression
        tokenIndex = tokenIndex + 1
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        tokenIndex = tokenIndex + 1
    elif tokens[tokenIndex-1] in ['-','~']:
        symbol = tokens[tokenIndex-1]
        tokenIndex = tokenIndex + 1
        result += compileTerm(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        if(symbol == '-'):
            result += "neg\n"
        else:
            result += "not\n"
    else:
        var = tokens[tokenIndex-1]
        if "stringConstant" in  txml[tokenIndex]:
            string_constant = tokens[tokenIndex-1].replace('"','')
            result += push("constant", len(string_constant))
            result += "call String.new 1\n"
            for char in string_constant:
                result += "push constant " + str(ord(char)) + "\n"
                result += "call String.appendChar 2\n"
            tokenIndex = tokenIndex + 1
        elif "keyword" in txml[tokenIndex]:
            if tokens[tokenIndex-1] == "true":
                result += "push constant 1\n"
                result += "neg\n"
            elif tokens[tokenIndex-1] != "this":
                result += "push constant 0\n"
            else:
                result += "push pointer 0\n"
            tokenIndex = tokenIndex + 1
        elif "Constant" in txml[tokenIndex]:
            result += push("constant", tokens[tokenIndex-1])
            tokenIndex = tokenIndex + 1
        elif tokens[tokenIndex] == "[":
            #var = tokens[tokenIndex-1]
            tokenIndex = tokenIndex + 2
            result += compileExpression(txml, tokens,  subroutineSymbolTable, subroutineSymbolCounts)
            tokenIndex = tokenIndex + 1
            kind = ""
            index = -1
            if var in classSymbolTable:
                kind = classSymbolTable[var][1]
                index = classSymbolTable[var][2]
            else:
                kind = subroutineSymbolTable[var][1]
                index = subroutineSymbolTable[var][2]
            result += push(kind, index) 
            result += "add\n"
            result += "pop pointer 1\n"
            result += "push that 0\n"
        elif tokens[tokenIndex] == "." or tokens[tokenIndex] == "(":
            tokenIndex = tokenIndex - 1 #gadavedi dasawyisze
            result += subroutineCall(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
            tokenIndex = tokenIndex + 1
        else:
            kind = ""
            index = -1
            if var in classSymbolTable:
                kind = classSymbolTable[var][1]
                index = classSymbolTable[var][2]
            else:
                kind = subroutineSymbolTable[var][1]
                index = subroutineSymbolTable[var][2]
            result += push(kind,index)
            tokenIndex = tokenIndex + 1
    return result

def subroutineCall(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global expressionListCounter
    tokenIndex = tokenIndex + 2
    identifierName = tokens[tokenIndex-2]
    result = ""
    extraParam = 0
    if tokens[tokenIndex-1] == "(": #subroutine
        result += "push pointer 0\n"
        extraParam = 1
        identifierName = classname + "." + identifierName
    elif tokens[tokenIndex-1] == ".": #classname/varname
        if identifierName in classSymbolTable or identifierName in subroutineSymbolTable:
            tokenIndex = tokenIndex + 1
            subroutine = tokens[tokenIndex-1]
            if identifierName in classSymbolTable:
                kind = classSymbolTable[identifierName][1]
                index = classSymbolTable[identifierName][2]
                typeof = classSymbolTable[identifierName][0]
                result += push(kind, index)
                identifierName = typeof + "." + subroutine
            elif identifierName in subroutineSymbolTable:
                kind = subroutineSymbolTable[identifierName][1]
                index = subroutineSymbolTable[identifierName][2]
                typeof = subroutineSymbolTable[identifierName][0]
                result += push(kind, index)
                identifierName = typeof + "." + subroutine
            extraParam = 1
            tokenIndex = tokenIndex + 1
        else:
            identifierName = identifierName + "." + tokens[tokenIndex]   #class
            tokenIndex = tokenIndex + 2
    result += compileExpressionList(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
    result += call(identifierName, expressionListCounter+extraParam)
    return result


def compileExpressionList(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts):
    global tokenIndex
    global expressionListCounter
    result = ""
    expressionListCounter = 0
    tokenIndex=tokenIndex+1#
    if tokens[tokenIndex-1] != ")": #eseigi expression
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        expressionListCounter += 1
    while tokens[tokenIndex-1] != ")":
        tokenIndex = tokenIndex + 1
        result += compileExpression(txml, tokens, subroutineSymbolTable, subroutineSymbolCounts)
        expressionListCounter += 1
    return result



def push(typeof, val):
    result = "push " + typeof + " " + str(val) + "\n"
    return result

def pop(typeof, val):
    result =  "pop " + typeof + " " + str(val) + "\n"
    return result

def ret():
    return 'return\n'

def function(name, var):
    return "function " + name + " " + str(var) + "\n"

def calc(op):
    operator_map = {'+':'add','-':'sub', '*':'call Math.multiply 2',
                   '/':'call Math.divide 2', '&':'and', '|':'or', '<':'lt',
                   '>':'gt', '=':'eq'}
    return operator_map[op] + "\n"

def call(func, arg):
    return "call " + func + " " + str(arg) + "\n"




for file,outfile in zip(fileList,outFileNames_vm):
    fileIn = open(file,'r') 
    fileOut = open(outfile,'w')
    rows = fileIn.readlines()
    textToTokenize = ""
    for line in rows:
        textToTokenize = textToTokenize + removeComments(line)
    textToTokenize = ' '.join(textToTokenize.split())
    tokens = tokenizer(textToTokenize)
    txml = makeTxml(tokens)
    tokenIndex = 1
    classSymbolTable = {}
    classSymbolCounts = {'static':0,'this':0}
    classname = file.split("/")
    classname = classname[len(classname)-1]
    classname = classname[0:len(classname)-5]
    code = compileClass(tokens, txml.splitlines())
    fileOut.write(code)
    fileIn.close()
    fileOut.close()
