# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from abc import abstractmethod

from PySide6.QtCore import (
    Qt,
    QPoint,
    QRectF,
)
from PySide6.QtGui import (
    QAction,
    QPen,
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
)

from .constants import (
    OCCURRENCE_PEN_COLOR,
    OCCURRENCE_BG_COLOR,
    OCCURRENCE_PEN_WIDTH_ON_CURSOR,
    OCCURRENCE_PEN_WIDTH_OFF_CURSOR,
    OCCURRENCE_HANDLE_WIDTH,
    OCCURRENCE_HANDLE_HEIGHT_FRACTION,
    TIMELINE_HEIGHT,
    TIMELINE_TITLE_HEIGHT,
)
from .event import ChooseEvent
from .textedit import TextEdit
from .utils import color_fg_from_bg


class Occurrence(QGraphicsRectItem):

    def __init__(
        self,
        timeline,
        begin_time: int,
        end_time: int,
    ):
        """Initializes the Occurrence widget"""
        super().__init__(timeline)
        self.brush_color = OCCURRENCE_BG_COLOR
        self.pen_color = OCCURRENCE_PEN_COLOR
        self.pen_width = OCCURRENCE_PEN_WIDTH_OFF_CURSOR
        self.event = None
        self.name = None
        self.timeline = timeline
        self.time_pane = timeline.time_pane
        self.mfps = self.time_pane.window.mfps()
        self.begin_time = begin_time
        self.end_time = end_time
        factor = self.time_pane.scene.width() / self.time_pane.duration
        begin_x_position = int(self.begin_time * factor)
        end_x_position = int(self.end_time * factor)
        self.begin_handle: OccurrenceHandle = None
        self.end_handle: OccurrenceHandle = None
        self.setRect(
            QRectF(
                0,
                0,
                end_x_position - begin_x_position,
                TIMELINE_HEIGHT - TIMELINE_TITLE_HEIGHT,
            )
        )

        self.setX(begin_x_position)
        self.setY(TIMELINE_TITLE_HEIGHT)
        self.comment: str = ""
        self.get_bounds()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self.time_pane.occurrence_under_creation:
                self.setSelected(True)
                self.get_bounds()

    def mouseReleaseEvent(self, event):
        return

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if self.time_pane.occurrence_under_creation is None:
            can_merge_previous = False
            for occurrence in self.timeline.occurrences():
                if (
                    occurrence.end_time == self.begin_time
                    and self.name == occurrence.name
                ):
                    can_merge_previous = True
                    break
            can_merge_next = False
            for occurrence in self.timeline.occurrences():
                if (
                    self.end_time == occurrence.begin_time
                    and self.name == occurrence.name
                ):
                    can_merge_next = True
                    break
            menu = QMenu()
            menu.addAction(
                QAction(
                    "Delete Occurrence",
                    self.time_pane.window,
                    shortcuts=[Qt.Key.Key_Backspace, Qt.Key.Key_Delete],
                    triggered=self.on_remove
                )
            )
            menu.addAction("Change occurrence event").triggered.connect(
                self.change_event
            )
            if can_merge_previous:
                menu.addAction(
                    "Merge with previous occurrence"
                ).triggered.connect(self.merge_previous)
            if can_merge_next:
                menu.addAction("Merge with next occurrence").triggered.connect(
                    self.merge_next
                )
            menu.addAction("Comment occurrence").triggered.connect(
                self.edit_comment
            )
            try:
                pos = event.screenPos()
            except AttributeError:
                # Got here via keyPresEvent
                pos = QPoint(
                    int(self.time_pane.window.width() / 2),
                    int(self.time_pane.window.height() / 2),
                )
            menu.exec(pos)

    def on_remove(self):
        answer = QMessageBox.question(
            self.time_pane.window,
            "Confirmation",
            "Do you want to remove the occurrence?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.remove()

    def edit_comment(self):
        comment_dialog = OccurrenceComment(self.comment, self.time_pane.window)
        comment_dialog.exec()
        if comment_dialog.result() == QMessageBox.DialogCode.Accepted:
            comment = comment_dialog.get_text()
            if self.comment != comment:
                self.comment = comment
                self.setToolTip(self.comment)
                self.time_pane.data_needs_save = True

    def merge_previous(self):
        for occurrence in self.timeline.occurrences():
            if (
                self.begin_time == occurrence.end_time
                and self.name == occurrence.name
            ):
                break
        self.begin_time = occurrence.begin_time
        occurrence.remove()
        self.update_rect()
        self.update()

    def merge_next(self):
        for occurrence in self.timeline.occurrences():
            if (
                self.end_time == occurrence.begin_time
                and self.name == occurrence.name
            ):
                break
        self.end_time = occurrence.end_time
        occurrence.remove()
        self.update_rect()
        self.update()

    def change_event(self):
        events_dialog = ChooseEvent(
            self.timeline.event_collection, self.timeline.time_pane.view
        )
        events_dialog.exec()
        if events_dialog.result() == QMessageBox.DialogCode.Accepted:
            event = events_dialog.get_chosen()
            if event != self.event:
                self.set_event(event)
                self.update()
                self.time_pane.data_needs_save = True

    def remove(self):
        self.time_pane.scene.removeItem(self)
        self.time_pane.data_needs_save = True
        del self

    def paint(self, painter, option, widget=None):
        # Draw the occurrence rectangle
        self.draw_rect(painter)

        # Draw the name of the occurrence in the occurrence rectangle
        self.draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def draw_rect(self, painter):
        """Draw the occurrence rectangle"""
        pen: QPen = QPen(self.pen_color)
        pen.setWidth(self.pen_width)
        painter.setPen(pen)
        painter.setBrush(self.brush_color)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def draw_name(self, painter):
        """Draws the name of the occurrence"""
        if self.name:
            col = color_fg_from_bg(self.brush_color)
            painter.setPen(col)
            painter.setBrush(col)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, self.name
            )

    def set_event(self, event=None):
        """Updates the event"""
        if event is None:
            self.event = None
            self.brush_color = OCCURRENCE_BG_COLOR
        else:
            self.event = event
            self.brush_color = event.color
            self.name = event.name
            self.setToolTip(
                self.comment if self.comment != "" else "(no comment)"
            )
            if self.begin_handle:
                self.begin_handle.setBrush(event.color)
                self.end_handle.setBrush(event.color)

    def update_style(self):
        if self.event:
            self.brush_color = self.event.color
            self.name = self.event.name

    def update_rect(self):
        new_rect = self.time_pane.scene.sceneRect()
        # Calculate position to determine width
        factor = new_rect.width() / self.time_pane.duration
        begin_x_position = self.begin_time * factor
        end_x_position = self.end_time * factor
        self.setX(begin_x_position)

        # Update the rectangle
        rect = self.rect()
        rect.setWidth(end_x_position - begin_x_position)
        self.setRect(rect)

        if self.begin_handle:
            self.begin_handle.setX(self.rect().x())
            self.end_handle.setX(self.rect().width())

    def update_begin_time(self, begin_time: int):
        self.begin_time = begin_time
        self.update_rect()
        self.update()

    def update_end_time(self, end_time: int):
        """Updates the end time"""
        self.end_time = end_time
        self.update_rect()
        self.update()

    # FIXME: It is strange that this method must be called when adding an occurrence to the timeline. It seems that it ws neeeded during the creation of a new occurrence via the interface and got stuck in the creation of occurrences via the data file
    def finish_creation(self):
        """Finish the creation of the occurrence"""
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

        self.begin_handle = OccurrenceBeginHandle(self)
        self.end_handle = OccurrenceEndHandle(self)

        # if begin_time is greater than end_time then swap times
        if self.begin_time > self.end_time:
            self.begin_time, self.end_time = self.end_time, self.begin_time
            self.update_rect()

        self.update()

    def show_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(True)
        if self.end_handle:
            self.end_handle.setVisible(True)

    def hide_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(False)
        if self.end_handle:
            self.end_handle.setVisible(False)

    def get_bounds(self):
        lower_bound = 0
        upper_bound = self.timeline.time_pane.duration
        # Loop through the occurrences of the associated timeline
        for a in self.timeline.occurrences():
            if a != self:
                if a.end_time <= self.begin_time:
                    lower_bound = max(
                        [lower_bound, a.end_time + int(a.mfps / 2)]
                    )
                if a.begin_time >= self.end_time:
                    upper_bound = min(
                        [upper_bound, a.begin_time - int(a.mfps / 2)]
                    )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_time_from_bounding_interval(self, time) -> int:
        if self.lower_bound and time < self.lower_bound:
            time = self.lower_bound
        elif self.upper_bound and time > self.upper_bound:
            time = self.upper_bound
            self.time_pane.window.media_player_pause()
        return time

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Menu:
            self.contextMenuEvent(event)


