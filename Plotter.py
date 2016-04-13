import os
import datetime

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from logger import Logger


class Plotter(object):
    def __init__(self, p_tup, stat, year=None):
        self.log = Logger('Plotter')

        self.p_tup = p_tup
        self.stat = stat
        self.year = year

        csv_dir = '{}\\CSV\\'.format(os.getcwd())
        csv_name = '{}_GameLogs_All.csv'.format(self.p_tup[0])
        self.csv_path = '{}{}'.format(self.csv_dir, csv_name)

        self.graph_dir = '{}\\Graphs\\'.format(os.getcwd())
        self.stat_ind = None
        self.cind = None
        self.dates = []
        self.stats = []

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

        with open(self.csv_path, 'rt') as game_logs:
            for row in game_logs:
                fields = row.replace('"', '').split(',')
                if row.startswith('Date'):
                    if self.stat not in fields:
                        self.log('Not a supported stat')
                        self.log('Supported stats are: {}'
                                 .format(fields), ex=True)
                    else:
                        self.stat_ind = fields.index(self.stat)
                        try:
                            self.cind = fields.index('PA')
                        except:
                            self.cind = fields.index('IP')
        self.log('Plotter created for: {}'.format(p_tup[1]))

    def per_game(self):
        with open(self.csv_path, 'rt') as game_logs:
            for row in game_logs:
                if row.startswith('Date') or row.startswith('Total'):
                    continue
                row = row.replace('"', '').replace('%', '')
                fields = row.split(',')
                d = map(int, fields[0].split('-'))
                c_date = datetime.date(*d)
                if self.year and c_date.year == self.year:
                    self.dates.insert(0, c_date)
                    self.stats.insert(0, fields[self.stat_ind])
                elif not self.year:
                    self.dates.insert(0, c_date)
                    self.stats.insert(0, fields[self.stat_ind])
        self.log('Got per game values of {} for {}'
                 .format(self.stat, self.p_tup[1]))
        plt.close()
        plt.plot(dates, self.stats, 'r.')
        plt.title('{} Per Game: {}'.format(self.p_tup[1], self.stat))
        plt.grid()
        file_name = '{}{}PerGame_{}.png'.format(self.graph_dir,
                                                self.p_tup[0],
                                                self.stat)
        self.log('Saving as: {}'.format(file_name))
        plt.savefig(file_name, bbox_inches='tight')
        return file_name

    def cum_avg(self):
        pas = []
        cma = []
        with open(self.csv_path, 'rt') as game_logs:
            for row in game_logs:
                if row.startswith('Date') or row.startswith('Total'):
                    continue
                row = row.replace('"', '').replace('%', '')
                fields = row.split(',')
                d = map(int, fields[0].split('-'))
                c_date = datetime.date(*d)
                try:
                    c_stat = float(fields[self.stat_ind])
                except ValueError:
                    if fields[self.stat_ind] == ' ':
                        self.log('Stat does not exists')
                        return
                if self.year and c_date.year == self.year:
                    dates.insert(0, c_date)
                    stats.insert(0, c_stat)
                    pas.insert(0, fields[self.cind])
                elif not self.year:
                    dates.insert(0, c_date)
                    stats.insert(0, c_stat)
                    pas.insert(0, fields[self.cind])
        p = stats[0]
        for n, s in enumerate(stats):
            if n == 0:
                cma.insert(0, s)
                continue
            p += pas[n]
            cma_n1 = cma[n-1] + (s - cma[n-1]) / p
            cma.append(cma_n1)
        self.log('Got cumulative average of {} for {}'
                 .format(self.stat, self.p_tup[1]))
        plt.close()
        plt.plot(dates, cma, 'r.')
        plt.title('{} Cumulative Average: {}'.format(self.p_tup[1], self.stat))
        plt.grid()
        file_name = '{}{}CumulativeAverage_{}.png'.format(self.graph_dir,
                                                          self.p_tup[0],
                                                          self.stat)
        self.log('Saving as: {}'.format(file_name))
        plt.savefig(file_name, bbox_inches='tight')
        return file_name


def main():
    pass

if __name__ == '__main__':
    main()
