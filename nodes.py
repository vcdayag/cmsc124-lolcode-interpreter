#  from main import printToConsole
from token_types import TT_DIV_OP, TT_MOD, TT_MUL_OP, TT_STRING, TT_SUB, TT_SUMMATION, TT_IDENTIFIER
from error import *
from tkinter import *
from tkinter import simpledialog
#  import main

ST = [{"type": "IT", "value": None}]
VT = {"IT": None}

class BasicNode:
    def __init__(self,token):
        self.token = token

    def __repr__(self) -> str:
        return f'({self.token})'


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
        printST()
        print(VT)
        # clear previous items in the lexemes treeview
        for x in tbl_sym.get_children():
            tbl_sym.delete(x)
        for index,key in enumerate(VT):
            tbl_sym.insert("",'end',iid=index,
            values=(key,VT[key]))


class NoobNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class NumbrNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class NumbarNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class YarnNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class OperatorNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class VariableNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


class StatementNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)

#ARITHMETICOP EXPR AN EXPR
class ArithmeticNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)
        left = self.check(EXPR1)
        right = self.check(EXPR2)

        if OP_TOKEN.type in (TT_SUMMATION):
            ST[0]["value"] = eval(left + "+" + right)
        elif OP_TOKEN.type in (TT_SUB):
            ST[0]["value"] = eval(left + "-" + right)
        elif OP_TOKEN.type in (TT_MUL_OP):
            ST[0]["value"] = eval(left + "*" + right)
        elif OP_TOKEN.type in (TT_DIV_OP):
            ST[0]["value"] = eval(left + "/" + right)
        elif OP_TOKEN.type in (TT_MOD):
            ST[0]["value"] = eval(left + "%" + right)

        self.value=ST[0]["value"]
        VT["IT"] = ST[0]["value"]
    
    def check(self, INPUT):
        if isinstance(INPUT,ArithmeticNode):
            return str(INPUT.value)
        elif isinstance(INPUT, VariableNode):
            if INPUT.token.val not in VT:
                    raise Error(INPUT.token,"Variable not Initialized")
            return str(VT[INPUT.token.val])
        elif isinstance(INPUT,StringNode):
            try:
                int(INPUT.token.val)
                float(INPUT.token.val)
            except ValueError:
                raise Error(INPUT.token,"Unable to use Arithmetic operations on Yarn")
            return str(INPUT.token.val)
        else:
            return str(INPUT.token.val)


#GIMMEH VAR
class GimmehNode(UnaryOpNode):
    def __init__(self, left, right, txt_console):
        super().__init__(left, right)
        answer = simpledialog.askstring("Input", f"Value for: {right.val}")
        ST[0]["value"] = answer
        VT["IT"] = ST[0]["value"]
        VT[right.val] = answer


#VISIBLE
class VisibleNode(UnaryOpNode):
    def __init__(self, left, right, txt_console):
        super().__init__(left, right)
        if not isinstance(right, VariableNode):
            txt_console.configure(state=NORMAL)
            txt_console.insert(INSERT,str(right.token.val)+'\n')
            txt_console.configure(state=DISABLED)
        else:
            if right.token.val not in VT:
                raise Error(right.token,"Variable not Initialized")
            txt_console.configure(state=NORMAL)
            txt_console.insert(INSERT,str(VT[right.token.val])+'\n')
            txt_console.configure(state=DISABLED)


#I HAS A Variable
class AssignmentShlongNode(UnaryOpNode):
    def __init__(self, IHASA, VAR):
        super().__init__(IHASA, VAR)
        ST.append({"type": "variable", "token": VAR.token.val, "value": None})


#I HAS A VAR ITZ EPXR
class AssignmentLongNode(BinOpNode):
    def __init__(self, IHASA, VAR, ITZ, EXPR) -> None:
        super().__init__(IHASA, VAR, ITZ, EXPR)
        if not isinstance(EXPR, ArithmeticNode):
            ST.append({"type": "variable", "token": VAR.token.val, "value": EXPR.token.val})
            ST[0]["value"] = EXPR.token.val
            if VAR.token.type not in TT_STRING:
                if VAR.token.val.isdigit():
                    VT[VAR.token.val] = eval(EXPR.token.val)
            VT[VAR.token.val] = EXPR.token.val
        else:
            ST.append({"type": "variable", "token": VAR.token.val, "value": ST[0]["value"]})
            VT[VAR.token.val] = ST[0]["value"]


#VAR R EXPR
class AssignmentShortNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)


#OPERATION EXPR AN EXPR
class ComparisonNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)

#
class BooleanLongNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)


#OPERATION EXPR
class BooleanShortNode(UnaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


#MAEK EXPR AN TYPE
class TypecastLongNode(BinOpNode):
    def __init__(self, OP_TOKEN, EXPR1, AN, EXPR2) -> None:
        super().__init__(OP_TOKEN, EXPR1, AN, EXPR2)


#MAEK EXPR possible
class TypecastShortNode(DoubleOpNode):
    def __init__(self, left, middle, right) -> None:
        super().__init__(left, middle, right)


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

#"STRINGBODY"
class StringNode(BasicNode):
    def __init__(self, token) -> None:
        super().__init__(token)


#TRUE OR FALSE
class TroofNode(BasicNode):
    def __init__(self, token):
        super().__init__(token)


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
    for entry in ST:
        print(entry)

