from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QThread
from python.utilis import default_msg, simulate_data
from python.plot import design_canvas, reset_canvas
from config import INPUT_PARAMETERS, SAVE_PLOT_NAMES
from matplotlib.animation import FFMpegWriter
import os

app = QApplication([])
with open("styles/style.qss", "r") as f:
    app.setStyleSheet(f.read())


class SpinFlight(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_window()
        self.buttons = []
        self.collapsible_inputs = {}
        self.simulation_inputs = {}
        self.magnus_data = {}
        self.file_paths = []
        plot_buffer = {}
        self.add_toolbar()
        design_canvas(self)
        self.add_center()
        self.make_input_labels()
        self.add_status_bar()
        self.simulate_btn.triggered.connect(self.simulate)
        self.reset_btn.triggered.connect(self.reset_button)
        self.save_btn.triggered.connect(self.save_plot)

    def set_window(self):
        self.setWindowTitle("SpinFlight")
        self.setWindowIcon(QIcon("icons/ball.svg"))
        self.setIconSize(QSize(30, 30))
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        initial_width = int(self.screen_width * 0.8)
        initial_height = int(self.screen_height * 0.7)
        self.setGeometry(500, 200, initial_width, initial_height)
        self.setMinimumSize(initial_width, initial_height)

    def add_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)
        self.toolbar_btn = {
            "simulate_btn": ["Simulate", "Start Simulation"],
            "reset_btn": ["Reset", "Reset All Data"],
            "export_btn": ["Export", "Save Data"],
        }
        self.add_buttons()

    def add_buttons(self):
        for button_name, [button_label, button_status] in self.toolbar_btn.items():
            action = QAction(button_label, self)
            if button_name == "export_btn":
                self.add_export_menu(action)
            action.setToolTip(button_status)
            setattr(self, button_name, action)
            self.toolbar.addAction(action)
            self.toolbar.addSeparator()

        for button in self.toolbar.findChildren(QToolButton):
            button.setCursor(Qt.PointingHandCursor)
            button.setPopupMode(QToolButton.InstantPopup)

    def add_export_menu(self, action):
        menu = QMenu()
        menu.setCursor(Qt.PointingHandCursor)
        save_btn = QAction("Save Plots")
        csv_btn = QAction("Export as CSV")
        setattr(self, "save_btn", save_btn)
        setattr(self, "csv_btn", csv_btn)
        menu.addAction(save_btn)
        menu.addAction(csv_btn)
        action.setMenu(menu)

    def get_unique_file_path(self, folder, filename):
        base_name, extension = os.path.splitext(filename)
        file_path = os.path.join(folder, filename)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(folder, f"{base_name}_{counter}{extension}")
            counter += 1
        return file_path

    def save_plot(self):
        if not self.magnus_data:
            self.status.showMessage(
                "No plots available to save! Please generate a plot first."
            )
            default_msg(self)
            return
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.status.addPermanentWidget(self.progress_bar)
        self.progress_bar.setFixedHeight(17)

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Export Folder",
        )
        if folder:
            self.progress_bar.setVisible(True)
            for button_name in self.toolbar_btn:
                getattr(self, button_name).setEnabled(False)
            for i, (plot_name, figure) in enumerate(SAVE_PLOT_NAMES.items(), start=1):
                if plot_name == "animation_plot":
                    filename = f"{plot_name}.mp4"
                    file_path = self.get_unique_file_path(folder, filename)
                    writer = FFMpegWriter(fps=60, bitrate=3000)
                    self.status.showMessage(f"Saving Plot 5 of 5.....")

                    def progress_callback(current_frame, total_frames):
                        animation_percent = int((current_frame / total_frames) * 20)
                        total_percent = 80 + animation_percent
                        self.progress_bar.setValue(total_percent)
                        QApplication.processEvents()

                    self.animation.save(
                        file_path, writer=writer, progress_callback=progress_callback
                    )
                    continue
                filename = f"{plot_name}.png"
                file_path = self.get_unique_file_path(folder, filename)
                self.show_progress(i)
                getattr(self, figure).savefig(file_path, dpi=300, bbox_inches="tight")

            for button_name in self.toolbar_btn:
                getattr(self, button_name).setEnabled(True)
            self.status.showMessage("Plots have been saved sucessfully!!", 3000)
            self.progress_bar.setVisible(False)
            default_msg(self)
        else:
            self.status.showMessage("Please Select a folder to save!!")
            default_msg(self)

    def show_progress(self, i):
        percent = int((i / 5) * 100)
        self.progress_bar.setValue(percent)
        self.status.showMessage(f"Saving Plot {i} of 5.....")
        QApplication.processEvents()

    def add_center(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout()
        central_widget.setLayout(self.layout)

        input_area = QScrollArea()
        input_area.setWidgetResizable(True)

        plot_area = QTabWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_layout.addWidget(plot_area)

        input_layout = QVBoxLayout()
        self.layout.addLayout(input_layout)
        input_layout.addWidget(input_area)

        self.welcome_layout = QVBoxLayout()

        app_icon_label = QLabel()
        app_icon = QPixmap()
        app_icon.load("icons/ball.svg")
        app_icon_width = int(self.screen_width * 0.2)
        app_icon_height = int(self.screen_height * 0.2)
        scaled_icon = app_icon.scaled(
            app_icon_width, app_icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        app_icon_label.setPixmap(scaled_icon)

        app_title = QLabel("Spin Flight")
        app_description = QLabel(
            "Set initial conditions and spin parameters to analyze trajectory, forces, and motion."
        )
        self.welcome_layout.addWidget(app_icon_label, alignment=Qt.AlignCenter)
        self.welcome_layout.addWidget(app_title, alignment=Qt.AlignCenter)
        self.welcome_layout.addWidget(app_description, alignment=Qt.AlignCenter)
        self.welcome_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.welcome_layout)
        app_title.setObjectName("AppTitle")
        app_description.setObjectName("AppDescription")
        self.layout.setStretch(0, 2)
        self.layout.setStretch(1, 7)
        self.add_inputs(input_area)
        self.add_tabs(plot_area)

    def add_inputs(self, input_area):
        input_widget = QWidget()
        self.input_layout = QVBoxLayout(input_widget)
        input_settings = {
            "Initial Parameters": {"is_visible": False},
            "Spin Parameters": {"is_visible": False},
            "Environment Variables": {"is_visible": False},
            "Simulation Settings": {"is_visible": False},
        }

        for input_setting in input_settings:
            button = QPushButton(input_setting)
            button.setCursor(Qt.PointingHandCursor)
            self.buttons.append(button)
            button.clicked.connect(
                lambda _, p=input_settings[input_setting]: self.btn_clicked(p)
            )
            self.input_layout.addWidget(button)
        self.input_layout.addStretch()
        input_area.setWidget(input_widget)

    def add_tabs(self, plot_area):
        tabs = ["Trajectory", "Velocity", "Acceleration", "Force", "Animation"]
        for tab_name, canvas_name in zip(tabs, self.canvas):
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(getattr(self, canvas_name))
            plot_area.addTab(page, tab_name)

    def make_input_labels(self):
        self.input_parameters = INPUT_PARAMETERS
        self.input_parameters_label = {
            section: {
                key: value
                for key, value in fields.items()
                if key not in ("Top Spin", "Side Spin")
            }
            for section, fields in self.input_parameters.items()
        }
        for button in self.buttons:
            button_text = button.text()
            index = self.input_layout.indexOf(button)
            input_fields = {
                QLabel(input_parameter): QLineEdit()
                for input_parameter in self.input_parameters_label[button_text]
            }
            self.simulation_inputs.update({button_text: input_fields})
            self.collapsible_inputs[button_text] = []

            current_index = index
            for label, text_field in input_fields.items():
                self.input_layout.insertWidget(current_index + 1, label)
                self.input_layout.insertWidget(current_index + 2, text_field)
                self.collapsible_inputs[button_text].append((label, text_field))
                label.setVisible(False)
                text_field.setVisible(False)
                current_index += 2

            if button_text == "Spin Parameters":
                self.top_spin = QRadioButton("Top Spin")
                self.side_spin = QRadioButton("Side Spin")
                self.no_spin = QRadioButton("No Spin")
                self.top_spin.setVisible(False)
                self.side_spin.setVisible(False)
                self.no_spin.setVisible(False)
                top_spin_value = QLineEdit()
                side_spin_value = QLineEdit()
                no_spin_value = QLineEdit()
                self.top_spin.toggled.connect(self.radio_button_click)
                self.side_spin.toggled.connect(self.radio_button_click)
                self.no_spin.toggled.connect(self.radio_button_click)
                self.simulation_inputs[button_text].update(
                    {
                        self.top_spin: top_spin_value,
                        self.side_spin: side_spin_value,
                    }
                )
                self.collapsible_inputs[button_text].extend(
                    [
                        (self.top_spin, top_spin_value),
                        (self.side_spin, side_spin_value),
                        (self.no_spin, no_spin_value),
                    ]
                )
                self.input_layout.insertWidget(current_index + 1, self.top_spin)
                self.input_layout.insertWidget(current_index + 2, self.side_spin)
                self.input_layout.insertWidget(current_index + 3, self.no_spin)

    def add_status_bar(self):
        self.status = self.statusBar()
        self.status.showMessage("Welcome to SpinFlight!!!")

    def btn_clicked(self, input_parameter):
        is_visible = input_parameter["is_visible"]
        button = app.sender()
        button_text = button.text()

        for label, text_field in self.collapsible_inputs[button_text]:
            if not isinstance(label, QRadioButton):
                text_field.setVisible(not is_visible)
            label.setVisible(not is_visible)

        input_parameter["is_visible"] = not is_visible

    def radio_button_click(self):
        for radio, lineedit in self.simulation_inputs["Spin Parameters"].items():
            if not isinstance(radio, QRadioButton):
                continue
            if self.no_spin.isChecked():
                lineedit.setText("0")
                continue
            if radio.isChecked():
                lineedit.setText("1")
            else:
                lineedit.setText("0")

    def simulate(self):
        reset_canvas(self)
        simulate_data(self)

    def reset_button(self):
        reset_canvas(self)
        self.magnus_data = {}
        for input_fields in self.simulation_inputs.values():
            for label, text_field in input_fields.items():
                if isinstance(label, QRadioButton):
                    label.setAutoExclusive(False)
                    label.setChecked(False)
                    label.setAutoExclusive(True)
                text_field.clear()
        self.status.showMessage("Data has been reset", 3000)
        default_msg(self)


def main():
    main_window = SpinFlight()
    main_window.show()
    app.exec_()
