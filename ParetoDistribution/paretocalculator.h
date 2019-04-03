#ifndef PARETOCALCULATOR_H
#define PARETOCALCULATOR_H

#include <QObject>
#include <QVector>
#include <QList>
#include <QUrl>

class ParetoCalculator : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QStringList words READ words NOTIFY wordsChanged)
    Q_PROPERTY(QVariantList mus READ mus NOTIFY musChanged)
    Q_PROPERTY(QVariantList vs READ vs NOTIFY vsChanged)

public:
    explicit ParetoCalculator(QObject *parent = nullptr);

    void resetData();

    const QStringList& words() const { return m_words; }
    const QVariantList& mus() const { return m_mus; }
    const QVariantList& vs() const { return m_vs; }

public slots:
    bool loadDataFromFiles(QList<QUrl> fileNames);
    void buildDistribution();
    void rebuildDistributionWithoutTail();
    QPointF getNearestPoint(QPointF point);
    QString getNearestPointName(QPointF point);

signals:
    void wordsChanged(const QStringList& words);
    void musChanged(const QVariantList& mus);
    void vsChanged(const QVariantList& vs);

private:
    QString m_processData {};

    QStringList m_words {};
    QVariantList m_mus {};
    QVariantList m_vs {};

    QVector<QPair<QString, int>> m_setOfWords;

private:
    void processSetOfWords();
};


#endif // PARETOCALCULATOR_H
