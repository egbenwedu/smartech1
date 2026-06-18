import pandas as pd
import numpy as np

# Generate 100 rows of dummy experimental data
data = {
    'amine_loading': np.random.uniform(10, 30, 100),
    'surface_area': np.random.uniform(300, 600, 100),
    'humidity': np.random.uniform(20, 80, 100),
    'temp': np.random.uniform(290, 320, 100),
}
# Create a fake capacity based on a formula
df = pd.DataFrame(data)
df['capacity'] = (df['amine_loading'] * 0.03) + (df['surface_area'] * 0.001) - (df['humidity'] * 0.002)

df.to_csv('adsorbent_data.csv', index=False)
print("File 'adsorbent_data.csv' created successfully!")