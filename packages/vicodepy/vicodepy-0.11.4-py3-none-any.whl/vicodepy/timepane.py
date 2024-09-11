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

import pandas as pd
from math import (
    inf,
    isinf,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QColor,
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QAbstractSlider,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QMessageBox,
    QScrollBar,
    QStyle,
)
from .constants import (
    CSV_HEADERS,
    EVENT_DEFAULT_COLOR,
    MINIMUM_ZOOM_FACTOR,
    OCCURRENCE_PEN_WIDTH_OFF_CURSOR,
    OCCURRENCE_PEN_WIDTH_ON_CURSOR,
    TIMELINE_HEIGHT,
    TIME_SCALE_HEIGHT,
    ZOOM_STEP,
)
from .event import (
    ChooseEvent,
    Event,
    EventCollection,
)
from .occurrence import (
    Occurrence,
    OccurrenceHandle,
)
from .timeline import (
    Timeline,
    TimelinePropertiesDialog,
)
from .timescale import TimeScale


class TimePaneView(QGraphicsView):

    def __init__(self, window):
        super().__init__(window)
        self.zoom_step = ZOOM_STEP
        self.zoom_shift = None
        self.minimum_zoom_factor = MINIMUM_ZOOM_FACTOR
        self.zoom_factor = self.minimum_zoom_factor
        self.window = window
        self.create_ui()

    def create_ui(self):
        vertical_scrollbar = QScrollBar(Qt.Orientation.Vertical, self)
        vertical_scrollbar.valueChanged.connect(
            self.on_vertical_scroll_value_changed
        )
        self.setVerticalScrollBar(vertical_scrollbar)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # This is necessary for getting the cursor being updated
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.scene = TimePaneScene(self)
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.setScene(self.scene)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not self.window.has_media():
                return
            mouse_pos = self.mapToScene(event.position().toPoint()).x()
            if event.angleDelta().y() > 0:
                self.zoom_shift = mouse_pos * (1 - self.zoom_step)
                self.zoom_in()
            else:
                self.zoom_shift = mouse_pos * (1 - 1 / self.zoom_step)
                self.zoom_out()
            self.zoom_shift = None
        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.angleDelta().y() > 0:
                action = QAbstractSlider.SliderSingleStepAdd
            else:
                action = QAbstractSlider.SliderSingleStepSub
            self.horizontalScrollBar().triggerAction(action)
        else:
            super().wheelEvent(event)

    def on_vertical_scroll_value_changed(self, value):
        """Allow the time scale to be always visible when scrolling"""
        if self.scene.time_pane.time_scale:
            self.scene.time_pane.time_scale.setPos(0, value)

    def zoom_in(self):
        self.zoom_factor *= self.zoom_step
        self.update_scale()

    def zoom_out(self):
        new_zoom_factor = self.zoom_factor / self.zoom_step
        if new_zoom_factor >= self.minimum_zoom_factor:
            self.zoom_factor = new_zoom_factor
            self.update_scale()

    def update_scale(self):
        # Update the size of the scene with zoom_factor
        self.scene.setSceneRect(
            0,
            0,
            self.width() * self.zoom_factor,
            self.scene.height(),
        )

        if self.zoom_shift:
            previous_anchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(self.zoom_shift, 0)
            self.setTransformationAnchor(previous_anchor)

    def set_position(self, time):
        # During the creation of a new occurrence
        if self.scene.time_pane.occurrence_under_creation:
            occurence = self.scene.time_pane.occurrence_under_creation
            time = occurence.get_time_from_bounding_interval(time)

        # Cope with selected occurrence
        for i in self.scene.time_pane.scene.selectedItems():
            if isinstance(i, Occurrence):
                time = i.get_time_from_bounding_interval(time)
                break

        # Set time of the video player
        self.window.set_media_player_position(int(time))

    def resizeEvent(self, a0):
        # FIXME: Instead of testing the presence of the time scale, test whether there is a video loaded
        if self.scene.time_pane.time_scale:
            origin = self.mapToScene(0, 0).x()
            width_before = self.scene.width() / self.zoom_factor
            width_after = self.width()
            shift = origin * (1 - width_after / width_before)
            self.update_scale()
            previous_anchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(shift, 0)
            self.setTransformationAnchor(previous_anchor)
        else:
            self.scene.setSceneRect(
                0,
                0,
                self.width(),
                self.scene.height(),
            )
        self.update()
        super().resizeEvent(a0)


