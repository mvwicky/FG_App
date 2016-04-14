import os
import sys
import shutil
import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from DataManager import DataManager
from Plotter import Plotter
from logger import Logger

try:
    test = QString('Test')
except NameError:
    QString = str


class Window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.log = Logger('Window')
        self.dim = (850, 500)

        self.data_manager = DataManager()
        self.data_manager.get_id_name_tups()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FG App')

        grid = QGridLayout()

        r = grid.rowCount()

        pitcher_button = QPushButton('Pitchers')
        batter_button = QPushButton('Batters')
        per_game_button = QPushButton('Per Game Graph', self)
        cum_avg_button = QPushButton('Cumulative Average Graph', self)

        self.player_select = QComboBox(self)
        self.stat_select = QComboBox(self)

        pitcher_button.connect(pitcher_button, SIGNAL('clicked()'),
                               self.pop_players)
        batter_button.connect(batter_button, SIGNAL('clicked()'),
                              self.pop_players)

        per_game_button.connect(per_game_button, SIGNAL('clicked()'),
                                self.make_per_game)
        cum_avg_button.connect(cum_avg_button, SIGNAL('clicked()'),
                               self.make_cum_avg)

        grid.addWidget(pitcher_button, 0, 0)
        grid.addWidget(batter_button, 0, 1)

        grid.addWidget(self.player_select, 1, 0)
        grid.addWidget(self.stat_select, 2, 0)

        grid.addWidget(per_game_button, 2, 1)
        grid.addWidget(cum_avg_button, 2, 2)

        self.mainWidget = QWidget(self)
        self.mainWidget.setLayout(grid)
        self.setCentralWidget(self.mainWidget)

        self.resize(*self.dim)
        self.center()

        self.log('Opening')
        self.show()

    def closeEvent(self, event):
        self.log('Closing')
        event.accept()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clean(self, csv=True, graph=True):
        pass

    def clean_logs(self):
        for file in os.listdir():
            if file.endswith('.log'):
                file_path = os.path.join(os.getcwd(), file)
                os.unlink(file_path)

    def pop_players(self):
        pass

    def pop_stats(self):
        pass

    def make_per_game(self):
        pass

    def make_cum_avg(self):
        pass


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
