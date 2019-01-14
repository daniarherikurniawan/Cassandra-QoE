import random
import numpy as np
import sys
import pandas as pd
import time


def get_median(priority_level, load_data):

    t_array = load_data[priority_level]
    t_array = np.array(t_array)
    median_ans = np.median(t_array)
    return median_ans

def get_average(priority_level, load_data):
    t_array = load_data[priority_level]
    t_array = np.array(t_array)
    average_ans = np.average(t_array)
    return average_ans

def get_random(priority_level, load_data): #if fifo, priority_level = 0
    t_array = load_data[priority_level]
    random.seed(time.time())
    random_answer = random.choice(t_array)
    return random_answer