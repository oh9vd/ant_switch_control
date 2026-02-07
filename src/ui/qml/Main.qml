import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: root
    width: 520
    height: 85
    visible: true
    title: appTitle
    component ToggleButton: Button {
        checkable: true
        width: 37
    }

    Column {
        anchors.centerIn: parent
        spacing: 1
        width: parent.width * 0.9

        Row {
            spacing: 8
            width: parent.width

            CheckBox {
                id: cbAutoA
                text: qsTr("Auto")
                enabled: !rbA0.checked
            }

            ButtonGroup {
                buttons: aRow.children
                exclusive: true
            }

            Row {
                id: aRow
                spacing: 6

                ToggleButton {
                    id: rbA0
                    text: qsTr("OFF")
                    enabled: true
                    onClicked: {
                        if (rbA0.checked) {
                            cbAutoA.checked = false;
                        }
                    }
                }

                ToggleButton {
                    id: rbA1
                    text: qsTr("1")
                    enabled: !rbB1.checked && !cbAutoA.checked
                }

                ToggleButton {
                    id: rbA2
                    text: qsTr("2")
                    enabled: !rbB2.checked && !cbAutoA.checked
                }

                ToggleButton {
                    id: rbA3
                    text: qsTr("3")
                    enabled: !rbB3.checked && !cbAutoA.checked
                }

                ToggleButton {
                    id: rbA4
                    text: qsTr("4")
                    enabled: !rbB4.checked && !cbAutoA.checked
                }

                ToggleButton {
                    id: rbA5
                    text: qsTr("5")
                    enabled: !rbB5.checked && !cbAutoA.checked
                }

                ToggleButton {
                    id: rbA6
                    text: qsTr("6")
                    enabled: !rbB6.checked && !cbAutoA.checked
                }
            }

            Label {
                id: lblRigA
                text: qsTr("A")
                font.bold: true
                horizontalAlignment: Text.AlignLeft
                width: 40
            }

            Label {
                id: lblRigAFreq
                horizontalAlignment: Text.AlignLeft
                width: 40
            }
        }

        Row {
            spacing: 8
            width: parent.width

            CheckBox {
                id: cbAutoB
                text: qsTr("Auto")
                enabled: !rbB0.checked
            }

            ButtonGroup {
                buttons: bRow.children
                exclusive: true
            }

            Row {
                id: bRow
                spacing: 6

                ToggleButton {
                    id: rbB0
                    text: qsTr("OFF")
                    enabled: true
                    onClicked: {
                        if (rbB0.checked) {
                            cbAutoB.checked = false;
                        }
                    }
                }

                ToggleButton {
                    id: rbB1
                    text: qsTr("1")
                    enabled: !rbA1.checked && !cbAutoB.checked
                }

                ToggleButton {
                    id: rbB2
                    text: qsTr("2")
                    enabled: !rbA2.checked && !cbAutoB.checked
                }

                ToggleButton {
                    id: rbB3
                    text: qsTr("3")
                    enabled: !rbA3.checked && !cbAutoB.checked
                }

                ToggleButton {
                    id: rbB4
                    text: qsTr("4")
                    enabled: !rbA4.checked && !cbAutoB.checked
                }

                ToggleButton {
                    id: rbB5
                    text: qsTr("5")
                    enabled: !rbA5.checked && !cbAutoB.checked
                }

                ToggleButton {
                    id: rbB6
                    text: qsTr("6")
                    enabled: !rbA6.checked && !cbAutoB.checked
                }
            }

            Label {
                id: lblRigB
                text: qsTr("B")
                horizontalAlignment: Text.AlignLeft
                width: 40
                font.bold: true
            }

            Label {
                id: lblRigBFreq
                horizontalAlignment: Text.AlignLeft
                width: 40
            }
        }
    }
    footer: ToolBar {
        height: 20
        Row {
            spacing: 8
            width: parent.width * 0.9
            Label {
                id: lblStatus
                text: "Status "
            }
            Label {
                id: lblVersion
                text: "Version " + appVersion
            }
        }
    }
}
