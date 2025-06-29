from __future__ import annotations
from typing import Union
from Token import *

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST) -> None:
        self.left = left
        self.op = op 
        self.token = self.op
        self.right = right

class Num(AST):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST) -> None:
        self.op = op
        self.token = self.op
        self.expr = expr

class Compound(AST):
    def __init__(self) -> None:
        self.children = []

class Assign(AST):
    def __init__(self, left: Var, op: Token, right: AST) -> None:
        self.left = left
        self.op = op
        self.token = op
        self.right = right

class Var(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

class Program(AST):
    def __init__(self, name: Token, block) -> None:
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations: list[Var], compoundStatement: Union[Assign, Compound]) -> None:
        self.declarations = declarations
        self.compoundStatement = compoundStatement

class VarDecl(AST):
    def __init__(self, varNode: Var, typeNode: Type) -> None:
        self.varNode = varNode
        self.typeNode = typeNode

class Type(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

class ProcedureDecl(AST):
    def __init__(self, procName: str, blockNode: Block):
        self.procName = procName
        self.blockNode = blockNode

class NoOp(AST):
    pass