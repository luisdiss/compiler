from compiler.sa.sa_utils import SA, ScopeDeclVisitor, InferenceVisitor
from typing import Any, Optional


def semantic_analyser(ast_root: Any) -> SA:
    """
    Executes the complete semantic analysis pipeline on the provided AST.

    This function orchestrates the two-phase semantic analysis process:
    1. **Scope Declaration**: Traverses the AST to build the scope hierarchy,
       populate symbol tables, and resolve identifier bindings.
    2. **Type Inference**: Traverses the AST again to infer types for expressions,
       validate function calls, and propagate type information through the scope tree.

    Args:
        ast_root: The root node of the Abstract Syntax Tree (AST) to analyze.

    Returns:
        The populated `SA` (Semantic Analysis) state object containing the
        fully resolved scope tree, symbol tables, and inferred types.
    """
    # Initialize the global semantic analysis state
    semantic_state: SA = SA()

    # Phase 1: Scope Declaration and Symbol Resolution
    # Builds the scope tree and binds identifiers to their definitions
    scope_decl_visitor: ScopeDeclVisitor = ScopeDeclVisitor(semantic_state)
    scope_decl_visitor.visit(ast_root)

    # Phase 2: Type Inference and Validation
    # Infers types for expressions and validates function calls against inferred signatures
    inference_visitor: InferenceVisitor = InferenceVisitor(semantic_state)
    inference_visitor.visit(ast_root)

    return semantic_state