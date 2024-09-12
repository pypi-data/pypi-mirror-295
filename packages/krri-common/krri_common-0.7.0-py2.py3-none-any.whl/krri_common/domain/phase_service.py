import math
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import numpy as np
import tiledb
from tiledb import ArraySchema

os.environ['TILEDB_NUM_THREADS'] = '4'


class PhaseService:

	def __init__(self, dir_path: str):
		self._dir_path = dir_path

	def batch_process_phase(self, measurement_time: datetime, data_batch: np.ndarray) -> str:
		"""
		batch process phase data
		:return: uri
		"""
		data_count = data_batch.shape[0]
		sample_count = data_batch.shape[1]

		# Define domain
		schema = self._create_array_schema(data_count, sample_count)
		file_time = str(measurement_time.strftime("%Y%m%d-%H%M%S%f"))
		uri = os.path.join(self._dir_path, f'{file_time}.tdb')
		fin_uri = os.path.join(self._dir_path, f'{file_time}.fin')
		tiledb.DenseArray.create(uri, schema)
		with tiledb.DenseArray(uri, mode='w') as A:
			A[:, :] = data_batch
		with open(fin_uri, 'w') as f:
			f.write('')
		return uri

	def _create_array_schema(self, data_count, sample_count) -> ArraySchema:
		row_tile = pow(10, int(math.log10(data_count)))
		col_tile = pow(10, int(math.log10(sample_count)))
		row_dim = tiledb.Dim(name="rows", domain=(0, data_count - 1), tile=row_tile if data_count > 1000 else 100,
							 dtype=np.int32)
		col_dim = tiledb.Dim(name="cols", domain=(0, sample_count - 1), tile=col_tile, dtype=np.int32)
		domain = tiledb.Domain(row_dim, col_dim)
		# Define attribute
		attr = tiledb.Attr(name="value", dtype=np.float64)
		# Define array schema
		schema = tiledb.ArraySchema(domain=domain, sparse=False, attrs=[attr])
		return schema

	def get_phase(self, start_time: datetime, time_range: int, offsets: List[int] = None) -> (float, np.ndarray):
		current_files = os.listdir(self._dir_path)
		current_files = list(filter(lambda x: x.endswith('.tdb'), current_files))
		current_files = sorted(current_files)
		target_time = start_time + timedelta(seconds=time_range - 1)
		phase_file_names = []
		for file in current_files:
			try:
				file_name_without_extension = Path(file).stem
				file_time = datetime.strptime(file_name_without_extension, "%Y%m%d-%H%M%S%f")
				if start_time <= file_time <= target_time:
					phase_file_names.append(file)
					if len(phase_file_names) == time_range:
						break
			except ValueError as e:
				pass
		if len(phase_file_names) < time_range:
			raise Exception("Not enough files")
		array = self.load_phase_from_files(phase_file_names, offsets)
		return start_time, array

	def load_phase_from_files(self, file_names: List[str], offsets: List[int] = None) -> np.ndarray:
		group_of_arrays = [array for array in
						   [self.load_phase_from_file(name, offsets) for name in file_names]]
		return np.vstack(group_of_arrays)

	def load_phase_from_file(self, file_name: str, offsets: List[int] = None) -> np.ndarray:
		with tiledb.DenseArray(os.path.join(self._dir_path, file_name), mode='r') as A:
			if offsets is not None:
				array = A.multi_index[:, offsets]
			else:
				array = A[:, :]
			return array['value']


