import os
import sys
import youtube_dl

from PyQt5 import QtCore, QtGui, QtWidgets
from des import Ui_MainWindow


class downloader(QtCore.QThread):                           # Класс потока для скачивания

    mysignal = QtCore.pyqtSignal(str)                       # Переменная сигнала

    def __init__(self, parent=None):                        # Конструктор класса
        super().__init__(parent) 
        self.url = None                                     # Переменная для ссылки


    def run(self):                                          # Основной метод
        self.mysignal.emit('Процесс скачивания запущен!')

        #ydl_opts = {'format': 'webm[abr>0]/bestaudio/best'}
        ydl_opts = {}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])                       # Передача ссылки в youtube_dl     

        self.mysignal.emit('Процесс скачивания завершен!')
        self.mysignal.emit('finish')


    def init_args(self, url):                               # Инициализация ссылки 
        self.url = url


class gui(QtWidgets.QMainWindow):                           # Класс интерфейса

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.download_folder = None                         # Путь к папке
        self.ui.pushButton.clicked.connect(self.get_folder) # Кнопка выбора директории
        self.ui.pushButton_2.clicked.connect(self.start)    # Кнопка скачать
        self.mythread = downloader()                        # Экземпляр класса с потоком
        self.mythread.mysignal.connect(self.handler)        # Обработчик сигнала

    
    def start(self):                
        if len(self.ui.lineEdit.text()) > 5:                # Проверка поля с ссылкой
            if self.download_folder != None:                # Проверка директории
                link = self.ui.lineEdit.text()              # Получение текста ссылки
                self.mythread.init_args(link)               # Передача значения ссылки в поток
                self.mythread.start()                       # Запуск основного обработчика
                self.locker(True)                           # Блокировка кнопок
            else:
               QtWidgets.QMessageBox.warning(self, "Ошибка", "Вы не выбрали папку!") 
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ссылка на видео не указана!")


    def get_folder(self):
        self.download_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку для сохранения') 
        os.chdir(self.download_folder)                      # Переход в выбранную папку


    def handler(self, value):
        if value == 'finish':                               # Разблокировка кнопок 
            self.locker(False)

        else:
            self.ui.plainTextEdit.appendPlainText(value)    # Вывод сигнала


    def locker(self, lock_value):
        base = [self.ui.pushButton, self.ui.pushButton_2]   # Список блокируемых кнопок

        for item in base:                                   # Цикл блокировки/разблокировки кнопок
            item.setDisabled(lock_value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = gui()
    win.show()
    sys.exit(app.exec_())