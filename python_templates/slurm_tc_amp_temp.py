import numpy as np
import h5py
import sys

data_loc = '{data_loc}'
num_of_chans = int('{num_of_chans}')
out_loc = '{out_loc}'


if '.npy' in data_loc:
    data = np.memmap(data_loc, dtype={data_type})
    data = data.reshape(num_of_chans, int(len(data)/num_of_chans), order='{order')

elif '.h5' in data_loc:
    file = h5py.File(data_loc)
    data = file['sig']

chan_index = int(list(sys.argv)[1])

chan = data[chan_index]

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
for index, i in enumerate(chan):
    if i >= std and index - prev_spike > inter_spike_window:
        spike_index = index + np.argmax(chan[index:index+inter_spike_window])
        spike_times.append(spike_index)
np.save(os.path.join(out_loc, 'chan_%d_spike_times.npy' % chan), spike_times)