import ast
import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtGui import QImage

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assistente.py"
TREE = ast.parse(SOURCE.read_text(encoding="utf-8"))
SPEC = importlib.util.spec_from_file_location("deckmate_assistente", SOURCE)
APP_MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(APP_MODULE)


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
    def test_root_and_project_sources_are_identical(self) -> None:
        root_copy = SOURCE.parent.parent / "assistente.py"
        if not root_copy.is_file():
            self.skipTest("the synchronized outer workspace copy is not in this checkout")
        self.assertEqual(SOURCE.read_bytes(), root_copy.read_bytes())

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

    def test_platform_guidance_and_short_prompt_remain(self) -> None:
        selector = next(
            node for node in TREE.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "selecionar_contexto_conhecimento"
        )
        names = {node.id for node in ast.walk(selector) if isinstance(node, ast.Name)}
        self.assertIn("CONHECIMENTO_LINUX", names)
        self.assertIn("CONHECIMENTO_STEAM_DECK", names)
        self.assertIn("TERMOS_SISTEMA", names)
        self.assertIn("TERMOS_STEAM_DECK", names)
        prompt = find_method("AplicativoAssistente", "enviar")
        prompt_source = ast.unparse(prompt)
        for phrase in (
            "selecionar_contexto_conhecimento", "TERMOS_CRIADOR",
            "direto e breve", "comece pelo resultado", "Nunca responda",
            "copiar no terminal", "diga isso claramente",
        ):
            self.assertIn(phrase, prompt_source)

    def test_app_uses_qt_without_tk_or_customtkinter(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("from PySide6.QtWidgets import", source)
        self.assertNotIn("tkinter", source.casefold())
        self.assertNotIn("customtkinter", source.casefold())
        self.assertNotIn("setWindowOpacity", source)
        self.assertNotIn('attributes("-alpha"', source)
        self.assertNotIn("_NET_WM_WINDOW_OPACITY", source)

    def test_live_window_has_translucent_black_root_and_opaque_controls(self) -> None:
        app = APP_MODULE.QApplication.instance() or APP_MODULE.QApplication([])
        with mock.patch.object(APP_MODULE.AplicativoAssistente, "iniciar_agente"):
            window = APP_MODULE.AplicativoAssistente()
        try:
            qt = APP_MODULE.Qt
            self.assertTrue(
                window.testAttribute(qt.WidgetAttribute.WA_TranslucentBackground)
            )
            root = window.centralWidget()
            self.assertIn("rgba(0, 0, 0, 128)", window.styleSheet())
            self.assertIn("rgba(0, 0, 0, 128)", root.styleSheet())
            self.assertEqual(1.0, window.windowOpacity())
            self.assertIn("#101114", window.chat_shell.styleSheet())
            self.assertIn("#101114", window.styleSheet())
            self.assertIn("#20242c", window.styleSheet())
            self.assertIn("color: #f3f4f6", window.styleSheet())
            self.assertNotIn("rgba(", window.chat_shell.styleSheet())
            window.show()
            app.processEvents()
            image = window.grab().toImage().convertToFormat(
                QImage.Format.Format_ARGB32
            )
            root_pixel = image.pixelColor(10, 60)
            self.assertEqual(128, root_pixel.alpha())
            panel_position = window.chat_shell.mapTo(
                window, APP_MODULE.QPoint(30, 40)
            )
            self.assertEqual(255, image.pixelColor(panel_position).alpha())
            button_position = window.botao_enviar.mapTo(
                window,
                APP_MODULE.QPoint(
                    window.botao_enviar.width() // 2,
                    window.botao_enviar.height() // 2,
                ),
            )
            self.assertEqual(255, image.pixelColor(button_position).alpha())
            self.assertIsInstance(window.logo, APP_MODULE.LogoDeckMate)
            self.assertFalse(window.logo.grab().isNull())
        finally:
            window.close()
            app.processEvents()

    def test_kwin_blur_is_gated_to_kde_x11_and_never_sets_global_alpha(self) -> None:
        method = find_method("AplicativoAssistente", "_ambiente_kwin_x11")
        source = ast.get_source_segment(SOURCE.read_text(encoding="utf-8"), method)
        self.assertIn('platform.system() == "Linux"', source)
        self.assertIn('QGuiApplication.platformName().casefold() == "xcb"', source)
        self.assertIn('os.environ.get("DISPLAY")', source)
        self.assertIn('"kde", "plasma"', source)
        blur = find_method("AplicativoAssistente", "configurar_blur_kwin")
        blur_source = ast.get_source_segment(
            SOURCE.read_text(encoding="utf-8"), blur
        )
        self.assertIn("_KDE_NET_WM_BLUR_BEHIND_REGION", blur_source)
        self.assertIn("XChangeProperty", blur_source)
        self.assertNotIn("NET_WM_WINDOW_OPACITY", blur_source)


if __name__ == "__main__":
    unittest.main()
