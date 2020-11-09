import interface
import MainBotCode
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtWidgets import QInputDialog
import discord
import AdditionThing
# import threading

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(600, 600, 300, 300)
        self.setWindowTitle('Подключим вашего бота')
        self.Label = QLabel('Ошибочка вышла, попробуйте ещё раз', self)
        self.Label.hide()
        token, ok_pressed = QInputDialog.getText(self, "Введите токен",
                                                "Введите токен вашего бота")
        if ok_pressed:
            try:
                MainBotCode.activate(token)
                self.close()
            except discord.errors.LoginFailure:
                self.error.show()
                AdditiomThing.timer_activate(5, end_func=self.end_this_party)
            except RuntimeError:
                self.error.show()
                AdditiomThing.timer_activate(5, end_func=self.end_this_party)

    def end_this_party(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = StartWindow()
    start.show()
    sys.exit(app.exec_())


# token: Njk5Mzc0OTAzNzQ4NDYwNTY0.XpTdog.TNBffWvyhLfZog5Yt-YnPrnGF9Y)


# bot_code.activate("Njk5Mzc0OTAzNzQ4NDYwNTY0.XpTdog.TNBffWvyhLfZog5Yt-YnPrnGF9Y")