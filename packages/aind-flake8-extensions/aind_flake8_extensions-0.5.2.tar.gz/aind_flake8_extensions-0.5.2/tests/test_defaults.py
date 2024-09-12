import ast
import unittest
from aind_flake8_extensions.plugin import run_ast_checks


class TestPlugin(unittest.TestCase):

    def check_code(self, code: str):
        """Helper method to run the PydanticFieldChecker on the provided code."""
        tree = ast.parse(code)
        return list(run_ast_checks(tree))

    def test_optional_field_missing_default(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: Optional[str] = Field(None, description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF001 Field 'name' should use 'default=None' for optional fields")

    def test_optional_no_field(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: Optional[str]
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][2], "PF001 Field 'name' should use 'default=None' for optional fields")

    def test_correct_optional_field(self):
        code = """
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the user")
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_no_fields(self):
        code = """
from pydantic import BaseModel

class MyModel(BaseModel):
    pass
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)

    def test_correct_required_default_set(self):
        code = """
from pydantic import BaseModel

class MyModel(BaseModel):
    stimulus_devices: List[int] = Field(default=[])
"""
        errors = self.check_code(code)
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
