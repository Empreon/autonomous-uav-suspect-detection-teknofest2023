import pickle
import os.path

def saveData(data, name):
    pickle_file = name + '.pkl'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pickle_file_path = os.path.join(current_directory, pickle_file)

    if os.path.isfile(pickle_file_path) and os.path.getsize(pickle_file_path) > 0:
        with open(pickle_file_path, 'rb') as f:
            location_data = pickle.load(f)
    else:
        location_data = []

    location_data.extend([data])

    with open(pickle_file_path, 'wb') as f:
        pickle.dump(location_data, f, protocol=2)
        f.close()
