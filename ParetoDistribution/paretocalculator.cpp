#include "paretocalculator.h"
#include <QFile>
#include <QDebug>
#include <math.h>

ParetoCalculator::ParetoCalculator(QObject *parent)
    : QObject(parent)
    , m_processData("")
{
}

bool ParetoCalculator::loadDataFromFiles(const QStringList& fileNames)
{
    bool isAnythingExists = false;

    for (auto fileName : fileNames)
    {
        QFile file(fileName);
        qDebug() << fileName;
        if ((file.exists()) && (file.open(QIODevice::ReadOnly)))
        {
            isAnythingExists = true;
            m_processData += file.readAll() + " ";
            file.close();
        }
        else
        {
            qDebug() << "Cannot open the file " << fileName;
        }
    }

    return isAnythingExists;
}

void ParetoCalculator::buildDistribution()
{
    QString preparedStr = m_processData.remove(QRegExp("[,.!?-\"\r\n]"));

    QStringList words = preparedStr.split(" ");
    QMap<QString, int> dict;

    for (int i(0); i < words.size(); ++i)
    {
        dict[words[i].toLower()]++;
    }

    QVector<QPair<QString, int>> setOfWords;
    for (auto it = dict.begin(); it != dict.end(); ++it)
    {
        setOfWords.push_back(qMakePair(it.key(), it.value()));
    }

    const int C = words.size();
    const int N = setOfWords.size();

    qSort(setOfWords.begin(), setOfWords.end(), [] (QPair<QString, int> a, QPair<QString, int> b)
    {
        return a.second > b.second;
    });

    auto gammaCalculator = [] (float mu, float v) -> float
    {
        return 1 - (std::log(mu) / std::log(v));
    };

    // process
    int sum = 0;
    for (int i(0); i < N; ++i)
    {
        sum += setOfWords[i].second;
        const float mu = float(sum) / C;
        const float v = float(i + 1) / N;

        // internal keeping
        m_words.append(setOfWords[i].first);
        m_mus.push_back(mu);
        m_vs.push_back(v);

//        qDebug() << "sum = " << sum << " MU = " << mu << " v = " << v << " g = " << gammaCalculator(mu, v);
    }
}
