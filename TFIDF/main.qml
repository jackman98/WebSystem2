import QtQuick 2.12
import QtQuick.Controls 2.5
import QtCharts 2.3
import QtQuick.Dialogs 1.3

ApplicationWindow {
    id: root

    width: 640
    height: 480

    title: qsTr("TFIDF Distribution")
    visible: true

    menuBar: MenuBar {
        MenuBarItem {
            text: "Build graphic"

            onTriggered: {
                _lineSeries.clear();
                calculator.execute();
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

    FileDialog {
        id: _fileDialog

        selectMultiple: true

        onAccepted: {
            if (!paretoCalculator.loadDataFromFiles(_fileDialog.fileUrls)) {
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

            name: "TFIDF Distribution"

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
            target: calculator

            onWordsChanged: {
                var words = calculator.words;

                var step = 1 / words.length;
                var j = 0;

                for (var i = 0; i < words.length; i++) {
                    console.log(words[i]['key'])
                    _lineSeries.append(words[i]['score'] * 100, j);
                    j = j + step;
                }

//                _mouseArea.enabled = true;
            }

//            onEmptyData: {
//                _popup.text = "Empty data!";
//                _popup.open();
//            }
        }
}
