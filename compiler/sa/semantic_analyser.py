from compiler.sa.sa_utils import SA, ScopeDeclVisitor, InferenceVisitor

def semantic_analyser(ast_root):
    semantic_state = SA()
    scopedeclvisitor = ScopeDeclVisitor(semantic_state)
    scopedeclvisitor.visit(ast_root)
    inferencevisitor = InferenceVisitor(semantic_state)
    inferencevisitor.visit(ast_root)