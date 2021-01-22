
import os
from pathlib import Path


def get_default_slurm_params():
    params = {
        'job_name':'egg',
        'output':'/home/camp/warnert/working/TEMP',
        'ntasks':1,
        'array':0,
        'time':'24:00:00',
        'memory':'50G',
        'partition':'cpu',
        'enviroment':'intan'
    }


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

def get_default_tc_params():
    params = {
        'output':'/home/camp/warnert/working/TEMP',
        'data_type':'np.uint16',

    }
    
def slurm_tcs(data_loc, data_shape, order='F', sds=4, pol='neg'):
    source_dir = Path(Path(__file__).parent)
    python_txt = open(os.path.join(source_dir, 'slurm_tc_temp.py'), 'r').read()
    python_txt = python_txt.format(
        data_loc=data_loc,

    )
    
