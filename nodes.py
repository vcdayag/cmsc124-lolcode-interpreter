from token_types import *
from error import *
from tkinter import *
from tkinter import simpledialog

IT = "IT"
NOOB = "NOOB"
NUMBAR = "NUMBAR"
NUMBR = "NUMBR"
YARN = "YARN"
TROOF = "TROOF"

ST = [{"type": "IT", "value": None}]
VT = {"IT": None}

def resetSymbolTable():
    global ST
    global VT
    ST = [{"type": "IT", "value": None}]
    VT = {"IT": None}
    
    global SYMBOL_TABLE
    SYMBOL_TABLE = {}

def toBool(value):
    return True if value == "WIN" else False
    
def toTroof(value):
    return "WIN" if value else "FAIL"

def toValue(inputValue):
    if isinstance(inputValue,ArithmeticNode):
        return str(inputValue.value)
    elif isinstance(inputValue, VariableNode):
        if inputValue.token.val not in SYMBOL_TABLE:
            raise ErrorSemantic(inputValue.token,"Variable not Initialized")
        
        return str(VT[inputValue.token.val])
    elif isinstance(inputValue,TroofNode):
        return inputValue.token.val

    return inputValue.token.val

class BasicNode:
    def __init__(self,token):
        self.token = token

    def __repr__(self) -> str:
        return f'({self.token})'
    
    def run(self):
        pass


class UnaryOpNode:
    def __init__(self,left, right):
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left}, {self.right})'


class BinOpNode:
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        self.OP_TOKEN = OP_TOKEN
        self.EXPR1 = EXPR1
        self.AN = AN
        self.EXPR2 = EXPR2

    def __repr__(self) -> str:
        return f'({self.OP_TOKEN}, {self.EXPR1}, {self.AN}, {self.EXPR2})'


class DoubleOpNode:
    def __init__(self, left, middle, right) -> None:
        self.left = left
        self.middle = middle
        self.right = right

    def __repr__(self) -> str:
        return f'({self.left}, {self.middle}, {self.right})'


class Program(DoubleOpNode):
    def __init__(self, start_node, body_node,end_node, tbl_sym) -> None:
        super().__init__(start_node, body_node, end_node)
        self.tbl_sym = tbl_sym
        self.run()
    
    def run(self):
        for statement in self.middle:
            statement.run()
        
        printST()
        # print(VT)
        # clear previous items in the lexemes treeview
        for x in self.tbl_sym.get_children():
            self.tbl_sym.delete(x)
        # for index,key in enumerate(VT):
        #     tbl_sym.insert("",'end',iid=index,
        #     values=(key,VT[key]))
        
        for index,key in enumerate(SYMBOL_TABLE):
            if SYMBOL_TABLE[key]["type"] == YARN:
                self.tbl_sym.insert("",'end',iid=index,
                values=(key,"\""+str(SYMBOL_TABLE[key]["value"])+"\""))
            else:
                self.tbl_sym.insert("",'end',iid=index,
                values=(key,SYMBOL_TABLE[key]["value"]))


class LiteralNode:
    def run(self):
        pass


# NULL
class NoobNode(LiteralNode):
    def __init__(self):
        self.value: None = None


# INTEGERS
class NumbrNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value: int = int(token.val)

# FLOATS
class NumbarNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value: float = float(token.val)
        
#"STRINGBODY"
class YarnNode(BasicNode,LiteralNode):
    def __init__(self, token) -> None:
        super().__init__(token)
        self.value: str = str(token.val)

#TRUE OR FALSE
class TroofNode(BasicNode,LiteralNode):
    def __init__(self, token):
        super().__init__(token)
        self.value = True if self.token.val == "WIN" else False

class OperatorNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class VariableNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class StatementNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def run(self):
        if self.right != None:
            self.right.run()

