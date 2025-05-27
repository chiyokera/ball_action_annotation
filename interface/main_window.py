from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from PyQt5.QtWidgets import QApplication
import media_player
import list_display
import event_selection

import list_management

# from utils.event_class import Event, ms_to_time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Defining the geometric properties of the window
        self.xpos_main_window = 0
        self.ypos_main_window = 0
        self.width_main_window = 1920
        self.height_main_window = 1080

        self.frame_duration_ms = 40

        self.half = 1

        # Defining some variables of the window
        self.title_main_window = "Event Annotator"

        # Setting the window appropriately
        self.setWindowTitle(self.title_main_window)
        self.setGeometry(
            self.xpos_main_window,
            self.ypos_main_window,
            self.width_main_window,
            self.height_main_window,
        )

        self.palette_main_window = self.palette()
        self.palette_main_window.setColor(QPalette.Window, Qt.black)

        # Initiate the sub-widgets
        self.init_main_window()

        # Show the window
        self.show()

    def init_main_window(self):

        # Add the media player
        self.media_player = media_player.MediaPlayer(self)
        video_display = QWidget(self)
        video_display.setLayout(self.media_player.layout)

        # Create the Event selection Window
        self.event_window = event_selection.EventSelectionWindow(self)

        # Add the list
        self.list_display = list_display.ListDisplay(self)

        # Create the original list of labels
        self.list_manager = list_management.ListManager()
        self.list_display.display_list(self.list_manager.create_text_list())

        # Layout the different widgets
        central_display = QWidget(self)
        self.setCentralWidget(central_display)

        final_layout = QHBoxLayout()
        final_layout.addWidget(video_display)
        final_layout.addWidget(self.list_display)

        central_display.setLayout(final_layout)

    def keyPressEvent(self, event):

        ctrl = False

        # Remove an event with the delete key
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            index = self.list_display.list_widget.currentRow()
            if index >= 0:
                self.list_manager.delete_event(index)
                # アノテーションリストからも削除
                if index < len(self.list_manager.annotation_list):
                    self.list_manager.annotation_list.pop(index)
                self.list_display.display_list(self.list_manager.create_text_list())
            self.setFocus()

        # Play or pause the video with the space key
        if event.key() == Qt.Key_Space:
            if self.media_player.play_button.isEnabled():
                self.media_player.play_video()
                self.setFocus()

        # Move one frame backwards in time
        if event.key() == Qt.Key_Left:
            if self.media_player.play_button.isEnabled():
                position = self.media_player.media_player.position()
                if position > self.frame_duration_ms:
                    self.media_player.media_player.setPosition(
                        position - self.frame_duration_ms
                    )
            self.setFocus()

        if event.key() == Qt.Key_Right:
            if self.media_player.play_button.isEnabled():
                position = self.media_player.media_player.position()
                duration = self.media_player.media_player.duration()
                if position < duration - self.frame_duration_ms:
                    self.media_player.media_player.setPosition(
                        position + self.frame_duration_ms
                    )
            self.setFocus()

        # Enter a new annotation
        if event.key() == Qt.Key_Return:
            if (
                self.media_player.play_button.isEnabled()
                and not self.media_player.media_player.state()
                == QMediaPlayer.PlayingState
            ):
                self.event_window.set_position()
                self.event_window.show()
                self.event_window.setFocus()
                self.event_window.list_widget.setFocus()
            self.setFocus()

        # Set the playback rate to normal
        if event.key() == Qt.Key_F1 or event.key() == Qt.Key_A:
            position = self.media_player.media_player.position()
            self.media_player.media_player.setPlaybackRate(1.0)
            self.media_player.media_player.setPosition(position)
            self.setFocus()

        # Set the playback rate to x2
        if event.key() == Qt.Key_F2 or event.key() == Qt.Key_Z:
            position = self.media_player.media_player.position()
            self.media_player.media_player.setPlaybackRate(2.0)
            self.media_player.media_player.setPosition(position)
            self.setFocus()

        # Set the playback rate to x4
        if event.key() == Qt.Key_F3 or event.key() == Qt.Key_E:
            position = self.media_player.media_player.position()
            self.media_player.media_player.setPlaybackRate(4.0)
            self.media_player.media_player.setPosition(position)
            self.setFocus()

        # Set the playback rate to x0.75
        if event.key() == Qt.Key_F4 or event.key() == Qt.Key_Q:
            position = self.media_player.media_player.position()
            self.media_player.media_player.setPlaybackRate(0.75)
            self.media_player.media_player.setPosition(position)
            self.setFocus()

        # Set the playback rate to x0.5
        if event.key() == Qt.Key_F5 or event.key() == Qt.Key_W:
            position = self.media_player.media_player.position()
            self.media_player.media_player.setPlaybackRate(0.5)
            self.media_player.media_player.setPosition(position)
            self.setFocus()

        if event.key() == Qt.Key_Escape:
            self.list_display.list_widget.setCurrentRow(-1)
            self.setFocus()

        if event.modifiers() and Qt.ControlModifier:
            ctrl = True

        if event.key() == Qt.Key_S and ctrl:
            if self.media_player.play_button.isEnabled():
                # 新しいアノテーション形式で保存
                if hasattr(self.media_player, "annotation_file"):
                    self.list_manager.save_annotation_file(
                        self.media_player.annotation_file, self.half
                    )
                    print(
                        f"アノテーションを保存しました: {self.media_player.annotation_file}"
                    )