class TimePaneScene(QGraphicsScene):

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.sceneRectChanged.connect(self.on_scene_changed)
        self.create_time_pane()

    def create_time_pane(self):
        self.time_pane = TimePane(self)
        self.time_pane.setY(TIME_SCALE_HEIGHT)
        self.addItem(self.time_pane)

    def on_scene_changed(self, rect):
        self.time_pane.on_change(rect)


class TimePane(QGraphicsRectItem):

    def __init__(self, scene):
        """Initialize the time pane graphics item"""
        super().__init__()
        self._duration = 0
        self._time = 0

        self.selected_timeline = None
        self.occurrence_under_creation: Occurrence = None
        self.scene = scene
        self.view = scene.view
        self.window = self.view.window
        self.time_scale = None
        self.data_needs_save = False
        self.scrollbar_width = self.window.style().pixelMetric(
            QStyle.PM_ScrollBarExtent
        )

    def on_change(self, rect):
        # Update occurrences
        for timeline in self.timelines():
            timeline.update_rect_width(rect.width())
            for occurrence in timeline.occurrences():
                occurrence.update_rect()

        if self.occurrence_under_creation:
            self.occurrence_under_creation.update_rect()

        # Update time scale display
        if self.time_scale:
            # Update cursor
            if self.duration:
                self.time_scale.cursor.setX(
                    self.time * rect.width() / self.duration
                )
            self.time_scale.update_rect()

    def select_cycle_timeline(self, delta):
        timelines = self.timelines()
        i, n = self.find_selected_timeline()
        selected_timeline = timelines[i]
        selected_timeline.select = False
        if delta > 0:
            if i == n - 1:
                i = -1
        else:
            if i == 0:
                i = n
        i += delta
        self.select_timeline(timelines[i])

    def find_selected_timeline(self):
        timelines = self.timelines()
        n = len(timelines)
        for i in range(n):
            if timelines[i].select:
                break
        return i, n

    def select_timeline(self, line):
        for tl in self.timelines():
            tl.select = False
        line.select = True
        self.occurrence_borders()
        line.update()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        if time != self._time:
            self._time = time
            self.on_time_changed()

    def on_time_changed(self):
        # First, update the current occurrence, if it exists. If the cursor
        # time goes beyond the allowed bounds, bring it back and do not update
        # the other widgets.
        if self.occurrence_under_creation:
            if (
                self.occurrence_under_creation.lower_bound
                and self.time < self.occurrence_under_creation.lower_bound
            ):
                self.time = self.occurrence_under_creation.lower_bound
            elif (
                self.occurrence_under_creation.upper_bound
                and self.time > self.occurrence_under_creation.upper_bound
            ):
                self.time = self.occurrence_under_creation.upper_bound
                if (
                    self.window.media_player_playback_state()
                    == QMediaPlayer.PlaybackState.PlayingState
                ):
                    self.window.media_player_pause()
            begin_time = self.occurrence_under_creation.begin_time
            mfps = self.window.mfps()
            if self.time >= begin_time:
                self.occurrence_under_creation.update_end_time(
                    self.time + int(mfps / 2)
                )
            else:
                self.occurrence_under_creation.update_end_time(
                    self.time - int(mfps / 2)
                )

        # Cope with selected occurrence
        for i in self.scene.selectedItems():
            if isinstance(i, Occurrence):
                self.time = i.get_time_from_bounding_interval(self.time)
                break

        # Update cursor position
        if self.time_scale.cursor:
            self.time_scale.cursor.setX(
                self.time * self.scene.width() / self.duration
            )

        if isinstance(self.scene.focusItem(), OccurrenceHandle):
            occurrence_handle: OccurrenceHandle = self.scene.focusItem()
            occurrence_handle.change_time(self.time)

        self.occurrence_borders()

    def occurrence_borders(self):
        # Change appearance of occurrence under the cursor
        # (Brute force approach; this ought to be improved)
        if not self.occurrence_under_creation:
            for tml in self.timelines():
                for ocr in tml.occurrences():
                    ocr.pen_width = OCCURRENCE_PEN_WIDTH_OFF_CURSOR
                    if tml.select:
                        if (
                            ocr.begin_time <= self.time
                            and ocr.end_time >= self.time
                        ):
                            ocr.pen_width = OCCURRENCE_PEN_WIDTH_ON_CURSOR

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration != self._duration:
            self._duration = duration
            # Recreate time pane scale and the cursor
            self.time_scale = TimeScale(self)
            self.scene.addItem(self.time_scale)
            self.view.update()

    def clear(self):
        # Clear timelineScene
        self.scene.clear()

    def handle_occurrence(self):
        """Handle the occurrence"""
        menu = self.window.menu
        if self.occurrence_under_creation is None:
            if self.selected_timeline.can_create_occurrence(self.time):
                mfps = self.window.mfps()
                self.occurrence_under_creation = Occurrence(
                    self.selected_timeline,
                    self.time - int(mfps / 2),
                    self.time + int(mfps / 2),
                )
            menu.start_occurence()
        else:
            # Finish the current occurrence
            events_dialog = ChooseEvent(
                self.selected_timeline.event_collection, self.view
            )
            events_dialog.exec()
            if events_dialog.result() == QMessageBox.DialogCode.Accepted:
                event = events_dialog.get_chosen()
                self.occurrence_under_creation.set_event(event)
                self.occurrence_under_creation.finish_creation()
                self.occurrence_under_creation = None
                self.on_time_changed()
            menu.finish_occurence()
            self.data_needs_save = True
            self.view.update()

    def new_timeline(self, where):
        if not isinf(where):
            order = self.selected_timeline.order
            if where < 0:
                where = order - 0.5
            else:
                where = order + 0.5
        timeline = Timeline("", where, "", self)
        dialog = TimelinePropertiesDialog(timeline)
        dialog.exec()
        if dialog.result() == QMessageBox.DialogCode.Accepted:
            name = dialog.get_name()
            if not self.check_new_timeline_name(name):
                self.delete_timeline(timeline)
                return
            timeline.name = name
            timeline.description = dialog.get_description()
            self.add_timeline(timeline)
            self.place_timelines()
            self.data_needs_save = True

    def check_new_timeline_name(self, name):
        if name == "":
            QMessageBox.warning(
                self.window, "Warning", "Timeline name cannot be empty"
            )
            return False
        if name in self.get_timeline_names():
            QMessageBox.warning(
                self.window,
                "Warning",
                f'A timeline with name "{name}" exists already',
            )
            return False
        return True

    def abort_occurrence_creation(self):
        if self.occurrence_under_creation is not None:
            confirm_box = ConfirmMessageBox(
                "Abort creation of occurrence?", self.window
            )
            if confirm_box.result() == ConfirmMessageBox.DialogCode.Accepted:
                self.occurrence_under_creation.remove()
                self.occurrence_under_creation = None
                self.view.update()
                self.window.menu.start_occurence()

    def add_timeline(self, timeline):
        # Set the timeline rectangle
        timeline.update_rect()

        # Select the new timeline
        for i in self.timelines():
            i.select = False
        timeline.select = True

        self.view.update_scale()

    def place_timelines(self):
        order = 0
        for i in self.timelines():
            i.order = order
            order += 1
        timelines = self.timelines()
        for timeline in timelines:
            timeline.setPos(0, timeline.order * TIMELINE_HEIGHT)

        # Adjust the height of of the scene
        rect = self.scene.sceneRect()
        height = len(self.timelines()) * TIMELINE_HEIGHT + TIME_SCALE_HEIGHT
        rect.setHeight(height)
        self.scene.setSceneRect(rect)

        # Set maximum height of the widget
        self.view.setMaximumHeight(int(height) + self.scrollbar_width + 2)

    def move_timeline(self, delta):
        if isinf(delta):
            if delta < 0:
                self.selected_timeline.order = -1
            else:
                self.selected_timeline.order = len(self.timelines())
        else:
            self.selected_timeline.order += delta * 1.5
        self.place_timelines()

    def add_data(self, data):
        for _, row in data.data.iterrows():
            # Search for timeline
            timeline = self.get_timeline_by_name(row["timeline"])

            # If timeline from csv doesn't exist in TimePane,
            # escape row
            if not timeline:
                continue

            # Search for event
            event = timeline.event_collection.get_event(row["event"])

            # If event from csv doesn't exist in timeline,
            # then add it
            if not event:
                continue

            occurrence = Occurrence(
                timeline,
                int(row["begin"]),
                int(row["end"]),
            )

            occurrence.set_event(event)
            occurrence.finish_creation()

    def get_timeline_by_name(self, name):
        """Get the timeline by name"""
        return next((x for x in self.timelines() if x.name == name), None)

    def has_occurrences(self) -> bool:
        return any(len(line.occurrences()) for line in self.timelines())

    def delete_occurrence(self):
        for i in self.scene.selectedItems():
            if isinstance(i, Occurrence):
                i.on_remove()
                break

    def timelines_from_config(self, config):
        if "timelines" in config:

            # Set all absent order fields with Inf
            for k, v in config["timelines"].items():
                if not v:
                    v = dict()
                    config["timelines"][k] = v
                if "order" not in v:
                    v["order"] = -inf
                if "description" not in v:
                    v["description"] = ""

            # Sort according to order first and alphabetically from
            # timeline name, otherwise from the "order" property In the
            # loop below, the "order" attribute of the Timeline items will
            # receiving increasing nteger values, starting at zero.
            order = 0
            for item in sorted(
                config["timelines"].items(),
                key=lambda x: (x[1]["order"], x[0]),
            ):
                # Get name and properties of the timeline
                name = item[0]
                properties = item[1]
                description = properties["description"]

                # Create timeline
                line = Timeline(name, order, description, self)
                order += 1

                # Add the timeline to the TimePane
                self.add_timeline(line)

                # Loop over events of the timeline
                event_collection = EventCollection()
                if "events" in properties:
                    for k, v in properties["events"].items():
                        event = Event(k)
                        try:
                            event.color = QColor(v["color"])
                        except KeyError:
                            event.color = EVENT_DEFAULT_COLOR
                        try:
                            event.description = v["description"]
                        except KeyError:
                            event.description = ""
                        event_collection.add_event(event)
                    line.event_collection = event_collection

            self.place_timelines()

    def timelines_to_dataframe(self):
        df = pd.DataFrame(columns=CSV_HEADERS)
        for timeline in sorted(self.timelines(), key=lambda x: x.name):
            for occurrence in timeline.occurrences():
                comment = occurrence.comment.replace('"', '\\"')
                row = [
                    timeline.name,
                    occurrence.event.name,
                    f"{occurrence.begin_time:.3f}",
                    f"{occurrence.end_time:.3f}",
                    comment,
                ]
                df.loc[len(df.index)] = row
        return df

    def timelines(self):
        # Always return a list sorted by order
        return sorted(
            [x for x in self.childItems() if isinstance(x, Timeline)],
            key=lambda x: x.order,
        )

    def delete_timeline(self, timeline):
        # If the timeline to delted is the selected one, select the next one
        if self.selected_timeline == timeline:
            timelines = self.timelines()
            new_selected = None
            for i in timelines:
                if i.order > timeline.order:
                    new_selected = i
                    break
            if not new_selected:
                new_selected = timelines[0]
            new_selected.select = True
        self.scene.removeItem(timeline)
        self.place_timelines()
        del timeline
        self.data_needs_save = True

    def get_timeline_names(self):
        return [x.name for x in self.timelines()]


class ConfirmMessageBox(QMessageBox):
    def __init__(self, message, parent=None):
        super().__init__(
            QMessageBox.Icon.Warning,
            "Warning",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            parent,
        )

        self.button(QMessageBox.StandardButton.Yes).clicked.connect(self.accept)
        self.button(QMessageBox.StandardButton.No).clicked.connect(self.reject)
        self.exec()
