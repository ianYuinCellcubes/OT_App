import sys
from PySide6.QtWidgets import QApplication
from source.player.Control.mainControl import MainController

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_main_view()
    controller.show_sub_view()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
