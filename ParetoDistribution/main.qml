import QtQuick 2.12
import QtQuick.Controls 2.5
import QtCharts 2.3
import Qt.labs.platform 1.1 as Labs

ApplicationWindow {
    id: root

    width: 640
    height: 480

    title: qsTr("Pareto Distribution")
    visible: true

    menuBar: MenuBar {
        MenuBarItem {
            text: "File"
            menu: Menu {
                Action {
                    text: "&Open"
                    onTriggered: {
                        _fileDialog.open();
                    }
                }
            }
        }
        MenuBarItem {
            text: "Build graphic"

            onTriggered: {
                _lineSeries.clear();
                paretoCalculator.buildDistribution();
            }

            onHoveredChanged: {
                highlighted = hovered;
            }
        }
        MenuBarItem {
            text: "Without tail"

            onTriggered: {
                _lineSeries.clear();
                paretoCalculator.rebuildDistributionWithoutTail();
            }

            onHoveredChanged: {
                highlighted = hovered;
            }
        }
        MenuBarItem {
            text: "Clear graphic"

            onTriggered: {
                _lineSeries.clear();
            }

            onHoveredChanged: {
                highlighted = hovered;
            }
        }
    }

    Popup {
        id: _popup

        property alias text: _label.text

        anchors.centerIn: Overlay.overlay

        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        width: parent.width / 2
        height: parent.height / 2

        Label {
            id: _label

            anchors.centerIn: parent

            fontSizeMode: Text.Fit
            minimumPixelSize: 10
            font.pixelSize: 24
        }

    }

    Labs.FileDialog {
        id: _fileDialog

        fileMode: Labs.FileDialog.OpenFiles

        onAccepted: {
            if (!paretoCalculator.loadDataFromFiles(_fileDialog.files)) {
                _popup.text = "Coudn't open file(s)";
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

        onEmptyData: {
            _popup.text = "Empty data!";
            _popup.open();
        }
    }
}
