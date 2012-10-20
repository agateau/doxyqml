/*
 *   Copyright 2012 Aurélien Gâteau <agateau@kde.org>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License as
 *   published by the Free Software Foundation; either version 2, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Library General Public License for more details
 *
 *   You should have received a copy of the GNU Library General Public
 *   License along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

import QtQuick 1.1
import org.kde.plasma.components 0.1 as PlasmaComponents
import org.kde.plasma.core 0.1 as PlasmaCore
import org.kde.homerun.fixes 0.1 as HomerunFixes

Item {
    id: main

    //- Defined by outside world -----------------------------------
    property QtObject sourceRegistry

    /// type:list<string> SourceIds used for this page
    property variant sources
    property bool configureMode

    property string searchCriteria

    //- Read-write properties --------------------------------------
    property bool showHeader: true

    //- Read-only properties ---------------------------------------
    // Defined for pages with a single view on a browsable model
    property QtObject pathModel: sourcesModel.count == 1 ? sourcesModel.get(0).model.pathModel : null

    function foo() {}

    signal sourcesUpdated(variant sources)
    signal closeRequested()
    signal openSourceRequested(string source)

    anchors.fill: parent

    //- Non visual elements ----------------------------------------
    ListModel {
        id: sourcesModel
    }

    //- Components -------------------------------------------------
    // Filter components
    Component {
        id: genericFilterComponent
        HomerunFixes.SortFilterModel {
            filterRegExp: main.searchCriteria
            property string name: sourceModel.name
            property int count: sourceModel.count

            property bool running: "running" in sourceModel ? sourceModel.running : false
            property QtObject pathModel: "pathModel" in sourceModel ? sourceModel.pathModel : null

            function trigger(index) {
                var sourceIndex = mapRowToSource(index);
                return sourceModel.trigger(sourceIndex);
            }

        }
    }

    Component {
        id: queryBindingComponent
        Binding {
            property: "query"
            value: main.searchCriteria
        }
    }

    // UI components
    Component {
        id: resultsViewComponent
        ResultsView {
            id: view
            width: parent.width
            configureMode: main.configureMode
            onIndexClicked: {
                handleTriggerResult(model.trigger(index));
            }
            onCurrentItemChanged: main.scrollToItem(currentItem)
        }
    }

    Component {
        id: multiResultsViewComponent
        Column {
            id: multiMain
            width: parent.width
            property alias model: repeater.model
            property bool showHeader

            property bool modelNeedsFiltering: false
            property variant favoriteModels

            // Expose the same focus API as ResultsView. Used when focus changes
            // from a single ResultsView source to a multi ResultsView source
            // and vice-versa
            signal focusOtherViewRequested(int key, int x)

            function focusLastItem() {
                lastView().focusLastItem();
            }

            function focusFirstItem() {
                firstView().focusFirstItem();
            }

            function focusLastItemAtX(x) {
                lastView().focusLastItemAtX(x);
            }

            function focusFirstItemAtX(x) {
                firstView().focusFirstItemAtX(x);
            }

            function isEmpty() {
                for (var idx = 0; idx < repeater.count; ++idx) {
                    if (!repeater.itemAt(idx).isEmpty()) {
                        return false;
                    }
                }
                return true;
            }

            Repeater {
                id: repeater
                delegate: ResultsView {
                    width: multiMain.width
                    configureMode: main.configureMode

                    model: multiMain.modelNeedsFiltering
                        ? createFilterForModel(repeater.model.modelForRow(index))
                        : repeater.model.modelForRow(index)
                    favoriteModels: multiMain.favoriteModels

                    onIndexClicked: {
                        handleTriggerResult(model.trigger(index));
                    }

                    onFocusOtherViewRequested: {
                        if (!main.navigate(repeater, index, key, x)) {
                            // No view matches, forward the request
                            multiMain.focusOtherViewRequested(key, x);
                        }
                    }

                    onCurrentItemChanged: main.scrollToItem(currentItem)
                }

                function viewAt(idx) {
                    return itemAt(idx);
                }

                onItemAdded: main.updateFocus()
            }

            function firstView() {
                return repeater.itemAt(0);
            }

            function lastView() {
                return repeater.itemAt(repeater.count - 1);
            }
        }
    }

    //- UI ---------------------------------------------------------
    PlasmaComponents.BusyIndicator {
        id: busyIndicator
        anchors {
            horizontalCenter: parent.horizontalCenter
        }
        y: 12

        opacity: running ? 0.5 : 0
    }

    ListView {
        id: availableSourcesView
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
        }
        width: configureMode ? parent.width * 0.2 : 0
        opacity: configureMode ? 1 : 0
        Behavior on width { NumberAnimation {} }
        Behavior on opacity { NumberAnimation {} }

        model: HomerunFixes.SortFilterModel {
            sourceModel: sourceRegistry.availableSourcesModel()
            sortRole: "display"
        }

        delegate: PlasmaComponents.Button {
            width: parent.width - 24
            text: model.display
            onClicked: {
                addSource(model.sourceId);
                main.updateSources();
            }
        }

        PlasmaCore.SvgItem {
            anchors {
                right: parent.right
                rightMargin: 12
                top: parent.top
                bottom: parent.bottom
            }
            width: naturalSize.width
            z: 1000
            svg: PlasmaCore.Svg {
                imagePath: "widgets/scrollwidget"
            }
            elementId: "border-right"
        }
    }

    Flickable {
        id: centralFlickable
        anchors {
            top: parent.top
            bottom: parent.bottom
            left: availableSourcesView.right
            right: scrollBar.left
        }
        clip: true
        contentHeight: centralColumn.height

        Column {
            id: centralColumn
            width: parent.width

            Repeater {
                id: repeater
                model: sourcesModel
                delegate: SourceItem {
                    id: editorMain
                    width: parent ? parent.width : 0
                    configureMode: main.configureMode
                    sourceRegistry: main.sourceRegistry
                    sourceId: model.sourceId
                    property QtObject view

                    onRemoveRequested: {
                        sourcesModel.remove(model.index);
                        main.updateSources();
                    }
                    onMoveRequested: {
                        sourcesModel.move(model.index, model.index + delta, 1);
                        main.updateSources();
                    }

                    onSourceIdChanged: {
                        model.model.destroy();
                        view.destroy();
                        var newModel = createModelForSource(sourceId, main);
                        sourcesModel.setProperty(model.index, "sourceId", sourceId);
                        sourcesModel.setProperty(model.index, "model", newModel);
                        view = createView(model.model, editorMain);
                        main.updateSources();
                    }

                    Component.onCompleted: {
                        view = createView(model.model, editorMain);
                        main.updateRunning();
                    }

                    function navigate(key, x) {
                        main.navigate(repeater, model.index, key, x);
                    }
                }

                function viewAt(idx) {
                    return itemAt(idx).view;
                }

                onItemAdded: main.updateFocus()
            }
        }
    }

    PlasmaComponents.ScrollBar {
        id: scrollBar
        flickableItem: centralFlickable
        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }
    }

    Behavior on opacity {
        NumberAnimation {
            duration: 200
        }
    }

    Component.onCompleted: {
        fillSourcesModel();
        updateFocus();
    }

    onActiveFocusChanged: {
        console.log("onActiveFocusChanged(), activeFocus=" + activeFocus);
        updateFocus();
    }

    //- Code -------------------------------------------------------
    function updateFocus() {
        console.log("Page.qml updateFocus()");
        if (!main.activeFocus) {
            return;
        }
        console.log("Page.qml updateFocus() main.activeFocus");
        if (repeater.count == 0) {
            return;
        }
        console.log("Page.qml updateFocus() repeater.count=" + repeater.count);
        repeater.viewAt(0).focusFirstItem();
    }

    function handleTriggerResult(result) {
        if (result) {
            closeRequested();
        }
    }

    function updateRunning() {
        for (var idx = 0; idx < sourcesModel.count; ++idx) {
            if (sourcesModel.get(idx).model.running) {
                busyIndicator.running = true;
                return;
            }
        }
        busyIndicator.running = false;
    }

    function createFilterForModel(model) {
        if (!model) {
            console.log("createFilterForModel: invalid model");
            return null;
        }
        return genericFilterComponent.createObject(model, {"sourceModel": model});
    }

    function createModelForSource(source, parent) {
        var model = sourceRegistry.createModelForSource(source, parent);
        if (!model) {
            return null;
        }

        if ("openSourceRequested" in model) {
            model.openSourceRequested.connect(main.openSourceRequested);
        }

        if ("query" in model) {
            // Model supports querying itself, bind the search criteria field to its "query" property
            queryBindingComponent.createObject(main, {"target": model});
        }

        if ("runningChanged" in model) {
            model.runningChanged.connect(main.updateRunning);
        }
        return model;
    }

    /**
     * Create a view from a model
     * 
     * @param type:QAbstractItemModel model the model to show in the view
     * @param type:Item parent the item which will be the parent of the view
     */
    function createView(model, parent) {
        var isMultiViewModel = "modelForRow" in model;
        var modelNeedsFiltering = !("query" in model);

        var viewArgs = {};
        viewArgs["favoriteModels"] = sourceRegistry.favoriteModels;
        viewArgs["model"] = model;
        viewArgs["showHeader"] = showHeader;
        if (modelNeedsFiltering) {
            if (isMultiViewModel) {
                viewArgs["modelNeedsFiltering"] = true;
            } else {
                viewArgs["model"] = createFilterForModel(model);
            }
        }

        var component = isMultiViewModel ? multiResultsViewComponent : resultsViewComponent;
        var view = component.createObject(parent, viewArgs);
        view.focusOtherViewRequested.connect(parent.navigate);
        return view;
    }

    function fillSourcesModel() {
        sources.forEach(addSource);
    }

    function updateSources() {
        var lst = new Array();
        for (var idx = 0; idx < sourcesModel.count; ++idx) {
            var item = sourcesModel.get(idx);
            lst.push(item.sourceId);
        }
        sourcesUpdated(lst);
    }

    function addSource(sourceId) {
        var model = createModelForSource(sourceId, main);
        if (!model) {
            console.log("addSource() could not create model for source: " + sourceId);
            return;
        }
        sourcesModel.append({
            sourceId: sourceId,
            model: model,
        });
    }

    function navigate(repeater, currentIdx, key, x) {
        function nextView() {
            for (var idx = currentIdx + 1; idx < repeater.count; ++idx) {
                var view = repeater.viewAt(idx);
                if (!view.isEmpty()) {
                    return view;
                }
            }
            return null;
        }

        function previousView() {
            for (var idx = currentIdx - 1; idx >= 0; --idx) {
                var view = repeater.viewAt(idx);
                if (!view.isEmpty()) {
                    return view;
                }
            }
            return null;
        }
        if (key == Qt.Key_Left) {
            var view = previousView();
            if (view) {
                view.focusLastItem();
                return true;
            }
        } else if (key == Qt.Key_Right) {
            var view = nextView();
            if (view) {
                view.focusFirstItem();
                return true;
            }
        } else if (key == Qt.Key_Up) {
            var view = previousView();
            if (view) {
                view.focusLastItemAtX(x);
                return true;
            }
        } else if (key == Qt.Key_Down) {
            var view = nextView();
            if (view) {
                view.focusFirstItemAtX(x);
                return true;
            }
        }
        return false;
    }

    function scrollToItem(item) {
        if (!item) {
            return;
        }
        var y = centralColumn.mapFromItem(item, 0, 0).y;
        if (y < centralFlickable.contentY) {
            centralFlickable.contentY = y;
        } else if (y + item.height > centralFlickable.contentY + centralFlickable.height) {
            centralFlickable.contentY = y + item.height - centralFlickable.height;
        }
    }
}
