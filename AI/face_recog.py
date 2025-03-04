import face_recognition
import cv2
import pickle

def faceProcess(frame, database):
    with open(database, 'rb') as f:
        known_face_encodings = pickle.load(f)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    results = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = "Suspect"
            results.append([top, right, bottom, left])
        else:
            name = "Unknown"
    return results
