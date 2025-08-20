from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'mediapipe',
        'cv2',
        'numpy',
        'PyQt5',
        'psutil',
    ],
    'includes': [
        'mediapipe.python._framework_bindings',
        'mediapipe.python.solutions.face_mesh',
        'mediapipe.python.solutions.drawing_utils',
        'mediapipe.python.solutions.drawing_styles',
        'mediapipe.python.solutions.face_detection',
        'mediapipe.python.solutions.hands',
        'mediapipe.python.solutions.pose',
    ],
    'resources': [
        # Add any extra files (like .env, icons, etc.) here if needed
    ],
    'plist': {
        'CFBundleName': 'BlinkTracker',
        'CFBundleDisplayName': 'BlinkTracker',
        'CFBundleIdentifier': 'com.yourdomain.blinktracker',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)