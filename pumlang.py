from Lexer_Classes import LexAnd, LexAsign, LexBinOp, LexBktClose, LexBktOpen, LexBool, LexBraceClose, LexBraceOpen, LexComma, LexElse, LexEnd, LexFloat, LexId, LexIf, LexInput, LexInt, LexNot, LexOr, LexPrint, LexSemicolon, LexType, LexWhile
import sys

space = {}
stack = []
state = True


class PrnEnd:
    def __init__(self):
        self.ty = "PrnEnd"
        self.value = "$"

    def evaluate(self):
        global state
        state = False


class PrnType:
    def __init__(self, value):
        self.value = value
        self.ty = "type"

    def evaluate(self):
        stack.append(PrnType(self.value))


class PrnId:
    def __init__(self, value):
        self.value = value
        self.ty = "id"

    def evaluate(self):
        stack.append(PrnId(self.value))


class PrnAsign:
    def __init__(self, pos):
        self.value = "="
        self.ty = "asign"
        self.pos = pos

    def evaluate(self):
        global space
        val = stack.pop(-1)
        idx = stack.pop(-1)
        typ = "NULL"
        if len(stack) > 0 and stack[-1].ty == "type":
            typ = stack.pop(-1)
        if val.ty != "id":
            if idx.value not in space:
                if typ == "NULL":
                    print(f"SyntaxError. Varible {idx.value} hasn't declared. line {self.pos[0] + 1}")
                    exit(0)
                else:
                    if val.ty != typ.value:
                        print(f"SyntaxError. Types of varible {typ.value} and value {val.ty} don't math. line {self.pos[0] + 1}")
                        exit(0)
                    else:
                        space[idx.value] = [typ.value, val.value]
            else:
                if typ != "NULL":
                    print(f"SyntaxError. Redefining a varible type. line {self.pos[0] + 1}")
                    exit(0)
                else:
                    if val.ty == space[idx.value][0]:
                        space[idx.value][1] = val.value
                    else:
                        print(f"SyntaxError. Types of varible {space[idx.value][0]} and value {val.ty} don't math. line {self.pos[0] + 1}")
                        exit(0)
        else:
            if val.value not in space:
                print(f"SyntaxError. Varible {val.value} hasn't declared. line {self.pos[0] + 1}")
                exit(0)
            if idx.value not in space:
                if typ == "NULL":
                    print(f"SyntaxError. Varible {idx.value} hasn't declared. line {self.pos[0] + 1}")
                    exit(0)
                else:
                    if space[val.value][0] != typ.value:
                        print(f"SyntaxError. Types of varible {typ.value} and value {val.ty} don't math. line {self.pos[0] + 1}")
                        exit(0)
                    else:
                        space[idx.value] = [typ.value, space[val.value][1]]
            else:
                if typ != "NULL":
                    print(f"SyntaxError. Redefining a varible type. line {self.pos[0] + 1}")
                    exit(0)
                else:
                    if space[val.value][0] == space[idx.value][0]:
                        space[idx.value][1] = space[val.value][1]
                    else:
                        print(f"SyntaxError. Types of varible {space[idx.value][0]} and value {val.ty} don't math. line {self.pos[0] + 1}")
                        exit(0)


class PrnGoto:
    def __init__(self, value="NULL"):
        self.value = value


class PrnGoto_tempo(PrnGoto):
    ty = "goto_tempo"

    def evaluate(self):
        global stack
        stack.append(PrnGoto_tempo(self.value))


class PrnGoto_active(PrnGoto):
    ty = "goto_active"

    def evaluate(self):
        global stack
        return self.value


class PrnIf:
    def __init__(self):
        self.value = ""
        self.ty = "if"

    def evaluate(self):
        global stack, space
        goto1 = stack.pop(-1)
        if len(stack) == 0:
            print((f"SyntaxError. There is not expression in the if block. line {self.pos[0] + 1}"))
            exit(0)
        else:
            exp = stack.pop(-1)
            if not exp.value:
                return goto1.value


