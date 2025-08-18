import cv2
import mediapipe as mp
import numpy as np

class BlinkDetector:
	def __init__(self):
		self._running = True
	
	def run(self):

		mp_face_mesh = mp.solutions.face_mesh
		face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
		mp_drawing = mp.solutions.drawing_utils

		LEFT_EYE = [33, 160, 158, 133, 153, 144]  
		RIGHT_EYE = [362, 385, 387, 263, 373, 380] 

		EAR_THRESHOLD = 0.24
		CONSEC_FRAMES = 2
		blink_count = 0
		frame_counter = 0

		cap = cv2.VideoCapture(0)
		if not cap.isOpened():
			print("Error: Could not open webcam.")
			while self._running:
				yield blink_count
			return

		while self._running:
			ret, frame = cap.read()
			if not ret:
				break
			rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			results = face_mesh.process(rgb_frame)

			if results.multi_face_landmarks:
				mesh_points = np.array([
					[p.x * frame.shape[1], p.y * frame.shape[0]]
					for p in results.multi_face_landmarks[0].landmark
				])
				left_ear = self.eye_aspect_ratio(mesh_points, LEFT_EYE)
				right_ear = self.eye_aspect_ratio(mesh_points, RIGHT_EYE)
				ear = (left_ear + right_ear) / 2.0

				if ear < EAR_THRESHOLD:
					frame_counter += 1
				else:
					if frame_counter >= CONSEC_FRAMES:
						blink_count += 1
					frame_counter = 0

				for idx in LEFT_EYE + RIGHT_EYE:
					point = tuple(np.int32(mesh_points[idx]))
					cv2.circle(frame, point, 2, (0, 255, 0), -1)

				cv2.putText(frame, f"Blinks: {blink_count}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				cv2.putText(frame, f"EAR: {ear:.2f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

			cv2.imshow('Eye Blink Detector (Press Q to quit)', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			
			yield blink_count 
			
		cap.release()

	def stop(self):
		self._running = False

	@staticmethod
	def euclidean_distance(point1, point2):
		return np.linalg.norm(np.array(point1) - np.array(point2))

	def eye_aspect_ratio(self, landmarks, eye_indices):
		p0 = landmarks[eye_indices[0]]  # left
		p1 = landmarks[eye_indices[1]]  # top1
		p2 = landmarks[eye_indices[2]]  # top2
		p3 = landmarks[eye_indices[3]]  # right
		p4 = landmarks[eye_indices[4]]  # bottom1
		p5 = landmarks[eye_indices[5]]  # bottom2
		A = self.euclidean_distance(p1, p5)
		B = self.euclidean_distance(p2, p4)
		C = self.euclidean_distance(p0, p3)
		ear = (A + B) / (2.0 * C)
		return ear



