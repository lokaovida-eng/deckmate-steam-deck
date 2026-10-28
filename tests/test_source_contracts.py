import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assistente.py"
TREE = ast.parse(SOURCE.read_text(encoding="utf-8"))


def find_assignment(name: str) -> ast.expr:
    for node in TREE.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            return node.value
    raise AssertionError(f"Assignment not found: {name}")


def find_method(class_name: str, method_name: str) -> ast.FunctionDef:
    for node in TREE.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for member in node.body:
                if isinstance(member, ast.FunctionDef) and member.name == method_name:
                    return member
    raise AssertionError(f"Method not found: {class_name}.{method_name}")


class SourceContractTests(unittest.TestCase):
    def test_permission_dialog_copy_exists_for_each_language(self) -> None:
        languages = ast.literal_eval(find_assignment("IDIOMAS"))
        self.assertEqual(
            {"en", "es", "pt", "ja", "mx", "de", "fr", "ru", "sv"},
            set(languages),
        )
        for language, translations in languages.items():
            with self.subTest(language=language):
                self.assertIn("permission_help", translations)
                self.assertIn("allow", translations)
                self.assertIn("deny", translations)
                self.assertNotIn("allow_session", translations)

    def test_tool_approval_is_always_a_single_action(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("permissao_sessao", source)
        permission_handler = find_method(
            "AplicativoAssistente", "solicitar_permissao"
        )
        calls = [
            node.func.id
            for node in ast.walk(permission_handler)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        ]
        self.assertIn("PermissionDecisionApproveOnce", calls)
        self.assertIn("PermissionDecisionReject", calls)

    def test_steam_deck_guidance_is_in_the_agent_context(self) -> None:
        prompt = find_method("AplicativoAssistente", "enviar")
        names = {
            node.id for node in ast.walk(prompt) if isinstance(node, ast.Name)
        }
        self.assertIn("CONHECIMENTO_SISTEMAS", names)
        assigned_names = {
            target.id
            for node in TREE.body
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        self.assertIn("CONHECIMENTO_STEAM_DECK", assigned_names)


if __name__ == "__main__":
    unittest.main()
