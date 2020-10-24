import datetime
import threading
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyglet

class ServerChoice(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Server_choice', self)


class NotificationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('NotificationWindow.ui', self)
        # self.FinalTimeEdit.
        self.start_time_set()
        [button.clicked.connect(self.change_hours) for button in self.hours_edit.buttons()]
        [button.clicked.connect(self.change_minuts) for button in self.minuts_edit.buttons()]
        [button.clicked.connect(self.change_seconds) for button in self.seconds_edit.buttons()]


    def start_time_set(self):
        year, month, day, hours, minuts, seconds = datetime.datetime.now().strftime('%Y %m %d %H %M %S').split()
        self.hours.setText(hours)
        self.minuts.setText(minuts)
        self.seconds.setText(str(int(seconds) + 1))

    def change_hours(self):
        if self.sender().text() == '⬆️':
            self.hours.setText(str((int(self.hours.text()) + 1) % 24))
        else:
            self.hours.setText(str((int(self.hours.text()) - 1) % 24))

    def change_minuts(self):
        if self.sender().text() == '⬆️':
            self.minuts.setText(str((int(self.minuts.text()) + 1) % 60))
        else:
            self.minuts.setText(str((int(self.minuts.text()) - 1) % 60))

    def change_seconds(self):
        if self.sender().text() == '⬆️':
            self.seconds.setText(str((int(self.seconds.text()) + 1) % 60))
        else:
            self.seconds.setText(str((int(self.seconds.text()) - 1) % 60))

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.notifications_add.clicked.connect(self.add_notification)
        self.WeAreNumberOne.clicked.connect(self.easter_egg)

    def easter_egg(self):
        easter_music = threading.Thread(target=self.sound_player, args=('WeAreNumberOne.mp3',))

    def sound_player(self, music):
        song = pyglet.media.load(music)
        song.play()
        # soung.volume(0.5)
        pyglet.app.run()


    def add_notification(self):
        self.new_ex = NotificationWindow()
        self.new_ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec_())