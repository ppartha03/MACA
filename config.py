import nltk
nltk.data.path.append("/NOBACKUP/nltk_data")

from mturk.gods import gods_server

config = {
    # 'main_function' : gods_server.main_response,
    # 'main_function' : gods_server.main_scoring,

    'io_timeout' : 5, # For input, in seconds
    'output_queue_timeout' : 0.25, # For output, in seconds

    # 'system_description_file' : './system_configs/echo_system.py'
    # 'system_description_file' : './system_configs/echo_training.py'
    # 'system_description_file' : './system_configs/hred_system.py'
    # 'system_description_file' : './system_configs/pomdp_system.py'
    # 'system_description_file' : './system_configs/retrieval_model_system.py'
    # 'system_description_file' : './system_configs/retrieval_training.py'

    # 'system_description_file' : './system_configs/mturk_collect_response.py'
    'system_description_file' : './system_configs/mturk_scoring.py'
}