import serial
from threading import Thread

class MPUWrapper(object):
    def __init__(self, device, speed, data_callback):
        # launches a daemon thread to handle data from the MPU.
        self.device = device
        self.speed = speed
        self.callback = data_callback
        
        self.t = Thread(target=self.on_data)
        self.t.daemon = True
        self.t.start()

    def on_data(self): 
        self.se = serial.Serial(self.device, self.speed, timeout=2)

        while True:
            try:
                l = self.se.readline()
                l = l.decode()
                data = l.split(" ")
                if len(data) == 1:
                    print("waiting for MPU to broadcast ...")

                l_acc = [float(data[0]), float(data[1]), float(data[2])]
                r_acc = [float(data[3]), float(data[4]), float(data[5])]
                r_gyr = [float(data[6]), float(data[7]), float(data[8])]
                r_mag = [float(data[9]), float(data[10]), float(data[11])]
                c_acc = [float(data[12]), float(data[13]), float(data[14])]
                c_mag = [float(data[15]), float(data[16]), float(data[17])]
                e_ang = [float(data[18]), float(data[19]), float(data[20])]
                r_quat = [float(data[21]), float(data[22]), float(data[23]), float(data[24])]
                c_quat = [float(data[25]), float(data[26]), float(data[27]), float(data[28])]
                fe_ang = [float(data[29]), float(data[30]), float(data[31])]
                res_acc = [float(data[32]), float(data[33]), float(data[34])]

                self.callback(l_acc, r_acc, r_gyr, r_mag, c_acc, c_mag, e_ang, r_quat, c_quat, fe_ang, res_acc)
            except Exception as e:
                # print(e);
                print("")
