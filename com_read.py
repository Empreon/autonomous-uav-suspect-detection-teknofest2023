import pickle
import os.path
import struct

def readData(database):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_directory, database)

    if os.path.isfile(pickle_file_path) and os.path.getsize(pickle_file_path) > 0:
        with open(pickle_file_path, 'rb') as f:
            try:
                location_data = pickle.load(f)
            except (EOFError, struct.error):
                location_data = []

        if len(location_data) > 0:
            return location_data[-1]
    else:
        return None

