class Error(Exception):
    def __init__(self, token, cause) -> None:
        self.token = token
        self.cause = cause

    def __repr__(self) -> str:
        return f'Error at {self.token}: {self.cause}'

    def __str__(self) -> str:
        return f'Error at {self.token}: {self.cause}'

class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos
    
    def __repr__(self) -> str:
        return f'LexerError at {self.pos}'

    def __str__(self) -> str:
        return f'LexerError at {self.pos}'

class ErrorSyntax(Error):
    def __init__(self,token,cause) -> None:
        super.__init__(token,cause)
    
    def __repr__(self) -> str:
        return f'SyntaxError at {self.token}: {self.cause}'

    def __str__(self) -> str:
        return f'SyntaxError at {self.token}: {self.cause}'

class ErrorSemantic(Error):
    def __init__(self,token,cause) -> None:
        super.__init__(token,cause)
    
    def __repr__(self) -> str:
        return f'SemanticError at {self.token}: {self.cause}'

    def __str__(self) -> str:
        return f'SemanticError at {self.token}: {self.cause}'