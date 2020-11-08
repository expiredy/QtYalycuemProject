import datetime
import threading
import sys
import discord
import config
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import pyglet

class ServerChoice(QMainWindow):
    def __init__(self, server):
        super().__init__()
        uic.loadUi('Servers_choice.ui', self)



class Server(QMainWindow):
    def __init__(self, server_at_worked_id):
        super().__init__()
        self.server_at_worked = config.SERVERS_DATA[config.name_of_bot][server_at_worked_id]['server_data']
        uic.loadUi('ServerSetup.ui', self)
        print(self.server_at_worked.name)
        self.setWindowTitle(self.server_at_worked.name)
        self.ExitButton.clicked.connect(self.back)
        self.channels_distribution()


    def channels_distribution(self):
        self.categories = {}
        for category in self.server_at_worked.categories:
            self.categories[category.id] = {}
            label = QLabel(self)
            label.setText(category.name)
            self.layoutWithChannels.addWidget(label)
            for channel in category.channels:
                self.categories[category.id][channel.id] = QPushButton(channel.name, self)
                self.layoutWithChannels.addWidget(self.categories[category.id][channel.id])
                self.categories[category.id][channel.id].clicked.connect(self.channel_settings)
                self.categories[category.id][channel.id].show()

    def channel_settings(self):
        print(self.sender().text())

    def back(self):
        self.close()


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
        self.hours.setText('<strong>' + hours + '<strong>')
        self.minuts.setText('<strong>' + minuts + '<strong>')
        self.seconds.setText('<strong>' + str(int(seconds) + 1) + '<strong>')

    def change_hours(self):
        if self.sender().text() == '🔼':
            self.hours.setText('<strong>' + str((int(self.hours.text().replace('<strong>', ''))
                                                 + 1) % 24) + '<strong>')
        else:
            self.hours.setText('<strong>' + str((int(self.hours.text().replace('<strong>', ''))
                                                 - 1) % 24) + '<strong>')

    def change_minuts(self):
        if self.sender().text() == '🔼':
            self.minuts.setText('<strong>' + str((int(self.minuts.text().replace('<strong>', ''))
                                                  + 1) % 60) + '<strong>')
        else:
            self.minuts.setText('<strong>' + str((int(self.minuts.text().replace('<strong>', ''))
                                                  - 1) % 60) + '<strong>')

    def change_seconds(self):
        if self.sender().text() == '🔼':
            self.seconds.setText('<strong>' + str((int(self.seconds.text().replace('<strong>', ''))
                                                   + 1) % 60) + '<strong>')
        else:
            self.seconds.setText('<strong>' + str((int(self.seconds.text().replace('<strong>', ''))
                                                   - 1) % 60) + '<strong>')

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.add_servers_choice()
        self.notifications_add.clicked.connect(self.add_notification)
        self.WeAreNumberOne.clicked.connect(self.easter_egg)

    def add_servers_choice(self):
        self.buttons_with_servers = {}
        for server_id in list(config.SERVERS_DATA[config.name_of_bot].keys()):
            button_server = QPushButton('\n\n' +
                                        config.SERVERS_DATA[config.name_of_bot][server_id]['server_data'].name
                                        + '\n\n', self)
            button_server.clicked.connect(self.open_server)
            self.layoutWithServers.addWidget(button_server)
            self.buttons_with_servers[server_id] =\
                {'server_data': config.SERVERS_DATA[config.name_of_bot][server_id]['server_data'],
                 'button': button_server}


    def open_server(self):
        for server in list(self.buttons_with_servers.keys()):
            if self.buttons_with_servers[server]['button'] == self.sender():
                print(server)
                self.buttons_with_servers[server]['window'] = Server(server)
                self.buttons_with_servers[server]['window'].show()
                break

    def easter_egg(self):
        easter_music = threading.Thread(target=self.sound_player, args=('WeAreNumberOne.mp3',))
        easter_music.start()

    def sound_player(self, music):
        song = pyglet.media.load(music)
        song.play()
        # soung.volume(0.5)
        pyglet.app.run()


    def add_notification(self):
        self.new_ex = NotificationWindow()
        self.new_ex.show()

def interface_start():
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    interface_start()