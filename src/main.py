import sys
import pprint
import argparse
import os
from PyQt5.QtWidgets import QApplication

# Add the interface directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "interface"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))

import main_window

if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = main_window.MainWindow()
    sys.exit(application.exec_())
