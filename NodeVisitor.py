class NodeVisitor(object):
    def visit(self, node):
        methodName = "visit" + type(node).__name__
        visitor = getattr(self, methodName, self.genericVisit)
        
        return visitor(node)

    def genericVisit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method") 