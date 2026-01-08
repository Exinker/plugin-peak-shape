import os
import pickle
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from multiprocessing import Queue
from pathlib import Path
from typing import Any, NewType

import matplotlib.pyplot as plt
from PySide6 import QtCore, QtGui, QtWidgets
from matplotlib.backend_bases import KeyEvent, MouseEvent, PickEvent
from matplotlib.figure import Figure

import plugin
from spectrumapp.helpers import find_tab, getdefault_object_name
from spectrumapp.types import Lims
from spectrumapp.widgets.graph_widget import MplCanvas
from spectrumlab.peaks.analyte_peaks.shapes.retrieve_shape import Canvas


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

    def keyPressEvent(  # noqa: N802
        self,
        event: KeyEvent,
    ) -> None:

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(True)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(True)
            case _:
                return None

    def keyReleaseEvent(  # noqa: N802
        self,
        event: KeyEvent,
    ) -> None:

        match event.key():
            case QtCore.Qt.Key.Key_Control:
                self.set_ctrl_modified(False)
            case QtCore.Qt.Key.Key_Shift:
                self.set_shift_modified(False)
            case _:
                return None

    def _pick_event(
        self,
        event: PickEvent,
    ) -> None:  # pragma: no cover
        return None

    def _button_press_event(
        self,
        event: MouseEvent,
    ) -> None:  # pragma: no cover
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

    def _button_release_event(
        self,
        event: MouseEvent,
    ) -> None:  # pragma: no cover

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

    def _motion_notify_event(
        self,
        event: MouseEvent,
    ) -> None:  # pragma: no cover

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

    def _zoom_event(
        self,
        press_event: MouseEvent | None,
        release_event: MouseEvent | None,
    ) -> None:  # pragma: no cover

        if (press_event is None) or (release_event is None):
            return None
        if any(
            getattr(obj, attr) is None
            for obj in [press_event, release_event]
            for attr in ['xdata', 'ydata']
        ):
            return None

        # update full lims
        self.set_full_lims(
            lims=(
                self.canvas.axes.get_xlim(),
                self.canvas.axes.get_ylim(),
            ),
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

    def _pan_event(
        self,
        press_event: MouseEvent | None,
        release_event: MouseEvent | None,
    ) -> None:  # pragma: no cover

        if (press_event is None) or (release_event is None):
            return None
        if any(
            getattr(obj, attr) is None
            for obj in [press_event, release_event]
            for attr in ['xdata', 'ydata']
        ):
            return None

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

        self.spectrum_view_widget = SpectrumViewWidget()
        layout.addWidget(self.spectrum_view_widget)

        self.shape_view_widget = ShapeViewWidget()
        layout.addWidget(self.shape_view_widget)

    @property
    def canvas(self) -> Sequence[Canvas]:

        return tuple([
            self.spectrum_view_widget.canvas,
            self.shape_view_widget.canvas,
        ])

    def update(self) -> None:

        content_widget = self.parent().parent()  # FIXME
        content_widget.setCurrentWidget(self)

        # self.spectrum_view_widget.update()
        # self.shape_view_widget.update()


class ContentWidget(QtWidgets.QTabWidget):

    def __init__(
        self,
        *args,
        indexes: Sequence[int],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.indexes = indexes

        for index in indexes:
            self.addTab(ViewWidget(), self.get_tab_name(index))

    @property
    def canvas(self) -> Sequence[Canvas]:

        canvas = []
        for n in self.indexes:
            canvas.append(self.widget(n).canvas)

        return tuple(canvas)

    def update(self, n: int) -> None:

        widget = find_tab(self, text=self.get_tab_name(n))
        widget.update()

    @staticmethod
    def get_tab_name(__index: int) -> str:

        return ' {n:>2} '.format(
            n=__index + 1,
        )


class ViewerWindow(QtWidgets.QWidget):

    def __init__(
        self,
        *args,
        indexes: Sequence[int],
        queue: Queue,
        flags: Mapping[QtCore.Qt.WindowType, bool] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.setObjectName('progressWindow')

        # title
        self.setWindowTitle(' '.join(map(lambda x: x.capitalize(), plugin.__name__.split('-'))))

        # flags
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)

        flags = flags or {
            # QtCore.Qt.WindowType.WindowStaysOnTopHint: False,
            # QtCore.Qt.WindowType.WindowCloseButtonHint: False,
            QtCore.Qt.WindowType.Window: True,
        }
        for key, value in flags.items():
            self.setWindowFlag(key, value)

        # style
        filepath = Path().resolve() / 'static' / 'view-window.css'
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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.content_widget = ContentWidget(
            indexes=indexes,
        )
        layout.addWidget(self.content_widget)

        # geometry
        self.setFixedSize(self.sizeHint())

        # queue
        self.queue = queue

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

        # show window
        self.show()

    def check_queue(self) -> None:

        while not self.queue.empty():
            n, data = self.queue.get_nowait()
            fig = pickle.loads(data)

            for canvas, axes in zip(self.content_widget.canvas[n], fig.get_axes()):
                _update_axes(canvas.figure.gca(), axes=axes)

                canvas.draw()

            self.update(n)

            plt.close(fig)

    def show(self) -> None:
        super().show()

    def update(self, n: int) -> None:

        self.content_widget.update(
            n=n,
        )

        app = QtWidgets.QApplication.instance()
        app.processEvents()

    def closeEvent(self, event):  # noqa: N802

        self.setParent(None)
        event.accept()


def _update_axes(__ax, axes):

    __ax.clear()

    for line in axes.get_lines():
        __ax.plot(
            line.get_xdata(),
            line.get_ydata(),
            color=line.get_color(),
            linestyle=line.get_linestyle(),
            linewidth=line.get_linewidth(),
            marker=line.get_marker(),
            markersize=line.get_markersize(),
            alpha=line.get_alpha(),
            label=line.get_label(),
        )

    for collection in axes.collections:
        if hasattr(collection, 'get_offsets'):
            offsets = collection.get_offsets()
            if len(offsets) > 0:
                __ax.scatter(
                    offsets[:, 0],
                    offsets[:, 1],
                    c=collection.get_facecolor(),
                    s=collection.get_sizes(),
                    alpha=collection.get_alpha(),
                    label=collection.get_label() if hasattr(collection, 'get_label') else None,
                )

    __ax.set_xlabel(axes.get_xlabel())
    __ax.set_ylabel(axes.get_ylabel())
    __ax.set_title(axes.get_title())
    __ax.set_xlim(axes.get_xlim())
    __ax.set_ylim(axes.get_ylim())

    if axes.get_legend():
        __ax.legend()
