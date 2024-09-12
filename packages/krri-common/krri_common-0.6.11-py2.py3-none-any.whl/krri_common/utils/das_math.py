from numpy import ndarray


class DasMath:
	@staticmethod
	def convert_diff_phase_to_phase(diff_phase: ndarray, b, a) -> ndarray:
		"""
		convert diff phase to phase
		:param diff_phase: diff phase
		:return: phase
		"""
		import numpy as np
		from scipy import signal
		diff_phase = np.ascontiguousarray(diff_phase)
		t_phase = np.cumsum(diff_phase, axis=0)
		t_phase = t_phase * (np.pi / 2 ** 15)
		filtered_t_phase = signal.filtfilt(b, a, t_phase, axis=0)
		return filtered_t_phase
