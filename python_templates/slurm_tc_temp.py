import numpy as np
import sys
import os

chan_index = list(sys.argv)[1]
data_loc = '{data_loc}' % int(chan_index)

data = np.load(data_loc, dtype='{dtype}')

thresh_multi = {thresh_multi}
std_method = {std_method}

pol = {polarity}

if std_method == 'std':
    threshold = np.std(chan)
elif std_method == 'quian':
    threshold = np.median(abs(chan)/0.6745)
elif std_method == 'rms':
    threshold = np.sqrt(np.mean(chan**2))

std = thresh_multi*threshold
if pol == 'neg':
    chan = -chan
elif pol == 'both':
    chan = abs(chan)
elif pol == 'pos':
    pass

inter_spike_window = {inter_spike_window}
prev_spike = -inter_spike_window
spike_times = []
for index, i in enumerate(data):
    if i >= std and index - prev_spike > inter_spike_window:
        spike_index = index + np.argmax(data[index:index+inter_spike_window])
        spike_times.append(spike_index)
np.save(data_loc.split('.npy')[1]+'_tcs.npy', spike_times)
