#ifndef FG_WINDOW_H
#define FG_WINDOW_H

#include <utility>

#include <QMainWindow>
#include <QString>
#include <QComboBox>

#include "logger.h"
#include "fg_parser.h"
#include "fg_plotter.h"

namespace Ui {
class FG_Window;
}

class FG_Window : public QMainWindow
{
    Q_OBJECT

public:
    explicit FG_Window(QWidget *parent = 0);
    ~FG_Window();

    void clean();
    void clean_logs();
    void look_for_csv();
    void populate_players();
    void populate_stats();

    void make_per_game(QString);
    void make_per_game(int);

    void make_cum_sum(QString);
    void make_cum_sum(int);

private:
    Ui::FG_Window *ui;

    std::pair<int, int> dim;
    QString csv_dir;
    QString graph_dir;
    logger log;
    fg_parser parser;
};

#endif // FG_WINDOW_H
