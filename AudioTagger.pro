#-------------------------------------------------
#
# Project created by QtCreator 2019-05-27T16:26:18
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = AudioTagger
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0


SOURCES += \
        run.py \
        AudioTagger/shortcuts_dialog.py

FORMS += \
    AudioTagger/gui/audio_tagger.ui \
    AudioTagger/gui/selection_list.ui \
    AudioTagger/gui/tag_dialog.ui \
    AudioTagger/gui/manage_related_dialog.ui \
    AudioTagger/gui/spectrogram_options.ui \
    AudioTagger/gui/shortcuts_dialog.ui \
    AudioTagger/gui/shortcuts_dialog2.ui

RESOURCES += \
    resources.qrc

TRANSLATIONS = AudioTagger/lang/en_GB.ts AudioTagger/lang/fr_FR.ts