class PrnWhile:
    def __init__(self):
        self.value = ""
        self.ty = "while"

    def evaluate(self):
        global stack, space
        goto1 = stack.pop(-1)
        if not len(stack):
            print((f"SyntaxError. There is not expression in the while block. line {self.pos[0] + 1}"))
            exit(0)
        else:
            exp = stack.pop(-1)
            if not exp.value:
                return goto1.value


class PrnOp:
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        self.ty = "binOperation"

    def evaluate(self):
        global space, stack
        try:
            a1 = stack.pop(-1)
            a2 = stack.pop(-1)
        except Exception:
            print(f"SyntaxError. There are not enough varibles for asgin. line {self.pos[0] + 1}")
            exit(0)
        t1 = a1.ty
        t2 = a2.ty
        value_a1 = a1.value
        value_a2 = a2.value
        if a1.ty == "id":
            if a1.value not in space:
                print(f"SyntaxError. Varible {a1.value} hasn't declared. line {self.pos[0] + 1}")
                exit(0)
            t1 = space[a1.value][0]
            value_a1 = space[a1.value][1]
        if a2.ty == "id":
            if a2.value not in space:
                print(f"SyntaxError. Varible {a2.value} hasn't declared. line {self.pos[0] + 1}")
                exit(0)
            t2 = space[a2.value][0]
            value_a2 = space[a2.value][1]
        # if t1 != t2:
        #     print(f"SyntaxError. Types of varibles {a1.value}: {t1}, {a2.value}: {a2.ty} don't match. line {self.pos[0] + 1}")
        #     exit(0)
        error = False
        if self.value == "+":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = int(value_a1 + value_a2)
            elif (isinstance(value_a1, float) and isinstance(value_a2, float)) or ((isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float))):
                x = float(value_a1 + value_a2)
            elif isinstance(value_a1, bool) and isinstance(value_a2, bool):
                x = bool(value_a1 + value_a2)
            else:
                error = True
        elif self.value == "-":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = int(value_a2 - value_a1)
            elif (isinstance(value_a1, float) and isinstance(value_a2, float)) or ((isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float))):
                x = float(value_a2 - value_a1)
            else:
                error = True
        elif self.value == "*":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = int(value_a2 * value_a1)
            elif (isinstance(value_a1, float) and isinstance(value_a2, float)) or ((isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float))):
                x = float(value_a2 * value_a1)
            else:
                error = True
        elif self.value == "/":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = int(value_a2 // value_a1)
            elif (isinstance(value_a1, float) and isinstance(value_a2, float)) or ((isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float))):
                x = float(value_a2 / value_a1)
            else:
                error = True
        elif self.value == "^":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = int(value_a2 ** value_a1)
            else:
                error = True
        elif self.value == "%":
            if isinstance(value_a1, int) and isinstance(value_a2, int):
                x = value_a2 % value_a1
            else:
                error = True
        elif self.value == "~":
            x = bool(value_a1 == value_a2)
        elif self.value == "or":
            if isinstance(value_a1, bool) and isinstance(value_a2, bool):
                x = bool(value_a2 or value_a1)
            else:
                error = True
        elif self.value == "and":
            if isinstance(value_a1, bool) and isinstance(value_a2, bool):
                x = bool(value_a2 and value_a1)
            else:
                error = True
        elif self.value == "<":
            if (isinstance(value_a1, bool) and isinstance(value_a2, bool)) or (isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float)) or (isinstance(value_a1, float) and isinstance(value_a2, float)) or (isinstance(value_a1, int) and isinstance(value_a2, int)):
                x = bool(value_a2 < value_a1)
            else:
                error = True
        elif self.value == ">":
            if (isinstance(value_a1, bool) and isinstance(value_a2, bool)) or (isinstance(value_a1, float) and isinstance(value_a2, int)) or (isinstance(value_a1, int) and isinstance(value_a2, float)) or (isinstance(value_a1, float) and isinstance(value_a2, float)) or (isinstance(value_a1, int) and isinstance(value_a2, int)):
                x = bool(value_a2 > value_a1)
            else:
                error = True
        if error:
            print(f"operation {self.value} is not possible for <{t1}> {value_a1}, <{t2}> {value_a2}")
            exit(0)
        if isinstance(x, bool):
            stack.append(PrnBool(bool(x)))
        elif isinstance(x, int):
            stack.append(PrnInt(int(x)))
        elif isinstance(x, float):
            stack.append(PrnFloat(float(x)))


