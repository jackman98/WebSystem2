import QtQuick 2.12
import QtQuick.Controls 2.5
import QtCharts 2.3
import QtQuick.Dialogs 1.3

ApplicationWindow {
    id: root

    width: 640
    height: 480

    title: qsTr("Pareto Distribution")
    visible: true

    menuBar: MenuBar {
        Menu {
            title: "File"
            Action {
                text: "&Open"
                onTriggered: {
                    _fileDialog.open();
                }
            }
        }
    }

    FileDialog {
        id: _fileDialog

        selectMultiple: true

        onAccepted: {
            if (paretoCalculator.loadDataFromFiles(_fileDialog.fileUrls)) {
                paretoCalculator.buildDistribution();
                // TODO need to call after reset the visual data
//                paretoCalculator.rebuildDistributionWithoutTail();
            }
        }
    }


    ChartView {
        id: _chartView

        anchors.fill: parent

        animationOptions: ChartView.AllAnimations
        antialiasing: true

        Label {
            id: _word
        }

        LineSeries {
            id: _lineSeries

            name: "Pareto Distribution"

            pointsVisible: true
        }

        MouseArea {
            id: _mouseArea

            anchors.fill: parent

            hoverEnabled: true
            enabled: false

            onMouseXChanged: {
                var pointIntoChartView = mapToItem(_chartView, mouseX, mouseY);

                var value = _chartView.mapToValue(pointIntoChartView, _lineSeries);

                _word.x = pointIntoChartView.x + 10;
                _word.y = pointIntoChartView.y + 10;

                _word.text = paretoCalculator.getNearestPointName(value);
            }
        }
    }

    Connections {
        target: paretoCalculator

        onWordsChanged: {
            for (var i = 0; i < words.length; i++) {
                _lineSeries.append(paretoCalculator.vs[i], paretoCalculator.mus[i]);
            }
            _mouseArea.enabled = true;
        }
    }
}