#ARITHMETICOP EXPR AN EXPR
class ArithmeticNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)
    
    def run(self):     
        self.EXPR1.run() 
        self.EXPR2.run() 
        
        left = self.check(self.EXPR1)
        right = self.check(self.EXPR2)

        if self.OP_TOKEN.type in (TT_SUMMATION):
            ST[0]["value"] = eval(left + "+" + right)
        elif self.OP_TOKEN.type in (TT_SUB):
            ST[0]["value"] = eval(left + "-" + right)
        elif self.OP_TOKEN.type in (TT_MUL_OP):
            ST[0]["value"] = eval(left + "*" + right)
        elif self.OP_TOKEN.type in (TT_DIV_OP):
            ST[0]["value"] = eval(left + "/" + right)
        elif self.OP_TOKEN.type in (TT_MOD):
            ST[0]["value"] = eval(left + "%" + right)
        elif self.OP_TOKEN.type in (TT_MAX):
            ST[0]["value"] = max((eval(left),eval(right)))
        elif self.OP_TOKEN.type in (TT_MIN):
            ST[0]["value"] = min((eval(left),eval(right)))

        self.value=ST[0]["value"]
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": NUMBAR, "value": self.value}
    
    def check(self, INPUT):
        if isinstance(INPUT,ArithmeticNode):
            return str(INPUT.value)
        elif isinstance(INPUT, VariableNode):
            if INPUT.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(INPUT.token,"Variable not Initialized")
            try:
                int(VT[INPUT.token.val])
                float(VT[INPUT.token.val])
            except ValueError:
                raise ErrorSemantic(INPUT.token,"Variable contains Yarn. Unable to use Arithmetic operations on Yarn")
            return str(VT[INPUT.token.val])
        elif isinstance(INPUT,YarnNode):
            try:
                int(INPUT.token.val)
                float(INPUT.token.val)
            except ValueError:
                raise ErrorSemantic(INPUT.token,"Unable to use Arithmetic operations on Yarn")

        return str(INPUT.token.val)


#GIMMEH VAR
class GimmehNode(UnaryOpNode):
    def __init__(self, left, right, txt_console):
        super().__init__(left, right)
        self.txt_console = txt_console
    
    def run(self):
        if self.right.token.val not in SYMBOL_TABLE:
            raise ErrorSemantic(self.right.token,"Variable not Initialized")
        answer = simpledialog.askstring("Input", f"Value for: {self.right.token.val}")
        
        ST[0]["value"] = answer
        VT["IT"] = ST[0]["value"]
        VT[self.right.token.val] = answer
        
        SYMBOL_TABLE[IT] = {"type": YARN, "value": answer}
        SYMBOL_TABLE[self.right.token.val]["type"] = YARN
        SYMBOL_TABLE[self.right.token.val]["value"] = answer
        

#SMOOSH
class SmooshNode():
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def run(self):
        self.left.run()
        
        valueList = []
        valueList.append(self.check(self.left))

        for value in self.right:
            value.run()
            valueList.append(self.check(value))
        
        self.value = ''.join(valueList)
        ST[0]["value"] = self.value
        VT["IT"] = self.value
        
        SYMBOL_TABLE[IT] = {"type": YARN, "value": self.value}
    
    def check(self,value):
        if isinstance(value, VariableNode):
            if value.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(value.token,"Variable not Initialized")
            return str(VT[value.token.val])
        elif isinstance(value,BooleanNode):
            return str(value.value)
        else:
            return str(value.token.val)

#VISIBLE
class VisibleNode(UnaryOpNode):
    def __init__(self, left, right, txt_console):
        super().__init__(left, right)
        self.txt_console = txt_console
    
    def run(self):
        for value in self.right:
            value.run()
            print(SYMBOL_TABLE)
            if isinstance(value, VariableNode):
                if value.token.val not in SYMBOL_TABLE:
                    raise ErrorSemantic(value.token,"Variable not Initialized")
                self.txt_console.configure(state=NORMAL)
                self.txt_console.insert(INSERT,str(VT[value.token.val]))
                self.txt_console.configure(state=DISABLED)
            elif isinstance(value,(BooleanNode, SmooshNode, ArithmeticNode, ComparisonNode)):
                self.txt_console.configure(state=NORMAL)
                self.txt_console.insert(INSERT,str(value.value))
                self.txt_console.configure(state=DISABLED)
            else:
                self.txt_console.configure(state=NORMAL)
                self.txt_console.insert(INSERT,str(value.token.val))
                self.txt_console.configure(state=DISABLED)
        self.txt_console.configure(state=NORMAL)
        self.txt_console.insert(INSERT,'\n')
        self.txt_console.configure(state=DISABLED)


