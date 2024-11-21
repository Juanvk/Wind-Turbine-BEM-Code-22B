import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# df = pd.read_csv('Blade_TSR_CP_Curve.txt', delim_whitespace=True)
# TSR_data = np.array(df['TSR'].tolist())
# Cp_data = np.array(df['Cp'].tolist())

# plt.plot(TSR_data, Cp_data)
# plt.xlabel('Tip Speed Ratio (TSR) [-]')
# plt.ylabel('Coefficient of Power (Cp) [%]')
# plt.grid()
# plt.show()

# Data
phases = ['Phase A (R_A)', 'Phase B (R_B)', 'Phase C (R_C)']
resistances = [0.5425, 0.5632, 0.5475]

# Create the bar chart with customized size and colors
plt.figure(figsize=(6, 4))
bars = plt.bar(phases, resistances, color=['blue', 'orange', 'green'])

# Add exact resistance values on top of the bars
for bar, resistance in zip(bars, resistances):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001, 
             f'{resistance:.4f}', ha='center', va='bottom', fontsize=10)

# Adjust y-axis to focus on the differences
plt.ylim(0.45, 0.57)

# Add labels and title
plt.xlabel('Phases')
plt.ylabel('Resistance [Ω]')
plt.title('Phase Resistances of the Generator')

# Display the chart
plt.tight_layout()
plt.show()