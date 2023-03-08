sigma = [0.5, 0.6, 0.8, 0.9]
integral = []

for sig in sigma:

    load_distribution_integral = -0.0852 * (sig ** 4) + 0.5703 * (sig ** 3) - 1.3343 * (sig ** 2) + 1.775 * sig - 0.0771
    integral.append(load_distribution_integral)

print('done')