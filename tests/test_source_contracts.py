import ast
import importlib.util
import os
import queue
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest import mock


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QEvent
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


def find_method(
    class_name: str, method_name: str
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    for node in TREE.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for member in node.body:
                if isinstance(
                    member, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) and member.name == method_name:
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

    def test_permission_summaries_exist_for_each_language(self) -> None:
        translations = ast.literal_eval(find_assignment("TEXTOS_PERMISSAO"))
        self.assertEqual(
            {"en", "es", "pt", "ja", "mx", "de", "fr", "ru", "sv"},
            set(translations),
        )
        for language, values in translations.items():
            with self.subTest(language=language):
                self.assertEqual(
                    {"generic", "storage_scan", "change_warning", "show_details"},
                    set(values),
                )

    def test_hardware_shortcut_does_not_consume_other_system_requests(self) -> None:
        cases = (
            "Quando meu Steam Deck foi comprado?",
            "Verifique se o Android Studio está instalado duas vezes.",
            "Procure arquivos duplicados, caches temporários e formas de liberar espaço.",
            "Sim, veja os arquivos do Android Studio e os caches.",
        )
        for request in cases:
            with self.subTest(request=request):
                self.assertFalse(
                    APP_MODULE.AplicativoAssistente.pedido_sobre_hardware(request)
                )
        self.assertTrue(
            APP_MODULE.AplicativoAssistente.pedido_sobre_hardware(
                "Quais são as especificações de hardware do meu Steam Deck?"
            )
        )

    def test_permission_summary_explains_storage_scan_and_flags_changes(self) -> None:
        summarize = APP_MODULE.AplicativoAssistente.resumir_permissao
        app = SimpleNamespace(idioma="pt")
        scan = SimpleNamespace(
            full_command_text=(
                "uname -srmo; cat /etc/os-release; df -hT; "
                'du -xhd1 "$HOME"'
            )
        )
        summary = summarize(app, scan, SimpleNamespace())
        self.assertIn("espaço em disco", summary)
        self.assertIn("Não pede para apagar arquivos", summary)
        change = SimpleNamespace(full_command_text="rm -rf /tmp/example")
        self.assertIn("pode alterar ou apagar", summarize(app, change, None))
        disguised_change = SimpleNamespace(
            full_command_text="find /tmp -delete; uname -a; df -h; du -sh /tmp"
        )
        self.assertIn(
            "pode alterar ou apagar",
            summarize(app, disguised_change, None),
        )

    def test_permission_dialog_hides_raw_command_until_requested(self) -> None:
        app = APP_MODULE.QApplication.instance() or APP_MODULE.QApplication([])
        with mock.patch.object(APP_MODULE.AplicativoAssistente, "iniciar_agente"):
            window = APP_MODULE.AplicativoAssistente()
        dialogs = []
        try:
            with mock.patch.object(
                APP_MODULE.QDialog,
                "exec",
                lambda dialog: dialogs.append(dialog) or 0,
            ):
                window.mostrar_dialogo_permissao(
                    SimpleNamespace(
                        full_command_text="uname -srmo; df -hT; du -xhd1 \"$HOME\""
                    ),
                    SimpleNamespace(tool_name="shell"),
                    queue.Queue(maxsize=1),
                )
            dialog = dialogs[0]
            summary = next(
                label for label in dialog.findChildren(APP_MODULE.QLabel)
                if "espaço em disco" in label.text()
            )
            details_toggle = dialog.findChild(APP_MODULE.QCheckBox)
            details = dialog.findChild(APP_MODULE.QPlainTextEdit)
            self.assertTrue(summary.wordWrap())
            self.assertTrue(details.isHidden())
            details_toggle.setChecked(True)
            self.assertFalse(details.isHidden())
        finally:
            window.close()
            window._poll_timer.stop()
            window._blur_timer.stop()
            window.deleteLater()
            app.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            app.processEvents()

    def test_creator_attribution_does_not_open_an_external_profile(self) -> None:
        extras = ast.literal_eval(find_assignment("TEXTOS_EXTRAS"))
        for language, translations in extras.items():
            with self.subTest(language=language):
                self.assertNotRegex(
                    translations["creator_answer"], r"https?://"
                )
        self.assertNotIn("webbrowser", SOURCE.read_text(encoding="utf-8"))

    def test_copilot_session_does_not_load_unrelated_user_configuration(self) -> None:
        create_session = find_method("AplicativoAssistente", "executar_agente")
        call = next(
            node for node in ast.walk(create_session)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "create_session"
        )
        self.assertTrue(
            any(
                keyword.arg == "enable_config_discovery"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is False
                for keyword in call.keywords
            )
        )

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
            "copiar no terminal", "diga isso claramente", "mensagem mais recente",
            "vários pedidos", "Um “sim” autoriza somente a ação",
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
            window._poll_timer.stop()
            window._blur_timer.stop()
            window.deleteLater()
            app.sendPostedEvents(None, QEvent.Type.DeferredDelete)
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
