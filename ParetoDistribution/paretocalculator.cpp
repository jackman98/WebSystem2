#include "paretocalculator.h"
#include <QFile>
#include <QDebug>
#include <math.h>

ParetoCalculator::ParetoCalculator(QObject *parent)
    : QObject(parent)
{
}

bool ParetoCalculator::loadDataFromFiles(QList<QUrl> fileNames)
{
    bool isAnythingExists = false;

    for (const auto& fileName : fileNames)
    {
        QString pathToFile = fileName.path();
        QFile file(pathToFile);
        qDebug() << pathToFile;

        if (file.exists() && file.open(QIODevice::ReadOnly))
        {
            isAnythingExists = true;
            m_processData += file.readAll() + " ";
            file.close();
        }
        else
        {
            qDebug() << "Cannot open the file " << pathToFile;
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
    setOfWords.reserve(dict.size());
    for (auto it = dict.begin(); it != dict.end(); ++it)
    {
        setOfWords.push_back(qMakePair(it.key(), it.value()));
    }

    const int C = words.size();
    const int N = setOfWords.size();

    std::sort(setOfWords.begin(), setOfWords.end(), [] (const QPair<QString, int>& a, const QPair<QString, int>& b)
    {
        return a.second > b.second;
    });

    //    auto gammaCalculator = [] (float mu, float v) -> float
    //    {
    //        return 1 - (std::log(mu) / std::log(v));
    //    };

    // process
    m_words.reserve(N);
    m_mus.reserve(N);
    m_vs.reserve(N);

    int sum = 0;

    for (int i(0); i < N; ++i)
    {
        sum += setOfWords[i].second;
        const float MU = float(sum) / C;
        const float V = float(i + 1) / N;

        // internal keeping
        m_words.append(setOfWords[i].first);
        m_mus.push_back(MU);
        m_vs.push_back(V);

        //        qDebug() << "sum = " << sum << " MU = " << MU << " v = " << V << " g = " << gammaCalculator(MU, V);
    }

    emit wordsChanged(m_words);
    emit musChanged(m_mus);
    emit vsChanged(m_vs);
}

QPointF ParetoCalculator::getNearestPoint(QPointF point)
{
    qreal x = m_vs[m_vs.size() - 1].toReal();
    qreal y = m_mus[m_mus.size() - 1].toReal();

    for (int i(0); i < m_vs.size(); ++i)
    {
        if (m_vs[i].toReal() >= point.rx()) {
            x = m_vs[i].toReal();
            break;
        }
    }

    for (int i(0); i < m_mus.size(); ++i)
    {
        if (m_mus[i].toReal() >= point.ry()) {
            y = m_mus[i].toReal();
            break;
        }
    }

    return QPointF(x, y);
}

QString ParetoCalculator::getNearestPointName(QPointF point)
{
    for (int i(0); i < m_words.size(); ++i)
    {
        if (m_vs[i].toReal() >= point.rx()) {
            return m_words[i];
        }
    }

    return m_words[m_words.size() - 1];
}
