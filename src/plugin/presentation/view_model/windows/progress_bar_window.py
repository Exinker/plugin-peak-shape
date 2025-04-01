import os
from collections.abc import Mapping
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

import plugin


class ProgressBarWindow(QtWidgets.QWidget):

    def __init__(
        self,
        *args,
        total: int,
        flags: Mapping[QtCore.Qt.WindowType, bool] | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.total = total

        self.setObjectName('progressWindow')

        # title
        self.setWindowTitle(' '.join(map(lambda x: x.capitalize(), plugin.__name__.split('-'))))

        # flags
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        flags = flags or {
            # QtCore.Qt.WindowType.WindowStaysOnTopHint: True,
            QtCore.Qt.WindowType.WindowCloseButtonHint: False,
            QtCore.Qt.WindowType.Window: True,
        }
        for key, value in flags.items():
            self.setWindowFlag(key, value)

        # style
        filepath = Path().resolve() / 'static' / 'progress-window.css'
        if os.path.exists(filepath):
            style = open(filepath, 'r').read()
            self.setStyleSheet(style)

        # icon
        filepath = Path().resolve() / 'static' / 'icon.ico'
        if os.path.exists(filepath):
            icon = QtGui.QIcon(str(filepath))
            self.setWindowIcon(icon)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(ContentWidget(
            parent=self,
        ))

        # geometry
        self.setFixedSize(QtCore.QSize(680, 200))

        # show window
        self.show()

    def update(self, n: int):

        progress = 100*n/self.total
        widget = self.findChild(QtWidgets.QProgressBar, 'progressBar')
        widget.setValue(progress)

        info = '<strong>PLEASE, WAIT!</strong>'
        widget = self.findChild(QtWidgets.QLabel, 'infoLabel')
        widget.setText(info)

        message = 'RETRIEVE PEAK\'S SHAPE: {n}/{total} is complited!'.format(
            n=n,
            total=self.total,
        )
        widget = self.findChild(QtWidgets.QLabel, 'messageLabel')
        widget.setText(message)

        app = QtWidgets.QApplication.instance()
        app.processEvents()

    def closeEvent(self, event):  # noqa: N802

        self.setParent(None)
        event.accept()


class ContentWidget(QtWidgets.QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('contentWidget')

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addSpacing(50)
        layout.addWidget(LoggingPlainTextEditWidget(
            '',
            parent=self,
        ))
        layout.addWidget(ProgressBarWidget(
            objectName='progressBar',
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='infoLabel',
            text='<strong>LOADING</strong>...',
            parent=self,
        ))
        layout.addWidget(LabelWidget(
            objectName='messageLabel',
            text='',
            parent=self,
        ))
        layout.addSpacing(50)


class LoggingPlainTextEditWidget(QtWidgets.QPlainTextEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('loggingPlainText')
        self.setPlaceholderText('')
        self.setEnabled(False)

        # geometry
        self.setFixedHeight(100)


class ProgressBarWidget(QtWidgets.QProgressBar):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setValue(0)


class LabelWidget(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
