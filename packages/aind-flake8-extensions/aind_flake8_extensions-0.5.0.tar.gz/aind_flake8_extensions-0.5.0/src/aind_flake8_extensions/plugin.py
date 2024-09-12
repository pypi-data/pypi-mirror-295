import ast
from typing import Any, Generator, Tuple


class PydanticDefaultChecker(ast.NodeVisitor):
    def __init__(self, tree: ast.AST) -> None:
        """Initialize with a ast tree

        Parameters
        ----------
        tree : ast.AST
            tree to use for analysis
        """
        self.tree = tree
        self.issues = []

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """Visit all nodes and generate issues as (int, int, str, type)

        Yields
        ------
        Generator[Tuple[int, int, str, type], None, None]
            
        """
        self.visit(self.tree)
        yield from self.issues

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        """Visit Annotated Assign nodes, i.e. of the type "name: type = ..."

        Don't change the naming convention, this is used by ast

        Parameters
        ----------
        node : ast.AnnAssign
            annotated assign node
        """
        self.check_field(node)
        self.generic_visit(node)

    def error_no_default(self, node: ast.AnnAssign):
        self.issues.append(
            (
                node.lineno,
                node.col_offset,
                f"PF001 Field '{node.target.id}' should use 'default=None' for optional fields",
                type(self),
            )
        )

    # def error_no_ellipsis(self, node: ast.AnnAssign):
    #     self.issues.append(
    #         (
    #             node.lineno,
    #             node.col_offset,
    #             f"PF002 Field '{node.target.id}' should use '...' for required fields",
    #             type(self),
    #         )
    #     )

    def check_field_optional(self, node: ast.AnnAssign) -> None:
        """Check fields in each node to see if they match the format:

        name: Optional[type] = Field(default=None, args)

        If not, flag issue PF001

        Parameters
        ----------
        node : ast.AnnAssign
            Node to check
        """
        if not any(kw.arg == "default" for kw in node.value.keywords):
            self.error_no_default(node)

    def check_field_required(self, node: ast.AnnAssign) -> None:
        """Check fields in each node to see if they match the format:

        name: type = Field(..., args)
        name: type = Field(default=value, args)

        If not, flag issue PF002

        Parameters
        ----------
        node : ast.AnnAssign
            Node to check
        """
        pass
        # if node.value.args:
        #     # Check if there are arguments with no keywords, fail if they aren't an ellipsis
        #     first_arg = node.value.args[0]
        #     if not isinstance(first_arg, ast.Constant) or first_arg.value is not Ellipsis:
        #         self.error_no_ellipsis
        # elif node.value.keywords:
        #     # Check if the first keyword is 'default'; that's fine, they passed a value
        #     if not node.value.keywords[0].arg == 'default':
        #         self.error_no_ellipsis(node)

        # else:
        #     # No arguments provided, defaulting to required field check
        #     self.error_no_ellipsis(node)

    def check_field(self, node: ast.AnnAssign) -> None:
        """Check fields to see if they match our default/ellipsis criteria

        Parameters
        ----------
        node : ast.AnnAssign
            Node to check
        """

        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "Field"
        ):
            # There is a Field()
            if isinstance(node.target, ast.Name):
                field_name = node.target.id
                type_annotation = node.annotation

                # Determine if the type is Optional
                is_optional = (
                    isinstance(type_annotation, ast.Subscript)
                    and isinstance(type_annotation.value, ast.Name)
                    and type_annotation.value.id == "Optional"
                )

                if is_optional:
                    self.check_field_optional(node)
                else:
                    self.check_field_required(node)
        else:
            # Handle missing Field case for required fields
            # if isinstance(node.target, )
            if isinstance(node.target, ast.Name):
                field_name = node.target.id
                type_annotation = node.annotation

                # Determine if the type is Optional
                is_optional = (
                    isinstance(type_annotation, ast.Subscript)
                    and isinstance(type_annotation.value, ast.Name)
                    and type_annotation.value.id == "Optional"
                )

                is_literal = (
                    isinstance(type_annotation, ast.Subscript)
                    and isinstance(type_annotation.value, ast.Name)
                    and type_annotation.value.id == "Literal"
                )

                if not is_literal:
                    if is_optional:
                        # Optional fields should have Field(default=None) at a minimum
                        self.error_no_default(node)
                    else:
                        # Required fields should have the ellipsis in Field
                        self.error_no_ellipsis(node)


def run_ast_checks(
    tree: ast.AST,
) -> Generator[Tuple[int, int, str, type], None, None]:
    checker = PydanticDefaultChecker(tree)
    yield from checker.run()
