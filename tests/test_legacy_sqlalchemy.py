# # tests/test_legacy_sqlalchemy.py
#
# import ast
# from pathlib import Path
# import pytest
#
# # Список запрещённых/устаревших вызовов SQLAlchemy
# FORBIDDEN = [
#     "session.query",
#     "declarative_base",
#     "Column",
# ]
#
# @pytest.mark.parametrize("file_path", list(Path("app/modules").rglob("*.py")))
# def test_no_legacy_sqlalchemy(file_path):
#     """
#     Проверяет, что в коде не используется legacy SQLAlchemy API.
#     Даже если модуль импортируется, deprecated вызовы должны быть найдены.
#     """
#     source = file_path.read_text()
#     tree = ast.parse(source)
#
#     for node in ast.walk(tree):
#         if isinstance(node, ast.Call):
#             func_name = ast.unparse(node.func)
#             for forbidden in FORBIDDEN:
#                 assert forbidden not in func_name, f"Legacy API '{forbidden}' found in {file_path}"
#
