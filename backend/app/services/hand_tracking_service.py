"""
MediaPipe Hand Tracking & Landmark Detection Service.
Uses MediaPipe 1.0 Tasks Vision HandLandmarker.
Detects 21 3D hand landmarks, thumb tip (#4), index tip (#8), wrist (#0), and handedness.
Draws visual gesture feedback (connecting line, landmark points, distance & brightness status).
"""
import os
import cv2
import math
import urllib.request
import numpy as np
import mediapipe as mp
from typing import Optional, Dict, Any, Tuple, List
from app.core.config import settings
from app.core.logging_config import logger
from app.core.constants import (
    LANDMARK_WRIST, LANDMARK_THUMB_TIP, LANDMARK_INDEX_TIP,
    LANDMARK_MIDDLE_TIP, LANDMARK_RING_TIP, LANDMARK_PINKY_TIP
)

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "hand_landmarker.task")

class HandTrackingService:
    def __init__(self):
        self.detection_confidence = settings.DETECTION_CONFIDENCE
        self.tracking_confidence = settings.TRACKING_CONFIDENCE
        self.max_num_hands = settings.MAX_NUM_HANDS
        self.detector = None

        self._ensure_model_file()
        self._init_detector()

    def _ensure_model_file(self):
        if not os.path.exists(MODEL_PATH):
            logger.info("Downloading MediaPipe hand_landmarker.task model...")
            try:
                urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
                logger.info("Hand landmarker model downloaded successfully.")
            except Exception as e:
                logger.error(f"Failed to download MediaPipe model asset: {e}")

    def _init_detector(self):
        try:
            from mediapipe.tasks import python as mp_python
            from mediapipe.tasks.python import vision

            if os.path.exists(MODEL_PATH):
                base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
                options = vision.HandLandmarkerOptions(
                    base_options=base_options,
                    num_hands=self.max_num_hands,
                    min_hand_detection_confidence=self.detection_confidence,
                    min_hand_presence_confidence=self.detection_confidence,
                    min_tracking_confidence=self.tracking_confidence
                )
                self.detector = vision.HandLandmarker.create_from_options(options)
                logger.info("MediaPipe HandLandmarker Tasks Vision pipeline initialized successfully.")
            else:
                logger.warning("hand_landmarker.task file missing. HandLandmarker detector unavailable.")
                self.detector = None
        except Exception as e:
            logger.error(f"Failed to initialize MediaPipe HandLandmarker: {e}")
            self.detector = None

    def update_confidence(self, det_conf: float, track_conf: float):
        self.detection_confidence = det_conf
        self.tracking_confidence = track_conf
        self._init_detector()

    def process_frame(self, frame_bgr: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Processes a single BGR OpenCV camera frame using MediaPipe HandLandmarker.
        """
        result_data = {
            "hand_detected": False,
            "num_hands": 0,
            "thumb_tip": None,
            "index_tip": None,
            "wrist": None,
            "distance": None,
            "is_open_hand": False,
            "landmarks": []
        }

        if self.detector is None or frame_bgr is None:
            return frame_bgr, result_data

        h, w, _ = frame_bgr.shape
        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        try:
            detection_result = self.detector.detect(mp_image)
        except Exception as ex:
            logger.error(f"MediaPipe detection error: {ex}")
            return frame_bgr, result_data

        if detection_result and detection_result.hand_landmarks:
            result_data["hand_detected"] = True
            result_data["num_hands"] = len(detection_result.hand_landmarks)

            primary_hand = detection_result.hand_landmarks[0]

            # Draw circles and connections for all detected hands
            for hand_landmarks in detection_result.hand_landmarks:
                for lm in hand_landmarks:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame_bgr, (cx, cy), 3, (0, 255, 0), cv2.FILLED)

            lm_list = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in primary_hand]
            result_data["landmarks"] = lm_list

            # Extract key landmark coordinates
            thumb = primary_hand[LANDMARK_THUMB_TIP]
            index = primary_hand[LANDMARK_INDEX_TIP]
            wrist = primary_hand[LANDMARK_WRIST]

            t_x, t_y = int(thumb.x * w), int(thumb.y * h)
            i_x, i_y = int(index.x * w), int(index.y * h)
            w_x, w_y = int(wrist.x * w), int(wrist.y * h)

            result_data["thumb_tip"] = (t_x, t_y)
            result_data["index_tip"] = (i_x, i_y)
            result_data["wrist"] = (w_x, w_y)

            # Calculate 2D Euclidean distance
            dx = thumb.x - index.x
            dy = thumb.y - index.y
            euclidean_distance = math.hypot(dx, dy)
            result_data["distance"] = euclidean_distance

            # Check open hand pause gesture (finger tips Y coordinates)
            is_open = (
                primary_hand[LANDMARK_INDEX_TIP].y < primary_hand[6].y and
                primary_hand[LANDMARK_MIDDLE_TIP].y < primary_hand[10].y and
                primary_hand[LANDMARK_RING_TIP].y < primary_hand[14].y and
                primary_hand[LANDMARK_PINKY_TIP].y < primary_hand[18].y
            )
            result_data["is_open_hand"] = is_open

            # Highlight Thumb Tip & Index Tip with customized circles & connecting line
            cv2.circle(frame_bgr, (t_x, t_y), 10, (255, 0, 128), cv2.FILLED)  # Magenta
            cv2.circle(frame_bgr, (t_x, t_y), 12, (255, 255, 255), 2)

            cv2.circle(frame_bgr, (i_x, i_y), 10, (0, 255, 255), cv2.FILLED)  # Cyan
            cv2.circle(frame_bgr, (i_x, i_y), 12, (255, 255, 255), 2)

            # Connecting distance line with midpoint circle
            cv2.line(frame_bgr, (t_x, t_y), (i_x, i_y), (0, 255, 0), 3)
            mid_x, mid_y = (t_x + i_x) // 2, (t_y + i_y) // 2
            cv2.circle(frame_bgr, (mid_x, mid_y), 6, (0, 255, 0), cv2.FILLED)

        return frame_bgr, result_data

hand_tracking_service = HandTrackingService()
