from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, NewType

from PySide6 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backend_bases import KeyEvent, MouseEvent, PickEvent

import plugin
from plugin.config import CONFIG
from spectrumapp.helpers import find_tab, getdefault_object_name
from spectrumapp.widgets.graph_widget import MplCanvas
from spectrumapp.types import Lims


DEFAULT_SIZE = QtCore.QSize(640, 480)
DEFAULT_LIMS = ((0, 1), (0, 1))


Index = NewType('Index', str)


@dataclass
class AxisLabel:
    xlabel: str
    ylabel: str


class BaseGraphWidget(QtWidgets.QWidget):

    def __init__(
        self,
        *args,
        object_name: str | None = None,
        size: QtCore.QSize = DEFAULT_SIZE,
        tight_layout: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._widget_size = size

        self._data = None
        self._point_labels = None
        self._axis_labels = None
        self._point_annotation = None
        self._zoom_region = None
        self._full_lims = None
        self._cropped_lims = None

        # object name
        object_name = object_name or getdefault_object_name(self)
        self.setObjectName(object_name)

        # focus
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()

        # layout and canvas
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.canvas = MplCanvas(
            tight_layout=tight_layout,
        )
        self.canvas.mpl_connect('pick_event', self._pick_event)
        self.canvas.mpl_connect('button_press_event', self._button_press_event)
        self.canvas.mpl_connect('button_release_event', self._button_release_event)
        self.canvas.mpl_connect('motion_notify_event', self._motion_notify_event)
        layout.addWidget(self.canvas)

        # pressed mouse and keys events
        self._mouse_event: MouseEvent | None = None
        self._ctrl_modified = False
        self._shift_modified = False

        # geometry
        self.setFixedSize(self._widget_size)

    @property
    def data(self) -> Mapping[Index, Any] | None:
        return self._data

    @property
    def point_labels(self) -> Mapping[Index, tuple[str, ...]] | None:
        return self._point_labels

    @property
    def axis_labels(self) -> AxisLabel | None:
        return self._axis_labels

    @property
    def default_lims(self) -> Lims:
        return DEFAULT_LIMS

    @property
    def full_lims(self) -> Lims | None:
        return self._full_lims

    @property
    def cropped_lims(self) -> Lims | None:
        return self._cropped_lims

    @property
    def ctrl_modified(self) -> bool:
        return self._ctrl_modified

    @property
    def shift_modified(self) -> bool:
        return self._shift_modified

    def update(self) -> None:

        self.canvas.draw_idle()

    def update_zoom(self, lims: Lims | None = None) -> None:
        """Update zoom to given `lims`."""

        xlim, ylim = lims or self.full_lims or self.default_lims

        self.canvas.axes.set_xlim(xlim)
        self.canvas.axes.set_ylim(ylim)
        self.canvas.draw_idle()

    def set_full_lims(self, lims: Lims) -> None:
        """Set full lims (maximum) to given `lims`."""

        if self._full_lims is None:
            self._full_lims = lims

    def set_cropped_lims(self, lims: Lims | None) -> None:
        """Set cropped lims to given `lims`."""

        self._cropped_lims = lims

    def set_shift_modified(self, __state: bool) -> None:
        self._shift_modified = __state

    def set_ctrl_modified(self, __state: bool) -> None:
        self._ctrl_modified = __state

    def sizeHint(self) -> QtCore.QSize:  # noqa: N802
        return self._widget_size

    def keyPressEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(True)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(True)
            case _:
                return None

    def keyReleaseEvent(self, event: KeyEvent) -> None:  # noqa: N802

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(False)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(False)
            case _:
                return None

    def _pick_event(self, event: PickEvent) -> None:  # pragma: no cover
        return None

    def _button_press_event(self, event: MouseEvent) -> None:  # pragma: no cover
        self._mouse_event = event

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
            return None

        if event.button == 3 and event.dblclick:
            self._mouse_event = None
            self.set_cropped_lims(lims=None)
            self.update_zoom(lims=self.full_lims)

    def _button_release_event(self, event: MouseEvent) -> None:  # pragma: no cover

        # update annotate
        # self._point_annotation.set_visible(False)
        self.canvas.draw_idle()

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
            if event.button == 1:
                self._pan_event(
                    self._mouse_event,
                    event,
                )
            return None

        if event.button == 3:
            self._zoom_event(
                self._mouse_event,
                event,
            )

    def _motion_notify_event(self, event: MouseEvent) -> None:  # pragma: no cover

        # update zoom and pan
        if self.ctrl_modified and self.shift_modified:
            return None

        if self.ctrl_modified:
            return None

        if self.shift_modified:
            if event.button == 1:
                self._pan_event(
                    self._mouse_event,
                    event,
                )
                return None

    def _zoom_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:  # pragma: no cover

        # update full lims
        self.set_full_lims(
            lims=(
                self.canvas.axes.get_xlim(),
                self.canvas.axes.get_ylim(),
            )
        )

        # update crop lims
        xlim = tuple(sorted(
            (event.xdata for event in (press_event, release_event)),
        ))
        ylim = tuple(sorted(
            (event.ydata for event in (press_event, release_event)),
        ))
        self.set_cropped_lims(
            lims=(xlim, ylim),
        )

        # update zoom
        self.update_zoom(
            lims=self.cropped_lims,
        )

    def _pan_event(self, press_event: MouseEvent, release_event: MouseEvent) -> None:  # pragma: no cover

        # update crop lims
        xlim, ylim = self.canvas.axes.get_xlim(), self.canvas.axes.get_ylim()
        xshift, yshift = release_event.xdata - press_event.xdata, release_event.ydata - press_event.ydata
        self.set_cropped_lims(
            lims=(
                [value - xshift for value in xlim],
                [value - yshift for value in ylim],
            ),
        )

        # update zoom
        self.update_zoom(
            lims=self._cropped_lims,
        )

    @property
    def figure(self) -> Figure:
        return self.canvas.figure


class SpectrumViewWidget(BaseGraphWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, size=QtCore.QSize(960, 480), **kwargs)


class ShapeViewWidget(BaseGraphWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, size=QtCore.QSize(480, 480), **kwargs)


class ViewWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.spectrumViewWidget = SpectrumViewWidget()
        layout.addWidget(self.spectrumViewWidget)

        self.shapeViewWidget = ShapeViewWidget()
        layout.addWidget(self.shapeViewWidget)

    @property
    def figures(self) -> Mapping[str, Figure]:

        figures = {
            'spectrum': self.spectrumViewWidget.figure,
            'shape': self.shapeViewWidget.figure,
        }

        return figures

    def update(self) -> None:

        tabWidget = self.parent().parent()  # FIXME
        tabWidget.setCurrentWidget(self)

        self.spectrumViewWidget.update()
        self.shapeViewWidget.update()


class TabViewWidget(QtWidgets.QTabWidget):

    def __init__(
        self,
        *args,
        n_tabs: int,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        for n in range(n_tabs):
            self.addTab(ViewWidget(), self.get_tab_name(n=n))

    @property
    def figures(self) -> Sequence[Mapping[str, Figure]]:

        figures = []
        for n in range(self.count()):
            figures.append(self.widget(n).figures)

        return figures

    def get_tab_name(self, n: int) -> str:
        return 'Detector {n}'.format(
            n=n+1,
        )

    def update(self, n: int) -> None:

        widget = find_tab(self, text=self.get_tab_name(n=n))
        widget.update()


class ViewWindow(QtWidgets.QWidget):

    def __init__(
        self,
        *args,
        n_tabs: int,
        flags: Sequence[QtCore.Qt.WindowType] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setObjectName('progressWindow')

        # title
        self.setWindowTitle(' '.join(map(lambda x: x.capitalize(), plugin.__name__.split('-'))))

        # flags
        flags = flags or (QtCore.Qt.WindowType.Window, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        for flag in flags:
            self.setWindowFlag(flag, True)

        # style
        # filepath = CONFIG.plugin_path / 'static' / 'view-window.css'
        # style = open(filepath, 'r').read()
        # self.setStyleSheet(style)

        # icon
        filepath = CONFIG.plugin_path / 'static' / 'icon.ico'
        icon = QtGui.QIcon(str(filepath))
        self.setWindowIcon(icon)

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.tabWidget = TabViewWidget(
            n_tabs=n_tabs,
        )
        layout.addWidget(self.tabWidget)

        # geometry
        self.setFixedSize(QtCore.QSize(1280, 720))

        # show window
        self.show()

    @property
    def figures(self) -> Sequence[Mapping[str, Figure]]:
        return self.tabWidget.figures

    def update(self, n: int) -> None:

        self.tabWidget.update(
            n=n,
        )

        app = QtWidgets.QApplication.instance()
        app.processEvents()

    def closeEvent(self, event):  # noqa: N802

        self.setParent(None)
        event.accept()
