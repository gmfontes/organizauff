import sys, json
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot, QUrl

from src.reader import read_subjects_csv

# ---------- caminhos ----------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "database.csv"
HTML_PATH = BASE_DIR / "src" / "styles" / "index.html"

# ---------- backend exposto ao JS ----------
class Backend(QObject):
    def __init__(self, subjects_by_period):
        super().__init__()
        self.data = subjects_by_period

    @Slot(result=str)
    def getSubjects(self):
        return json.dumps(self.data, ensure_ascii=False)

# ---------- prepara dados ----------
subjects = read_subjects_csv(CSV_PATH)

periods = {}
for code, occurrences in subjects.items():
    for i, subj in enumerate(occurrences):
        period = subj["period"]
        periods.setdefault(period, []).append({
            "id": f"{code}_{i}",
            "code": code,
            "name": subj["name"]
        })

# ---------- app ----------
app = QApplication(sys.argv)

view = QWebEngineView()
channel = QWebChannel()
backend = Backend(periods)

channel.registerObject("backend", backend)
view.page().setWebChannel(channel)

view.load(QUrl.fromLocalFile(str(HTML_PATH)))
view.resize(1400, 900)
view.show()

sys.exit(app.exec())
