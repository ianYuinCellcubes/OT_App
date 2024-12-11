import sys
from PySide6.QtWidgets import QApplication
from source.OT.Control.mainControl import MainController

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_main_view()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()