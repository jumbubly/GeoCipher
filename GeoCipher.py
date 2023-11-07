import sys
import requests
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QTextEdit
from PyQt6.QtGui import QFont, QPalette, QColor, QTextCharFormat, QTextCursor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer

class GeoCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GeoCipher")
        self.setGeometry(100, 100, 800, 250)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()


        ascii_title_label = QLabel(
            """
            █████▀████████████████████████████████████████████
            █─▄▄▄▄█▄─▄▄─█─▄▄─█─▄▄▄─█▄─▄█▄─▄▄─█─█─█▄─▄▄─█▄─▄▄▀█
            █─██▄─██─▄█▀█─██─█─███▀██─███─▄▄▄█─▄─██─▄█▀██─▄─▄█
            ▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▀▀▄▀▄▀▄▄▄▄▄▀▄▄▀▄▄▀
            """
        )
        ascii_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ascii_title_label.setWordWrap(True)
        layout.addWidget(ascii_title_label)

        self.ip_label = QLabel("Enter IP Address:")
        self.coord_label = QLabel("Enter Latitude and Longitude (comma-separated):")
        self.ip_input = QLineEdit()
        self.coord_input = QLineEdit()
        self.get_ip_data_button = QPushButton("Get IP Data")
        self.get_coord_data_button = QPushButton("Get Coordinate Data")
        self.reset_button = QPushButton("Reset Data")

        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.coord_label)
        layout.addWidget(self.coord_input)
        layout.addWidget(self.get_ip_data_button)
        layout.addWidget(self.get_coord_data_button)
        layout.addWidget(self.reset_button)

        self.get_ip_data_button.clicked.connect(self.get_ip_geo_data)
        self.get_coord_data_button.clicked.connect(self.get_coord_geo_data)
        self.reset_button.clicked.connect(self.reset_data)

        central_widget.setLayout(layout)

        self.ip_result_window = None
        self.coord_result_window = None

    def get_ip_geo_data(self):
        input_text = self.ip_input.text()
        if not input_text:
            self.display_ip_result("Please enter an IP address.")
            return

        url = f"https://ipinfo.io/{input_text}/json"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'loc' in data:
                    lat_long = data['loc'].split(',')
                    latt = lat_long[0]
                    longt = lat_long[1]
                    city = data.get('city', 'N/A')
                    country = data.get('country', 'N/A')
                    result_text = f"Latitude: {latt}\nLongitude: {longt}\nCity: {city}\nCountry: {country}"
                    self.display_ip_result(result_text)
                elif 'city' in data and 'country' in data:
                    city = data['city']
                    country = data['country']
                    result_text = f"City: {city}\nCountry: {country}"
                    self.display_ip_result(result_text)
                else:
                    self.display_ip_result("Data not found for the given input.")
            else:
                self.display_ip_result(f"Failed to retrieve data. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.display_ip_result(f"Error: {e}")

    def get_coord_geo_data(self):
        input_text = self.coord_input.text()
        if not input_text:
            self.display_coord_result("Please enter latitude and longitude.")
            return

        if input_text.count(",") == 1:
            lat, long = input_text.split(",")
            if not (lat.strip() and long.strip()):
                self.display_coord_result("Invalid latitude and longitude format. Please use 'latitude,longitude'.")
                return
            url = f"https://geocode.xyz/{lat},{long}?geoit=json"
        else:
            self.display_coord_result("Invalid latitude and longitude format. Please use 'latitude,longitude'.")
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'city' in data and 'stnumber' in data:
                    city = data['city']
                    street_number = data['stnumber']
                    street_address = data.get('staddress', 'N/A')
                    country = data.get('country', 'N/A')
                    result_text = f"City: {city}\nStreet: {street_number} {street_address}\nCountry: {country}"
                    self.display_coord_result(result_text)
                elif 'error' in data:
                    self.display_coord_result("Data not found for the given input.")
                else:
                    self.display_coord_result("Data not found for the given input.")
            else:
                self.display_coord_result(f"Failed to retrieve data. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.display_coord_result(f"Error: {e}")

    def reset_data(self):
        self.ip_input.clear()
        self.coord_input.clear()
        self.close_result_windows()

    def close_result_windows(self):
        for result_window in [self.ip_result_window, self.coord_result_window]:
            if result_window:
                result_window.close()
        self.ip_result_window = None
        self.coord_result_window = None

    def display_ip_result(self, result_text):
        if self.ip_result_window is None:
            self.ip_result_window = ResultWindow(result_text, "IP GeoCipher")
            self.ip_result_window.show()
        else:
            self.ip_result_window.update_text("")
            self.ip_result_window.text = result_text
            self.ip_result_window.show()
            self.ip_result_window.start_animation()

    def display_coord_result(self, result_text):
        if self.coord_result_window is None:
            self.coord_result_window = ResultWindow(result_text, "Coordinates GeoCipher")
            self.coord_result_window.show()
        else:
            self.coord_result_window.update_text("")
            self.coord_result_window.text = result_text
            self.coord_result_window.show()
            self.coord_result_window.start_animation()

class ResultWindow(QDialog):
    def __init__(self, text, title):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.result_label = QTextEdit()
        self.result_label.setPlainText("")
        self.result_label.setReadOnly(True)
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.result_label.setFont(font)

        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.text = text
        self.current_text = ""
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_speed = 50


        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(142, 45, 197))
        dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

        self.setPalette(dark_palette)

    def showEvent(self, event):
        super().showEvent(event)
        self.start_animation()

    def start_animation(self):
        self.animation_timer.start(self.animation_speed)
        self.current_text = ""
        self.text_index = 0

    def update_animation(self):
        if self.text_index < len(self.text):
            self.current_text += self.text[self.text_index]
            self.result_label.setPlainText(self.current_text)
            self.text_index += 1
            self.set_text_color()
        else:
            self.animation_timer.stop()

    def set_text_color(self):
        char_format = QTextCharFormat()
        char_format.setForeground(QColor(0, 255, 0))

        cursor = self.result_label.textCursor()
        cursor.setPosition(self.text_index - 1)
        cursor.setPosition(self.text_index, QTextCursor.MoveMode.KeepAnchor)
        cursor.setCharFormat(char_format)
        self.result_label.setTextCursor(cursor)

def main():
    app = QApplication(sys.argv)


    app.setStyle("Fusion")

    window = GeoCipherApp()
    window.show()


    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, QColor(142, 45, 197))
    dark_palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    window.setPalette(dark_palette)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