# def get_phase(self, start_time: datetime, time_range: int, pulse_rate: int) -> (float, np.ndarray):
# 	"""
# 	get phase data from start_time to end_time
# 	:param pulse_rate: pulse rate
# 	:param time_range: retrieve time range
# 	:param start_time: start time
# 	:return: (begin_timestamp, phase data)
# 	"""
# 	# get second
# 	get_file_count_range = time_range + 1
# 	current_files = os.listdir(self._dir_path)
# 	target_time = start_time + timedelta(seconds=get_file_count_range)
# 	filtered_files = []
# 	for file in current_files:
# 		try:
# 			file_name_without_extension = file.split('.')[0]
# 			file_time = datetime.strptime(file_name_without_extension, "%Y%m%d-%H%M%S%f")
# 			if start_time + timedelta(seconds=-1) <= file_time <= target_time:
# 				filtered_files.append(file)
# 				continue
# 		except ValueError as e:
# 			# Not a valid file name
# 			pass
# 	if len(filtered_files) < get_file_count_range:
# 		raise Exception("Not enough files")
# 	sorted_files = sorted(filtered_files)
# 	array = self.phase_load_array_from_files(start_time, pulse_rate, time_range, sorted_files)
# 	return start_time, array

# def phase_load_array_from_files(self, start_time: datetime, pulse_rate: int, time_range: int,
# 								filtered_files: List[str]) -> np.ndarray:
# 	time_unit = 1 / pulse_rate
# 	start_file_time = datetime.strptime(filtered_files[0].split('.')[0], "%Y%m%d-%H%M%S%f")
# 	array = None
# 	for name in filtered_files:
# 		loaded_array = fastnumpyio.load(os.path.join(self._dir_path, name))
# 		if array is None:
# 			array = loaded_array
# 			continue
# 		array = np.concatenate((array, loaded_array), axis=0)
# 	start_index = 0
# 	while True:
# 		compare_time = start_file_time + timedelta(seconds=time_unit * start_index)
# 		if compare_time >= start_time:
# 			break
# 		start_index += 1
# 	return array[start_index:start_index + pulse_rate * time_range, :]


if __name__ == '__main__':
	# PhaseService test
	dir_path = 'D:\\temp'
	phase_service = PhaseService(dir_path)
	# batch_process_phase test
	measurement_time = datetime.now()
	data_batch = np.random.rand(2500, 9000)
	start_time = time.time()
	uri = phase_service.batch_process_phase(measurement_time, data_batch)
	print(f"Data write time: {time.time() - start_time:.4f} sec")
	# Single file load test

	start_time = time.time()
	entire_phase = phase_service.load_phase_from_file(uri)
	print(f'entire_phase: {entire_phase.shape}')
	print(f"Data read time: {time.time() - start_time:.4f} sec")

	# Single file load with offset test
	offsets = [1, 2, 3, 4, 5]
	start_time = time.time()
	phase = phase_service.load_phase_from_file("E:\\tiledb\\20240625-103813000384.tdb", offsets)
	print(f'phase: {phase.shape}')
	print(f"Data read time: {time.time() - start_time:.4f} sec")

	measurement_time, phase = phase_service.get_phase(measurement_time, 1, offsets)
	print(f'phase: {phase.shape}')
	print(f"Data read time: {time.time() - start_time:.4f} sec")

# # Multiple file load test
# file_names = ['20240826-104338043286.tdb', '20240826-104339043286.tdb', '20240826-104340043286.tdb',
# 			  '20240826-104341043286.tdb', '20240826-104342043286.tdb']
# start_time = time.time()
# entire_phase = phase_service.load_phase_from_files(file_names)
# print(f'entire_phase: {entire_phase.shape}')
# print(f"Data read time: {time.time() - start_time:.4f} sec")
# # Multiple file load with offset test
# start_time = time.time()
# phase = phase_service.load_phase_from_files(file_names, offsets)
# print(f'phase: {phase.shape}')
# print(f"Data read time: {time.time() - start_time:.4f} sec")
# 
# # get_phase test
# start_time = time.time()
# measurement_time = datetime.strptime("20240826-104338043286", "%Y%m%d-%H%M%S%f")
# measurement_time, phase = phase_service.get_phase(measurement_time, 5, offsets)
# print(f'phase: {phase.shape}')
# print(f"Data read time: {time.time() - start_time:.4f} sec")
