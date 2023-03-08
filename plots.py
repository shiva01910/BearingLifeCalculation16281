from cProfile import label
from matplotlib import pyplot as plt
import numpy as np
import os
import pathlib
import math

def run_plots(bearing):
    fig, axs = plt.subplots(2)
    fig.set_figheight(5)
    fig.set_figwidth(12)
    for item in range(bearing.num_rollers):
        if not(np.isnan(bearing.bearing_model['contact_stresses_inner_array'][item,:]).all()):
            axs[0].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_inner_array'][item,:], label=round(bearing.roller_model['roller_positions'][item], 1))
    # axs[0].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_inner_array'][1,:], label=round(bearing.roller_model['roller_positions'][1], 1))
    # axs[0].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_inner_array'][3,:], label=round(bearing.roller_model['roller_positions'][3], 1))
    # axs[0].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_inner_array'][5,:], label=round(bearing.roller_model['roller_positions'][5], 1))
            axs[0].grid(True)
            axs[0].legend(bbox_to_anchor=(1.0, 1.0))
            axs[0].set_title('Inner Raceway Contact Stress')

            axs[1].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_outer_array'][item,:], label=round(bearing.roller_model['roller_positions'][item], 1))
    # axs[1].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_outer_array'][1,:], label=round(bearing.roller_model['roller_positions'][1], 1))
    # axs[1].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_outer_array'][3,:], label=round(bearing.roller_model['roller_positions'][3], 1))
    # axs[1].plot(bearing.lamina_model['lamina_positions'], bearing.bearing_model['contact_stresses_outer_array'][5,:], label=round(bearing.roller_model['roller_positions'][5], 1))
            axs[1].grid(True)
            axs[1].legend(bbox_to_anchor=(1.0, 1.0))
            axs[1].set_title('Outer Raceway Contact Stress')

    plt.xlabel("Roller position(mm)")
    plt.ylabel("Contact Stress (Mpa)")

    # save as images
    outContactStress = pathlib.Path(os.getcwd()) / 'outfig' / 'Contact_Stress'

    plt.savefig(outContactStress, dpi=100)
    #plt.show()
    plt.close()



    # Polar Plot
    for item in range(len(bearing.roller_model['roller_loads'])):
        if isinstance(bearing.roller_model['roller_loads'][item], complex):
            bearing.roller_model['roller_loads'][item] = 0

    bearing.roller_model['roller_positions'], bearing.roller_model['roller_loads']  = \
            (list(t) for t in zip(*sorted(zip(bearing.roller_model['roller_positions'], bearing.roller_model['roller_loads'])))) 
    r = (np.nan_to_num(bearing.roller_model['roller_loads'])).tolist()
    r.append(r[0])
    theta = [item * math.pi / 180 for item in bearing.roller_model['roller_positions']] 
    theta.append(2 * math.pi)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta, r)
    ax.grid(True)

    ax.set_title("Roller Loads", va='bottom')
    rollerLoads = pathlib.Path(os.getcwd()) / 'outfig' / 'Roller_loads'

    plt.savefig(rollerLoads, dpi=100)
    #plt.show()
    plt.close()


    # Roller Profile plot
    profile_data = [i * 1000 for i in bearing.profile_data]
    plt.plot(bearing.lamina_model['lamina_positions'], profile_data, label='Roller Profile')
    plt.xlabel("Roller distance(mm)")
    plt.ylabel("Profile (um)")
    plt.title("Roller Profile")
    plt.grid(True)
    profile = pathlib.Path(os.getcwd()) / 'outfig' / 'Profile'
    plt.savefig(profile, dpi=100)
    plt.close()



    