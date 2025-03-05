grammar MiniGo;

@lexer::header {
from lexererr import *
}

@lexer::members {

prevToken = None  # Track the last emitted token

def emit(self):
    tk = self.type
    result = super().emit()  # Get the next token
    if tk == self.UNCLOSE_STRING:
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.NL:
        if self.prevToken and self.prevToken.type in [
        self.ID, self.INT_LIT, self.FLOAT_LIT, self.STRING_LIT, self.BOOL_LIT,
        self.BOOLEAN, self.STRING, self.INT, self.FLOAT, self.NIL_LIT,
        self.RPAR, self.RCUR, self.RSQU, self.RETURN, self.CONTINUE, self.BREAK]: 
            result.type = self.SEMICOL
            result.text = ";"
            self.prevToken = result
            return result 
        else:
            result = self.nextToken()
            self.prevToken = result
            #print(f"Token emitted: {result}")
            return result;
    else:
        self.prevToken = result
        #print(f"Token emitted: {result}")
        return result  
}

options{
	language=Python3;
}

program  : decllist EOF ;
decllist:  decl decllist | decl;
decl: funcdecl | vardecl | condecl | arraydecl | typdecl;

typdecl: structdecl | interfacedecl;

vardecl: VAR ID typ? INIASSIGN expr SEMICOL | VAR ID typ SEMICOL ;
typ: INT | FLOAT | BOOLEAN | STRING | ID ;

condecl: CONST ID INIASSIGN expr SEMICOL;

funcdecl: FUNC strucinst? ID para functyp? stm SEMICOL;
functyp: typ | arraytyp;
arraytyp: nullabledimension typ;
para: LPAR paralist RPAR;
paralist: paralistprime | ;
paralistprime: paraelement COMMA paralistprime | paraelement;
paraelement: idlist typ | arraypara;
arraypara: ID arraytyp;
nullabledimension: nulldimen nullabledimension | nulldimen;
nulldimen: LSQU arrayaccess? RSQU;
idlist: ID COMMA idlist | ID;
stm: LCUR statementlist RCUR;
strucinst: LPAR ID ID RPAR;

arraydecl: VAR ID dimension typ (INIASSIGN array_lit)? SEMICOL;
dimension: dimen dimension | dimen;
dimen: LSQU arrayaccess RSQU;

structdecl: TYPE ID STRUCT field SEMICOL;
field: LCUR fieldlistprime RCUR;
fieldlistprime: fieldele fieldlistprime | fieldele;
fieldele: ID functyp SEMICOL;

interfacedecl: TYPE ID INTERFACE LCUR methodprime RCUR SEMICOL;
methodprime: method methodprime | method;
method: ID para functyp? SEMICOL;

array_lit: dimension typ arrayini;
arrayini: LCUR arrayinilist RCUR;
arrayinilist: arrayiniele COMMA arrayinilist | arrayiniele;
arrayiniele: expr | arrayini;

struct_lit: ID LCUR fieldinilist RCUR;
fieldinilist: fieldiniprime | ;
fieldiniprime: fieldini COMMA fieldiniprime | fieldini;
fieldini: ID COL expr;

expr: expr OR expr1 | expr1;
expr1: expr1 AND expr2 | expr2;
expr2: expr2 (EQUAL | NEQUAL | LESS | LESSEQ | GREAT | GREATEQ) expr3 | expr3;
expr3: expr3 (ADD | SUB) expr4 | expr4;
expr4: expr4 (MUL | DIV | MOD) expr5 | expr5;
expr5: (SUB | NEG) expr5 | expr6;
expr6: expr6 LSQU arrayaccess RSQU | expr6 DOT expr7 | expr7;
expr7: literal | ID | LPAR expr RPAR | functioncall;
functioncall: ID LPAR exprlist RPAR;
exprlist: exprprime | ;
exprprime: expr COMMA exprprime | expr;
literal: INT_LIT | FLOAT_LIT | STRING_LIT | BOOL_LIT | NIL_LIT | array_lit| struct_lit ;
arrayaccess: INT_LIT | expr;

