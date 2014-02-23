import numpy as np

class MahonyAHRS:
	"""
	An implementation of Mahony's AHRS algorithm. Details of the algorithm
	and paper are available here.

	http://www.x-io.co.uk/node/8#open_source_ahrs_and_imu_algorithms

	The class structure is adapted from Madgwick's matlab code.
	"""

	"""
	global variables.
	"""
	#---------------------------------------------------------------------------
	SamplePeriod = 1/256.0

	# output quaternion describing the Earth relative to the sensor.
	Quaternion = [1, 0, 0, 0]

	# algorithm proportional gain.
	Kp = 1

	# algorithm integral gain.
	Ki = 0

	# integral error.
	eInt = [0, 0, 0]
	#---------------------------------------------------------------------------

	"""
	public methods.
	"""
	#---------------------------------------------------------------------------

	def __init__(self, *args):
		"""

		"""

		for i in range(0, len(args), 2):
			if args[i] == "SamplePeriod":
				self.SamplePeriod = args[i + 1]
			elif args[i] == "Quaternion":
				self.Quaternion = args[i + 1]
			elif args[i] == "Kp":
				self.Kp = args[i + 1]
			elif args[i] == "Ki":
				self.Ki = args[i + 1]

	def UpdateIMU(self, Gyroscope, Accelerometer, quaternProd):
		"""

		"""

		q = np.array(self.Quaternion)

		if np.linalg.norm(Accelerometer) == 0:
			return

		# normalize the accelerometer measurement.
		Accelerometer = Accelerometer / np.linalg.norm(Accelerometer)

		# estimate the direction of gravity and magnetic flux.
		v = [2*(q[1]*q[3] - q[0]*q[2]), \
			 2*(q[0]*q[1] + q[2]*q[3]), \
			 q[0]**2 - q[1]**2 - q[2]**2 + q[3]**2]

		# error is sum of cross product between estimated direction and measured
		# direction of field.
		e = np.cross(Accelerometer, v)

		# note that self.eInt is a numpy array so any multiplications by
		# constants will be carried out element wise.
		if self.Ki > 0:
			self.eInt = np.add(self.eInt, e) * self.SamplePeriod
		else:
			self.eInt = np.array([0, 0, 0])

		# apply feedback terms.
		a = self.Kp * e
		b = self.eInt * self.Ki
		c = np.add(a, b)
		Gyroscope = np.add(Gyroscope, c)

		# compute the rate of change of quaternion.
		qDot = 0.5*quaternProd(q, [0, Gyroscope[0], Gyroscope[1], Gyroscope[2]])

		# integrate to yield quaternion.
		q = q + qDot * self.SamplePeriod

		# normalize the quaternion.
		self.Quaternion = q / np.linalg.norm(q)

