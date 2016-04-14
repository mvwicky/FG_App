import os
import csv

import CSV_Gen

from logger import Logger


class DataManager(object):
    def __init__(self):
        self.log = Logger('DataManager')

        self.csv_gen = CSV_Gen.CSV_Gen()

        self.id_name_tups = {'pit': [],
                             'bat': []}
        self.log('Data Manager created')
        self.csv_gen.init_info_csv()

    def names(self, cat):
        if cat not in ('pit', 'bat'):
            self.log('Category is not pitchers or batters')
            return False

    def get_id_name_tups(self, pit=True, bat=True):
        if not (pit or bat):
            self.log('Not getting any ids')
            return False
        elif not (pit and bat):
            p_type = 'pit' if pit else 'bat'
            tups = []
            file_path = self.csv_gen.info_path[p_type]
            if not os.path.exists(file_path):
                self.log('{} info file does not exist, fetching'
                         .format('Pitching' if pit else 'Batting'))
                self.csv_gen.init_info_csv(pit, bat)
            with open(file_path, 'rt', newline='\n') as file:
                for row in file:
                    if row.startswith('ID#'):
                        continue
                    row = row.replace('"', '')
                    row = row.replace('\r', '').replace('\n', '')
                    fields = row.replace('"', '').split(',')
                    tups.append((int(fields[0]), fields[1]))
                    self.id_name_tups[p_type] = tups
                return tups
        elif pit and bat:
            pit_id = self.get_id_name_tups(True, False)
            bat_id = self.get_id_name_tups(False, True)
            return {'pit': pit_id,
                    'bat': bat_id}

    def get_player_type(self, player):
        # modify to get where the player player most
        if type(player) == str:
            if player in self.ids['pit'].keys():
                return 'pit'
            if player in self.ids['bat'].keys():
                return 'bat'
        elif type(player) == int:
            if player in self.ids['pit'].values():
                return 'pit'
            if player in self.ids['bat'].values():
                return 'bat'
        self.log('Getting player type failed, exiting',
                 ex=True)

    def get_player_info_tup(self, player):
        p_type = self.get_player_type(player)
        if type(player) == str:
            p_id = self.ids[p_type][player]
            p_name = player
        elif type(player) == int:
            p_id = player
            p_name = None
            for p in self.ids[p_type]:
                if self.ids[p_type][p] == p_id:
                    p_name = p
                    break
        return (p_id, p_name, self.get_player_type(player))

    def get_in_both(self, player):
        if type(player) == str:
            in_pit = player in self.ids['pit'].keys()
            in_bat = player in self.ids['bat'].keys()
        elif type(player) == int:
            in_pit = player in self.ids['pit'].values()
            in_bat = player in self.ids['bat'].values()
        else:
            self.log('Determining if player in both lists failed, exiting',
                     ex=True)
        return in_pit and in_bat

    def get_stats(self, p_type):
        if p_type not in ('pit', 'bat'):
            self.log('Invalid player type')
            return 'Could not get stats'
        else:
            stat_file = self.csv_gen.game_log_stat_types()[p_type]
            with open(stat_file, 'rt', newline='\n') as file:
                for row in file:
                    row = row.replace('"', '')
                    row = row.replace('\r', '').replace('\n', '')
                    fields = row.replace('"', '').split(',')
                    return fields


def main():
    pass

if __name__ == '__main__':
    main()