class OccurrenceHandle(QGraphicsRectItem):

    def __init__(self, occurrence: Occurrence, time: int, x: float):
        super().__init__(occurrence)
        self.occurrence = occurrence
        self.time = time

        self.pen: QPen = QPen(self.occurrence.pen_color)
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_OFF_CURSOR)
        self.setPen(self.pen)
        self.setBrush(self.occurrence.brush_color)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)

        self.height = (
            OCCURRENCE_HANDLE_HEIGHT_FRACTION * occurrence.rect().height()
        )
        self.setRect(
            QRectF(
                -OCCURRENCE_HANDLE_WIDTH / 2,
                -self.height / 2,
                OCCURRENCE_HANDLE_WIDTH,
                self.height,
            )
        )

        self.setX(x)
        self.setY(occurrence.rect().height() / 2)

    @abstractmethod
    def change_time(self, new_time):
        self.time = new_time
        self.occurrence.time_pane.data_needs_save = True

    def focusInEvent(self, event):
        self.occurrence.setSelected(True)
        self.occurrence.time_pane.window.set_video_position(self.time)
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_ON_CURSOR)
        self.setPen(self.pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.occurrence.setSelected(False)
        self.pen.setWidth(OCCURRENCE_PEN_WIDTH_OFF_CURSOR)
        self.setPen(self.pen)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setY(self.occurrence.rect().height() / 2)

            # With the mouse, the coordinate X is changed, but we need to
            # change the time.
            time = int(
                event.scenePos().x()
                * self.occurrence.time_pane.duration
                / self.occurrence.time_pane.scene.width()
            )

            time = self.occurrence.get_time_from_bounding_interval(time)

            self.occurrence.time_pane.window.set_video_position(time)


class OccurrenceBeginHandle(OccurrenceHandle):

    def __init__(self, occurrence: Occurrence):
        super().__init__(occurrence, occurrence.begin_time, 0)

    def change_time(self, time):
        t = time - int(self.occurrence.mfps / 2)
        super().change_time(t)
        self.occurrence.update_begin_time(t)


class OccurrenceEndHandle(OccurrenceHandle):
    def __init__(self, occurrence: Occurrence):
        super().__init__(
            occurrence, occurrence.end_time, occurrence.rect().width()
        )

    def change_time(self, time):
        t = time + int(self.occurrence.mfps / 2)
        super().change_time(t)
        self.occurrence.update_end_time(t)


class OccurrenceComment(QDialog):
    def __init__(self, text="", widget=None):
        super().__init__(widget)
        self.setWindowTitle("Occurrence comment")

        layout = QFormLayout(self)
        self.input = TextEdit(self, text)
        layout.addRow(self.input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_text(self):
        return self.input.toPlainText()
