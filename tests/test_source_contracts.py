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

    def test_platform_guidance_is_selected_for_relevant_requests(self) -> None:
        selector = next(
            node for node in TREE.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "selecionar_contexto_conhecimento"
        )
        names = {
            node.id for node in ast.walk(selector) if isinstance(node, ast.Name)
        }
        self.assertIn("CONHECIMENTO_LINUX", names)
        self.assertIn("CONHECIMENTO_STEAM_DECK", names)
        selector_names = {
            node.id for node in ast.walk(selector) if isinstance(node, ast.Name)
        }
        self.assertIn("TERMOS_SISTEMA", selector_names)
        self.assertIn("TERMOS_STEAM_DECK", selector_names)
        prompt = find_method("AplicativoAssistente", "enviar")
        prompt_names = {
            node.id for node in ast.walk(prompt) if isinstance(node, ast.Name)
        }
        self.assertIn("selecionar_contexto_conhecimento", prompt_names)
        self.assertIn("TERMOS_CRIADOR", prompt_names)
        self.assertIn("direto e breve", ast.unparse(prompt))
        self.assertIn("comece pelo resultado", ast.unparse(prompt))
        self.assertIn("Nunca responda", ast.unparse(prompt))
        self.assertIn("copiar no terminal", ast.unparse(prompt))
        self.assertIn("diga isso claramente", ast.unparse(prompt))
        self.assertNotIn("CONHECIMENTO_SISTEMAS", {
            target.id
            for node in TREE.body
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        })

    def test_translucency_has_a_conservative_fallback(self) -> None:
        init = find_method("AplicativoAssistente", "__init__")
        source = ast.get_source_segment(SOURCE.read_text(encoding="utf-8"), init)
        self.assertIsNotNone(source)
        self.assertIn('attributes("-alpha", OPACIDADE_JANELA)', source)
        self.assertIn("except tk.TclError as exc", source)
        self.assertIn("logging.warning", source)


if __name__ == "__main__":
    unittest.main()
