import os
os.environ['PYTHONPATH'] = '.'

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import argparse
import config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Risk Prediction Tool")
    parser.add_argument('--extended', default=False, help="Extended version. Use this option to enable more algorithms.", action='store_true')
    args = parser.parse_args()
    if args.extended:
        config.USE_EXTENDED_ALGORITHMS = True

    app = QApplication(sys.argv)
    app.processEvents()
    css = """
        QPushButton {
            background: #00c8f8;
            color: #fefefe;
            border: 1px solid black;
            padding: 2px 5px;
            border-radius: 4px;
        }
    """
    app.setStyleSheet(css)

    main_win = MainWindow()
    sys.exit(app.exec_())
