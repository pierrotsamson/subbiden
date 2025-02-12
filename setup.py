from setuptools import setup

APP = ['subbiden.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['whisper', 'torch', 'tkinter', 'librosa'],
    'includes': ['whisper', 'numpy', 'tqdm'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
