import nltk
nltk.data.path.append("/NOBACKUP/nltk_data")

config = {
	'io_timeout' : 10,
	# 'system_description_file' : './system_configs/echo_system.py'
	# 'system_description_file' : './system_configs/echo_training.py'
	# 'system_description_file' : './system_configs/hred_system.py'
	# 'system_description_file' : './system_configs/pomdp_system.py'

	'system_description_file' : './system_configs/retrieval_model_system.py'
}