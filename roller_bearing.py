import math
import numpy as np
import out
import plots




# Given Data
# Misalingment, Radial Load

# Bearing Data
# Roller dia, roller length, effective length, roller profile, bearing material properies (Y, posisson ratio), Pitch diameter of bearing

class Bearing:
    def __init__(self, radial_load: float, misalignment: float, dynamic_capacity: float, num_rollers: int, pitch_diameter: float, length_roller: float,
                effective_length_roller: float, roller_end_radius: list, roller_diameter: float, contact_angle: float, posisson_ratio: float, elastic_mod: float, 
                radial_clearance: float, bearing_type: int, num_laminas: int) -> None:
        
        self.radial_load = radial_load
        self.misalignment = misalignment
        self.dynamic_capacity = dynamic_capacity
        self.num_rollers = num_rollers
        self.pitch_diameter = pitch_diameter
        self.length_roller = length_roller
        self.effective_length_roller = effective_length_roller
        self.roller_end_radius = roller_end_radius
        self.roller_diameter = roller_diameter
        self.contact_angle = contact_angle
        self.poisson_ratio = posisson_ratio
        self.elastic_mod = elastic_mod
        self.radial_clearance = radial_clearance
        self.bearing_type = bearing_type
        self.num_laminas = num_laminas




    # Algorithm to calculate load on each roller
    # Alorith based on NASA papaer  (NASA/TM - 2012-217115)
    def calculate_load_on_each_roller(self):
        
        stribeck_number = 5 
        load_distribution_integral = 1 / stribeck_number
        stribeck_number_calculated = 0 
        if self.bearing_type == 1: # Roller bearing
            n = 1.11
        if self.bearing_type == 0: # Ball bearing
            n = 1.5
        while 1:
            normal_stiffness = 0.1647 * self.elastic_mod * (self.effective_length_roller ** (8/9))      
            total_deflection = (self.radial_clearance / 2) + (self.radial_load / self.num_rollers / normal_stiffness / load_distribution_integral) ** (1 / n)
            load_zone = 1 / 2 - self.radial_clearance / 4 / total_deflection
            if load_zone < 0.5:
                load_distribution_integral = 0.3268 * (load_zone ** 0.4203)
            if load_zone == 0.5:
                load_distribution_integral = 0.2451
            if load_zone > 0.5 and load_zone <= 2:
                load_distribution_integral = -0.0852 * (load_zone ** 4) + 0.5703 * (load_zone ** 3) - 1.3343 * (load_zone ** 2) + 1.775 * load_zone - 0.0771
            stribeck_number_calculated = 1 / load_distribution_integral

            if ((stribeck_number - stribeck_number_calculated) / stribeck_number) > 0.001:
                stribeck_number = stribeck_number_calculated
                load_distribution_integral = 1 / stribeck_number
            else:
                break
        each_roller_angular_position, each_roller_loads, each_roller_deflection = [],  [], []
        pmax = stribeck_number_calculated * self.radial_load / self.num_rollers
        each_roller_loads.append(pmax)
        each_roller_deflection.append((self.radial_clearance / 2) + (self.radial_load / self.num_rollers / normal_stiffness / load_distribution_integral) ** (1 / n))
        theta = 360 / self.num_rollers
        each_roller_angular_position.append(0)
        self.load_zone = load_zone
        

        for item in range(int((self.num_rollers - 1)/ 2)):
            each_roller_angular_position.append((item + 1) * theta)
            each_roller_angular_position.append((self.num_rollers - 2 * (item + 1)) * theta + (item + 1) * theta)
            each_roller_loads.append(pmax * (math.cos((item + 1) * theta * math.pi / 180)) ** (1.11))
            each_roller_loads.append(pmax * (math.cos((item + 1) * theta * math.pi / 180)) ** (1.11))
            each_roller_deflection.append(each_roller_deflection[0] * (math.cos((item + 1) * theta * math.pi / 180)))
            each_roller_deflection.append(each_roller_deflection[0] * (math.cos((item + 1) * theta * math.pi / 180)))

        # Fix the roller loads from complex number to zero
        for i in range(len(each_roller_loads)):
            if isinstance(each_roller_loads[i], complex):
                each_roller_loads[i] = 0

        self.roller_model = {
            'roller_positions' : each_roller_angular_position,
            'roller_loads' : each_roller_loads,
            'roller_deflections' : each_roller_deflection
        }
        
    # Create Laminal model
    def create_lamina_model(self):
        self.lamina_model = {}
        lamina_lengths, lamina_positions = [], []
        lamina_length = (self.length_roller - self.roller_end_radius[0] - self.roller_end_radius[1]) / self.num_laminas

        # First lamina details
        first_lamina_length = lamina_length
        lamina_lengths.append(first_lamina_length)
        first_lamina_position = self.roller_end_radius[0] + first_lamina_length / 2 - self.length_roller / 2
        lamina_positions.append(first_lamina_position)

        for item in range(self.num_laminas - 2):
            lamina_positions.append(self.roller_end_radius[0] + first_lamina_length + (item + 1) * lamina_length - self.length_roller / 2)
            lamina_lengths.append(lamina_length)

        # Last Lamina Details
        last_lamina_length = first_lamina_length
        lamina_lengths.append(last_lamina_length)
        last_lamina_position = self.length_roller / 2 - last_lamina_length / 2 - self.roller_end_radius[1] # assuming first and last lamina are same
        lamina_positions.append(last_lamina_position)

        self.lamina_model.update({'lamina_positions' : lamina_positions})
        self.lamina_model.update({'lamina_lengths' : lamina_lengths})

    def get_roller_profile(self, selection: int, profile_data: list = []):
        if selection == 1: # default IS016281 profile
            for item in self.lamina_model['lamina_positions']:
                    if self.effective_length_roller <= 2.5 * self.roller_diameter:
                        profile_data.append(0.00035 * self.roller_diameter * math.log(1 / (1 - (2 * item / self.effective_length_roller) ** 2)))
                    else:
                        if abs(item) <= ((self.effective_length_roller - 2.5 * self.roller_diameter) / 2):
                            profile_data.append(0)
                        else:
                            profile_data.append(0.0005 * self.roller_diameter * math.log(1 / (1 - ((2 * abs(item) - (self.effective_length_roller - 2.5 * self.roller_diameter)) / 2.5 / self.roller_diameter) ** 2)))
            self.profile_data = profile_data    
        
        if selection == 2: # external profile data
            with open('profile.txt', 'r') as readobj:
                for line in readobj.readlines():
                    profile_data.append(float(line.split('\t')[1]) / 1000)
            self.profile_data = profile_data
        if selection == 3: # No prfiling
            for item in self.lamina_model['lamina_positions']:
                profile_data.append(0)
            self.profile_data = profile_data   

    def calculate_load_deflection_on_each_lamina(self):
        self.bearing_model = {}
        list1 = []
        list2 = []
        for i in range(len(self.roller_model['roller_deflections'])): # looping through each roller
            lamina_deflections =[]
            lamina_loads = []
            for j in range(len(self.lamina_model['lamina_positions'])): # lopping through each lamina
                try:
                    phi_j = math.atan(math.tan(self.misalignment / 1000) * math.cos(self.roller_model['roller_positions'][i] * math.pi / 180))
                    # math.cos(self.roller_model['roller_positions'][i] * math.pi / 180)
                    deflection = self.roller_model['roller_deflections'][i] - \
                                    self.lamina_model['lamina_positions'][j] * math.tan(phi_j) - \
                                        self.radial_clearance / 2 -  self.profile_data[j]
                    if deflection < 0:
                        deflection = 0
                except:
                    deflection = 0
                lamina_loads.append(35948 / self.num_laminas * math.pow((self.effective_length_roller), 8 / 9) * math.pow(deflection, 10 / 9))
                lamina_deflections.append(deflection)
            
            list1.append(lamina_deflections)
            list2.append(lamina_loads)

        self.bearing_model.update({'deflection_array' : np.array(list1)})
        self.bearing_model.update({'load_array' : np.array(list2)})


    def calculate_hertzian_stresses(self):
        list1, list2, list3, list4 = [], [], [], []

        for i in range(len(self.roller_model['roller_deflections'])): # looping through each roller
            contact_stresses_inner =[]
            semi_widths_inner = []
            contact_stresses_outer =[]
            semi_widths_outer = []
            contact_area_inner, contact_load_inner = 0, 0
            contact_area_outer, contact_load_outer = 0, 0
            for j in range(len(self.lamina_model['lamina_lengths'])): # lopping through each lamina

                semi_width_inner = math.sqrt(4 * self.bearing_model['load_array'][i][j] * ((1 - self.poisson_ratio ** 2) / self.elastic_mod + (1 - self.poisson_ratio ** 2) / \
                            self.elastic_mod) / \
                            #(math.pi * self.lamina_model['lamina_lengths'][j] * (1 / (self.roller_diameter / 2) + 1 / (self.pitch_diameter / 2 - self.roller_diameter / 2))))
                            (math.pi * self.lamina_model['lamina_lengths'][j] * (1 / (self.roller_diameter / 2) + 1 / (self.pitch_diameter / 2 - self.roller_diameter / 2))))
                           
                semi_width_outer = math.sqrt(4 * self.bearing_model['load_array'][i][j] * ((1 - self.poisson_ratio ** 2) / self.elastic_mod + (1 - self.poisson_ratio ** 2) / \
                            self.elastic_mod) / (math.pi * self.lamina_model['lamina_lengths'][j] * (1 / (self.roller_diameter / 2) + \
                                #1 / (self.pitch_diameter / 2 + self.roller_diameter / 2 + 1000000))))
                                0)))

                contact_stress_inner = 2 * self.bearing_model['load_array'][i][j] / math.pi / semi_width_inner / self.lamina_model['lamina_lengths'][j]
                contact_stress_outer = 2 * self.bearing_model['load_array'][i][j] / math.pi / semi_width_outer / self.lamina_model['lamina_lengths'][j]
                contact_area_inner += semi_width_inner * 2 * self.lamina_model['lamina_lengths'][j]
                contact_load_inner += self.bearing_model['load_array'][i][j]
                contact_area_outer += semi_width_outer * 2 * self.lamina_model['lamina_lengths'][j]
                contact_load_outer += self.bearing_model['load_array'][i][j]

                semi_widths_inner.append(semi_width_inner)
                semi_widths_outer.append(semi_width_outer)
                contact_stresses_inner.append(contact_stress_inner)
                contact_stresses_outer.append(contact_stress_outer)
            
            
            if semi_widths_inner[0] != 0:
                if max(semi_widths_inner) / semi_widths_inner[0] < 1.05: # first lamina
                    imaginary_area = (math.sqrt(3) * math.pow(2 * semi_widths_inner[0], 2)/ 4) # equilateral traingle as imaginable area
                    edge_load = imaginary_area * contact_load_inner / contact_area_inner
                    contact_stresses_inner[0] += edge_load / imaginary_area 

            if semi_widths_inner[-1] != 0:
                if max(semi_widths_inner) / semi_widths_inner[-1] < 1.5: # first lamina
                    imaginary_area = (math.sqrt(3) * math.pow(2 * semi_widths_inner[-1], 2)/ 4) # equilateral traingle as imaginable area
                    edge_load = imaginary_area * contact_load_inner / contact_area_inner
                    contact_stresses_inner[-1] += edge_load / imaginary_area 
            

            list1.append(contact_stresses_inner)
            list2.append(semi_widths_inner)
            list3.append(contact_stresses_outer)
            list4.append(semi_widths_outer)
        
        
        self.bearing_model.update({'contact_stresses_inner_array' : np.array(list1)})
        self.bearing_model.update({'semi_width_inner_array' : np.array(list2)})
        self.bearing_model.update({'contact_stresses_outer_array' : np.array(list3)})
        self.bearing_model.update({'semi_width_outer_array' : np.array(list4)})

    # equivalent load on laminas
    def calculate_equivalent_load_on_laminas(self):
        gamma = self.roller_diameter * math.cos(self.contact_angle * math.pi / 180) / self.pitch_diameter
        qkei_laminas = []
        qkee_laminas = []
        for i in range(len(self.lamina_model['lamina_positions'])):
            qkei = 0
            qkee = 0
            for j in range(self.num_rollers):

                stress_inner = 0 if math.isnan(self.bearing_model['contact_stresses_inner_array'][j, i]) else self.bearing_model['contact_stresses_inner_array'][j, i]
                stress_outer = 0 if math.isnan(self.bearing_model['contact_stresses_outer_array'][j, i]) else self.bearing_model['contact_stresses_outer_array'][j, i]
                qkei += math.pow(math.pow(( stress_inner  / 271), 2) * self.roller_diameter *\
                                (1 - gamma) * (self.effective_length_roller / self.num_laminas), 4)
                qkee += math.pow(math.pow((stress_outer / 271), 2) * self.roller_diameter *\
                                (1 + gamma) * (self.effective_length_roller / self.num_laminas), 4.5)

            qkei = math.pow(qkei / self.num_rollers, (1 / 4))
            qkee = math.pow(qkee / self.num_rollers, (1 / 4.5))
            qkei_laminas.append(qkei)
            qkee_laminas.append(qkee)
        print(sum(qkei_laminas))
        print(sum(qkee_laminas))
        qkci = (self.dynamic_capacity / ( 0.83 * 0.378 * self.num_rollers * math.cos(self.contact_angle * math.pi / 180) * math.pow(1, (7 / 9)))) * ((1 + (1.038 * ((1 - gamma) / \
                (1 + gamma)) ** (143 / 108)) ** (9/2)) ** (2/9)) * (math.pow(1 / self.num_laminas, (7 / 9)))
        qkce = (self.dynamic_capacity / ( 0.83 * 0.364 * self.num_rollers * math.cos(self.contact_angle * math.pi / 180) * math.pow(1, (7 / 9)))) * ((1 + (1.038 * ((1 - gamma) / \
                (1 + gamma)) ** (143 / 108)) ** (-9/2)) ** (2/9)) * (math.pow(1 / self.num_laminas, (7 / 9)))
        
        reference_life = 0
        for item in range(len(qkei_laminas)):
            reference_life += (math.pow((qkei_laminas[item] / qkci), 4.5) + math.pow((qkee_laminas[item] / qkce), 4.5))
        reference_life = math.pow(reference_life, -8 / 9)
        self.reference_life = reference_life

    # Proces
    def run_analysis(self):
        self.calculate_load_on_each_roller()
        self.create_lamina_model()
        self.get_roller_profile(selection=1)
        self.calculate_load_deflection_on_each_lamina()
        self.calculate_hertzian_stresses()
        self.calculate_equivalent_load_on_laminas()
        plots.run_plots(self)
        out.create_output(self)

    def run_analysis_taper(self):

        self.create_lamina_model()
        self.get_roller_profile(selection=1)
        self.calculate_load_deflection_on_each_lamina()
        self.calculate_hertzian_stresses()
        self.calculate_equivalent_load_on_laminas()
        plots.run_plots(self)
        out.create_output(self)










