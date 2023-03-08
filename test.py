from cmath import cos, sin

from numpy import half
import roller_bearing
import math
import numpy as np


bearing = roller_bearing.Bearing(radial_load=1.1773e5, misalignment=-1.923, dynamic_capacity=2.37e5, num_rollers=17, pitch_diameter=95.5, 
                    length_roller=24, effective_length_roller=22.63,
                    roller_end_radius=[0.74, 0.63], roller_diameter=16, contact_angle=30.139,
                    posisson_ratio=0.3, elastic_mod=2.05e5, radial_clearance=0.0, bearing_type=1, num_laminas=151)
bearing.run_analysis()

contact_angle = 30.139 * math.pi / 180
taper_angle = 8.7 * math.pi / 180
half_taper = (taper_angle / 2)
inner_race_angle = contact_angle - taper_angle
gamma_avg_angle = (contact_angle + inner_race_angle) / 2
big_end_diameter = 2 * (bearing.length_roller / 2) * math.sin(taper_angle / 2) + bearing.roller_diameter
# assumptions
u, v, phi = -6, -6, 0.005
rm = big_end_diameter * math.sin(gamma_avg_angle) / 2 / math.tan(half_taper)
e = (rm - big_end_diameter * math.cos(gamma_avg_angle) / 2 - bearing.length_roller * math.sin(inner_race_angle)) * math.tan(contact_angle) + \
        big_end_diameter * math.sin(gamma_avg_angle)/ 2 - bearing.length_roller * math.cos(inner_race_angle) / 2

delta_x, delta_y, delta_z = 34.67 / 1000, 12.87 / 1000, 53.91 / 1000
misaligned_x, misaligned_y = 0.95059 / 1000, 2.016 / 1000

E = bearing.elastic_mod / (1 - bearing.poisson_ratio ** 2)
eff_len = (bearing.length_roller - (bearing.roller_end_radius[0] + bearing.roller_end_radius[1]) * math.cos(half_taper))
Rs = 115

flange_to_normal = 3.410 
flange_angle = (180 - (90 + flange_to_normal + (90 - gamma_avg_angle * 180 / math.pi))) * math.pi / 180

lambda_roller = np.arcsin(big_end_diameter / 2 / Rs)


pwf_x_roll = -Rs * math.sin(gamma_avg_angle - flange_angle)
pwf_y_roll = Rs * math.cos(lambda_roller) - Rs * math.cos(gamma_avg_angle - flange_angle)

kappa = (rm / Rs - math.sin(half_taper) * math.cos(lambda_roller)) / math.sin(flange_angle)
cf = 1