class AssignmentNode():
    def assign(self,VAR,EXPR):
        if EXPR == None:
            ST.append({"type": "variable", "token": VAR.token.val, "value": None})
            VT[str(VAR.token.val)] = None
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": None, "value": None}        
        elif isinstance(EXPR, ArithmeticNode):
            ST.append({"type": "variable", "token": VAR.token.val, "value": ST[0]["value"]})
            VT[str(VAR.token.val)] = ST[0]["value"]
            
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBAR, "value": SYMBOL_TABLE[IT]["value"]}
        
        elif isinstance(EXPR, BooleanNode):
            ST.append({"type": "variable", "token": VAR.token.val, "value": EXPR.value})
            VT[str(VAR.token.val)] = ST[0]["value"]
            
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": TROOF, "value": SYMBOL_TABLE[IT]["value"]}
        
        elif isinstance(EXPR, VariableNode):
            ST.append({"type": "variable", "token": VAR.token.val, "value": VT[str(EXPR.token.val)]})
            VT[str(VAR.token.val)] = VT[str(EXPR.token.val)]
            
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": SYMBOL_TABLE[IT]["type"], "value": SYMBOL_TABLE[IT]["value"]}
        
        else:
            ST.append({"type": "variable", "token": VAR.token.val, "value": EXPR.token.val})
            ST[0]["value"] = EXPR.token.val
            if VAR.token.type not in TT_STRING:
                if VAR.token.val.isdigit():
                    VT[VAR.token.val] = eval(EXPR.token.val)
                    SYMBOL_TABLE[str(VAR.token.val)] = {"type": NUMBAR, "value": eval(EXPR.token.val)}
            
            VT[str(VAR.token.val)] = EXPR.token.val
            SYMBOL_TABLE[str(VAR.token.val)] = {"type": YARN, "value": EXPR.token.val}

#I HAS A Variable
class AssignmentShlongNode(UnaryOpNode,AssignmentNode):
    def __init__(self, IHASA, VAR):
        super().__init__(IHASA, VAR)
    
    def run(self):
        self.assign(self.right, None)


#I HAS A VAR ITZ EPXR
class AssignmentLongNode(BinOpNode,AssignmentNode):
    def __init__(self, IHASA, VAR, ITZ, EXPR) -> None:
        super().__init__(IHASA, VAR, ITZ, EXPR)
    
    def run(self):
        self.EXPR2.run()
        self.assign(self.EXPR1,self.EXPR2)


#VAR R EXPR
class AssignmentShortNode(DoubleOpNode,AssignmentNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)
    
    def run(self):
        self.right.run()
        self.assign(self.left,self.right)


#OPERATION EXPR AN EXPR
class ComparisonNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)
    
    def run(self):
        self.EXPR1.run()
        self.EXPR2.run()
        
        left = toValue(self.EXPR1)
        right = toValue(self.EXPR2)
        output = None
        
        if self.OP_TOKEN.type in (TT_EQU_OP):
            output = left == right
        elif self.OP_TOKEN.type in (TT_NEQU):
            output = left != right

        self.value = toTroof(output)
        ST[0]["value"] = self.value
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}

class BooleanNode():
    def tobool(self,INPUT):
        return True if self.check(INPUT) == "WIN" else FALSE
    
    def totroof(self,INPUT):
        return "WIN" if INPUT else "FAIL"

    def check(self, INPUT):
        if isinstance(INPUT,TroofNode):
            return str(INPUT.token.val)
        elif isinstance(INPUT, VariableNode):
            if INPUT.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(INPUT.token,"Variable not Initialized")
            
            if VT[INPUT.token.val] not in ("WIN","FAIL"):
                raise ErrorSemantic(INPUT.token,"Variable contain Yarn. Unable to use Boolean operations on Yarn")
            
            return str(VT[INPUT.token.val])
        elif isinstance(INPUT,YarnNode):
            if VT[INPUT.token.val] not in ("WIN","FAIL"):
                raise ErrorSemantic(INPUT.token,"Unable to use Boolean operations on Yarn")

        raise ErrorSemantic(INPUT.token,"Invalid value for boolean operations")
        # return str(INPUT.token.val)

class BooleanInfNode(UnaryOpNode, BooleanNode):
    def __init__(self, op_token, left, right):
        super().__init__(left,right)
        self.op_token = op_token
    
    def run(self):
        self.left.run()
        
        output = self.tobool(self.left)
        if self.op_token.type in (TT_AND_INF):
            for value in self.right:
                value.run()
                output = output and self.tobool(value)
        elif self.op_token.type in (TT_OR_INF):
            for value in self.right:
                value.run()
                output = output or self.tobool(value)
        
        self.value = self.totroof(output)
        ST[0]["value"] = self.value
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}
        

#
class BooleanLongNode(BinOpNode,BooleanNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)
    
    def run(self):
        self.EXPR1.run()
        self.EXPR2.run()
        
        leftval = self.check(self.EXPR1)
        rightval = self.check(self.EXPR2)
        left = True if leftval == "WIN" else False
        right = True if rightval == "WIN" else False
        
        output = None

        if self.OP_TOKEN.type in (TT_AND):
            output = left and right
        elif self.OP_TOKEN.type in (TT_OR_OP):
            output = left or right
        elif self.OP_TOKEN.type in (TT_XOR):
            output = not (left or right)
        
        ST[0]["value"] = "WIN" if output else "FAIL"
        self.value = ST[0]["value"]
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


