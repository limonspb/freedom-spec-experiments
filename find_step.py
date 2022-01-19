import pandas as pd
import matplotlib.pyplot as plt

def find_first_step_index(data):
    index = 0
    for value in data:
        if value > 1500:
            break
        index += 1
    return index

def find_step_up_index(data, step_number):
    index = 0
    current_step_number = 0
    is_currently_up = False

    for value in data:
        if value > 1500 and not is_currently_up:
            is_currently_up = True
            if current_step_number == step_number:
                break
            else:
                current_step_number += 1

        if value < 1500:
            is_currently_up = False

        index += 1

    return index

def find_step_down_index(data, step_number):
    index = 0
    current_step_number = 0
    is_currently_up = False

    for value in data:
        if value < 1500 and is_currently_up:
            is_currently_up = False
            if current_step_number == step_number:
                break
            else:
                current_step_number += 1

        if value > 1500:
            is_currently_up = True

        index += 1

    return index
