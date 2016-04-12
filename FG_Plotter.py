import datetime

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from logger import Logger

class FG_Plotter(object):
	def __init__(self, file_name, p_tup, stat, graph_dir, year=None):
		self.log = Logger('FG_Plotter')
		if not file_name.endswith('.csv'):
			self.log('Input file is not a csv', ex=True)
		self.file_name = file_name
		self.p_tup = p_tup
		self.stat = stat
		self.graph_dir = graph_dir
		self.year = year
		self.stat_ind = None

		if self.file_name.find(str(self.p_tup[0])) == -1:
			self.log('Warning: Input file does not contain input player id, output may be incorrect')

		with open(self.file_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date'):
					if self.stat not in fields:
						self.log('Not a supported stat')
						self.log('Supported stats are: {}'.format(fields), ex=True)
					else:
						self.stat_ind = fields.index(self.stat)

	def per_game(self):
		dates = []
		stats = []
		with open(self.file_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date') or row.startswith('Total'):
					continue
				d = fields[0].split('-')
				c_date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
				if self.year and c_date.year == self.year:
					dates.insert(0, c_date)
					stats.insert(0, fields[self.stat_ind])
				elif not self.year:
					dates.insert(0, c_date)
					stats.insert(0, fields[self.stat_ind])
		self.log('Got per game values of {} for {}'.format(self.stat, self.p_tup[1]))
		plt.close()
		plt.plot(dates, stats, 'r.')
		plt.title('{} Per Game: {}'.format(self.p_tup[1], self.stat))
		plt.grid()
		file_name = '{}{}PerGame_{}.png'.format(self.graph_dir, self.p_tup[0], self.stat)
		self.log('Saving as: {}'.format(file_name))
		plt.savefig(file_name, bbox_inches='tight')
		return file_name

	def cum_avg(self):
		dates = []
		stats = []
		with open(self.file_name, 'rt') as game_logs:
			for row in game_logs:
				fields = row.replace('"', '').split(',')
				if row.startswith('Date') or row.startswith('Total'):
					continue
				d = fields[0].split('-')
				c_date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
				c_stat = float(fields[self.stat_ind])
				if self.year and c_date.year == self.year:
					dates.insert(0, c_date)
					stats.insert(0, c_stat)
				elif not self.year:
					dates.insert(0, c_date)
					stats.insert(0, c_stat)
		cma = []
		for n, s in enumerate(stats):
			if n == 0:
				cma.insert(0, s)
				continue 
			cma_n1 = cma[n-1] + (s - cma[n-1]) / n
			cma.append(cma_n1)
		self.log('Got cumulative average of {} for {}'.format(self.stat, self.p_tup[1]))
		plt.close()
		plt.plot(dates, cma, 'r.')
		plt.title('{} Cumulative Average: {}'.format(self.p_tup[1], self.stat))
		plt.grid()
		file_name = '{}{}CumulativeAverage_{}.png'.format(self.graph_dir, self.p_tup[0], self.stat)
		self.log('Saving as: {}'.format(file_name))
		plt.savefig(file_name, bbox_inches='tight')
		return file_name

def main():
	pass

if __name__=='__main__':
	main()