#OPERATION EXPR
class BooleanShortNode(UnaryOpNode,BooleanNode):
    def __init__(self, left, right):
        super().__init__(left, right)
    
    def run(self):
        self.right.run()
        
        val = self.check(self.right)
        output = not val
        
        ST[0]["value"] = "WIN" if output else "FAIL"
        self.value = ST[0]["value"]
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": TROOF, "value": self.value}


class TypecastNode:
    def run(self,expr,token):
        value = self.getValue(expr)
        originalType = self.getType(expr)
        newType = token.val
        
        self.value = self.getCastedValue(expr,value,originalType,newType)
        
        ST[0]["value"] = self.value
        VT["IT"] = ST[0]["value"]
        
        SYMBOL_TABLE[IT] = {"type": newType, "value": self.value}
        
        if isinstance(expr,VariableNode):
            SYMBOL_TABLE[str(expr.token.val)] = {"type": newType, "value": self.value}
    
    def getType(self,expr):
        if isinstance(expr,VariableNode):
            if expr.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(expr.token,"Variable not Initialized")
            return SYMBOL_TABLE[expr.token.val]["type"]
        elif isinstance(expr,(BooleanNode,ComparisonNode)):
            return TROOF
        elif isinstance(expr,SmooshNode):
            return YARN
    
    def getValue(self, expr):
        if isinstance(expr,VariableNode):
            if expr.token.val not in SYMBOL_TABLE:
                raise ErrorSemantic(expr.token,"Variable not Initialized")
            return SYMBOL_TABLE[expr.token.val]["value"]
        elif isinstance(expr,(BooleanNode,ComparisonNode)):
            return expr.val
        elif isinstance(expr,SmooshNode):
            return expr.val
    
    def getCastedValue(self,expr, value, originalType, newType):
        res = None
        if originalType == NUMBR:
            if newType == "NUMBR":
                res = int(value)
            elif newType == "NUMBAR":
                res = float(value)
            elif newType == "YARN":
                res = str(value)
        elif originalType == NUMBAR:
            if newType == "NUMBR":
                res = int(value)
            elif newType == "NUMBAR":
                res = float(value)
            elif newType == "YARN":
                res = str(value)
        elif originalType == YARN:
            if newType == "NUMBR":
                try:
                    int(value)
                except ValueError:
                    raise ErrorSemantic(expr.token,"Unable to Typecast Yarn {value} to Numbr")
                res = int(value)
            elif newType == "NUMBAR":
                try:
                    float(value)
                except ValueError:
                    raise ErrorSemantic(expr.token,"Unable to Typecast Yarn {value} to Numbar")
                res = float(value)
            elif newType == "YARN":
                res = str(value)
        
        return res
        
        
#MAEK EXPR AN TYPE
class TypecastLongNode(BinOpNode,TypecastNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)
    
    def run(self):
        super().run(self.EXPR1,self.EXPR2)


#MAEK EXPR possible
class TypecastShortNode(DoubleOpNode,TypecastNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)
    
    def run(self):
        super().run(self.middle,self.right)


#OPERATION EXPR
class SwitchNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


#OMG VALUE STATEMENT
class SwitchCaseNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)


#OMGWTF
class DefaultCaseNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


#
class CaseBreakNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


#ORLY
class IfNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


#MEBBE VALUE ELSEBODY
class ElseIfNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)


#NOWAI
class ElseNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class LoopNodeShort:
    def __init__(self, del_start, label_start, operation, yr, var, codeblock, del_end, label_end) -> None:
        self.del_start = del_start
        self.label_start = label_start
        self.operation = operation
        self.yr = yr
        self.var = var
        self.codeblock = codeblock
        self.del_end = del_end
        self.label_end = label_end

    def __repr__(self) -> str:
        return f'({self.del_start}, {self.label_start}, {self.operation}, {self.yr}, {self.var}, {self.codeblock}, {self.del_end}, {self.label_end})'


class LoopNodeLong:
    def __init__(self, del_start, label_start, operation, yr, var, cond, cond_expr, codeblock, del_end, label_end) -> None:
        self.del_start = del_start
        self.label_start = label_start
        self.operation = operation
        self.yr = yr
        self.var = var
        self.cond = cond
        self.cond_expr = cond_expr
        self.codeblock = codeblock
        self.del_end = del_end
        self.label_end = label_end

    def __repr__(self) -> str:
        return f'({self.del_start}, {self.label_start}, {self.operation}, {self.yr}, {self.var}, {self.cond},{self.cond_expr},{self.codeblock}, {self.del_end})'


def printST():
    for key,value in SYMBOL_TABLE.items():
        print(key,value)

SYMBOL_TABLE = {
    IT: None
}