class PrnFloat:
    def __init__(self, value):
        self.value = value
        self.ty = "float"

    def evaluate(self):
        stack.append(PrnFloat(self.value))


class PrnBool:
    def __init__(self, value):
        self.value = value
        self.ty = "bool"

    def evaluate(self):
        stack.append(PrnBool(self.value))


class PrnNot:
    def __init__(self, pos):
        self.ty = "not"
        self.pos = pos
        self.value = ""

    def evaluate(self):
        global stack
        if not len(stack) or stack[-1].ty != "bool":
            print(f"SyntaxError. Object {stack[-1].ty} after not isn't bool. line {self.pos[0] + 1}")
            exit(0)


class PrnInt:
    def __init__(self, value):
        self.ty = "int"
        self.value = value

    def evaluate(self):
        stack.append(PrnInt(self.value))


class PrnInput:
    def __init__(self, pos):
        self.pos = pos
        self.ty = "input"
        self.value = ""

    def evaluate(self):
        global space, stack
        if len(stack) == 0:
            print(f"SyntaxError. There are not variables to input. line {self.pos[0] + 1}")
            exit(0)
        else:
            idx = stack.pop(-1)
            if idx.ty != "id":
                print(f"SyntaxError. Input can not be used for objects of the {idx.ty} type. line {self.pos[0] + 1}")
                exit(0)
            else:
                if idx.value not in space:
                    print(f"SyntaxError. Input can not be used for undeclared variables. line {self.pos[0] + 1}")
                    exit(0)
                else:
                    x = input()
                    try:
                        if space[idx.value][0] == "int":
                            space[idx.value][1] = int(x)
                        elif space[idx.value][0] == "float":
                            space[idx.value][1] = float(x)
                        elif space[idx.value][0] == "bool":
                            space[idx.value][1] = bool(x)
                        else:
                            print("code line 236. Unknown type of variable")
                    except Exception:
                        print(f"SyntaxError. Types of variable {idx.value} <{space[idx.value][0]}> and input do not math> . line {self.pos[0] + 1}")
                        exit(0)


class PrnPrint:
    def __init__(self):
        self.ty = "print"
        self.value = ""

    def evaluate(self):
        global space
        if len(stack) == 0:
            print()
        else:
            val = stack.pop(-1)
            if val.ty == "id":
                if val.value in space:
                    print(space[val.value][1])
                else:
                    print(val.value)
            else:
                print(val.value)