while 1:
    x_force, y_force, z_force = 0, 0, 0
    for angle in bearing.roller_model['roller_positions']:
        angle = angle * math.pi / 180
        q_i_sum, q_e_sum, q_f_sum = 0, 0, 0
        for index, position in enumerate(bearing.lamina_model['lamina_positions']):
            corner_pos = position + bearing.length_roller / 2
            profile_coeff_roller = (rm / math.sin(gamma_avg_angle) - corner_pos) * math.tan(half_taper) + bearing.profile_data[index]
            profile_coeff_inner = (rm / math.sin(gamma_avg_angle) - corner_pos) * math.tan(half_taper) + 0
            profile_coeff_outer = (rm / math.sin(gamma_avg_angle) - corner_pos) * math.tan(half_taper) + 0

            re_x = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_outer * math.cos(gamma_avg_angle)) * math.cos(angle)
            re_y = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_outer * math.cos(gamma_avg_angle)) * math.sin(angle)
            re_z = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_outer * math.cos(gamma_avg_angle)) / math.tan(90 * math.pi / 180  - angle)

            ri_displaced_x = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_inner * math.cos(gamma_avg_angle)) * math.cos(angle) + delta_x + \
                            misaligned_y * (e + corner_pos * math.cos(gamma_avg_angle) - profile_coeff_inner * math.sin(gamma_avg_angle))
            ri_displaced_y = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_inner * math.cos(gamma_avg_angle)) * math.sin(angle) + delta_y + \
                            misaligned_x * (e + corner_pos * math.cos(gamma_avg_angle) - profile_coeff_inner * math.sin(gamma_avg_angle))
            ri_displaced_z = (rm - corner_pos * math.sin(gamma_avg_angle) + profile_coeff_inner * math.cos(gamma_avg_angle)) / math.tan(90 * math.pi / 180  - angle) + delta_z

            shivam2 = Rs * math.sin(flange_angle)
            shivam3 = Rs * math.cos(lambda_roller) * math.sin(gamma_avg_angle)
            shivam1 = (rm - Rs * math.cos(lambda_roller) * math.sin(gamma_avg_angle) + Rs * math.sin(flange_angle)) * math.cos(angle)

            rf_displaced_x = (rm - Rs * math.cos(lambda_roller) * math.sin(gamma_avg_angle) + Rs * math.sin(flange_angle)) * math.cos(angle) + delta_x + \
                            misaligned_y * (e + Rs * math.cos(lambda_roller) * math.cos(gamma_avg_angle) - Rs * math.cos(flange_angle))
            rf_displaced_y = (rm - Rs * math.cos(lambda_roller) * math.sin(gamma_avg_angle) + Rs * math.sin(flange_angle)) * math.sin(angle) + delta_y + \
                            misaligned_x * (e + Rs * math.cos(lambda_roller) * math.cos(gamma_avg_angle) - Rs * math.cos(flange_angle))
            rf_displaced_z = (rm - Rs * math.cos(lambda_roller) * math.sin(gamma_avg_angle) + Rs * math.sin(flange_angle)) / math.tan(90 * math.pi / 180  - angle) + delta_z 
                            
                            
            de = profile_coeff_roller * math.cos(half_taper) + corner_pos * math.sin(half_taper) + rm * math.cos(contact_angle) + e * math.sin(contact_angle) - \
                (re_x * math.cos(angle) + re_y * math.sin(angle)) * math.cos(contact_angle) - re_z * math.sin(contact_angle)
            di = profile_coeff_roller * math.cos(half_taper) + corner_pos * math.sin(half_taper) - rm * math.cos(inner_race_angle) - e * math.sin(inner_race_angle) + \
                (ri_displaced_x * math.cos(angle) + ri_displaced_y * math.sin(angle)) * math.cos(inner_race_angle) + ri_displaced_z * math.sin(inner_race_angle)


            df = -pwf_x_roll * math.sin(gamma_avg_angle - flange_angle) - pwf_y_roll * math.cos(gamma_avg_angle - flange_angle) + rm * math.sin(flange_angle) - \
                e * math.cos(flange_angle) - (rf_displaced_x * math.cos(angle) + rf_displaced_y * math.sin(angle)) * math.sin(flange_angle) + \
                rf_displaced_z * math.cos(flange_angle)

            delta_e = u * math.cos(half_taper) + v * math.sin(half_taper) + (corner_pos * math.cos(half_taper) - profile_coeff_roller * math.sin(half_taper)) * phi + de
            delta_i = -u * math.cos(half_taper) + v * math.sin(half_taper) - (corner_pos * math.cos(half_taper) - profile_coeff_roller * math.sin(half_taper)) * phi + di
            delta_f = -u * math.sin(gamma_avg_angle - flange_angle) - v * math.cos(half_taper - flange_angle) + \
                        (pwf_x_roll * math.cos(gamma_avg_angle - flange_angle) - pwf_y_roll * math.sin(gamma_avg_angle - flange_angle)) * phi + df

            q_i = math.pi * E * eff_len * \
                    ((delta_i / 7.358 / eff_len) ** 1.11)
            q_e = math.pi * E * eff_len * \
                    ((delta_e / 7.358 / eff_len) ** 1.11)
            xxx = math.pow((delta_f / Rs), 1.5)
            q_f = cf * E * (Rs ** 2) * math.pow((delta_f / Rs), 1.5)
            q_i_sum += q_i
            q_e_sum += q_e
            q_f_sum += q_f

        lhs = (q_i_sum - q_e_sum) * math.cos(half_taper)
        rhs = q_f_sum * math.sin(gamma_avg_angle - flange_angle)
        print('done')
        
        x_force += q_i_sum * math.cos(angle)
        print('done')
    
