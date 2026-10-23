"""Orange3 전용 스크립트가 Orange 파이썬에서 돌도록 맞춰 주는 공통 도우미.

프로젝트 파이썬(`python`)에는 Orange가 없다. Orange 3.35 설치본에 딸린 파이썬으로 다시 실행한다.
- 환경변수 ORANGE_PYTHON이 있으면 그 경로를, 없으면 이 PC의 기본 설치 경로를 쓴다.
- 화면 없이 위젯을 만들 수 있게 QT_QPA_PLATFORM=offscreen을 기본값으로 둔다.
"""
import os
import subprocess
import sys

DEFAULT_ORANGE_PYTHON = r"C:/Users/PC/AppData/Local/Programs/Orange/python.exe"
ORANGE_VERSION = "3.35.0"


def orange_python():
    return os.environ.get("ORANGE_PYTHON", DEFAULT_ORANGE_PYTHON)


def ensure_orange_python(script_path):
    """Orange를 import할 수 없으면 Orange 파이썬으로 같은 스크립트를 다시 실행하고 종료한다."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        import Orange  # noqa: F401
        import orangecanvas  # noqa: F401
        isolate_widget_settings()
        return
    except ImportError:
        pass
    exe = orange_python()
    if not os.path.exists(exe):
        print(f"[오류] Orange 파이썬을 찾을 수 없습니다: {exe}\n"
              f"       Orange {ORANGE_VERSION}을 설치하거나 환경변수 ORANGE_PYTHON에 python.exe 경로를 지정하세요.")
        sys.exit(2)
    sys.exit(subprocess.call([exe, os.path.abspath(script_path), *sys.argv[1:]]))


_SETTINGS_DIR = None


def isolate_widget_settings():
    """위젯 설정 기본값·문맥(context)을 실행마다 새 임시 폴더에 두게 한다.

    Orange 위젯은 바꾼 설정과 '이 열 구성에서는 이 설정'이라는 문맥을 사용자 폴더(%LOCALAPPDATA%\\python\\...\\widgets)에
    저장하고, 다음에 같은 열 구성의 데이터가 들어오면 새 위젯에도 그 설정을 되살린다. 그러면 빌드 스크립트가 지정한
    설정(예: Impute 합격여부 = Remove rows)이 다음 실측의 '새 위젯'에 몰래 섞인다(2026-10-23 실제로 105/107 측정이 엇갈림).
    위젯 클래스를 import하기 전에 불러야 한다."""
    global _SETTINGS_DIR
    if _SETTINGS_DIR is None:
        import tempfile
        from orangewidget.settings import set_widget_settings_dir_components
        _SETTINGS_DIR = tempfile.mkdtemp(prefix="orange-course-widget-settings-")
        set_widget_settings_dir_components(_SETTINGS_DIR, "isolated")
    return _SETTINGS_DIR


def check_orange_version():
    import Orange.version
    if Orange.version.short_version != ORANGE_VERSION:
        print(f"[주의] Orange {Orange.version.short_version}에서 실행 중입니다. 이 과정은 {ORANGE_VERSION} 기준입니다.")


def widget_registry():
    """Orange 캔버스와 같은 방식으로 위젯 레지스트리를 만든다."""
    from orangecanvas.registry import WidgetRegistry
    from Orange.canvas import config
    cfg = config.Config()
    reg = WidgetRegistry()
    cfg.widget_discovery(reg).run(cfg.widgets_entry_points())
    return reg
