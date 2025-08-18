import mediapipe as mp
import sys
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QHBoxLayout, QSizePolicy, QStackedWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot
import psutil
import auth
from blink_detector import BlinkDetector
from datetime import datetime

class LoginScreen(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.init_ui()
 
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.user_label = QLabel("Username")
        self.user_label.setStyleSheet("color: white;")
        self.user_input = QLineEdit()
        self.user_input.setStyleSheet("background: #222; color: white; border: 1px solid #444;")
        self.pass_label = QLabel("Password")
        self.pass_label.setStyleSheet("color: white;")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("background: #222; color: white; border: 1px solid #444;")
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background: #444; color: white;")
        self.login_btn.clicked.connect(self.handle_login)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.setStyleSheet("background #111;")
        self.consent_checkbox = QCheckBox("I consent to data collection (GDPR)")
        self.consent_checkbox.setStyleSheet("color: white;")
        layout.addWidget(self.consent_checkbox)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()
        consent = self.consent_checkbox.isChecked()
        token = auth.cloud_authenticate(username, password, )
        if token:
            self.on_login(username, token, consent)
        else:
            self.user_input.clear()
            self.pass_input.clear()
            self.user_label.setText("Username (Try Again)")
            self.user_label.setStyleSheet("color: red;")
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
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background: #111;")
        self.stack = QStackedWidget()
        self.login_screen = LoginScreen(self.login_success)
        self.main_screen = MainScreen()
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.main_screen)
        self.setCentralWidget(self.stack)
        self.token = None

        self.blink_thread = None
        self.blink_count = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def login_success(self, username, token, consent):
        self.token = token
        self.consent = consent
        self.stack.setCurrentWidget(self.main_screen)
        self.start_blink_detection()

    def start_blink_detection(self):
        self.blink_thread = BlinkThread()
        self.blink_thread.blink_count_signal.connect(self.update_blink_count)
        self.blink_thread.start()

    @pyqtSlot(int)
    def update_blink_count(self, count):
        self.blink_count = count
        self.main_screen.blink_label.setText(f"Blinks: {self.blink_count}")
        if self.token:
            success = auth.post_blink_data(self.token, count)
            if not success:
                auth.cache_blink_data({"blink_count": count, "timestamp": datetime.now().isoformat()})
            else:
                auth.sync_cached_blinks(self.token)


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
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())