class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.lexems = []
        self.line = 0
        self.chr = 0
        self.bufer = ""

    def lex(self):
        Lexer.S(self)

    def S(self):  # Стартовое состояние
        if len(self.bufer) > 0:
            print("Debug Error: при переходе в состояние S bufer оказался непустым")
            exit(0)
        if self.pos >= len(self.code):
            return
        x = self.code[self.pos]
        if x in ["\t", " "]:
            self.pos += 1
            self.chr += 1
            Lexer.S(self)
        elif x == "\n":
            self.line += 1
            self.chr = 0
            self.pos += 1
            self.chr += 1
            Lexer.S(self)
        elif x == ",":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexComma((self.line, self.chr)))
            Lexer.S(self)
        elif x == ";":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexSemicolon((self.line, self.chr)))
            Lexer.S(self)
        elif x == "{":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexBraceOpen((self.line, self.chr)))
            Lexer.S(self)
        elif x == "}":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexBraceClose((self.line, self.chr)))
            Lexer.S(self)
        elif x == "(":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexBktOpen((self.line, self.chr)))
            Lexer.S(self)
        elif x == ")":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexBktClose((self.line, self.chr)))
            Lexer.S(self)
        elif x == "=":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexAsign((self.line, self.chr)))
            Lexer.S(self)
        elif x in ["+", "-", "*", "/", "^", "%", "~", "<", ">"]:
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexBinOp((self.line, self.chr), x))
            Lexer.S(self)
        elif x == "$":
            self.pos += 1
            self.chr += 1
            self.lexems.append(LexEnd((self.line, self.chr)))
            Lexer.S(self)
        elif x.isdigit():
            self.bufer += x
            self.pos += 1
            self.chr += 1
            Lexer.N(self)
        elif x.isalpha():
            self.bufer += x
            self.pos += 1
            self.chr += 1
            Lexer.C(self)
        else:
            print(f"SyntaxError. Invalid character \"{x}\" after \"Start\" block. line {self.line + 1}, character {self.chr}")
            exit(0)

    def C(self):  # Состояние ввода символов строк (Character)
        if self.pos >= len(self.code):
            return
        x = self.code[self.pos]
        if x.isalpha():
            self.bufer += x
            self.pos += 1
            self.chr += 1
            Lexer.C(self)
        elif x in [" ", ";", "{", "}", "(", ")", "=", "~", ","]:
            word = self.bufer
            self.bufer = ""
            if word == "false":
                self.lexems.append(LexBool((self.line, self.chr), False))
            elif word == "true":
                self.lexems.append(LexBool((self.line, self.chr), True))
            elif word in ["int", "bool", "float"]:
                self.lexems.append(LexType((self.line, self.chr), word))
            elif word == "if":
                self.lexems.append(LexIf((self.line, self.chr)))
            elif word == "else":
                self.lexems.append(LexElse((self.line, self.chr)))
            elif word == "while":
                self.lexems.append(LexWhile((self.line, self.chr)))
            elif word == "input":
                self.lexems.append(LexInput((self.line, self.chr)))
            elif word == "print":
                self.lexems.append(LexPrint((self.line, self.chr)))
            elif word == "and":
                self.lexems.append(LexAnd((self.line, self.chr)))
            elif word == "or":
                self.lexems.append(LexOr((self.line, self.chr)))
            elif word == "not":
                self.lexems.append(LexNot((self.line, self.chr)))
            else:
                self.lexems.append(LexId((self.line, self.chr), word))
            Lexer.S(self)
        else:
            print(f"SyntaxError. Invalid character \"{x}\" after \"String\" block. line {self.line + 1}, character {self.chr}")
            exit(0)

    def N(self):  # Состояние ввода числа iNt
        if self.pos >= len(self.code):
            return
        x = self.code[self.pos]
        if x.isdigit():
            self.bufer += x
            self.pos += 1
            self.chr += 1
            Lexer.N(self)
        elif x == ".":
            self.bufer += x
            self.pos += 1
            self.chr += 1
            Lexer.F(self)
        elif x in [" ", ",", ";", "+", "-", "*", "/", "~", "%", "^", ")"]:
            self.lexems.append(LexInt((self.line, self.chr), self.bufer))
            self.bufer = ""
            Lexer.S(self)
        else:
            print(f"SyntaxError. Invalid character \"{x}\" after \"Int\" block. line {self.line + 1}, character {self.chr}")
            exit(0)

    def F(self):  # Состояние ввода числа Float
        if self.pos >= len(self.code):
            return
        x = self.code[self.pos]
        if x.isdigit():
            self.pos += 1
            self.chr += 1
            self.bufer += x
            Lexer.F(self)
        elif x in [" ", ",", ";", "+", "-", "*", "/", "^", "~", ")"]:
            self.lexems.append(LexFloat((self.line, self.chr), self.bufer))
            self.bufer = ""
            Lexer.S(self)
        else:
            print(f"SyntaxError. Invalid character \"{x}\" after \"Float\" block. line {self.line + 1}, character {self.chr}")
            exit(0)


