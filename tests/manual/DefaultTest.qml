import QtQuick 1.0

Item {
    /**
     * Content to show in this item
     */
    default property alias content: col.data

    Column {
        id: col
    }
}
