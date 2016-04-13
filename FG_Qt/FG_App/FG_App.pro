#-------------------------------------------------
#
# Project created by QtCreator 2016-04-12T17:17:06
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = FG_App
TEMPLATE = app


SOURCES += main.cpp\
        fg_window.cpp \
    fg_parser.cpp \
    fg_plotter.cpp \
    logger.cpp

HEADERS  += fg_window.h \
    fg_parser.h \
    fg_plotter.h \
    logger.h

FORMS    += fg_window.ui
