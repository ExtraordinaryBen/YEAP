import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from apng import *
from Icons import *
import os.path
import ffmpeg

APP_NAME = "YEAP"
DEFAULT_DELAY = 100


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QMetaType.type("QItemSelection")
        self.setWindowTitle(APP_NAME)
        self.icons = Icons()
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        #self.setMinimumSize(500, 350)
        self.resize(500, 350)
        #self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        #Top ToolBar
        self.tb = self.addToolBar("Menu")
        self.tb.setMovable(False)
        self.tb.setContextMenuPolicy(Qt.PreventContextMenu)

        self.newAction = QAction(self.icons.New, "New", self)
        self.tb.addAction(self.newAction)
        self.newAction.triggered.connect(self.main_widget.newAnimation)
        self.newAction.setEnabled(False)

        self.openAction = QAction(self.icons.Open, "Open", self)
        self.tb.addAction(self.openAction)
        self.openAction.triggered.connect(self.main_widget.openAnimation)

        self.appendAction = QAction(self.icons.Append, "Append", self)
        self.tb.addAction(self.appendAction)
        self.appendAction.triggered.connect(self.main_widget.appendAnimation)
        self.appendAction.setEnabled(False)

        self.saveAction = QAction(self.icons.Save, "Save", self)
        self.tb.addAction(self.saveAction)
        self.saveAction.triggered.connect(self.main_widget.saveAnimation)
        self.saveAction.setEnabled(False)

        self.saveAsAction = QAction(self.icons.SaveAs, "SaveAs", self)
        self.tb.addAction(self.saveAsAction)
        self.saveAsAction.triggered.connect(self.main_widget.saveAsAnimation)
        self.saveAsAction.setEnabled(False)

        self.exportMP4Action = QAction(self.icons.Movie, "Export to MP4", self)
        self.tb.addAction(self.exportMP4Action)
        self.exportMP4Action.triggered.connect(self.main_widget.exportAnimation)
        self.exportMP4Action.setEnabled(False)

        self.tb.addWidget(SpacerWidget())

        #self.undoAction = QAction(self.icons.Undo, "Undo", self)
        #self.tb.addAction(self.undoAction)
        #self.undoAction.triggered.connect(self.main_widget.undoLastAction)
        #self.undoAction.setEnabled(False)

        self.copyAction = QAction(self.icons.Copy, "Copy", self)
        self.tb.addAction(self.copyAction)
        self.copyAction.triggered.connect(self.main_widget.copyFrame)
        self.copyAction.setEnabled(False)

        self.pasteAction = QAction(self.icons.Paste, "Paste", self)
        self.tb.addAction(self.pasteAction)
        self.pasteAction.triggered.connect(self.main_widget.pasteFrame)
        self.pasteAction.setEnabled(False)

        self.deleteAction = QAction(self.icons.Delete, "Delete", self)
        self.tb.addAction(self.deleteAction)
        self.deleteAction.triggered.connect(self.main_widget.deleteFrames)
        self.deleteAction.setEnabled(False)

        self.tb.addSeparator()

        self.optionsMenu = QMenu("Options", self)
        self.hideListAction = QAction("Hide Frame Reel", self.optionsMenu)
        self.hideListAction.setCheckable(True)
        self.hideListAction.triggered.connect(self.main_widget.toggleList)
        self.optionsMenu.addAction(self.hideListAction)

        self.optionButton = QToolButton(self)
        self.optionButton.setPopupMode(QToolButton.InstantPopup)
        self.optionButton.setFocusPolicy(Qt.NoFocus)
        self.optionButton.setIcon(self.icons.Options)
        self.optionButton.setMenu(self.optionsMenu)
        self.tb.addWidget(self.optionButton)
        #self.optionsMenu.triggered.connect()

        #Bottom ToolBar
        self.tb2 = QToolBar("PlayerControls")
        self.tb2.setMovable(False)
        self.tb2.setContextMenuPolicy(Qt.PreventContextMenu)

        self.tb2.addWidget(SpacerWidget())

        self.startAction = QAction(self.icons.Start, "First Frame", self)
        self.startAction.setEnabled(False)
        self.tb2.addAction(self.startAction)
        self.startAction.triggered.connect(self.main_widget.firstFrame)

        self.backAction = QAction(self.icons.Back, "Back Frame", self)
        self.backAction.setEnabled(False)
        self.tb2.addAction(self.backAction)
        self.backAction.triggered.connect(self.main_widget.backFrame)

        self.playBeginningAction = QAction(self.icons.PlayBeginning, "Play from Beginning", self)
        self.playBeginningAction.setEnabled(False)
        self.tb2.addAction(self.playBeginningAction)
        self.playBeginningAction.triggered.connect(self.main_widget.playBeginningAnimation)

        self.playAction = QAction(self.icons.Play, "Play", self)
        self.playAction.setEnabled(False)
        self.tb2.addAction(self.playAction)
        self.playAction.triggered.connect(self.main_widget.playCurrentAnimation)

        self.stopAction = QAction(self.icons.Stop, "Stop", self)
        self.stopAction.setEnabled(False)
        self.tb2.addAction(self.stopAction)
        self.stopAction.triggered.connect(self.main_widget.stopPlaying)

        self.loopAction = QAction(self.icons.Loop, "Loop", self)
        self.loopAction.setEnabled(False)
        self.loopAction.setCheckable(True)
        self.loopAction.triggered.connect(self.main_widget.ChangesMade)
        self.tb2.addAction(self.loopAction)

        self.nextAction = QAction(self.icons.Next, "Next Frame", self)
        self.nextAction.setEnabled(False)
        self.tb2.addAction(self.nextAction)
        self.nextAction.triggered.connect(self.main_widget.nextFrame)

        self.endAction = QAction(self.icons.End, "Last Frame", self)
        self.endAction.setEnabled(False)
        self.tb2.addAction(self.endAction)
        self.endAction.triggered.connect(self.main_widget.lastFrame)

        self.tb2.addWidget(SpacerWidget())

        self.dw = DelayWidget(self.tb)
        self.dw.delayLine.valueChanged.connect(self.main_widget.delay_handler)
        self.tb2.addWidget(self.dw)

        self.addToolBar(Qt.BottomToolBarArea, self.tb2)

        self.center()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def enableTopToolBar(self):
        self.newAction.setEnabled(True)
        self.openAction.setEnabled(True)
        self.appendAction.setEnabled(True)
        #self.saveAction.setEnabled(True)
        #self.main_widget.CheckForChanges()
        self.saveAsAction.setEnabled(True)
        self.exportMP4Action.setEnabled(True)
        self.copyAction.setEnabled(True)
        self.deleteAction.setEnabled(True)

    def DisableTopToolBar(self):
        self.newAction.setEnabled(False)
        self.openAction.setEnabled(False)
        self.appendAction.setEnabled(False)
        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.exportMP4Action.setEnabled(False)
        self.copyAction.setEnabled(False)
        self.pasteAction.setEnabled(False)
        self.deleteAction.setEnabled(False)

    def PlayerToolBarPlayMode(self):
        self.startAction.setEnabled(False)
        self.backAction.setEnabled(False)
        self.playAction.setEnabled(False)
        self.playBeginningAction.setEnabled(False)
        self.stopAction.setEnabled(True)
        self.nextAction.setEnabled(False)
        self.endAction.setEnabled(False)
        self.dw.delayLine.setEnabled(False)

    def PlayerToolBarEditMode(self):
        self.startAction.setEnabled(True)
        self.backAction.setEnabled(True)
        self.playAction.setEnabled(True)
        self.playBeginningAction.setEnabled(True)
        self.stopAction.setEnabled(False)
        self.loopAction.setEnabled(True)
        self.nextAction.setEnabled(True)
        self.endAction.setEnabled(True)
        self.dw.delayLine.setEnabled(True)

    def PlayerToolBarDisable(self):
        self.startAction.setEnabled(False)
        self.backAction.setEnabled(False)
        self.playAction.setEnabled(False)
        self.playBeginningAction.setEnabled(False)
        self.stopAction.setEnabled(False)
        self.loopAction.setEnabled(False)
        self.nextAction.setEnabled(False)
        self.endAction.setEnabled(False)
        self.dw.delayLine.setEnabled(False)

    def closeEvent(self, event):
        if self.saveAction.isEnabled():
            event.ignore()
            result = QMessageBox.question(self, "Unsaved Changes",
                "Do you want to save changes before quitting?",
                QMessageBox.Cancel | QMessageBox.Save | QMessageBox.Discard, QMessageBox.Save)

            if result != QMessageBox.Cancel:
                if result == QMessageBox.Save:
                    self.main_widget.saveAnimation()
                event.accept()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        #self.setStyleSheet("background-color:red;")
        self.layout = QHBoxLayout(self)
        self.frameView = QLabel(self)
        self.frameView.setMinimumSize(300, 300)
        self.layout.addStretch()
        self.layout.addWidget(self.frameView)
        self.layout.addStretch()
        self.list = FrameList(self)
        self.list.currentItemChanged.connect(self.frame_change)
        self.list.itemSelectionChanged.connect(self.check_selection)
        #self.list.setFocusPolicy(Qt.NoFocus)

        self.layout.addWidget(self.list)

        self.cb = QApplication.clipboard()
        self.cb.dataChanged.connect(self.cb_handler)

        self.timer = QTimer()
        self.playing = False

        self.setLayout(self.layout)

    def firstFrame(self):
        self.list.setCurrentRow(0, QItemSelectionModel.ClearAndSelect)

    def backFrame(self):
        curRow = self.list.currentRow()
        if curRow > 0:
            self.list.setCurrentRow(curRow - 1, QItemSelectionModel.ClearAndSelect)

    def nextFrame(self):
        curRow = self.list.currentRow()
        if curRow < self.list.count() - 1:
            self.list.setCurrentRow(curRow + 1, QItemSelectionModel.ClearAndSelect)
            return True
        else:
            return False

    def lastFrame(self):
        self.list.setCurrentRow(self.list.count() - 1, QItemSelectionModel.ClearAndSelect)

    def advanceFrame(self):
        if self.playing is True:
            if self.nextFrame():
                self.timer.singleShot(self.list.currentItem().delay, self.advanceFrame)
            elif (self.list.currentRow() == self.list.count() - 1) and (
                    self.parent().loopAction.isChecked()):
                self.firstFrame()
                self.timer.singleShot(self.list.currentItem().delay, self.advanceFrame)
            else:
                self.stopPlaying()

    def checkIfAnimationSaved(self, message):
        if self.parent().saveAction.isEnabled():
            result = QMessageBox.question(self, "Unsaved Changes",
            "Do you want to save changes before " + message + "?",
            QMessageBox.Cancel | QMessageBox.Save | QMessageBox.Discard, QMessageBox.Save)

            if result == QMessageBox.Cancel:
                return False
            elif result == QMessageBox.Save:
                self.saveAnimation()
                return True

        return True

    def newAnimation(self):
        if not self.checkIfAnimationSaved("creating a new animation"):
            return

        self.list.clear()
        self.list.filename = ""
        self.frameView.clear()
        self.parent().PlayerToolBarDisable()
        self.parent().saveAction.setEnabled(False)
        self.parent().saveAsAction.setEnabled(False)
        self.parent().exportMP4Action.setEnabled(False)
        self.parent().appendAction.setEnabled(False)
        self.parent().dw.delayLine.setValue(DEFAULT_DELAY)
        self.parent().setWindowTitle(APP_NAME)

    def appendAnimation(self):
        filenames = QFileDialog.getOpenFileNames(self, "Select file(s) to Append", "", "Images (*.apng *.png *.jpg)")
        if filenames:
            print("filenames:", filenames)
            for filename in filenames:
                self.openFile(filename)
        self.ChangesMade()

    def openAnimation(self):
        if not self.checkIfAnimationSaved("opening an animation"):
            return

        filenames = QFileDialog.getOpenFileNames(self, "Open file(s)", "", "Images (*.apng *.png *.jpg)")
        if filenames:
            print("filenames:", filenames)
            self.list.clear()
            self.frameView.clear()
            for filename in filenames:
                self.openFile(filename)

    def openFile(self, filename):
        #To-Do: Add JPG support
        self.setFilename(filename)
        im = APNG().open(filename)
        if im.num_plays == 0:
            self.parent().loopAction.setChecked(True)
        for i, (png, control) in enumerate(im.frames):
            px = QPixmap()
            px.loadFromData(png.to_bytes())
            if control:
                item = FrameItem(px, control.delay * (1000 // control.delay_den))
            else:
                item = FrameItem(px, DEFAULT_DELAY)
            self.list.addItem(item)

        self.firstFrame()
        self.list.update()
        self.parent().enableTopToolBar()
        self.parent().saveAction.setEnabled(False)
        self.parent().PlayerToolBarEditMode()

    def setFilename(self, name):
        self.list.filename = name
        self.parent().setWindowTitle(APP_NAME + " - " + os.path.basename(name))

    def saveAnimation(self):
        if self.list.filename:
            self.saveFile(self.list.filename)
        else:
            self.saveAsAnimation()

    def saveAsAnimation(self):
        if self.list.count() > 0:
            filename, ext = QFileDialog.getSaveFileNameAndFilter(self, "Save file", "", "*.png;;*.apng")
            if filename:
                ext = ext[1:]
                print("filename:", filename, "Type: " + ext)
                if ext not in filename:
                    filename += ext
                self.saveFile(filename)

    def saveFile(self, filename):
        if filename:
            im = APNG()
            if self.parent().loopAction.isChecked():
                im.num_plays = 0
            else:
                im.num_plays = 1

            for i in range(0, self.list.count()):
                byteArray = QByteArray()
                buf = QBuffer(byteArray)
                self.list.item(i).frame.save(buf, "PNG")
                png = MyPNG.from_bytes(byteArray.data())
                #png.save("save{i}.png".format(i=i))
                im.append(png, delay=self.list.item(i).delay)

            im.save(filename)
            self.setFilename(filename)
            self.parent().saveAction.setEnabled(False)

    def exportAnimation(self):
        if not self.checkIfAnimationSaved("exporting"):
            return

        filename, ext = QFileDialog.getSaveFileNameAndFilter(self, "Save file", ".mp4", "*.mp4")
        if filename:
            ext = ext[1:]
            print("filename:", filename, "Type: " + ext)
            if ext not in filename:
                filename += ext
            print("new filename", filename)
            (ffmpeg
                .input(self.list.filename)
                .output(filename, pix_fmt='yuv420p',
                    tune='animation', vf='scale=trunc(iw/2)*2:trunc(ih/2)*2')
                .overwrite_output()
                .run()
            )

    def playBeginningAnimation(self):
        self.list.setCurrentRow(0)
        self.playAnimation()

    def playCurrentAnimation(self):
        if(self.list.currentRow() == self.list.count() - 1):
            self.list.setCurrentRow(0)
        self.playAnimation()

    def playAnimation(self):
        self.playing = True
        self.parent().PlayerToolBarPlayMode()
        self.parent().DisableTopToolBar()
        self.list.setEnabled(False)
        self.timer.singleShot(self.list.currentItem().delay, self.advanceFrame)

    def stopPlaying(self):
        self.timer.stop()
        self.parent().enableTopToolBar()
        self.parent().PlayerToolBarEditMode()
        self.list.setEnabled(True)
        self.parent().dw.delayLine.setEnabled(True)
        self.playing = False
        self.CheckForChanges()

    def cb_handler(self):
        print("Clipboard data changed!")
        if self.cb.mimeData().hasImage():
            self.parent().pasteAction.setEnabled(True)
        else:
            self.parent().pasteAction.setEnabled(False)

    def delay_handler(self, newValue):
        if self.list.count() > 0 and newValue != self.list.currentItem().delay:
            self.list.currentItem().delay = newValue
            self.ChangesMade()
            print("New delay", self.list.currentItem().delay)

    def copyFrame(self):
        if self.list.currentItem() is not None:
                toCopy = self.list.currentItem().frame
                self.cb.setPixmap(toCopy)
                print("Sent to clipboard!", toCopy)
        else:
            print("Nothing currently selected???")

    def pasteFrame(self):
        print("Paste-to!")

        for selectedItem in self.list.selectedItems():
            self.list.setItemSelected(selectedItem, False)

        item = FrameItem(self.cb.pixmap())
        self.list.insertItem(self.list.currentRow() + 1, item)
        self.list.setCurrentItem(item)
        self.list.scrollToItem(item)
        self.list.update()
        self.parent().enableTopToolBar()
        self.parent().PlayerToolBarEditMode()
        self.ChangesMade()

    def deleteFrames(self):
        items = self.list.selectedItems()
        if items:
            print("Delete key and something selected!!!")
            for item in items:
                if self.list.count() == 1:
                    return
                row = self.list.row(item)
                self.list.takeItem(row)
                if row >= self.list.count():
                    row -= 1

            self.list.setCurrentRow(row)
            self.list.scrollToItem(self.list.currentItem())
            self.list.update()
            self.ChangesMade()
            if self.list.count() == 0:
                self.frameView.clear()
                self.parent().PlayerToolBarDisable()

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste) and (event.isAutoRepeat() is False
            and self.parent().pasteAction.isEnabled()):
            self.pasteFrame()

        elif event.matches(QKeySequence.Copy):
            self.copyFrame()

        elif event.matches(QKeySequence.Cut):
            if self.list.currentItem() is not None:
                print("Cut key and something selected!!!")

        elif event.matches(QKeySequence.Save) and self.parent().saveAction.isEnabled():
            if self.list.filename:
                print("Save key and something open!!!")
                self.saveAnimation()
            else:
                print("Save key and something new!!!")
                self.saveAsAnimation()


        elif event.matches(QKeySequence.Delete):
            self.deleteFrames()

    def frame_change(self, current, previous):
        if current is not None:
            self.frameView.setPixmap(current.frame)
            self.frameView.setMinimumSize(current.frame.width(), current.frame.height())
            self.parent().dw.delayLine.setValue(current.delay)

    def check_selection(self):
        if self.list.selectedItems() and self.list.isEnabled():
            self.parent().copyAction.setEnabled(True)
            self.parent().deleteAction.setEnabled(True)
        else:
            self.parent().copyAction.setEnabled(False)
            self.parent().deleteAction.setEnabled(False)

    def ChangesMade(self):
        self.parent().saveAction.setEnabled(True)
        self.CheckForChanges()

    def CheckForChanges(self):
        if not self.parent().saveAction.isEnabled() and "*" in self.parent().windowTitle():
            self.parent().saveAction.setEnabled(True)

        elif self.parent().saveAction.isEnabled() and "*" not in self.parent().windowTitle():
            self.parent().setWindowTitle(self.parent().windowTitle() + "*")

    def toggleList(self, checked):
        if checked:
            self.list.hide()
        else:
            self.list.show()


class FrameList(QListWidget):
    def __init__(self, parent=None):
        super(FrameList, self).__init__(parent)
        self.setFixedWidth(150)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        self.filename = ""
        #self.setViewMode(QListWidget.IconMode)
        self.setFlow(QListWidget.TopToBottom)
        self.setWrapping(False)
        self.setIconSize(QSize(80, 80))
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListView.Static)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        #self.setDragEnabled(True)
        #self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, event):
        super(FrameList, self).dropEvent(event)
        print("Drop event called!")
        self.update()
        self.parent().ChangesMade()

    def update(self):
        for i in range(0, self.count()):
                    self.item(i).setText(str(i + 1))