statement: decl| assignstm | ifstm | forstm | breakstm | returnstm | continuestm | callstm;
assignstm: lhs (ASSIGN | ADDASGN | SUBASGN | MULASGN | DIVASGN | MODASGN) expr SEMICOL;
lhs: ID | ID dimension | ID DOT ID;

ifstm: IF LPAR expr RPAR SEMICOL? LCUR statementlist RCUR SEMICOL? eliflist elstm? SEMICOL;
eliflist: elifstmlist | ;
elifstmlist: elifstm SEMICOL? elifstmlist | elifstm;
elstm: ELSE LCUR statementlist RCUR SEMICOL?;
elifstm: ELSE IF LPAR expr RPAR SEMICOL? LCUR statementlist RCUR SEMICOL?;

statementlist: statement statementlist | statement;

forstm: FOR condi LCUR statementlist RCUR SEMICOL;
condi: expr | inifor | rangefor;
inifor: forvarini SEMICOL expr SEMICOL assignfor;
forvarini: (ID ASSIGN expr) | VAR ID typ? INIASSIGN expr; 
assignfor: lhs (ASSIGN | ADDASGN | SUBASGN | MULASGN | DIVASGN | MODASGN) expr;
rangefor: ID COMMA ID ASSIGN RANGE ID;

breakstm: BREAK SEMICOL;
continuestm: CONTINUE SEMICOL;
returnstm: RETURN expr? SEMICOL;
callstm: functioncall SEMICOL;

//comment
LINE_CMT: '//' ~[\r\n]* -> skip;
BLOCK_COMT: '/*' (CMT | .)*? '*/' -> skip;
fragment CMT: '/*' .*? '*/';

//reserved keyword
IF: 'if' ;
ELSE: 'else' ;
FOR: 'for' ;
RETURN: 'return' ;
FUNC: 'func' ;
TYPE: 'type' ;
STRUCT: 'struct' ;
INTERFACE: 'interface' ;
STRING: 'string' ;
INT: 'int' ;
FLOAT: 'float' ;
BOOLEAN: 'boolean' ;
CONST: 'const' ;
VAR: 'var' ;
CONTINUE: 'continue' ;
BREAK: 'break' ;
RANGE: 'range' ;

//operator
ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
MOD: '%' ;
EQUAL: '==' ;
NEQUAL: '!=' ;
LESS: '<' ;
LESSEQ: '<=' ;
GREAT: '>' ;
GREATEQ: '>=' ;
AND: '&&' ;
OR: '||' ;
NEG: '!' ;
ASSIGN: ':=' ;
ADDASGN: '+=' ;
SUBASGN: '-=' ;
MULASGN: '*=' ;
DIVASGN: '/=' ;
MODASGN: '%=' ;
INIASSIGN: '=' ;
DOT: '.' ;

//seperator
LPAR: '(' ;
RPAR: ')' ;
LCUR: '{' ;
RCUR: '}' ;
LSQU: '[' ;
RSQU: ']' ;
COMMA: ',' ;
SEMICOL: ';' ;
COL: ':';


//literal
INT_LIT: [1-9] Digit* | '0' | '0' [Bb] [01]+ | '0' [Oo] [0-7]+ | '0' [Xx] [0-9A-Fa-f]+;
FLOAT_LIT: Digit+ '.' Digit* Expo? ;
STRING_LIT: '"' STRING_CHAR* '"' {self.text = self.text[1:-1]} ;
fragment STRING_CHAR: ~[\\"]  | ESCAPE  ;
fragment ESCAPE: '\\' [ntr"\\]; 
UNCLOSE_STRING: '"' STRING_CHAR* ('\r\n' | '\n' | EOF) {
    raise UncloseString(self.text[1:])
};

ILLEGAL_ESCAPE: '"' STRING_CHAR* ('\\' ~[ntr"\\]) {
    raise IllegalEscape(self.text[1:])
};

fragment Digit: [0-9] ;
fragment Expo: [Ee] [+-]? Digit+ ;
BOOL_LIT: 'true' | 'false' ;
NIL_LIT: 'nil' ;

ID: [A-Za-z_] [A-Za-z_0-9]* ;


//NL: '\n' -> skip; //skip newlines
NL: '\n' | '\r\n';

WS : [ \t\r]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: . {raise ErrorToken(self.text)};
