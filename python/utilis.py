from PyQt5.QtWidgets import QRadioButton, QTabWidget
from PyQt5.QtCore import QTimer, Qt
from python.calculation import run_magnus_simulation
from python.plot import plot_calculated_data
from config import INPUT_LIMITS


class InputError(Exception):
    pass


class RangeError(Exception):
    pass


def validate_input(parameter_limit, value):
    low = parameter_limit["minimum"]
    high = parameter_limit["maximum"]
    unit = parameter_limit["unit"]
    if not (low <= value <= high):
        raise RangeError(
            f"{parameter_limit['parameter']} should be in range [{low} to {high}]{unit}"
        )


def simulate_data(self):
    try:
        for input_parameter, data_item in self.simulation_inputs.items():
            for label, text_edit in data_item.items():
                input_variable = self.input_parameters[input_parameter][label.text()]
                if text_edit.text() == "":
                    if (
                        isinstance(label, QRadioButton)
                        and not self.side_spin.isChecked()
                        and not self.top_spin.isChecked()
                        and not self.no_spin.isChecked()
                    ):
                        raise Exception(f"Please select a spin type!")

                    raise InputError(f"Missing Input for {label.text()}")
                validate_input(INPUT_LIMITS[input_variable], float(text_edit.text()))
                self.magnus_data[input_variable] = float(text_edit.text())
        self.status.showMessage("Simulation Completed!!")
        self.calculated_data = run_magnus_simulation(self.magnus_data)
        add_plot_area(self)
        plot_calculated_data(self)

    except InputError as e:
        self.status.showMessage(str(e), 3000)
        default_msg(self)
    except RangeError as e:
        self.status.showMessage(str(e), 3000)
        default_msg(self)
    except ValueError:
        self.status.showMessage(f"Invalid Input! Please Enter a Numeric value!", 3000)
        default_msg(self)
    except Exception as e:
        self.status.showMessage(str(e), 3000)
        default_msg(self)


def default_msg(self):
    QTimer.singleShot(3000, lambda: self.status.showMessage("Welcome to SpinFlight!!!"))


def add_plot_area(self):
    if self.plot_layout not in [
        self.layout.itemAt(i).layout() for i in range(self.layout.count())
    ]:
        self.welcome_layout.setParent(None)
        self.layout.addLayout(self.plot_layout)
        self.layout.setStretch(0, 2)
        self.layout.setStretch(1, 7)
        tab_bar = self.findChild(QTabWidget).tabBar()
        tab_bar.setCursor(Qt.PointingHandCursor)
