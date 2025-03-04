import sys
import json
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QCheckBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QColor

class QuranApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📖 Quran Pak Audio Player ")
        self.setGeometry(100, 100, 600, 550)

        # 🌟 Apply Custom Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: white;
                font-family: Arial;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3e8ef7;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6fa3ef;
            }
            QComboBox, QLineEdit {
                background-color: #2e2e3e;
                color: white;
                border: 1px solid #6fa3ef;
                padding: 5px;
            }
            QCheckBox {
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()

        # 📌 Reciter Selection
        self.reciterLabel = QLabel("🎙️ Reciter:")
        layout.addWidget(self.reciterLabel)

        self.reciterCombo = QComboBox()
        self.reciterCombo.addItems(["Abdul Basit Abdul Samad", "Mishary Rashid Alafasy", "Saad Al-Ghamdi"])
        layout.addWidget(self.reciterCombo)

        # 📖 Surah Selection
        self.surahLabel = QLabel("📖 Chapter:")
        layout.addWidget(self.surahLabel)

        self.surahCombo = QComboBox()
        self.loadSurahs()
        layout.addWidget(self.surahCombo)

        # 🔢 Aya Input
        self.ayaLabel = QLabel("🔢 Aya #:")
        layout.addWidget(self.ayaLabel)

        self.ayaInput = QLineEdit()
        layout.addWidget(self.ayaInput)

        # 🎵 Audio Player
        self.audioPlayer = QMediaPlayer(None, QMediaPlayer.LowLatency)  # ✅ Fixes some playback issues

        # ▶ Play Button
        self.playButton = QPushButton("▶ Play Audio")
        self.playButton.clicked.connect(self.playSurahAudio)
        layout.addWidget(self.playButton)

        # 🛑 Stop Button
        self.stopButton = QPushButton("⏹️ Stop")
        self.stopButton.clicked.connect(self.stopAudio)
        layout.addWidget(self.stopButton)

        # ⏭️ Next Surah Button
        self.nextButton = QPushButton("⏭️ Next Surah")
        self.nextButton.clicked.connect(self.playNextSurah)
        layout.addWidget(self.nextButton)

        # ⬇ Download Button
        self.downloadButton = QPushButton("⬇ Download MP3")
        self.downloadButton.clicked.connect(self.downloadAudio)
        layout.addWidget(self.downloadButton)

        # 🔄 Auto Play Option
        self.autoPlayCheck = QCheckBox("Auto Play")
        layout.addWidget(self.autoPlayCheck)

        # 🖌️ Animated Credit Label
        self.creditLabel = QLabel("Created by Farhana Ahsan")
        self.creditLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.creditLabel)

        self.setLayout(layout)

        # Color Animation Setup
        self.colors = ["#ff4757", "#ff9f1a", "#2ed573", "#1e90ff", "#6c5ce7"]
        self.color_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animateColor)
        self.timer.start(500)  # Change color every 500ms

    def animateColor(self):
        """Animate credit label color"""
        self.creditLabel.setStyleSheet(f"color: {self.colors[self.color_index]}; font-size: 14px; font-weight: bold;")
        self.color_index = (self.color_index + 1) % len(self.colors)

    def loadSurahs(self):
        try:
            with open("surahs.json", "r", encoding="utf-8") as file:
                self.surahs = json.load(file)
                for surah in self.surahs:
                    self.surahCombo.addItem(f"{surah['id']}: {surah['name']}")
        except FileNotFoundError:
            self.surahLabel.setText("❌ surahs.json file not found!")

    def playSurahAudio(self):
        selected_index = self.surahCombo.currentIndex()
        if selected_index < 0:
            return

        surah = self.surahs[selected_index]
        audio_url = surah["audio"]

        self.audioPlayer.setMedia(QMediaContent(QUrl(audio_url)))
        self.audioPlayer.play()

    def stopAudio(self):
        """Stop the audio playback"""
        self.audioPlayer.stop()

    def playNextSurah(self):
        """Play the next Surah in the list"""
        current_index = self.surahCombo.currentIndex()
        if current_index < len(self.surahs) - 1:
            self.surahCombo.setCurrentIndex(current_index + 1)
            self.playSurahAudio()

    def downloadAudio(self):
        selected_index = self.surahCombo.currentIndex()
        if selected_index < 0:
            return

        surah = self.surahs[selected_index]
        webbrowser.open(surah["audio"])  # ✅ Opens in default browser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuranApp()
    window.show()
    sys.exit(app.exec_())
