#include "fg_window.h"
#include "ui_fg_window.h"


FG_Window::FG_Window(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::FG_Window)
{
    ui->setupUi(this);
}

FG_Window::~FG_Window()
{
    delete ui;
}
