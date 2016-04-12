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
		grid = QGridLayout()

		r = grid.rowCount()

		self.parser.get_ids_web()

		self.mainWidget = QWidget(self)
		self.mainWidget.setLayout(grid)
		self.setCentralWidget(self.mainWidget)
		self.resize(*self.dim)
		self.center()
		self.log('Opening')
		self.show()

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
		

def main():
	app = QApplication(sys.argv)
	window = FG_Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()