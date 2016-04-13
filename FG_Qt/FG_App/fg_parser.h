#ifndef FG_PARSER_H
#define FG_PARSER_H

#include <unordered_map>
#include <utility>

#include <QString>

#include "logger.h"

class fg_parser
{
public:
    fg_parser(QString);

    QString get_player_type(QString);
    QString get_player_type(int);

    std::map<QString, int> get_id_name_tup(QString);
    std::map<QString, int> get_id_name_tup(int);

    void get_ids_csv(bool pit=true, bool bat=true);
    void get_ids_web(bool pit=true, bool bat=true);

    QString get_game_logs(QString, bool clean=false);
    QString get_game_logs(int, bool clean=false);

    QString get_play_logs(QString, bool clean=false);
    QString get_play_logs(int, bool clean=false);

private:
    logger log;
    QString csv_dir;
    static QString pitcher_csv;
    static QString batter_csv;

    std::unordered_map<QString, int> pitcher_ids;
    std::unordered_map<QString, int> batter_ids;
};

#endif // FG_PARSER_H
