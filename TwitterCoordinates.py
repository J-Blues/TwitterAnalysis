import pandas as pd
import numpy as np

lat = []
lon = []

def splitLatLong(coordinates):
    for value in dict(coordinates).values():
        if type(value) is float:
            lon.append(np.NaN)
            lat.append(np.NaN)
        elif type(value) is np.float64:
            lon.append(np.NaN)
            lat.append(np.NaN)
        else:
            bracketStartIndex = value.find('[')
            bracketStopIndex = value.find(']')
            values = value[bracketStartIndex+1:bracketStopIndex].split(",")
            lon.append(values[0])
            lat.append(values[1])

## Local Variables
path = r'D:\Research_Assistant\DataBase\COVID\twitter-daily\twitter_data_analysis2020-03_11.csv'
path_split = path.split('.')
path_new = path_split[0] + '_CoordinatesReport.csv'
df = pd.read_csv(path)

try:
    splitLatLong(df['coordinates'])

    df['longitude'] = lon
    df['latitude'] = lat

    df.to_csv(path_new)
    print('\nDone: Coordinates column has been split into Longitude and '
          'Latitude columns the results have been saved to a new CSV Report')

except OSError as e:
    print('OS error: {0}'.format(e))
except IOError as e:
    print('I/O error({0}): {1}'.format(e.errno, e.strerror))
except ValueError as e:
    print('Value error: ' + e.args[0])
except Exception as e:
    print('Unexpected error: ' + e.args[0])