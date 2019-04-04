# This Python file uses the following encoding: utf-8
import sys
import tfidf as T
from PyQt5 import QtCore, QtWidgets, QtQuick
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

if __name__ == '__main__':
    app = QtWidgets.QApplication( sys.argv )

    view = QtQuick.QQuickView()

    calculator = T.Calculator()

    view.rootContext().setContextProperty("calculator", calculator)
    view.setSource( QtCore.QUrl( "./WebSystem2/TFIDF/main.qml" ) )
#    view.show()

    sys.exit( app.exec_() )

#if __name__ == "__main__":
#    import sys

#    # создаём экземпляр приложения
#    app = QGuiApplication(sys.argv)
#    # создаём QML движок
#    engine = QQmlApplicationEngine()
#    # создаём объект калькулятора
##    calculator = Calculator()
#    # и регистрируем его в контексте QML
##    engine.rootContext().setContextProperty("calculator", calculator)
#    # загружаем файл qml в движок
#    engine.load("./WebS ystem2/TFIDF/main.qml")

#    engine.quit.connect(app.quit)
#    sys.exit(app.exec_())
