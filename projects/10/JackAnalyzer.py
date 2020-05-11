import sys
import os
import re

path = sys.argv[1]
isFile = os.path.isfile(path)
fileList = []
outFileNames_txml = []
outFileNames_xml = []
tokenIndex = 1
ind = "  "

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
    outFileNames_txml.append(path[0:(len(path)-5)] + 'T.xml')
    outFileNames_xml.append(path[0:(len(path)-5)] + '.xml')
else:
    for filename in os.listdir(path):
        if filename.endswith(".jack"):
            fileList.append(path+"/"+filename)
            outFileNames_txml.append(path + "/" + filename[0:len(filename)-5] + 'T.xml')
            outFileNames_xml.append(path + "/" + filename[0:len(filename)-5] + '.xml')
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

def makeTxml(tokens, fileOut):
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
    fileOut.write(txml)
    return txml

def compilationEngine(tokens, txml, indent):
    global tokenIndex
    xml = "<class>\n"
    xml = xml + compileClass(tokens, txml, indent+1)
    xml = xml + "</class>\n"
    return xml

def terminal():
    pass

def nonTerminal():
    pass

def compileClass(tokens, txml, indent):
    global tokenIndex
    result = indent*ind + txml[tokenIndex] + "\n" #class
    result += indent*ind + txml[tokenIndex+1] + "\n" #main
    result += indent*ind + txml[tokenIndex+2] + "\n" #{
    tokenIndex = tokenIndex+3
    while tokens[tokenIndex-1] == "field" or tokens[tokenIndex-1] == "static" :
        result += indent*ind + "<classVarDec>" + "\n"
        result += compileClassVarDec(txml, tokens, indent)
        result += indent*ind + "</classVarDec>" + "\n"
    while (tokens[tokenIndex-1] == "constructor" or tokens[tokenIndex-1] == "function" or tokens[tokenIndex-1] == "method"):
        result += indent*ind + "<subroutineDec>" + "\n"
        result += compileSubroutineDec(txml, tokens, indent);
        result += indent*ind + "</subroutineDec>" + "\n"
    result += indent*ind + txml[tokenIndex] + "\n" #}
    return result

