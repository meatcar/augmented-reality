import numpy as np

class QuaternionLibrary:
	"""
	Contains functions relevant to the AHRS algorithm.
	"""

	def quaternProd(self, a, b):
		"""
		calculate the quaternion product for given quaternions a, b.
		"""

		ab = np.array([0, 0, 0, 0])
		ab[0] = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
		ab[1] = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
		ab[2] = a[0] * b[2] - a[1] * b[3] + a[2] * b[0] + a[3] * b[1]
		ab[3] = a[0] * b[3] + a[1] * b[2] - a[2] * b[1] + a[3] * b[0]

		return ab

	def quatern2rotMat(self, q):
		"""
		convert the quaternion orientation to a rotation matrix.
		"""

		R = np.zeros(shape=(3,3))

		R[0,0] = 2 * q[0]**2 - 1 + 2 * q[1]**2
		R[0,1] = 2 * (q[1] * q[2] + q[0] * q[3])
		R[0,2] = 2 * (q[1] * q[3] - q[0] * q[2])

		R[1,0] = 2 * (q[1] * q[2] - q[0] * q[3])
		R[1,1] = 2 * q[0]**2 - 1 + 2 * q[2]**2
		R[1,2] = 2 * (q[2] * q[3] + q[0] * q[1])
		
		R[2,0] = 2 * (q[1] * q[3] + q[0] * q[2])
		R[2,1] = 2 * (q[2] * q[3] - q[0] * q[1])
		R[2,2] = 2 * q[0]**2 - 1 + 2 * q[3]**2

		return R
