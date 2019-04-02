#include <QApplication>
#include <QQmlContext>
#include <QQmlApplicationEngine>

#include "paretocalculator.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QApplication app(argc, argv);

    ParetoCalculator paretoCalculator;

    QQmlApplicationEngine engine;

    engine.rootContext()->setContextProperty("paretoCalculator", &paretoCalculator);

    engine.load(QStringLiteral("qrc:/main.qml"));

    return app.exec();
}
