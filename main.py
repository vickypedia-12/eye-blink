import mediapipe as mp
_ = mp.solutions.hands.Hands
import sys
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QHBoxLayout, QSizePolicy, QStackedWidget, QCheckBox, 
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
import psutil
import auth
from blink_detector import BlinkDetector
from datetime import datetime
import json
 
class LoginScreen(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.init_ui()
 
    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        card = QWidget()
        card.setStyleSheet("""
            background: #222;
            border-radius: 14px;
            padding: 28px 24px 24px 24px;
            min-width: 320px;
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        logo = QLabel()
        logo.setPixmap(QPixmap("image.png").scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo)
        title = QLabel("Blink Tracker Login")
        title.setStyleSheet("color: #fff; font-size: 20px; font-weight: bold; margin-bottom: 14px;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.user_label = QLabel("Username")
        self.user_label.setStyleSheet("color: #ccc; font-size: 13px; margin-top: 8px;")
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("""
            background: #111;
            color: #fff;
            border: 1.2px solid #444;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
        """)
        card_layout.addWidget(self.user_label)
        card_layout.addWidget(self.user_input)

        self.pass_label = QLabel("Password")
        self.pass_label.setStyleSheet("color: #bbb; font-size: 15px; margin-top: 10px;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("""
            background: #111;
            color: #fff;
            border: 1.2px solid #444;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
        """)
        card_layout.addWidget(self.pass_label)
        card_layout.addWidget(self.pass_input)

        self.consent_checkbox = QCheckBox("I consent to data collection (GDPR)")
        self.consent_checkbox.setStyleSheet("""
            color: #bbb;
            font-size: 12px;
            margin-top: 10px;
        """)
        card_layout.addWidget(self.consent_checkbox)

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
            background: #fff;
            color: #111;
            font-size: 14px;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 8px 0;
            margin-top: 14px;
        """)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        outer_layout.addWidget(card)
        self.setStyleSheet("""
            QWidget {
                background: #111;
            }
        """)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        consent = self.consent_checkbox.isChecked()
        try:
            token = auth.cloud_authenticate(username, password)
        except Exception as e:
            self.user_label.setText("No internet connection")
            self.user_label.setStyleSheet("color: #ff5252; font-size: 13px;")
            return
        if token:
            self.on_login(username, token, consent)
        else:
            self.user_input.clear()
            self.pass_input.clear()
            self.user_label.setText("Username (Try Again)")
            self.user_label.setStyleSheet("color: #ff5252; font-size: 13px;")

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.blink_label = QLabel("Blinks: 0")
        self.blink_label.setStyleSheet("color: white; font-size:48px; font-weight: bold;")
        self.blink_label.setAlignment(Qt.AlignCenter)
        self.blink_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        stats_layout = QHBoxLayout()
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet("color: #bbb; font-size: 18px;")
        self.mem_label = QLabel("Memory: 0 MB")
        self.mem_label.setStyleSheet("color: #bbb; font-size: 18px;")
        self.power_label = QLabel("Power: N/A")
        self.power_label.setStyleSheet("color: #bbb; font-size: 18px;")
        stats_layout.addWidget(self.cpu_label)
        stats_layout.addWidget(self.mem_label)
        stats_layout.addWidget(self.power_label)

        main_layout.addWidget(self.blink_label)
        main_layout.addLayout(stats_layout)
        self.setLayout(main_layout)
        self.setStyleSheet("background: #222;")

class BlinkThread(QThread):
    blink_count_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.detector = BlinkDetector()
        self._running = True
    
    def run(self):
        for count in self.detector.run():
            if not self._running:
                break
            self.blink_count_signal.emit(count)

    def stop(self):
        self._running = False
        self.detector.stop()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blink Tracker")
        self.setGeometry(100, 100, 320, 200)
        self.setStyleSheet("background: #111;")
        self.stack = QStackedWidget()
        self.login_screen = LoginScreen(self.login_success)
        self.main_screen = MainScreen()
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.main_screen)
        self.setCentralWidget(self.stack)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.token = None
        self.blink_thread = None
        self.blink_count = 0
        self.last_blink_count = 0
        self.current_minute_blinks = 0
        self.batch_start_time = datetime.now()
        self.batch_timer = QTimer()
        self.batch_timer.timeout.connect(self.send_blink_batch)
        self.batch_timer.start(60000)
        self.token = load_token()
        if self.token:
            self.stack.setCurrentWidget(self.main_screen)
            auth.sync_cached_blinks(self.token)
            self.start_blink_detection()
    
    @pyqtSlot(int)
    def update_blink_count(self,count):
        self.blink_count = count
        self.main_screen.blink_label.setText(f"Blinks: {self.blink_count}")
        if count > self.last_blink_count:
            self.current_minute_blinks += (count - self.last_blink_count)
        self.last_blink_count = count

    def send_blink_batch(self):
        if self.token and self.current_minute_blinks > 0:
            from_time =  self.batch_start_time.replace(microsecond=0).isoformat()
            to_time = datetime.now().replace(microsecond=0).isoformat()
            data = {
                "blink_count": self.current_minute_blinks,
                "from_timestamp": from_time,
                "to_timestamp": to_time,
            }
            print("Sending batch:", data)
            result = auth.post_blink_batch(self.token, data)
            if result == "expired":
                clear_token()
                self.token = None
                self.stack.setCurrentWidget(self.login_screen)
                return
            if not result:
                auth.cache_blink_data(data)
            else:
                sync_result = auth.sync_cached_blinks(self.token)
                if sync_result == "expired":
                    clear_token()
                    self.token = None
                    self.stack.setCurrentWidget(self.login_screen)
                    return
            self.current_minute_blinks = 0
            self.batch_start_time = datetime.now()
        else:
            self.batch_start_time = datetime.now()


    def login_success(self, username, token, consent):
        self.token = token
        self.consent = consent
        save_token(token)
        self.stack.setCurrentWidget(self.main_screen)
        sync_result = auth.sync_cached_blinks(self.token)
        if sync_result == "expired":
            clear_token()
            self.token = None
            self.stack.setCurrentWidget(self.login_screen)
            return
        self.start_blink_detection()

    def start_blink_detection(self):
        self.blink_thread = BlinkThread()
        self.blink_thread.blink_count_signal.connect(self.update_blink_count)
        self.blink_thread.start()

    def update_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().used // (1024 * 1024)
        self.main_screen.cpu_label.setText(f"CPU: {cpu}%")
        self.main_screen.mem_label.setText(f"Memory: {mem} MB")
        self.main_screen.power_label.setText("Power: N/A")

    def closeEvent(self, event):
        if self.blink_thread:
            self.blink_thread.stop()
            self.blink_thread.wait()
        event.accept()
    
def save_token(token):
    with open("token_cache.json", "w") as f:
        json.dump({"token": token}, f)

def load_token():
    try:
        with open("token_cache.json", "r") as f:
            return json.load(f).get("token")
    except Exception:
        return None 
    
def clear_token():
    import os
    try:
        os.remove("token_cache.json")
    except Exception:
        pass
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())