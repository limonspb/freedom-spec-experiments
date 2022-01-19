from tkinter import Y
import pandas as pd
import matplotlib.pyplot as plt
from find_step import find_first_step_index
from find_step import find_step_up_index

step_to_test = 0

#files = ["old_cnhl_30C_1", "old_cnhl_30C_2", "old_tattu_1", "old_tattu_2"]

#files = ["533_battery1_test1", "old_tattu_1"]
#files = ["cnhl_70c_battery1_test1", "old_tattu_1"]

#files = ["533_battery1_test1", "cnhl_70c_battery1_test1"]
#files = ["533_battery2_test1", "cnhl_70c_battery2_test1"]

#files = ["533_battery1_test1", "533_battery1_test2", "533_battery1_test3"]
#files = ["533_battery2_test1", "533_battery2_test2", "533_battery2_test3"]

#files = ["533_battery1_test1", "533_battery2_test1"]

#files = ["cnhl_70c_battery1_test1", "cnhl_70c_battery1_test2", "cnhl_70c_battery1_test3"]
#files = ["cnhl_70c_battery2_test1", "cnhl_70c_battery2_test2", "cnhl_70c_battery2_test3"]

#files = ["heated_NOT_battery", "heated_115F_battery"]

#files = ["533_battery1_full_throttle", "cnhl_70c_battery1_full_throttle"]

#files = ["motor_temp_test\\cold_1", "motor_temp_test\\not_cold_1"]
#files = ["motor_temp_test\\cold_2", "motor_temp_test\\not_cold_2"]
#files = ["motor_temp_test\\cold_3", "motor_temp_test\\not_cold_3"]

#files = ["533_battery1_full_throttle", "cnhl_70c_battery1_full_throttle", "ovonic_full_throttle", "old_tattu_full_throttle"]

files = ["ovonic_full_throttle", "533_battery1_full_throttle", "black_cnhl_30c_old_full_throttle", "old_tattu_full_throttle", "cnhl_70c_battery1_full_throttle"]

#dividers = [166, 206]
erpm_multiplier = 100 * 2 / 14

throttle_column_name = "rcCommand[3]"
moving_average_rpm_window = 100
moving_average_voltage_window = 100
time_divider = 1000000
time_column_name = "time"
voltage_column_name = "vbatLatest"

motor_columns = []
for motor_index in range(4):
    motor_columns.append('debug[{}]'.format(motor_index))

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

file_index = 0
for file_name in files:
    file_data = pd.read_csv('logs\\day1\\' + file_name + '.BBL.csv', skiprows = 93)
    x = file_data["time"] / time_divider
    index_of_step = find_step_up_index(file_data[throttle_column_name], step_to_test)
    x = x - x[index_of_step]
    y = 0
    for motor_column in motor_columns:
        y += file_data[motor_column]

    y /= (4.0) / erpm_multiplier

    if ("dividers" in locals()):
        y /= dividers[file_index]

    y = y.rolling(moving_average_rpm_window).mean()
    ax1.plot(x, y, label = file_name)

    voltage = file_data[voltage_column_name] / 100 / 3
    voltage = voltage.rolling(moving_average_voltage_window).mean()

    ax1.set(xlabel='time (sec)', ylabel='RPM')
    ax2.set(xlabel='time (sec)', ylabel='Voltage')


    ax2.plot(x, voltage, label = file_name)

    file_index += 1

ax1.legend()
ax2.legend()

previous_y_click = 0

def onclick(event):
    global previous_y_click
    percentage = (event.ydata / previous_y_click - 1) * 100
    square_percentage = (event.ydata**2 / previous_y_click**2 - 1) * 100
    print("Bigger by {:.2f}%".format(percentage))
    print("Square bigger by {:.2f}%".format(square_percentage))

    previous_y_click = event.ydata

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
