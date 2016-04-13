import os
import sys
import shutil
import datetime

import requests
from bs4 import BeautifulSoup

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from FG_Parser import FG_Parser
from FG_Plotter import FG_Plotter
from logger import Logger

try:
    test = QString('Test')
except NameError:
    QString = str


class FG_Window(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.dim = (850, 500)

        self.csv_dir = '{}\\CSV\\'.format(os.getcwd())
        self.graph_dir = '{}\\Graphs\\'.format(os.getcwd())

        self.log = Logger('FG_Window')

        if not os.path.exists(self.csv_dir):
            self.log('No CSV directory')
            try:
                os.makedirs(self.csv_dir)
            except:
                self.log('Problem making CSV directory', ex=True)
            else:
                self.log('CSV directory created: {}'.format(self.csv_dir))
        else:
            self.log('CSV directory: {}'.format(self.csv_dir))
        if not os.path.exists(self.graph_dir):
            self.log('No graph directory')
            try:
                os.makedirs(self.graph_dir)
            except:
                self.log('Problem making graph directory', ex=True)
            else:
                self.log('Graph directory created: {}'.format(self.graph_dir))
        else:
            self.log('Graph directory: {}'.format(self.graph_dir))

        self.parser = FG_Parser(self.csv_dir)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FG App')
        self.parser.get_ids_web()
        grid = QGridLayout()

        r = grid.rowCount()

        self.p_label = QLabel('Pitcher CSV: Not Found', self)
        self.b_label = QLabel('Batter CSV: Not Found', self)
        self.look_for_csv()

        grid.addWidget(self.p_label, 0, 0)
        grid.addWidget(self.b_label, 0, 1)

        self.type_select = QComboBox(self)
        self.player_select = QComboBox(self)
        self.stat_select = QComboBox(self)

        grid.addWidget(self.type_select, 2, 0)
        grid.addWidget(self.player_select, 3, 0)
        grid.addWidget(self.stat_select, 4, 0)

        per_game_button = QPushButton('Per Game Graph', self)
        cum_sum_button = QPushButton('Cumulative Sum Graph', self)

        per_game_button.connect(per_game_button, SIGNAL('clicked()'),
                                self.make_per_game)
        cum_sum_button.connect(cum_sum_button, SIGNAL('clicked()'),
                               self.make_cum_sum)
        grid.addWidget(per_game_button, 4, 1)
        grid.addWidget(cum_sum_button, 4, 2)

        self.mainWidget = QWidget(self)
        self.mainWidget.setLayout(grid)
        self.setCentralWidget(self.mainWidget)

        self.resize(*self.dim)
        self.center()

        self.pop_players()
        self.pop_stats()

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
        dirs = []
        if csv:
            dirs.append(self.csv_dir)
        if graph:
            dirs.append(self.graph_dir)
        if not dirs:
            self.log('Not cleaning anything')
            return
        for d in dirs:
            if os.path.exists(d):
                if not os.listdir(d):
                    self.log('Nothing to clean')
                    continue
                for item in os.listdir(d):
                    item_path = os.path.join(d, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                            self.log('Deleted file: {}'.format(item_path))
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            self.log('Deleted folder: {}'.format(item_path))
                    except Exception as e:
                        print(e)
            if os.listdir(d):
                self.log('Problem cleaning: {}'.format(d))
            else:
                self.log('Directory not found: {}'.format(d))
        self.look_for_csv()

    def clean_logs(self):
        for file in os.listdir():
            if file.endswith('.log'):
                file_path = os.path.join(os.getcwd(), file)
                os.unlink(file_path)

    def look_for_csv(self):
        pitcher_csv = self.parser.pitcher_csv
        batter_csv = self.parser.batter_csv
        if pitcher_csv in os.listdir(self.csv_dir):
            self.p_label.setText('Pitcher CSV: Found')
        else:
            self.p_label.setText('Pitcher CSV: Not Found')
        if batter_csv in os.listdir(self.csv_dir):
            self.b_label.setText('Batter CSV: Found')
        else:
            self.p_label.setText('Batter CSV: Not Found')

    def pop_players(self):
        pass

    def pop_stats(self, player=None):
        if player:
            p_type = self.parser.get_player_type(player)

    def make_per_game(self):
        name = self.sender().text()
        file_name = self.parser.get_game_logs(name)
        p_tup = self.parser.get_id_name_tup(name)
        p = FG_Plotter(file_name, p_tup, 'wOBA', self.graph_dir)
        p.per_game()

    def make_cum_sum(self):
        name = self.sender().text()
        file_name = self.parser.get_game_logs(name)
        p_tup = self.parser.get_id_name_tup(name)
        p = FG_Plotter(file_name, p_tup, 'wOBA', self.graph_dir)
        p.cum_sum()


def main():
    app = QApplication(sys.argv)
    window = FG_Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
