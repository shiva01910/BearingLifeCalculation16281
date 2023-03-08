

from numpy import half
import roller_bearing
import math
import numpy as np


bearing = roller_bearing.Bearing(radial_load=76635.9, misalignment=-2.229, dynamic_capacity=2.37e5, num_rollers=17, pitch_diameter=95.5, 
                    length_roller=24, effective_length_roller=22.63,
                    roller_end_radius=[0.74, 0.63], roller_diameter=16, contact_angle=30.139,
                    posisson_ratio=0.3, elastic_mod=2.05e5, radial_clearance=-0.0, bearing_type=1, num_laminas=151)



delta_a, delta_r = 53.91 / 1000, 36.98 / 1000
sigma = (1 / 2) * (1 + (delta_a / delta_r) * math.tan(bearing.contact_angle * math.pi / 180))

#load_distribution_integral = -0.0852 * (sigma ** 4) + 0.5703 * (sigma ** 3) - 1.3343 * (sigma ** 2) + 1.775 * sigma - 0.0771

#load_distribution_integral = 0.134
# theta = math.acos(1 - 2 * sigma)

# f_theta1 = math.pow((1 - (1 - math.cos(-theta)) / 2 / sigma), 1.11) * math.cos(-theta / 3) * 2 * theta
# f_theta1_3 = math.pow((1 - (1 - math.cos(theta / 3)) / 2 / sigma), 1.11) * math.cos(theta / 3) * 6 * theta

# f_theta1_a = math.pow((1 - (1 - math.cos(-theta)) / 2 / sigma), 1.11) * 2 * theta
# f_theta1_3_a = math.pow((1 - (1 - math.cos(theta / 3)) / 2 / sigma), 1.11) * 6 * theta

# integral_r = (1 / 2 / math.pi) * (f_theta1 + f_theta1_3)
# integral_a = (1 / 2 / math.pi) * (f_theta1_a + f_theta1_3_a)

integral_r = 0.26
# q_max = bearing.radial_load / bearing.num_rollers / integral_r / math.cos(bearing.contact_angle * math.pi / 180)
# # q_max_a = 78013.7 / 17 / integral_a / math.sin(bearing.contact_angle * math.pi / 180)
# normal_stiffness = 0.1647 * bearing.elastic_mod * (bearing.effective_length_roller ** (8/9))
# each_roller_deflection = ((bearing.radial_load / bearing.num_rollers  / normal_stiffness / integral_r) ** (1 / 1.11))
# theta = 360 / bearing.num_rollers


each_roller_angular_position, each_roller_loads, each_roller_deflection = [],  [], []
pmax = bearing.radial_load / bearing.num_rollers / integral_r / math.cos(bearing.contact_angle * math.pi / 180)
each_roller_loads.append(pmax)
each_roller_deflection.append(delta_a * math.sin(bearing.contact_angle * math.pi / 180) + delta_r * math.cos(bearing.contact_angle * math.pi / 180))
theta = 360 / bearing.num_rollers
each_roller_angular_position.append(0)
bearing.load_zone = sigma


for item in range(int((bearing.num_rollers - 1)/ 2)):
    angle = (item + 1) * theta * math.pi / 180
    each_roller_angular_position.append((item + 1) * theta)
    each_roller_angular_position.append((bearing.num_rollers - 2 * (item + 1)) * theta + (item + 1) * theta)
    try:
        each_roller_loads.append(pmax* (1 - (1 - math.cos(angle)) / 2 / sigma) ** (1.11))
        each_roller_loads.append(pmax* (1 - (1 - math.cos(angle)) / 2 / sigma) ** (1.11))
        
    except:
        each_roller_loads.append(0)
        each_roller_loads.append(0)
        

    try:
        each_roller_deflection.append(each_roller_deflection[0]* (1 - (1 - math.cos(angle)) / 2 / sigma))
        each_roller_deflection.append(each_roller_deflection[0]* (1 - (1 - math.cos(angle)) / 2 / sigma))
    except:
        each_roller_deflection.append(0)
        each_roller_deflection.append(0)

# Fix the roller loads from complex number to zero
for i in range(len(each_roller_loads)):
    if isinstance(each_roller_loads[i], complex):
        each_roller_loads[i] = 0
    if isinstance(each_roller_deflection[i], complex):
        each_roller_deflection[i] = 0

bearing.roller_model = {
    'roller_positions' : each_roller_angular_position,
    'roller_loads' : each_roller_loads,
    'roller_deflections' : each_roller_deflection
}










bearing.run_analysis_taper()
print('done')