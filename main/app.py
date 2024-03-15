from pathlib import Path

from PIL import ImageGrab
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QDesktopWidget, \
    QAction, QInputDialog, QShortcut, QMainWindow

import edit_image
import predict_hero_icons
import predict_win
from hero_data import hero_list
from pynput import keyboard


def match_heroes_to_ids(predicted_teams):
    id_name_dict = {name: hero_id for hero_id, name in (element.split(':') for element in hero_list.hero_ids)}
    return [int(id_name_dict[hero]) for hero in predicted_teams]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = None

        self.screenshot_button = None
        self.winner_label = None

        self.team_labels = []
        self.dire_layout = None
        self.radiant_layout = None

        self.alt_pressed = None
        self.listener = None
        self.screenshotShortcut = None
        self.screenshotKey = None

        self.initUI()
        self.keyboard_listener()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout(centralWidget)

        self.setupButton()
        self.setupWinnerLabel()
        self.setupTeams()
        self.setupMenuBar()

        self.setWindowTitle('Dota 2 Draft Predictor')
        self.resize(1080, 540)
        self.centerWindow()
        self.show()

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setupMenuBar(self):
        menubar = self.menuBar()
        settingsMenu = menubar.addMenu('Settings')

        setScreenshotKeyAction = QAction('Set Screenshot Key', self)
        setScreenshotKeyAction.triggered.connect(self.setScreenshotKey)
        settingsMenu.addAction(setScreenshotKeyAction)

        self.updateShortcut()

    def setScreenshotKey(self):
        text, ok = QInputDialog.getText(self, 'Set Screenshot Key', 'Enter the new screenshot key (e.g., Alt+P):')
        if ok and text:
            self.screenshotKey = text
            self.updateShortcut()
            self.screenshot_button.setText(f'Make Screenshot\n({self.screenshotKey})')

    def updateShortcut(self):
        if hasattr(self, 'screenshotShortcut') and self.screenshotShortcut:
            self.screenshotShortcut.activated.disconnect()

        keyCombination = QKeySequence(self.screenshotKey)
        self.screenshotShortcut = QShortcut(keyCombination, self)
        self.screenshotShortcut.activated.connect(self.take_screenshot)

    def setupButton(self):
        self.screenshotKey = 'Alt+P'
        self.screenshot_button = QPushButton(f'Make Screenshot\n({self.screenshotKey})', self)
        self.screenshot_button.setFixedSize(100, 100)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.layout.addWidget(self.screenshot_button, alignment=Qt.AlignCenter)

    def setupWinnerLabel(self):
        self.winner_label = QLabel('Predicted Match Winner:', self)
        self.winner_label.setStyleSheet('font-weight: bold; font-size: 24px; text-align: center;')
        self.layout.addWidget(self.winner_label, alignment=Qt.AlignCenter)
        self.winner_label.hide()

    def setupTeams(self):
        teams_layout = QHBoxLayout()
        teams_info = [('Radiant', 'green'), ('Dire', 'red')]

        for team_name, color in teams_info:
            team_layout = QVBoxLayout()
            team_label = QLabel(f'{team_name}', self)
            team_label.setStyleSheet(f'color: {color}; font-size: 20px')
            team_layout.addWidget(team_label)
            team_label.hide()
            self.team_labels.append(team_label)

            hero_layout = QHBoxLayout()
            hero_layout.setSpacing(5)
            team_layout.addLayout(hero_layout)

            setattr(self, f'{team_name.lower()}_layout', hero_layout)

            teams_layout.addLayout(team_layout)

        teams_layout.addStretch(1)
        self.layout.addLayout(teams_layout)

    def keyboard_listener(self):
        self.alt_pressed = False

        def on_press(key):
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.alt_pressed = True

        def on_release(key):
            try:
                if (key == keyboard.KeyCode.from_char('p') or key == keyboard.KeyCode.from_char(
                        'P')) and self.alt_pressed:
                    QApplication.instance().postEvent(self, QEvent(QEvent.User))
                    self.alt_pressed = False
                if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.alt_pressed = False
            except AttributeError:
                pass

        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    def event(self, event):
        if event.type() == QEvent.User:
            self.take_screenshot()
            return True
        return super(MainWindow, self).event(event)

    def take_screenshot(self):
        screenshot = ImageGrab.grab()
        screenshot_path = Path("current_screenshot.jpg")
        screenshot.save(screenshot_path)

        output_dir = Path("./output_directory")
        edit_image.crop_hero_icons_percent(screenshot_path, output_dir)

        predicted_teams = predict_hero_icons.predict_teams(output_dir)
        hero_ids = match_heroes_to_ids(predicted_teams)

        predicted_winner = predict_win.predict_match_winner(hero_ids)

        self.display_heroes(predicted_teams)

        self.winner_label.show()
        for team_label in self.team_labels:
            team_label.show()

        self.winner_label.setText(f'Predicted Match Winner: {predicted_winner[0]}')

    def display_heroes(self, teams):
        for layout, heroes in zip([self.radiant_layout, self.dire_layout], [teams[:5], teams[5:]]):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            for hero in heroes:
                icon_path = Path(f"../hero_data/hero_icons/{hero}.jpg")
                if icon_path.exists():
                    pixmap = QPixmap(str(icon_path))
                    label = QLabel()
                    label.setPixmap(pixmap.scaled(64, 64))
                    layout.addWidget(label)


if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MainWindow()
    app.exec_()
