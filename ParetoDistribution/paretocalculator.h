#ifndef PARETOCALCULATOR_H
#define PARETOCALCULATOR_H

#include <QObject>
#include <QVector>

class ParetoCalculator : public QObject
{
    Q_OBJECT
public:
    explicit ParetoCalculator(QObject *parent = nullptr);

    bool loadDataFromFiles(const QStringList& fileNames);
    void buildDistribution();

    const QStringList& getNames() const { return m_words; }
    const QVector<float>& getMus() const { return m_mus; }
    const QVector<float>& getVs() const { return m_vs; }

private:
    QString m_processData;

    QStringList m_words;
    QVector<float> m_mus;
    QVector<float> m_vs;
};

// !! - Example of using - !!
//#include "paretocalculator.h"

//QStringList fileNames = QFileDialog::getOpenFileNames(this,
//    tr("Open Document"), "", tr("Document Files (*.docx *.txt)"));

//ParetoCalculator calculator;
//const bool isDataPresent = calculator.loadDataFromFiles(fileNames);
//if (isDataPresent)
//{
//    calculator.buildDistribution();

//    //Use calculated data
//    QStringList names = calculator.getNames();
//    QVector<float> mus = calculator.getMus();
//    QVector<float> vs = calculator.getVs();
//}
//else
//{
//    qDebug() << "Prepare data.";
//}

#endif // PARETOCALCULATOR_H
