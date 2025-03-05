from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *

class ASTGeneration(MiniGoVisitor):
    # def visitProgram(self,ctx:MiniGoParser.ProgramContext):
    #     return Program([self.visit(i) for i in ctx.decl()])

    # def visitDecl(self,ctx:MiniGoParser.DeclContext):
    #     return self.visit(ctx.getChild(0))

    # def visitFuncdecl(self,ctx:MiniGoParser.FuncdeclContext):
    #     return FuncDecl(ctx.ID().getText(),[],VoidType(),Block([]))
    	
    # def visitVardecl(self,ctx:MiniGoParser.VardeclContext):
    #     return VarDecl(ctx.ID().getText(),IntType(),None)

    # def visit(self, ctx):
    #     if ctx is None:
    #         print("Visit missing")
    #     return ctx.accept(self)
    
    # Visit a parse tree produced by MiniGoParser#program.
    #program  : decllist EOF ;
    def visitProgram(self, ctx:MiniGoParser.ProgramContext):
        return Program(self.visit(ctx.decllist()))

    # Visit a parse tree produced by MiniGoParser#decllist.
    #decllist:  decl decllist | decl;
    def visitDecllist(self, ctx:MiniGoParser.DecllistContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.decl())]
        return [self.visit(ctx.decl())] + self.visit(ctx.decllist())

        

    # Visit a parse tree produced by MiniGoParser#decl.
    #decl: funcdecl | vardecl | condecl | arraydecl | typdecl;
    def visitDecl(self, ctx:MiniGoParser.DeclContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#typdecl.
    #typdecl: structdecl | interfacedecl;
    def visitTypdecl(self, ctx:MiniGoParser.TypdeclContext):
        if ctx.structdecl():
            return self.visit(ctx.structdecl())
        else:
            return self.visit(ctx.interfacedecl())


    # Visit a parse tree produced by MiniGoParser#vardecl.
    #vardecl: VAR ID typ? INIASSIGN expr SEMICOL | VAR ID typ SEMICOL ;
    def visitVardecl(self, ctx:MiniGoParser.VardeclContext):
        if ctx.getChildCount() == 6:
            return VarDecl(ctx.ID().getText(),self.visit(ctx.typ()),self.visit(ctx.expr()))
        elif ctx.getChildCount() == 5:
            return VarDecl(ctx.ID().getText(),None,self.visit(ctx.expr()))
        else:
            return VarDecl(ctx.ID().getText(),self.visit(ctx.typ()),None)


    # Visit a parse tree produced by MiniGoParser#typ.
    #typ: INT | FLOAT | BOOLEAN | STRING | ID ;
    def visitTyp(self, ctx:MiniGoParser.TypContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BoolType()
        elif ctx.STRING():
            return StringType()
        else:
            return Id(ctx.ID().getText())



    # Visit a parse tree produced by MiniGoParser#condecl.
    #condecl: CONST ID typ? INIASSIGN expr SEMICOL;
    def visitCondecl(self, ctx:MiniGoParser.CondeclContext):
        if ctx.getChildCount() == 6:
            return ConstDecl(ctx.ID().getText(), self.visit(ctx.typ()), self.visit(ctx.expr()))
        return ConstDecl(ctx.ID().getText(), None, self.visit(ctx.expr()))



    # Visit a parse tree produced by MiniGoParser#funcdecl.
    #funcdecl: FUNC strucinst? ID para functyp? stm SEMICOL;
    def visitFuncdecl(self, ctx:MiniGoParser.FuncdeclContext):
        funcname = ctx.ID().getText()
        parame = self.visit(ctx.para())
        if ctx.functyp():
            ftype = self.visit(ctx.functyp())
        else:
            ftype = VoidType()
        if ctx.strucinst():
            structpart = self.visit(ctx.strucinst())
        else:
            structpart = None
        block = self.visit(ctx.stm())
        if ctx.strucinst():
            return MethodDecl(structpart[0],structpart[1], FuncDecl(funcname, parame, ftype, Block(block)) )
        else: 
            return FuncDecl(funcname, parame, ftype, Block(block))


    # Visit a parse tree produced by MiniGoParser#functyp.
    #functyp: typ | arraytyp;
    def visitFunctyp(self, ctx:MiniGoParser.FunctypContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#arraytyp.
    #arraytyp: nullabledimension typ;
    def visitArraytyp(self, ctx:MiniGoParser.ArraytypContext):
        dimen = self.visit(ctx.nullabledimension())
        return ArrayType(dimen, self.visit(ctx.typ()))


    # Visit a parse tree produced by MiniGoParser#para.
    #para: LPAR paralist RPAR;
    def visitPara(self, ctx:MiniGoParser.ParaContext):
        return self.visit(ctx.paralist())


    # Visit a parse tree produced by MiniGoParser#paralist.
    # paralist: paralistprime | ;
    def visitParalist(self, ctx:MiniGoParser.ParalistContext):
        if ctx.getChildCount():
            return self.visit(ctx.paralistprime())
        else:
            return []


    # Visit a parse tree produced by MiniGoParser#paralistprime.
    # paralistprime: paraelement COMMA paralistprime | paraelement;
    def visitParalistprime(self, ctx:MiniGoParser.ParalistprimeContext):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.paraelement()) + self.visit(ctx.paralistprime())
        return self.visit(ctx.paraelement())


    # Visit a parse tree produced by MiniGoParser#paraelement.
    # paraelement: idlist typ | arraypara;
    def visitParaelement(self, ctx:MiniGoParser.ParaelementContext):
        if ctx.idlist():
            listOfVar = self.visit(ctx.idlist())
            typ = self.visit(ctx.typ())
            return list(map(lambda x: ParamDecl(x, typ), listOfVar))
        return [self.visit(ctx.arraypara())]

    # Visit a parse tree produced by MiniGoParser#arraypara.
    #arraypara: ID arraytyp;
    def visitArraypara(self, ctx:MiniGoParser.ArrayparaContext):
        return ParamDecl(ctx.ID().getText(), self.visit(ctx.arraytyp()))


    # Visit a parse tree produced by MiniGoParser#nullabledimension.
    #nullabledimension: nulldimen nullabledimension | nulldimen;
    def visitNullabledimension(self, ctx:MiniGoParser.NullabledimensionContext):
        if ctx.getChildCount() == 2:
            return [self.visit(ctx.nulldimen())] + self.visit(ctx.nullabledimension())
        return [self.visit(ctx.nulldimen())]


    # Visit a parse tree produced by MiniGoParser#nulldimen.
    #nulldimen: LSQU arrayaccess? RSQU;
    def visitNulldimen(self, ctx:MiniGoParser.NulldimenContext):
        if ctx.arrayaccess():
            return self.visit(ctx.arrayaccess())
        else: return None


    # Visit a parse tree produced by MiniGoParser#idlist.
    #idlist: ID COMMA idlist | ID;
    def visitIdlist(self, ctx:MiniGoParser.IdlistContext):
        if ctx.getChildCount() == 3:
            return [ctx.ID().getText()] + self.visit(ctx.idlist())
        return [ctx.ID().getText()]


    # Visit a parse tree produced by MiniGoParser#stm.
    #stm: LCUR statementlist RCUR;
    def visitStm(self, ctx:MiniGoParser.StmContext):
        return self.visit(ctx.statementlist())


    # Visit a parse tree produced by MiniGoParser#strucinst.
    #strucinst: LPAR ID ID RPAR;
    def visitStrucinst(self, ctx:MiniGoParser.StrucinstContext):
        return (ctx.ID(0).getText(), Id(ctx.ID(1).getText()))


    # Visit a parse tree produced by MiniGoParser#arraydecl.
    # arraydecl: VAR ID dimension typ (INIASSIGN array_lit)? SEMICOL;
    def visitArraydecl(self, ctx:MiniGoParser.ArraydeclContext):
        varname = ctx.ID().getText()
        dimen = self.visit(ctx.dimension())
        vartyp = self.visit(ctx.typ())
        if ctx.INIASSIGN():
            return VarDecl(varname, ArrayType(dimen, vartyp),self.visit(ctx.array_lit()))
        return VarDecl(varname, ArrayType(dimen, vartyp),None)


    # dimension: dimen dimension | dimen;
    # Visit a parse tree produced by MiniGoParser#dimension.
    def visitDimension(self, ctx:MiniGoParser.DimensionContext):
        if ctx.getChildCount() == 2:
            return [self.visit(ctx.dimen())] + self.visit(ctx.dimension())
        return [self.visit(ctx.dimen())]

    # dimen: LSQU arrayaccess RSQU;
    # Visit a parse tree produced by MiniGoParser#dimen.
    def visitDimen(self, ctx:MiniGoParser.DimenContext):
        return self.visit(ctx.arrayaccess())


    # Visit a parse tree produced by MiniGoParser#structdecl.
    # structdecl: TYPE ID STRUCT field SEMICOL;
    def visitStructdecl(self, ctx:MiniGoParser.StructdeclContext):
        return StructType(ctx.ID().getText(), self.visit(ctx.field()), [])


    # Visit a parse tree produced by MiniGoParser#field.
    # field: LCUR fieldlistprime RCUR;
    def visitField(self, ctx:MiniGoParser.FieldContext):
        return self.visit(ctx.fieldlistprime())


    # Visit a parse tree produced by MiniGoParser#fieldlistprime.
    # fieldlistprime: fieldele fieldlistprime | fieldele;
    def visitFieldlistprime(self, ctx:MiniGoParser.FieldlistprimeContext):
        return [self.visit(ctx.fieldele())] + self.visit(ctx.fieldlistprime()) if ctx.fieldlistprime() else [self.visit(ctx.fieldele())]


    # Visit a parse tree produced by MiniGoParser#fieldele.
    # fieldele: ID functyp SEMICOL;
    def visitFieldele(self, ctx:MiniGoParser.FieldeleContext):
        return (ctx.ID().getText(),self.visit(ctx.functyp()))


    # Visit a parse tree produced by MiniGoParser#interfacedecl.
    # interfacedecl: TYPE ID INTERFACE LCUR methodprime RCUR SEMICOL;
    def visitInterfacedecl(self, ctx:MiniGoParser.InterfacedeclContext):
        return InterfaceType(ctx.ID().getText(), self.visit(ctx.methodprime()))


    # Visit a parse tree produced by MiniGoParser#methodprime.
    # methodprime: method methodprime | method;
    def visitMethodprime(self, ctx:MiniGoParser.MethodprimeContext):
        return [self.visit(ctx.method())] + self.visit(ctx.methodprime()) if ctx.methodprime() else [self.visit(ctx.method())]


    # Visit a parse tree produced by MiniGoParser#method.
    # method: ID para functyp? SEMICOL;
    def visitMethod(self, ctx:MiniGoParser.MethodContext):
        param = self.visit(ctx.para())
        meparam = []
        for x in param:
            meparam += [x.parType]
        if ctx.functyp():
            typ = self.visit(ctx.functyp())
        else:
            typ = VoidType()
        return Prototype(ctx.ID().getText(), meparam, typ)


    # Visit a parse tree produced by MiniGoParser#array_lit.
    # array_lit: dimension typ arrayini;
    def visitArray_lit(self, ctx:MiniGoParser.Array_litContext):
        return ArrayLiteral(self.visit(ctx.dimension()), self.visit(ctx.typ()), self.visit(ctx.arrayini()))


    # Visit a parse tree produced by MiniGoParser#arrayini.
    # arrayini: LCUR arrayinilist RCUR;
    def visitArrayini(self, ctx:MiniGoParser.ArrayiniContext):
        return self.visit(ctx.arrayinilist())


    # Visit a parse tree produced by MiniGoParser#arrayinilist.
    # arrayinilist: arrayiniele COMMA arrayinilist | arrayiniele;
    def visitArrayinilist(self, ctx:MiniGoParser.ArrayinilistContext):
        return [self.visit(ctx.arrayiniele())] + self.visit(ctx.arrayinilist()) if ctx.arrayinilist() else [self.visit(ctx.arrayiniele())]


    # Visit a parse tree produced by MiniGoParser#arrayiniele.
    # arrayiniele: expr | arrayini;
    def visitArrayiniele(self, ctx:MiniGoParser.ArrayinieleContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#struct_lit.
    # struct_lit: ID LCUR fieldinilist RCUR;
    def visitStruct_lit(self, ctx:MiniGoParser.Struct_litContext):
        return StructLiteral(ctx.ID().getText(), self.visit(ctx.fieldinilist()))

    # Visit a parse tree produced by MiniGoParser#fieldinilist.
    # fieldinilist: fieldiniprime | ;
    def visitFieldinilist(self, ctx:MiniGoParser.FieldinilistContext):
        if ctx.fieldiniprime():
            return self.visit(ctx.fieldiniprime())
        return []


    # Visit a parse tree produced by MiniGoParser#fieldiniprime.
    # fieldiniprime: fieldini COMMA fieldiniprime | fieldini;
    def visitFieldiniprime(self, ctx:MiniGoParser.FieldiniprimeContext):
        return [self.visit(ctx.fieldini())] + self.visit(ctx.fieldiniprime()) if ctx.fieldiniprime() else [self.visit(ctx.fieldini())]


    # Visit a parse tree produced by MiniGoParser#fieldini.
    # fieldini: ID COL expr;
    def visitFieldini(self, ctx:MiniGoParser.FieldiniContext):
        return (ctx.ID().getText(), self.visit(ctx.expr()))


    # Visit a parse tree produced by MiniGoParser#expr.
    #expr: expr OR expr1 | expr1;
    def visitExpr(self, ctx:MiniGoParser.ExprContext):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.OR().getText(),self.visit(ctx.expr()),self.visit(ctx.expr1()))
        return self.visit(ctx.expr1()) 


    # Visit a parse tree produced by MiniGoParser#expr1.
    #expr1: expr1 AND expr2 | expr2;
    def visitExpr1(self, ctx:MiniGoParser.Expr1Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.AND().getText(),self.visit(ctx.expr1()),self.visit(ctx.expr2()))
        return self.visit(ctx.expr2()) 


    # Visit a parse tree produced by MiniGoParser#expr2.
    #expr2: expr2 (EQUAL | NEQUAL | LESS | LESSEQ | GREAT | GREATEQ) expr3 | expr3;
    def visitExpr2(self, ctx:MiniGoParser.Expr2Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expr2()),self.visit(ctx.expr3()))
        return self.visit(ctx.expr3()) 


    # Visit a parse tree produced by MiniGoParser#expr3.
    #expr3: expr3 (ADD | SUB) expr4 | expr4;
    def visitExpr3(self, ctx:MiniGoParser.Expr3Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))
        return self.visit(ctx.expr4())


    # Visit a parse tree produced by MiniGoParser#expr4.
    #expr4: expr4 (MUL | DIV | MOD) expr5 | expr5;
    def visitExpr4(self, ctx:MiniGoParser.Expr4Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.expr4()),self.visit(ctx.expr5()))
        return self.visit(ctx.expr5())


    # Visit a parse tree produced by MiniGoParser#expr5.
    #expr5: (SUB | NEG) expr5 | expr6;
    def visitExpr5(self, ctx:MiniGoParser.Expr5Context):
        if ctx.getChildCount() == 2:
            return UnaryOp(ctx.getChild(0).getText(),self.visit(ctx.expr5()))
        return self.visit(ctx.expr6())


    # Visit a parse tree produced by MiniGoParser#expr6.
    #expr6: expr6 LSQU arrayaccess RSQU | expr6 DOT expr7 | expr7;
    def visitExpr6(self, ctx:MiniGoParser.Expr6Context):
        if ctx.getChildCount() == 4:
            arrayname = self.visit(ctx.expr6())
            accessfield = self.visit(ctx.arrayaccess())
            return ArrayCell(self.visit(ctx.expr6()), [accessfield])
        elif ctx.DOT():
            funcpart = self.visit(ctx.expr7())
            methodName = funcpart.funname
            methodarg = funcpart.args
            return MethCall(self.visit(ctx.expr6()), methodName, methodarg)
        return self.visit(ctx.expr7())

    # Visit a parse tree produced by MiniGoParser#expr7.
    #expr7: literal | ID | LPAR expr RPAR | functioncall;
    def visitExpr7(self, ctx:MiniGoParser.Expr7Context):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.expr():
            return self.visit(ctx.expr())
        else:
            return self.visit(ctx.functioncall())


    # Visit a parse tree produced by MiniGoParser#functioncall.
    # functioncall: ID LPAR exprlist RPAR;
    def visitFunctioncall(self, ctx:MiniGoParser.FunctioncallContext):
        return FuncCall(ctx.ID().getText(), self.visit(ctx.exprlist()))


    # Visit a parse tree produced by MiniGoParser#exprlist.
    # exprlist: exprprime | ;
    def visitExprlist(self, ctx:MiniGoParser.ExprlistContext):
        if ctx.exprprime():
            return self.visit(ctx.exprprime())
        else:
            return []


    # Visit a parse tree produced by MiniGoParser#exprprime.
    # exprprime: expr COMMA exprprime | expr;
    def visitExprprime(self, ctx:MiniGoParser.ExprprimeContext):
        if ctx.COMMA():
            return [self.visit(ctx.expr())] + self.visit(ctx.exprprime())
        return [self.visit(ctx.expr())]


    # Visit a parse tree produced by MiniGoParser#literal.
    # literal: INT_LIT | FLOAT_LIT | STRING_LIT | BOOL_LIT | array_lit| struct_lit;
    def visitLiteral(self, ctx:MiniGoParser.LiteralContext):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.BOOL_LIT():
            return BooleanLiteral(bool(ctx.BOOL_LIT().getText()))
        elif ctx.array_lit():
            return self.visit(ctx.array_lit())
        else:
            return self.visit(ctx.struct_lit())


    # Visit a parse tree produced by MiniGoParser#arrayaccess.
    # arrayaccess: INT_LIT | expr;
    def visitArrayaccess(self, ctx:MiniGoParser.ArrayaccessContext):
        return IntLiteral(int(ctx.INT_LIT().getText())) if ctx.INT_LIT() else self.visit(ctx.expr())


    # Visit a parse tree produced by MiniGoParser#statement.
    # statement: decl| assignstm | ifstm | forstm | breakstm | returnstm | continuestm | callstm;
    def visitStatement(self, ctx:MiniGoParser.StatementContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by MiniGoParser#assignstm.
    # assignstm: lhs (ASSIGN | ADDASGN | SUBASGN | MULASGN | DIVASGN | MODASGN) expr SEMICOL;
    def visitAssignstm(self, ctx:MiniGoParser.AssignstmContext):
        lhs = self.visit(ctx.lhs())
        rhs = self.visit(ctx.expr())
        if ctx.ASSIGN():
            return Assign(lhs, rhs)
        elif ctx.ADDASGN():
            return Assign(lhs, BinaryOp("+", lhs, rhs))
        elif ctx.SUBASGN():
            return Assign(lhs, BinaryOp("-", lhs, rhs))
        elif ctx.MULASGN():
            return Assign(lhs, BinaryOp("*", lhs, rhs))
        elif ctx.DIVASGN():
            return Assign(lhs, BinaryOp("/", lhs, rhs))
        else:
            return Assign(lhs, BinaryOp("%", lhs, rhs))


    # Visit a parse tree produced by MiniGoParser#lhs.
    # lhs: ID | ID dimension | ID DOT ID;
    def visitLhs(self, ctx:MiniGoParser.LhsContext):
        if ctx.getChildCount() == 1:
            return Id(ctx.ID(0).getText())
        elif ctx.getChildCount() == 2:
            return ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.dimension()))
        else:
            return FieldAccess(Id(ctx.ID(0).getText()), ctx.ID(1).getText())


    # Visit a parse tree produced by MiniGoParser#ifstm.
    #ifstm: IF LPAR expr RPAR SEMICOL? LCUR statementlist RCUR SEMICOL? eliflist elstm? SEMICOL;
    def visitIfstm(self, ctx:MiniGoParser.IfstmContext):
        condition = self.visit(ctx.expr())
        ifblock = self.visit(ctx.statementlist())
        elif_part = self.visit(ctx.eliflist())
        if ctx.elstm():
            else_part = self.visit(ctx.elstm())
        else:
            else_part = None
        else_stm = self.elseStmHelper(elif_part, else_part)
        return If(condition,Block(ifblock), Block(else_stm))
    def elseStmHelper(self, elif_part, else_part):
        else_body = else_part
        for elif_body in elif_part:
            else_body = If(elif_body[0], elif_body[1], else_body)
        return else_body

    # Visit a parse tree produced by MiniGoParser#eliflist.
    # eliflist: elifstmlist | ;
    def visitEliflist(self, ctx:MiniGoParser.EliflistContext):
        return self.visit(ctx.elifstmlist()) if ctx.elifstmlist() else []


    # Visit a parse tree produced by MiniGoParser#elifstmlist.
    # elifstmlist: elifstm SEMICOL? elifstmlist | elifstm;
    def visitElifstmlist(self, ctx:MiniGoParser.ElifstmlistContext):
        return [self.visit(ctx.elifstm())] + self.visit(ctx.elifstmlist())


    # Visit a parse tree produced by MiniGoParser#elstm.
    # elstm: ELSE LCUR statementlist RCUR SEMICOL?;
    def visitElstm(self, ctx:MiniGoParser.ElstmContext):
        return self.visit(ctx.statementlist())


    # Visit a parse tree produced by MiniGoParser#elifstm.
    # elifstm: ELSE IF LPAR expr RPAR SEMICOL? LCUR statementlist RCUR SEMICOL?;
    def visitElifstm(self, ctx:MiniGoParser.ElifstmContext):
        return (self.visit(ctx.expr()), self.visit(ctx.statementlist()))


    # Visit a parse tree produced by MiniGoParser#statementlist.
    # statementlist: statement statementlist | statement;
    def visitStatementlist(self, ctx:MiniGoParser.StatementlistContext):
        return [self.visit(ctx.statement())] + self.visit(ctx.statementlist()) if ctx.statementlist() else [self.visit(ctx.statement())]


    # Visit a parse tree produced by MiniGoParser#forstm.
    # forstm: FOR condi LCUR statementlist RCUR SEMICOL;
    def visitForstm(self, ctx:MiniGoParser.ForstmContext):
        condition = self.visit(ctx.condi())
        if condition[0] == 1:
            return ForBasic(condition[1], Block(self.visit(ctx.statementlist())))
        elif condition[0] == 2:
            return ForStep(condition[1][0], condition[1][1], condition[1][2], Block(self.visit(ctx.statementlist())))
        else:
            return ForEach(condition[1][0], condition[1][1], condition[1][2], Block(self.visit(ctx.statementlist())))

    # Visit a parse tree produced by MiniGoParser#condi.
    # condi: expr | inifor | rangefor;
    def visitCondi(self, ctx:MiniGoParser.CondiContext):
        if ctx.expr():
            return (1,self.visit(ctx.getChild(0)))
        elif ctx.inifor():
            return (2,self.visit(ctx.getChild(0)))
        else:
            return (3,self.visit(ctx.getChild(0)))
        
    # Visit a parse tree produced by MiniGoParser#inifor.
    # inifor: forvarini SEMICOL expr SEMICOL assignfor;
    def visitInifor(self, ctx:MiniGoParser.IniforContext):
        return (self.visit(ctx.forvarini()), self.visit(ctx.expr()), self.visit(ctx.assignfor()))


    # Visit a parse tree produced by MiniGoParser#forvarini.
    # forvarini: (ID ASSIGN expr) | VAR ID typ? INIASSIGN expr; 
    #chua xu ly
    def visitForvarini(self, ctx:MiniGoParser.ForvariniContext):
            return Assign(Id(ctx.ID().getText()), self.visit(ctx.expr()))


    # Visit a parse tree produced by MiniGoParser#assignfor.
    # assignfor: lhs (ASSIGN | ADDASGN | SUBASGN | MULASGN | DIVASGN | MODASGN) expr;
    def visitAssignfor(self, ctx:MiniGoParser.AssignforContext):
        lhs = self.visit(ctx.lhs())
        rhs = self.visit(ctx.expr())
        if ctx.ASSIGN():
            return Assign(lhs, rhs)
        elif ctx.ADDASGN():
            return Assign(lhs, BinaryOp("+", lhs, rhs))
        elif ctx.SUBASGN():
            return Assign(lhs, BinaryOp("-", lhs, rhs))
        elif ctx.MULASGN():
            return Assign(lhs, BinaryOp("*", lhs, rhs))
        elif ctx.DIVASGN():
            return Assign(lhs, BinaryOp("/", lhs, rhs))
        else:
            return Assign(lhs, BinaryOp("%", lhs, rhs))


    # Visit a parse tree produced by MiniGoParser#rangefor.
    # rangefor: ID COMMA ID ASSIGN RANGE ID;
    def visitRangefor(self, ctx:MiniGoParser.RangeforContext):
        return (Id(ctx.ID(0).getText()), Id(ctx.ID(1).getText()), Id(ctx.ID(2).getText()))


    # Visit a parse tree produced by MiniGoParser#breakstm.
    # breakstm: BREAK SEMICOL;
    def visitBreakstm(self, ctx:MiniGoParser.BreakstmContext):
        return Break()


    # Visit a parse tree produced by MiniGoParser#continuestm.
    # continuestm: CONTINUE SEMICOL;
    def visitContinuestm(self, ctx:MiniGoParser.ContinuestmContext):
        return Continue()


    # Visit a parse tree produced by MiniGoParser#returnstm.
    # returnstm: RETURN expr? SEMICOL;
    def visitReturnstm(self, ctx:MiniGoParser.ReturnstmContext):
        return Return(self.visit(ctx.expr())) if ctx.expr() else Return(None)


    # Visit a parse tree produced by MiniGoParser#callstm.
    # callstm: functioncall SEMICOL;
    def visitCallstm(self, ctx:MiniGoParser.CallstmContext):
        return self.visit(ctx.functioncall())

    

