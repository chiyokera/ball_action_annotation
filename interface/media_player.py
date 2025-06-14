# Adapted from https://codeloop.org/python-how-to-create-media-player-in-pyqt5/
import os
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QStyle,
    QSlider,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

# ここではQWidgetのsetLayout用のモジュールをつくる


class MediaPlayer(QWidget):

    def __init__(self, main_window):

        # Defining the elements of the media player
        super().__init__()

        self.main_window = main_window

        # Media Player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Video Widget
        self.video_widget = QVideoWidget()

        # Button to open a new file
        self.open_file_button = QPushButton("Open video")
        self.open_file_button.clicked.connect(self.open_file)

        # Button for playing the video
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_video)

        # Button to save annotation
        self.save_button = QPushButton("保存")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_annotation)

        # Button for the slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout.addWidget(self.open_file_button)
        hboxLayout.addWidget(self.play_button)
        hboxLayout.addWidget(self.save_button)
        hboxLayout.addWidget(self.slider)

        # create vbox layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(hboxLayout)

        self.media_player.setVideoOutput(self.video_widget)

        # Media player signals
        self.media_player.stateChanged.connect(self.mediastate_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        self.path_label = None

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != "":
            self.load_video_file(filename)

    def load_video_file(self, filename):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.play_button.setEnabled(True)
        self.save_button.setEnabled(True)

        # たぶんこいつが悪さしてる、ファイル名は 1.mkv,と2.mkvとかじゃないから、filepath[0]=1 とかじゃない
        # self.main_window.half = int(filpath[0])
        self.main_window.half = 1

        # 新しいアノテーション用のファイル名を設定
        video_dir = os.path.dirname(filename)
        video_name = os.path.splitext(os.path.basename(filename))[0]
        self.annotation_file = os.path.join(video_dir, f"{video_name}_annotations.json")

        # 既存のアノテーションファイルがあるかチェック
        if os.path.isfile(self.annotation_file):
            self.main_window.list_manager.create_list_from_annotation_file(
                self.annotation_file, self.main_window.half
            )
            self.main_window.list_display.display_list(
                self.main_window.list_manager.create_text_list()
            )
            print(
                f"既存のアノテーションファイルを読み込みました: {self.annotation_file}"
            )
        else:
            # 新しいアノテーション用に空のリストを初期化
            self.main_window.list_manager.init_new_annotation()
            self.main_window.list_display.display_list([])
            print(f"新しいアノテーションファイルを作成します: {self.annotation_file}")

    def save_annotation(self):
        """アノテーションを保存"""
        if hasattr(self, "annotation_file"):
            self.main_window.list_manager.save_annotation_file(
                self.annotation_file, self.main_window.half
            )
            print(f"アノテーションを保存しました: {self.annotation_file}")
        else:
            print("保存するアノテーションファイルが設定されていません")

    def get_last_label_file(self):
        path_label = self.path_label
        folder_label = os.path.dirname(path_label)
        if os.path.isfile(folder_label + "/Labels-ball.json"):
            return folder_label + "/Labels-ball.json"
        else:
            return path_label

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()

        else:
            self.media_player.play()

    def mediastate_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_errors(self):
        self.play_button.setEnabled(False)
        print("Error: " + self.media_player.errorString())
