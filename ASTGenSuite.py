import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    # def test_simple_program(self):
    #     """Simple program: int main() {} """
    #     input = """func main() {};"""
    #     expect = str(Program([FuncDecl("main",[],VoidType(),Block([]))]))
    #     self.assertTrue(TestAST.checkASTGen(input,expect,300))

    # def test_more_complex_program(self):
    #     """More complex program"""
    #     input = """var x int ;"""
    #     expect = str(Program([VarDecl("x",IntType(),None)]))
    #     self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    # def test_call_without_parameter(self):
    #     """More complex program"""
    #     input = """func main () {}; var x int ;"""
    #     expect = str(Program([FuncDecl("main",[],VoidType(),Block([])),VarDecl("x",IntType(),None)]))
    #     self.assertTrue(TestAST.checkASTGen(input,expect,302))
    def test_simple_vardecl1(self):
        input = """var x int\n"""
        expect = str(Program([VarDecl("x",IntType(),None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,303))
    def test_simple_vardecl2(self):
        input = """var x int = a + b\n"""
        expect = str(Program([VarDecl("x",IntType(),BinaryOp("+",Id("a"),Id("b")))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,304))
    def test_simple_funcdecl3(self):
        """func (Person p) hello (a int, b string) {}\n"""
        input = """func (p Person) hello (a int, b string) {var x int;}\n"""
        expect = str(Program([MethodDecl("p",Id("Person"),FuncDecl("hello",[ParamDecl("a", IntType()), ParamDecl("b", StringType())], VoidType(), None))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,305))
    def test_simple_funcdecl2(self):
        """func hello (a int, b string) {}\n"""
        input = """func hello (a int, b string) {var x int = a + b;}\n"""
        expect = str(Program([FuncDecl("hello",[ParamDecl("a", IntType()), ParamDecl("b", StringType())], VoidType(), Block([VarDecl("x",IntType(),BinaryOp("+",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,306))
    def test_simple_funcdecl3(self):
        """func hellokyty (a,b int, arr[a][b] int ) {var x int = a + b;}\n"""
        input = """func hellokyty (a,b int, arr[a][b] int ) {var x int = a + b;}\n"""
        expect = str(Program([FuncDecl("hellokyty",[ParamDecl("a", IntType()), ParamDecl("b", IntType()), ParamDecl("arr", ArrayType([Id("a"), Id("b")], IntType()))], VoidType(), Block([VarDecl("x",IntType(),BinaryOp("+",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,307))
    def test_simple_funcdecl4(self):
        """func hellokyty (a,b int, arr[a][b] int ) string {var x int = a + b;}\n"""
        input = """func hellokyty (a,b int, arr[a][b] int ) string {var x int = a + b;}\n"""
        expect = str(Program([FuncDecl("hellokyty",[ParamDecl("a", IntType()), ParamDecl("b", IntType()), ParamDecl("arr", ArrayType([Id("a"), Id("b")], IntType()))], StringType(), Block([VarDecl("x",IntType(),BinaryOp("+",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,308))
    def test_simple_funcdecl5(self):
        """var arr[3][4] int; """
        input = """var arr[3][4] int; """
        expect = str(Program([VarDecl("arr",ArrayType([IntLiteral(3), IntLiteral(4)], IntType()), None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,309))
    def test_simple_funcdecl6(self):
        """var arr[3][a+b] int; """
        input = """var arr[3][a+b] int; """
        expect = str(Program([VarDecl("arr",ArrayType([IntLiteral(3), BinaryOp("+",Id("a"),Id("b"))], IntType()), None)]))
        self.assertTrue(TestAST.checkASTGen(input,expect,310))
    def test_simple_funcdecl7(self):
        """func hellokyty () string {var x int = a + b;}\n"""
        input = """func hellokyty () string {var x int = a + b;}\n"""
        expect = str(Program([FuncDecl("hellokyty", [], StringType(), Block([VarDecl("x",IntType(),BinaryOp("+",Id("a"),Id("b")))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,311))
    def test_simple_struct1(self):
        """struct 1"""
        input = """type Person struct {
                    name string ;
                    age int ;
                };"""
        expect = str(Program([StructType("Person", [("name",StringType()),("age", IntType())], [])]))
        self.assertTrue(TestAST.checkASTGen(input,expect,312))
    def test_simple_interface1(self):
        """interface 1"""
        input = """type Calculator interface {
                    Subtract(a, b float, c int) float;
                    Reset()
                };"""
        expect = str(Program([InterfaceType("Calculator", [Prototype("Subtract",[FloatType(), FloatType(), IntType()],FloatType()), Prototype("Reset",[],VoidType())])]))
        self.assertTrue(TestAST.checkASTGen(input,expect,313))
    def test_simple_arraylit1(self):
        """var x = [3][4]int{a,b,c};"""
        input = """var x = [3][4]int{a,b,c};"""
        expect = str(Program([VarDecl("x", None, ArrayLiteral([IntLiteral(3),IntLiteral(4)], IntType(), [Id("a"), Id("b"), Id("c")]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,314))
    def test_simple_arraylit2(self):
        """var x = [3][4]int{{0,1,2},{3,4,5},{7}};"""
        input = """var x = [3][4]int{{0,1,2},{3,4,5},{7}}\n"""
        expect = str(Program([VarDecl("x", None, ArrayLiteral([IntLiteral(3),IntLiteral(4)], IntType(), [[IntLiteral(0), IntLiteral(1), IntLiteral(2)], [IntLiteral(3), IntLiteral(4), IntLiteral(5)], [IntLiteral(7)]]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,315))
    def test_simple_structlit1(self):
        """var p = Person{name: "Alice", age: 30}"""
        input = """var p = Person{name: "Alice", age: 30};"""
        expect = str(Program([VarDecl("p", None, StructLiteral("Person",[("name", StringLiteral("Alice")),("age", IntLiteral(int(30)))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,316))
    def test_simple_ifstm1(self):
        """func main() { if x > 0 { call(1800)\n } else { call(1801); } }\n"""
        input = """func main() string { if (x > 0) {p:=call(1800)\n } else {p:=call(1801); }; };"""
        expect = str(Program([FuncDecl("main",[], StringType(), Block([If(BinaryOp(">",Id("x"),IntLiteral(0)),Block([Assign(Id("p"), FuncCall("call",[IntLiteral(1800)]))]),Block([Assign(Id("p"), FuncCall("call",[IntLiteral(1801)]))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,317))
    def test_simple_forstm2(self):
        """for 1"""
        input = """func main() string { 
         for (i<5){
         i += 1;}; };"""
        expect = str(Program([FuncDecl("main", [], StringType(), Block([ForBasic(BinaryOp("<", Id("i"), IntLiteral(5)), Block([Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1)))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,318))
    def test_simple_for2(self):
        """for 2"""
        input = """func main() string { 
         for i := 0;i<5; i+=1{
         i += 1;}; };"""
        expect = str(Program([FuncDecl("main", [], StringType(), Block([ForStep(Assign(Id("i"),IntLiteral(0)), BinaryOp("<", Id("i"), IntLiteral(5)), Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1))),  Block([Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1)))]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,319))
    def test_simple_for3(self):
        """for 3"""
        input = """func main() string { 
         for i := 0;i<5; i+=1{
         i += 1\n break;}; };"""
        expect = str(Program([FuncDecl("main", [], StringType(), Block([ForStep(Assign(Id("i"),IntLiteral(0)), BinaryOp("<", Id("i"), IntLiteral(5)), Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1))),  Block([Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1))), Break()]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,320))
    def test_simple_for4(self):
        """for 4"""
        input = """func main() string { 
         for x,y := range array{
         i += 1\n return;}; };"""
        expect = str(Program([FuncDecl("main", [], StringType(), Block([ForEach(Id("x"), Id("y"), Id("array"),  Block([Assign(Id("i"), BinaryOp("+", Id("i"),IntLiteral(1))), Return(None)]))]))]))
        self.assertTrue(TestAST.checkASTGen(input,expect,321))
    
    