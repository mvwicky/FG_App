import os
import csv
import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer

from logger import Logger


class CSV_Gen(object):
    def __init__(self):
        self.log = Logger('CSV_Gen', save_dir='logs')
        self.urls = {'leaders': 'http://fangraphs.com/leaders.aspx',
                     'game_logs': 'http://fangraphs.com/statsd.aspx',
                     'play_logs': 'http://fangraphs.com/statsp.aspx'}

        self.info_csv = {'pit': 'PitcherInfo.csv',
                         'bat': 'BatterInfo.csv'}
        self.csv_dir = os.path.abspath('CSV')

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

        self.info_path = {'pit': os.path.join(self.csv_dir,
                                              self.info_csv['pit']),
                          'bat': os.path.join(self.csv_dir,
                                              self.info_csv['bat'])}
        self.log('CSV generator created')

    def init_info_csv(self, pit=True, bat=True, clean=False):
        if not (pit or bat):
            self.log('Getting no ids')
            return
        if not clean:
            if pit and os.path.exists(self.info_path['pit']):
                self.log('Pitcher Info already found in: {}'
                         .format(self.info_path['pit']))
                return self.info_path['pit']
            if bat and os.path.exists(self.info_path['bat']):
                self.log('Batter Info already found in: {}'
                         .format(self.info_path['bat']))
                return self.info_path['bat']
        if not (bat and pit):
            if clean:
                self.log('Cleaning {}er Info csv'
                         .format('pitch' if pit else 'batt'))
            opts = {'pos': 'all', 'lg': 'all', 'qual': 0, 'type': 8,
                    'season': 2016, 'month': 0, 'season1': 1871, 'ind': 0,
                    'team': 0, 'rost': 0, 'age': 0, 'filter': '', 'players': 0,
                    'page': '1_30'}
            opts['stats'] = 'pit' if pit else 'bat'
            self.log('Init {}er info csv'.format('pitch' if pit else 'batt'))
            res = requests.get(self.urls['leaders'], params=opts)
            if res.url.find('error') != -1:
                self.log('Problem getting {}ing leaderboards'
                         .format('pitch' if pit else 'batt'))
                self.log(res.url, ex=True)
            soup = BeautifulSoup(res.content, 'lxml')
            self.log(
                'Successful query, finding number of pages in {} leaderboard'
                .format('pitching' if pit else 'batting'))
            num_pages = 1
            for link in soup('a'):
                if link.get('title') == 'Last Page':
                    href = link.get('href')
                    equals = href.find('=', href.find('page'))
                    uscore = href.find('_', equals)
                    num_pages = href[equals+1:uscore]
                    if num_pages.isnumeric():
                        num_pages = int(num_pages)
                    else:
                        self.log('Problem finding number of pages')
                        self.log('Value found: {}'.format(num_pages), ex=True)
                    break
            self.log('Num pages in {}ing leaderboard: {} '
                     .format('pitch' if pit else 'batt', num_pages))
            ids = dict()
            for page in range(1, num_pages + 1):
                c_page = '{}_30'.format(page)
                opts['page'] = c_page
                res = requests.get(self.urls['leaders'], params=opts)
                if res.url.find('error') != -1:
                    self.log('Problem getting page {} from {}ing leaderboards'
                             .format(page, 'pitch' if pit else 'batt'))
                tbody = SoupStrainer('tbody')
                soup = BeautifulSoup(res.content, 'lxml', parse_only=tbody)
                self.log('Parsing page {} of {} ({}ers leaderboard)'.format(
                    page, num_pages, 'Pitch' if pit else 'Batt'))
                for row in soup('tr'):
                    for cell in row('td'):
                        for child in cell.children:
                            if str(child).find('playerid=') != -1:
                                child = str(child)
                                pid_loc = child.find('playerid')
                                equals = child.find('=', pid_loc)
                                ampers = child.find('&', equals)
                                p_id = child[equals+1:ampers]
                                close_a = child.find('>')
                                open_a = child.find('</', close_a)
                                p_name = child[close_a+1:open_a]
                                ids[p_name] = p_id
            p_type = 'pit' if pit else 'bat'
            self.log('Done parsing')
            with open(self.info_path[p_type], 'w', newline='\n') as csv_file:
                player_writer = csv.writer(csv_file, delimiter=',')
                header = ['ID#', 'Name', 'Primary']
                player_writer.writerow(header)
                for name, i in ids.items():
                    player_writer.writerow([i, name])
            self.log('Info written to: {}'.format(self.info_path[p_type]))
            if bat and pit:
                self.init_info_csv(True, False, clean)
                self.init_info_csv(False, True, clean)

    def player_has_game_logs(self, p_id):
        assert isinstance(p_id, int)
        opts = {'playerid': p_id, 'season': 'all'}
        res = requests.get(self.urls['game_logs'], params=opts)
        if res.url.find('error') != -1:
            return False
        else:
            return True

    def game_log_stat_types(self, pit=True, bat=True):
        if not (pit or bat):
            self.log('Not getting any stat types')
            return None
        if not (pit and bat):
            p_type = 'pit' if pit else 'bat'
            csv_name = '{}_GameLogStatTypes.csv'.format(p_type)
            file_path = os.path.join(self.csv_dir, csv_name)
            if os.path.exists(file_path):
                self.log('File already generated: {}'.format(csv_name))
                return file_path
            with open(self.info_path[p_type], 'rt', newline='\n') as file:
                for row in file:
                    if row.startswith('ID#'):
                        continue
                    row = row.replace('"', '')
                    row = row.replace('\r', '').replace('\n', '')
                    p_tup = (row.split(',')[0], row.split(',')[1])
                    g_log = self.game_logs(p_tup)
                    if g_log:
                        break
            with open(g_log, 'rt') as game_file:
                for row in game_file:
                    row.replace('"', '').replace('\r', '').replace('\n', '')
                    if row.startswith('Date'):
                        fields = row.split(',')
                        if pit:
                            stats = fields[4:]
                        if bat:
                            stats = fields[5:]
            with open(file_path, 'w', newline='\n') as stat_file:
                stat_writer = csv.writer(stat_file, delimiter=',')
                stat_writer.writerow(stats)
            self.log('Stat types written to: {}'.format(csv_name))
            return file_path
        if pit and bat:
            p_file = self.game_log_stat_types(True, False)
            b_file = self.game_log_stat_types(False, True)
            return {'pit': p_file,
                    'bat': b_file}

    def game_logs(self, p_tup, clean=False):
        assert isinstance(p_tup[0], int), isinstance(p_tup[1], str)
        csv_name = '{}_GameLogs_All.csv'.format(p_tup[0])
        file_path = os.path.join(self.csv_dir, csv_name)
        # Make sure that the file does not exist
        if os.path.exists(file_path) and not clean:
            self.log('File already generated: {}'.format(csv_name))
            return file_path
        opts = {'playerid': p_tup[0], 'season': 'all'}
        res = requests.get(self.urls['game_logs'], params=opts)
        if res.url.find('error') != -1:
            self.log('Problem getting game logs for: {}, may not exist'
                     .format(p_tup[1]))
            return False
        self.log('Getting game logs for: {}'.format(p_tup[1]))
        rows = SoupStrainer('tr')
        soup = BeautifulSoup(res.content, 'lxml', parse_only=rows)
        headers = []
        game_stats = []
        for head in soup('th', class_='rgHeader'):
            headers.append(head.text)
        cRow = []
        for cell in soup('td'):
            if cell.get('class'):
                for elem in cell.get('class'):
                    if elem.find('grid_line_') != -1:
                        cRow.append(cell.text)
        if cRow:
            game_stats.append(cRow)
        self.log('Game logs found, writing to csv')
        with open(file_path, 'w', newline='\n') as player_csv:
            player_writer = csv.writer(player_csv, delimiter=',')
            player_writer.writerow(headers)
            for game in game_stats:
                player_writer.writerow(game)
        self.log('Game logs for {} written to: {}'.format(p_tup[1], file_path))
        return file_path

    def play_logs(self, p_tup, clean=False):
        assert isinstance(p_tup[0], int), isinstance(p_tup[1], str)
        csv_name = '{}_PlayLogsAll.csv'.format(p_tup[0])
        file_path = os.path.join(self.csv_dir, csv_name)
        # Make sure that the file does not exist
        if os.path.exists(file_path) and not clean:
            self.log('File already generated: {}'.format(csv_name))
            return file_path
        opts = {'playerid': p_tup[0]}
        res = requests.get(self.urls['play_logs'], params=opts)
        if res.url.find('error') != -1:
            self.log('Problem getting play logs for: {}, may not exist'
                     .format(p_tup[1]))
            return False
        self.log('Getting play logs for: {}'.format(p_tup[1]))
        soup = BeautifulSoup(res.content, 'lxml')
        years = []
        headers = []
        for div in soup('div', id='PlayStats1_tsLog', class_='RadTabStrip'):
            for span in div('span', class_='rtsTxt'):
                if span.text.isnumeric():
                    years.append(int(span.text))
        for head in soup('thead'):
            for col in head('th', class_='rgHeader'):
                headers.append(col.get_text())

        with open(file_name, 'w', newline='\n') as file:
            player_writer = csv.writer(file, delimiter=',')
            player_writer.writerow(headers)

        for year in years:
            opts['season'] = year
            res = requests.get(url, params=opts)
            if res.url.find('error') != -1:
                self.log('Problem getting play logs for: {}, year: {}'
                         .format(p_tup[1], year))
                return file_name
            tbody = SoupStrainer('tbody')
            soup = BeautifulSoup(res.content, 'lxml', parse_only=tbody)
            plays = []
            for row in soup('tr'):
                c_play = []
                for cell in row('td'):
                    if cell.get('class'):
                        for cl in cell.get('class'):
                            if cl.find('grid_line_') != -1:
                                c_play.append(cell.text)
                d = map(int, (('{}/{}'.format(c_play[0], year)).split('/')))
                c_play[0] = datetime.date(d[2], d[0], d[1])
                plays.append(c_play)
            with open(file_path, 'a', newline='\n') as file:
                player_writer = csv.writer(file, delimiter=',')
                dates = []
                for play in plays:
                    player_writer.writerow(play)
        self.log('Play logs for {} written to: {}'.format(p_tup[1], csv_name))
        return file_path


def main():
    pass


if __name__ == '__main__':
    main()