class Parser:
    def __init__(self, lexems):
        self.lexems = lexems
        self.pos = 0
        self.prn = []

    def Parse(self):
        Parser.P(self)

    def P(self):
        Parser.B(self)
        if self.lexems[self.pos].ty != "end":
            print("SyntaxError. excess symbols at the end of the program")
            exit(0)
        if self.pos == len(self.lexems):
            print("SyntaxError. Missing terminating character at the end of the program")
            exit(0)
        elif self.lexems[self.pos].ty == "end":
            self.prn.append(PrnEnd())

    def B(self):
        if self.lexems[self.pos].value == "{":
            self.pos += 1
            Parser.S(self)
            while self.lexems[self.pos].value == ";":
                self.pos += 1
                Parser.S(self)
            if self.lexems[self.pos].value == "}":
                self.pos += 1
            else:
                print(f"SyntaxError. Missing closing brace character at the end of the block of commands. line {self.lexems[self.pos].pos[0]}, character")
                exit(0)
        else:
            print(f"SyntaxError. Missing opening brace character at the begining of the block of commands. line {self.lexems[self.pos].pos[0]}, character")
            exit(0)

    def S(self):
        if self.lexems[self.pos].value in ["int", "bool", "float"]:
            self.prn.append(PrnType(self.lexems[self.pos].value))
            self.pos += 1
        if self.lexems[self.pos].ty == "id":
            self.prn.append(PrnId(self.lexems[self.pos].value))
            self.pos += 1
            if self.lexems[self.pos].ty == "comma":
                while self.lexems[self.pos].ty == "comma":
                    self.pos += 1
                    if self.lexems[self.pos].ty == "id":
                        self.prn.append(PrnId(self.lexems[self.pos].value))
                        self.pos += 1
                    else:
                        print(f"SyntaxError. Missing ID after comma. line {self.lexems[self.pos].pos[0] + 1}")
                        exit(0)
            elif self.lexems[self.pos].ty == "asign":
                self.pos += 1
                Parser.E(self)
                self.prn.append(PrnAsign(self.lexems[self.pos].pos))
            else:
                print(f"SyntaxError. Missing asign (=) after ID block. line {self.lexems[self.pos].pos[0] + 1}")
                exit(0)
        elif self.lexems[self.pos].ty == "if":
            self.pos += 1
            if self.lexems[self.pos].ty == "bktOpen":
                self.pos += 1
                Parser.E(self)
                if self.lexems[self.pos].ty == "bktClose":
                    self.pos += 1
                    goto1 = PrnGoto_tempo()
                    self.prn.append(goto1)
                    self.prn.append(PrnIf())
                    Parser.B(self)
                    goto2 = PrnGoto_active()
                    self.prn.append(goto2)
                    goto1.value = len(self.prn)
                    if self.lexems[self.pos].ty == "else":
                        self.pos += 1
                        Parser.B(self)
                        goto2.value = len(self.prn)
                else:
                    print(f"SyntaxError. Missing bktClose after expression block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                    exit(0)
            else:
                print(f"SyntaxError. Missing bktOpen after if. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                exit(0)
        elif self.lexems[self.pos].ty == "while":
            self.pos += 1
            if self.lexems[self.pos].ty == "bktOpen":
                self.pos += 1
                point = len(self.prn)
                Parser.E(self)
                goto1 = PrnGoto_tempo()
                self.prn.append(goto1)
                self.prn.append(PrnWhile())
                if self.lexems[self.pos].ty == "bktClose":
                    self.pos += 1
                    Parser.B(self)
                    goto2 = PrnGoto_active()
                    goto2.value = point
                    self.prn.append(goto2)
                    goto1.value = len(self.prn)
                else:
                    print(f"SyntaxError. Missing bktClose after while block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                    exit(0)

            else:
                print(f"SyntaxError. Missing bktOpen after while block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                exit(0)
        elif self.lexems[self.pos].ty == "input":
            posd = self.lexems[self.pos].pos
            self.pos += 1
            if self.lexems[self.pos].ty == "bktOpen":
                self.pos += 1
                Parser.E(self)
                self.prn.append(PrnInput(posd))
                if self.lexems[self.pos].ty == "bktClose":
                    self.pos += 1
                else:
                    print(f"SyntaxError. Missing bktClose after input block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                    exit(0)
            else:
                print(f"SyntaxError. Missing bktOpen after input block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                exit(0)
        elif self.lexems[self.pos].ty == "print":
            self.pos += 1
            if self.lexems[self.pos].ty == "bktOpen":
                self.pos += 1
                Parser.E(self)
                self.prn.append(PrnPrint())
                if self.lexems[self.pos].ty == "bktClose":
                    self.pos += 1
                else:
                    print(f"SyntaxError. Missing bktClose after print block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                    exit(0)
            else:
                print(f"SyntaxError. Missing bktOpen after print block. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                exit(0)

    def E(self):
        Parser.E1(self)
        if self.lexems[self.pos].ty == "binOperation":
            op = self.lexems[self.pos]
            self.pos += 1
            Parser.E1(self)  # Проблемный момент. Непонятно что делать, если происходит следующая ситуация E1 E1. Обрабатывается лишь случай E1 BinOp E1
            self.prn.append(PrnOp(op.value, op.pos))

    def E1(self):
        Parser.T(self)
        while self.lexems[self.pos].ty in ["binOperation", "or"]:
            op = self.lexems[self.pos]
            self.pos += 1
            Parser.T(self)
            self.prn.append(PrnOp(op.value, op.pos))

    def T(self):
        Parser.F(self)
        while self.lexems[self.pos].value in ["*", "/", "%", "and"]:
            op = self.lexems[self.pos]
            self.pos += 1
            Parser.F(self)
            self.prn.append(PrnOp(op.value, op.pos))

    def F(self):
        if self.lexems[self.pos].ty == "id":
            self.prn.append(PrnId(self.lexems[self.pos].value))
            self.pos += 1
        elif self.lexems[self.pos].ty == "float":
            self.prn.append(PrnFloat(self.lexems[self.pos].value))
            self.pos += 1
        elif self.lexems[self.pos].ty == "bool":
            self.prn.append(PrnBool(self.lexems[self.pos].value))
            self.pos += 1
        elif self.lexems[self.pos].ty == "not":
            self.prn.append(PrnNot(self.lexems[self.pos].pos))
            self.pos += 1
            Parser.F(self)
        elif self.lexems[self.pos].ty == "int":
            self.prn.append(PrnInt(self.lexems[self.pos].value))
            self.pos += 1
        elif self.lexems[self.pos].ty == "bktOpen":
            self.pos += 1
            Parser.E(self)
            if self.lexems[self.pos].ty == "bktClose":
                self.pos += 1
            else:
                print(f"SyntaxError. A bktClose <)> is missing. line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
                exit(0)
        else:
            print(f"SyntaxError. F block isn't correct (Maybe a bktOpen <(> is missing). line {self.lexems[self.pos].pos[0]}, character {self.lexems[self.pos].pos[1]}")
            exit(0)


class Machine:
    pos = 0

    def __init__(self, prn):
        self.prn = prn

    def run(self):
        global space, stack, state
        while state:
            # print(self.prn[self.pos].value, stack)
            res = self.prn[self.pos].evaluate()
            if res is not None and res != "NULL":
                self.pos = res
            else:
                self.pos += 1


code = open("code.txt", "r").read() + " "
# code = open(sys.argv[1], "r").read()
lexer = Lexer(code)
lexer.lex()
lexer.lexems.append(LexEnd(-1))
parser = Parser(lexer.lexems)
parser.Parse()
machine = Machine(parser.prn)
machine.run()


def out():
    for x in lexer.lexems:
        print((x.ty, x.value))
    print()


def out_prn():
    i = 0
    for x in parser.prn:
        print([i, x.ty, x.value], end=" ")
        i += 1
    print()