class FrameItem(QListWidgetItem):
    def __init__(self, pixmap, delay=100, parent=None):
        super(FrameItem, self).__init__(parent)
        self.frame = pixmap
        self.setIcon(QIcon(self.frame))
        self.setSizeHint(QSize(100, 100))
        self.delay = delay
        self.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)


class DelayWidget(QWidget):
    def __init__(self, image, parent=None):
        super(DelayWidget, self).__init__(parent)
        #self.setContentsMargins(0, 0, 0, 0)
        hlayout = QHBoxLayout(self)
        hlayout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Delay:", self)
        label.setFixedWidth(50)
        ms = QLabel("ms", self)
        ms.setFixedWidth(30)

        self.delayLine = QSpinBox(self)
        self.delayLine.setRange(1, 9999)
        self.delayLine.setValue(100)
        self.delayLine.setSingleStep(5)
        self.delayLine.setEnabled(False)
        #validator = QIntValidator(1, 9999, self)
        #self.delayLine.setValidator(validator)
        self.delayLine.setFixedWidth(70)

        hlayout.addWidget(label, 0, Qt.AlignLeft)
        hlayout.addWidget(self.delayLine, 0, Qt.AlignLeft)
        hlayout.addWidget(ms, 0, Qt.AlignLeft)

        self.setLayout(hlayout)


class SpacerWidget(QWidget):
    def __init__(self, parent=None):
        super(SpacerWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: purple")


class MyPNG(PNG):
    def __init__(self):
        super(MyPNG, self).__init__()

    @classmethod
    def from_bytes(cls, b):
        png = super(MyPNG, cls).from_bytes(b)
        png.chunks[:] = [x for x in png.chunks if x[0] != "pHYs" and x[0] != "sBIT"]
        return png


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
