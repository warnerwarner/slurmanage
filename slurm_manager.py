
import os
from pathlib import Path
import datetime
import numpy as np

def get_default_slurm_params():
    '''
    Retirms a dictionary of default parameters for the slurm template file

    job_name - The name of the job, default, egg
    output - Location for both the output and error files, default
             /home/camp/warnert/working/TEMP
    ntasks - The number of tasks for the job, default 1
    array - Job array, default 0,
    time - Time requested to complete the job, default
    '''
    params = {
        'job_name':'egg',
        'output':'/home/camp/warnert/working/TEMP',
        'ntasks':1,
        'array':'0',
        'time':'01:00:00',
        'memory':'50G',
        'partition':'cpu',
        'enviroment':'intan'
    }
    return params


def create_slurm_file(python_file_name, file_name='slurm_temp', **kwargs):
    p = get_default_slurm_params()
    for i in kwargs:
        p[i]=kwargs[i]
    output_loc = p['output']+file_name+'_%a.out'
    error_loc = p['output']+file_name+'_%a.err'
    temp_text = open('slurm_template.sh', 'r').read()
    temp_text = temp_text.format(
        job_name=p['job_name'],
        output_loc=output_loc,
        error_loc=error_loc,
        ntasks=p['ntasks'],
        array=p['array'],
        time=p['time'],
        memory=p['memory'],
        partition=p['partition'],
        enviroment=p['enviroment'],
        file_name=python_file_name
    )
    with open(os.path.join(p['output'], file_name+'.sh'), 'w') as f:
        f.write(temp_text)

def get_default_python_tc_params():
    '''
    Returns a dictionary of default parameters for the python template file

    output - Location to save the file and the output to,
             default /home/camp/warnert/working/TEMP
    data_type - The data type of the data, only used if data is saved as binary
                default, np.uint16
    order - The order of the data, either C, or F, only used if data is binary
            default, F
    thresh_multi - The multiple of stds for thresholds to be found, default 4
    std_method - The method to calculate the std, can be std, quian, or rms,
                 default, std
    polarity - The polarity of spikes to be detected, can be pos, neg, or both
               default neg.
    inter_spike_window - The number of samples to be left between consecutive
                         spikes, default, 120
    '''
    params = {
        'output':'/home/camp/warnert/working/TEMP',
        'data_type':'np.uint16',
        'order':'F',
        'thresh_multi':'4',
        'std_method':'std',
        'polarity':'neg',
        'inter_spike_window':'120'
    }
    return params
    
def slurm_tcs_old(data_loc, data_shape, **kwargs):
    '''
    Creates a python and a bash script to launch a series of python processes to
    find threshold crossings, by splitting data up by channel. To find the
    default parameters used call get_default_python_tc_params and
    get_default_slurm_params functions. To change any of these pass them along
    as additional parameters.

    Args:
    data_loc - The location of the data, can either be h5 or binary data type
    data_shape - The shape of the data, channels x time_points
    '''
    source_dir = Path(Path(__file__).parent)
    python_p = get_default_python_tc_params()
    slurm_p = get_default_slurm_params()
    for i in kwargs:
        if i in python_p:
            python_p[i] = kwargs[i]
        elif i in slurm_p:
            slurm_p[i] = kwargs[i]
    python_p['output'] = python_p['output']+'/'+str(datetime.date.today())
    slurm_p['output'] = slurm_p['output'] + '/'+str(datetime.date.today())
    python_txt = open(os.path.join(source_dir, 'slurm_tc_temp.py'), 'r').read()
    python_txt = python_txt.format(
        data_loc=data_loc,
        num_of_chans=data_shape[0],
        out_loc=python_p['output']+'"/slurm_tcs_%d.npy" % chan_index',
        data_type=python_p['data_type'],
        order=python_p['order'],
        thresh_multi=python_p['thresh_multi'],
        std_method=python_p['std_method'],
        polarity=python_p['polarity'],
        inter_spike_window=python_p['inter_spike_window'],

    )
    
def slurm_tcs(data, **kwargs):
    source_dir = Path(Path(__file__).parent)
    python_p = get_default_python_tc_params()
    slurm_p = get_default_slurm_params()
    for i in kwargs:
        if i in python_p:
            python_p[i] = kwargs[i]
        if i in slurm_p:
            slurm_p[i] = kwargs[i]
    python_p['dtype']=type(data[0, 0])
    python_p['output'] = python_p['output'] + '/' + str(datetime.date.today())
    for index, i in enumerate(data):
        np.save(os.path.join(python_p['output'], 'chan_data_%d.npy' % index), i)
    python_p['data_loc']=os.path.join(python_p['output'], 'chan_data_%d.npy') + " % chan_index"
    python_txt = open(os.path.join(source_dir, 'python_templates', 'slurm_c_temp.py'), 'r').read()
    python_txt = python_txt.format(
        data_loc=python_p['data_loc'],
        dtype=python_p['dtype'],
        polarity=python_p['polarity'],
        inter_spike_window=python_p['inter_spike_window'],

    )