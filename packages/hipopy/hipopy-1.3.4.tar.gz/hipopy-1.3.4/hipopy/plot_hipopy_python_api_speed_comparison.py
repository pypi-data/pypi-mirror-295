import matplotlib.pyplot as plt
import numpy as np

# Set output file name
figname = 'speed_comparison.pdf'

# Set numerator file data
num1 = 25000 #EVENTS for example_output.hipo
num2 = 2.88*10**6 #EVENTS for nSidis_005521.hipo
ylabel  = 'Events/s'
figname = 'events_speed_comparison.pdf'
loc = 'best'
# num1 = 11*25000 #ENTRIES*EVENTS for example_output.hipo
# num2 = 131*2.88*10**6 #ENTRIES*EVENTS for nSidis_005521.hipo
# ylabel  = 'Entries$\cdot$Events/s'
# figname = 'entries_events_speed_comparison.pdf'
# loc = 'upper center'
# num1 = 11 #MB for example_output.hipo
# num2 = 6*10**3 #MB for nSidis_005521.hipo
# ylabel  = 'MB/s'
# figname = 'memory_speed_comparison.pdf'
# loc = 'best'

# Set data for HIPOPy
data_hipopy = {
        'example_output.hipo': num1/(0.204), #ms ± 510 µs #(2 banks, 11 entries, 11MB, 25K events)
        'nSidis_005521.hipo': num2/(4*60+56), #(10 banks, 131 entries, 6GB, 2.88M events) # 4min 56s ± 246 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    }
x_hipopy = list(data_hipopy.keys())
y_hipopy = list(data_hipopy.values())

# Set data for hipo python API
data_hipo = {
        'example_output.hipo': num1/(5.95), #s ± 42 ms, #(2 banks, 11 entries, 11MB, 25K events)
        'nSidis_005521.hipo': num2/(1*3600+52*60+7), #(10 banks, 131 entries, 6GB, 2.88M events) # 1h 52min 7s
    }
x_hipo = list(data_hipo.keys())
y_hipo = list(data_hipo.values())

# Get some nicer plot settings 
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'

SMALL_SIZE = 30
MEDIUM_SIZE = 36
BIGGER_SIZE = 40

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# # Plot comparison
# figsize = (16,10)
# width = 0.25
# fig, ax = plt.subplots(figsize=figsize)
# plt.yscale('log')
# ax.bar(x_hipopy, y_hipopy, label='HIPOPy', width=1.5*width, align='edge')
# ax.bar(x_hipo, y_hipo, label='Hipo Python API', width=width, align='center')
# ax.legend()
# plt.xlabel('Input file')
# plt.ylabel('Events/s')
# plt.title('Time comparison')
# fig.savefig('hipopy_python_api_speed_comparison.pdf')
# plt.show()

# Reformat data
xlabels = x_hipopy
x = np.arange(len(xlabels))  # the label locations
ymeans = {
    'HIPOPy': y_hipopy,
    'Hipo Python API': y_hipo,
}
width = 0.25  # the width of the bars
multiplier = 0

# Plot comparison
figsize = (16,10)
fig, ax = plt.subplots(figsize=figsize)
for attribute, measurement in ymeans.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3, fmt='%.3g')
    multiplier += 1
ax.set_xlabel('File name')
ax.set_ylabel(ylabel,usetex=True)
ax.set_title('Speed Comparison')
ax.set_xticks(x + width, x_hipopy)
ax.legend(loc=loc)
plt.yscale('log')
plt.savefig(figname)
plt.show()
