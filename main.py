import roller_bearing
import plots
import out






bearing = roller_bearing.Bearing(radial_load=1.1773e5, misalignment=-1.923, dynamic_capacity=2.37e5, num_rollers=17, pitch_diameter=95.5, 
                    length_roller=24, effective_length_roller=22.63,
                    roller_end_radius=[0.74, 0.63], roller_diameter=16, contact_angle=30.139,
                    posisson_ratio=0.3, elastic_mod=2.05e5, radial_clearance=-0.035, bearing_type=1, num_laminas=151)
bearing.run_analysis()
print('done')
