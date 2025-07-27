import numpy as np
from scipy.interpolate import CubicSpline
import struct

#choose one file , comment all others


x = np.array([0, 20, 42, 54, 64])
y = np.array([0, 471, 864, 973, 1023])
offsets=[0x00C9E25A,0x00C9E362,0x00C9E46A,  28837514, 28837778, 28838042]
filename='com.qti.tuned.star_semco_s5kgn2_wide.bin'

#x = np.array([0, 5, 25, 43, 64])
#y = np.array([0, 163, 614, 830, 1023])
#offsets=[0x0058B6F2,0x0058B7FA,0x0058B902]
#filename='com.qti.tuned.star_semco_imx586_ultra.bin'


#x = np.array([0, 11, 22, 46, 64])
#y = np.array([0, 154, 352,788 , 1023])
#offsets=[0x003BDF8E,0x003BE096,0x003BE19E,   3990686, 3990950, 3991214]
#filename='com.qti.tuned.star_semco_imx586_tele.bin'





# Create cubic spline
spline = CubicSpline(x, y, bc_type='natural')


def interpolate(value):
    return spline(value)


x_vals = np.linspace(0, 64, 65)
y_vals = interpolate(x_vals)


lin_vals= np.linspace(0, 1023, 65)




def write_floats_to_file(filename, y_vals, offset):
    with open(filename, 'r+b') as f:
        f.seek(offset)
        for val in y_vals:
            # float 4-byte little-endian
            f.write(struct.pack('<f', val))

def read_floats_from_file(filename, offset, count):
    floats = []
    with open(filename, 'rb') as f:
        f.seek(offset)
        for _ in range(count):
            data = f.read(4)
            if len(data) < 4:
                raise EOFError("Not enough data for reading float")
            val = struct.unpack('<f', data)[0]
            floats.append(val)
    return floats



for offset in offsets:
  write_floats_to_file(filename, y_vals, offset)

