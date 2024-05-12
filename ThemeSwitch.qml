import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    width: 200
    height: 100
    color: backgroundRect.color

    property bool isOn: false

    Rectangle {
        id: backgroundRect
        anchors.fill: parent
        radius: 50
        color: isOn ? "#1D1F2C" : "#3D7EAE"
        Behavior on color {
            ColorAnimation { duration: 300 }
        }
    }

    Rectangle {
        id: toggle
        width: 60
        height: 60
        radius: 30
        color: "#FFFFFF"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: isOn ? 130 : 10
        Behavior on anchors.leftMargin {
            NumberAnimation { duration: 300 }
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.isOn = !root.isOn
            }
        }
    }
}
