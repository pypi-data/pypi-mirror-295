import matplotlib.pyplot as plt
import numpy as np

# Set data for HIPOPy
data_hipopy = {
        'example_output.hipo': 0.204, #ms ± 510 µs #(2 banks, 11 entries, 11MB, 25K events)
        'nSidis_005521.hipo': 4*60+56, #(10 banks, 131 entries, 6GB, 2.88M events) # 4min 56s ± 246 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    }
x_hipopy = list(data_hipopy.keys())
y_hipopy = list(data_hipopy.values())
yerr_hipopy = [0.000510,0.246]

# Set data for hipo python API
data_hipo = {
        'example_output.hipo': 5.95, #s ± 42 ms, #(2 banks, 11 entries, 11MB, 25K events)
        'nSidis_005521.hipo': 15, #(10 banks, 131 entries, 6GB, 2.88M events)
    }
x_hipo = list(data_hipo.keys())
y_hipo = list(data_hipo.values())
yerr_hipo   = [0.042,0.1]

#DEBUGGING
print('x_hipopy = ',x_hipopy)
print('y_hipopy = ',y_hipopy)
print('x_hipo = ',x_hipo)
print('y_hipo = ',y_hipo)

# Get some nicer plot settings 
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'

SMALL_SIZE = 20
MEDIUM_SIZE = 24
BIGGER_SIZE = 28

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

extraargs_hipopy = {
    'fmt' : 'bo',
    'capsize' : 1.0,
    'elinewidth' : 1.0,
    'capthick' : 1.0,
    'markersize' : 10,
}
extraargs_hipo = {
    'fmt' : 'ro',
    'capsize' : 1.0,
    'elinewidth' : 1.0,
    'capthick' : 1.0,
    'markersize' : 10,
}

# Plot comparison
figsize = (16,10)
width = 0.25
fig, ax = plt.subplots(figsize=figsize)
plt.yscale('log')
ax.errorbar(x_hipopy, y_hipopy, yerr=yerr_hipopy, label='HIPOPy', **extraargs_hipopy) #width=1.5*width, align='edge',
ax.errorbar(x_hipo, y_hipo, yerr=yerr_hipo, label='Hipo Python API', **extraargs_hipo) #width=width, align='center', 
ax.legend()
plt.xlabel('Input file')
plt.ylabel('Time (s)')
plt.title('Time comparison')
fig.savefig('hipopy_python_api_speed_comparison.pdf')
plt.show()
