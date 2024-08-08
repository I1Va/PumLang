class Lex:
    def __init__(self, pos):
        self.pos = pos
        self.ty = ""
        self.value = ""


class LexFloat(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.value = float(value)
        self.ty = "float"


class LexInt(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.value = int(value)
        self.ty = "int"


class LexComma(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "comma"
        self.value = ","


class LexBraceOpen(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "braceOpen"
        self.value = "{"


class LexSemicolon(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "semicolon"
        self.value = ";"


class LexBraceClose(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "braceClose"
        self.value = "}"


class LexBktOpen(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "bktOpen"
        self.value = "("


class LexEnd(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "end"
        self.value = "$"


class LexBktClose(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "bktClose"
        self.value = ")"


class LexBinOp(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.ty = "binOperation"
        self.value = value


class LexAsign(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "asign"
        self.value = "="


class LexBool(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.ty = "bool"
        self.value = value


class LexType(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.ty = "type"
        self.value = value


class LexId(Lex):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.ty = "id"
        self.value = value


class LexIf(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "if"


class LexElse(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "else"


class LexWhile(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "while"


class LexInput(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "input"


class LexPrint(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "print"


class LexAnd(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "and"
        self.value = "and"


class LexOr(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.value = "or"
        self.ty = "or"


class LexNot(Lex):
    def __init__(self, pos):
        super().__init__(pos)
        self.ty = "not"