def compileClassVarDec(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    while(tokens[tokenIndex-1] != ";"):
        result += indent*ind + txml[tokenIndex] + "\n"
        tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #appends ;
    tokenIndex = tokenIndex + 1
    return result

def compileSubroutineDec(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    result += indent*ind + txml[tokenIndex] + "\n" #constructor/function/method
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #return type
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #parameter name
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #(
    tokenIndex = tokenIndex + 1
    result += indent*ind +"<parameterList>"+"\n"
    result += compileParameterList(txml, tokens, indent)
    result += indent*ind +"</parameterList>"+"\n"
    result += indent*ind + txml[tokenIndex] + "\n" #)
    tokenIndex = tokenIndex + 1
    result += indent*ind +"<subroutineBody>"+"\n"
    result += compileSubroutineBody(txml, tokens, indent)
    result += indent*ind +"</subroutineBody>"+"\n"
    return result;

def compileParameterList(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = ""
    while(tokens[tokenIndex-1] != ")"):
        result += indent*ind + txml[tokenIndex] + "\n"
        tokenIndex = tokenIndex + 1
    return result

def compileSubroutineBody(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = indent*ind + txml[tokenIndex] + "\n" #{
    tokenIndex = tokenIndex + 1
    opencnt = 1
    #!!!!!!!!! aq xdeba ragacaa (an zemot)
    while tokens[tokenIndex-1] == "var":
        result += indent*ind + "<varDec>" + "\n"
        result += compileVarDec(txml, tokens, indent)
        result += indent*ind + "</varDec>" + "\n"
    result += indent*ind + "<statements>" + "\n"
    result += compileStatements(txml, tokens, indent)
    result += indent*ind + "</statements>"+ "\n"
     #       
    result += indent*ind + txml[tokenIndex] + "\n" #}
    tokenIndex = tokenIndex+ 1
    return result

def compileVarDec(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    result += indent*ind + txml[tokenIndex] + "\n" #var
    tokenIndex = tokenIndex + 1
    while(tokens[tokenIndex-1] != ";"):
        result += indent*ind + txml[tokenIndex] + "\n"
        tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #appends ;
    tokenIndex = tokenIndex + 1
    return result

def compileStatements(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    while tokens[tokenIndex-1] == "let" or tokens[tokenIndex-1] == "if" or tokens[tokenIndex-1] == "while" or tokens[tokenIndex-1] == "do" or tokens[tokenIndex-1] == "return":
        if tokens[tokenIndex-1] == "let":
            result += indent*ind + "<letStatement>"+"\n"
            result += compileLet(txml, tokens, indent)
            result += indent*ind + "</letStatement>"+"\n"
        elif tokens[tokenIndex-1] == "if":
            result += indent*ind + "<ifStatement>"+"\n"
            result += compileIf(txml, tokens, indent)
            result += indent*ind + "</ifStatement>"+"\n"
        elif tokens[tokenIndex-1] == "while":
            result += indent*ind + "<whileStatement>"+"\n"
            result += compileWhile(txml, tokens, indent)
            result += indent*ind + "</whileStatement>"+"\n"
        elif tokens[tokenIndex-1] == "do":
            result += indent*ind + "<doStatement>"+"\n"
            result += compileDo(txml, tokens, indent)
            result += indent*ind + "</doStatement>"+"\n"
        elif tokens[tokenIndex-1] == "return":
            result += indent*ind + "<returnStatement>"+"\n"
            result += compileReturn(txml, tokens, indent)
            result += indent*ind + "</returnStatement>"+"\n"
    return result

def compileLet(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = indent*ind + txml[tokenIndex] + "\n" #let
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #var
    tokenIndex = tokenIndex + 1
    if tokens[tokenIndex-1] == "[":
        result += indent*ind + txml[tokenIndex] + "\n" #[
        tokenIndex = tokenIndex + 1
        result += indent*ind + "<expression>" + "\n" 
        result += compileExpression(txml, tokens, indent)
        result += indent*ind + "</expression>" + "\n" 
        result += indent*ind + txml[tokenIndex] + "\n" #]
        tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #=
    tokenIndex = tokenIndex + 1
    result += indent*ind + "<expression>" + "\n"
    result += compileExpression(txml, tokens, indent)
    result += indent*ind + "</expression>" + "\n"
    result += indent*ind + txml[tokenIndex] + "\n" #;
    tokenIndex = tokenIndex + 1
    return result

def compileIf(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1 
    result = indent*ind + txml[tokenIndex] + "\n" #if
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #(
    tokenIndex = tokenIndex + 1
    result += indent*ind + "<expression>" + "\n"
    result += compileExpression(txml, tokens, indent)
    result += indent*ind + "</expression>" + "\n"
    result += indent*ind + txml[tokenIndex] + "\n" #)
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #{
    tokenIndex = tokenIndex + 1
    #
    result += indent*ind + "<statements>" + "\n"
    result += compileStatements(txml, tokens, indent)
    result += indent*ind + "</statements>" + "\n"
    #
    result += indent*ind + txml[tokenIndex] + "\n" #}
    tokenIndex = tokenIndex + 1
    if tokens[tokenIndex-1] == "else":
        result += indent*ind + txml[tokenIndex] + "\n" #else
        tokenIndex = tokenIndex + 1
        result += indent*ind + txml[tokenIndex] + "\n" #{
        tokenIndex = tokenIndex + 1
        #
        result += indent*ind + "<statements>" + "\n"
        result += compileStatements(txml, tokens, indent)
        result += indent*ind + "</statements>" + "\n"
        #
        result += indent*ind + txml[tokenIndex] + "\n" #}
        tokenIndex = tokenIndex + 1
    #tokenIndex = tokenIndex + 1
    return result

def compileWhile(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    result = indent*ind + txml[tokenIndex] + "\n" #while
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #(
    tokenIndex = tokenIndex + 1
    result += indent*ind + "<expression>" + "\n"
    result += compileExpression(txml, tokens, indent)
    result += indent*ind + "</expression>" + "\n"
    result += indent*ind + txml[tokenIndex] + "\n" #)
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #{
    tokenIndex = tokenIndex + 1
    #
    result += indent*ind + "<statements>" + "\n"
    result += compileStatements(txml, tokens, indent)
    result += indent*ind + "</statements>" + "\n"
    #
    result += indent*ind + txml[tokenIndex] + "\n" #}
    tokenIndex = tokenIndex + 1
    return result

def compileDo(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = indent*ind + txml[tokenIndex] + "\n" #do
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #var/routine
    tokenIndex = tokenIndex + 1
    if tokens[tokenIndex-1] == ".":
        result += indent*ind + txml[tokenIndex] + "\n" #.
        tokenIndex = tokenIndex + 1
        result += indent*ind + txml[tokenIndex] + "\n" #subroutine
        tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #(
    tokenIndex = tokenIndex + 1
    #
    result += indent*ind + "<expressionList>" + "\n"
    result += compileExpressionList(txml, tokens, indent)
    result += indent*ind + "</expressionList>" + "\n"
    #
    result += indent*ind + txml[tokenIndex] + "\n" #)
    tokenIndex = tokenIndex + 1
    result += indent*ind + txml[tokenIndex] + "\n" #;
    tokenIndex = tokenIndex + 1
    return result

def compileReturn(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = indent*ind + txml[tokenIndex] + "\n" #return
    tokenIndex = tokenIndex + 1
    if tokens[tokenIndex-1] != ";":
        result += indent*ind + "<expression>" + "\n"
        result += compileExpression(txml, tokens, indent)
        result += indent*ind + "</expression>" + "\n"
    result += indent*ind + txml[tokenIndex] + "\n" #;
    tokenIndex = tokenIndex + 1
    return result

def compileExpression(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = indent*ind + "<term>" + "\n"
    result += compileTerm(txml, tokens, indent)
    result += indent*ind + "</term>" + "\n"
    while tokens[tokenIndex-1] in ['+','-','*','/','&','|','<','>','=']:
        result += indent*ind + txml[tokenIndex] + "\n" #op 
        tokenIndex = tokenIndex + 1
        result += indent*ind + "<term>" + "\n"
        result += compileTerm(txml, tokens, indent)
        result += indent*ind + "</term>" + "\n"
    return result

def compileTerm(txml, tokens, indent):
    global tokenIndex
    indent = indent + 1
    result = ""
    if tokens[tokenIndex-1] == "(": #meaning its expression
        result += indent*ind + txml[tokenIndex] + "\n" #(
        tokenIndex = tokenIndex + 1
        result += indent*ind + "<expression>" + "\n"
        result += compileExpression(txml, tokens, indent)
        result += indent*ind + "</expression>" + "\n"
        result += indent*ind + txml[tokenIndex] + "\n" #)
        tokenIndex = tokenIndex + 1
    elif tokens[tokenIndex-1] in ['-','~']:
        result += indent*ind + txml[tokenIndex] + "\n" #- or ~
        tokenIndex = tokenIndex + 1
        result += indent*ind + "<term>" + "\n"
        result += compileTerm(txml, tokens, indent)
        result += indent*ind + "</term>" + "\n"
    else:
        result += indent*ind + txml[tokenIndex] + "\n" #any other thing: constants, expressionList, subroutineCall
        tokenIndex = tokenIndex + 1
        if tokens[tokenIndex-1] == "(":
            result += indent*ind + txml[tokenIndex] + "\n" #(
            tokenIndex = tokenIndex + 1
            result += indent*ind + "<expressionList>" + "\n"
            result += compileExpressionList(txml, tokens, indent)
            result += indent*ind + "</expressionList>" + "\n"
            result += indent*ind + txml[tokenIndex] + "\n" #)
            tokenIndex = tokenIndex + 1
        elif tokens[tokenIndex-1] == "[": #expression
            result += indent*ind + txml[tokenIndex] + "\n" #[
            tokenIndex = tokenIndex + 1
            result += indent*ind + "<expression>" + "\n"
            result += compileExpression(txml, tokens, indent)
            result += indent*ind + "</expression>" + "\n"
            result += indent*ind + txml[tokenIndex] + "\n" #]
            tokenIndex = tokenIndex + 1
        elif tokens[tokenIndex-1] == ".": #subroutine
            result += indent*ind + txml[tokenIndex] + "\n" #should be .
            tokenIndex = tokenIndex + 1
            result += indent*ind + txml[tokenIndex] + "\n" #name
            tokenIndex = tokenIndex + 1
            result += indent*ind + txml[tokenIndex] + "\n" #[
            tokenIndex = tokenIndex + 1
            result += indent*ind + "<expressionList>" + "\n"
            result += compileExpressionList(txml, tokens, indent)
            result += indent*ind + "</expressionList>" + "\n"
            result += indent*ind + txml[tokenIndex] + "\n" #]
            tokenIndex = tokenIndex + 1
    return result

def compileExpressionList(txml, tokens, indent):
    global tokenIndex
    result = ""
    indent = indent + 1
    if tokens[tokenIndex-1] != ")": #eseigi expression
        result += indent*ind + "<expression>" + "\n"
        result += compileExpression(txml, tokens, indent)
        result += indent*ind + "</expression>" + "\n"
    while tokens[tokenIndex-1] != ")":
        result += indent*ind + txml[tokenIndex] + "\n" #,
        tokenIndex = tokenIndex + 1
        result += indent*ind + "<expression>" + "\n"
        result += compileExpression(txml, tokens, indent)
        result += indent*ind + "</expression>" + "\n"
    return result
    
for file,outfile_txml,outfile_xml in zip(fileList,outFileNames_txml,outFileNames_xml):
    fileIn = open(file,'r') 
    fileOut_txml = open(outfile_txml,'w')
    fileOut_xml = open(outfile_xml,'w')
    rows = fileIn.readlines()
    textToTokenize = ""
    for line in rows:
        textToTokenize = textToTokenize + removeComments(line)
    textToTokenize = ' '.join(textToTokenize.split())
    tokens = tokenizer(textToTokenize)
    txml = makeTxml(tokens, fileOut_txml)

    tokenIndex = 1
    xml = compilationEngine(tokens, txml.splitlines(), 0)
    fileOut_xml.write(xml)
    
    fileIn.close()
    fileOut_txml.close()
    fileOut_xml.close()
