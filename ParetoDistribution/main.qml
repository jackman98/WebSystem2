import QtQuick 2.12
import QtQuick.Window 2.12
import QtCharts 2.3

Window {
    id: root

    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    property var modelOfWords: ["word1", "word2", "word3", "word4", "word5"]

    ChartView {
        title: "Line"
        anchors.fill: parent
        antialiasing: true

        LineSeries {
            name: "LineSeries"
            axisX: CategoryAxis {

                labelsAngle: 90
                labelsPosition: CategoryAxis.AxisLabelsPositionOnValue

                startValue: 0

                Component.onCompleted: {
                    for (var i = 0; i < root.modelOfWords.length; i++) {
                        append(root.modelOfWords[i], i + 1);
                    }
                }
            }

            XYPoint { x: 0; y: 0 }
            XYPoint { x: 1.1; y: 2.1 }
            XYPoint { x: 1.9; y: 3.3 }
            XYPoint { x: 2.1; y: 2.1 }
            XYPoint { x: 2.9; y: 4.9 }
            XYPoint { x: 3.4; y: 3.0 }
            XYPoint { x: 4.1; y: 3.3 }
            onHovered: console.log("onClicked: " + point.x + ", " + point.y);
        }
    }
}
