import cv2
import mediapipe as mp

from pose_detector import PoseDetector
from angle_utils import calculate_angle
from feedback import speak, posture_feedback
from evaluation import calculate_accuracy
from report_generator import generate_report

mp_pose = mp.solutions.pose

stop_flag = False


def start_camera(exercise="Squat"):
    global stop_flag
    stop_flag = False

    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    stage = None
    rep_count = 0

    feedback_history = []

    # ✅ NEW FOR REP GRAPH
    rep_accuracies = []
    current_rep_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.find_pose(frame)
        angle = None
        feedback_text = ""

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            LS = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            LE = lm[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            LW = lm[mp_pose.PoseLandmark.LEFT_WRIST.value]

            RS = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            RE = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            RW = lm[mp_pose.PoseLandmark.RIGHT_WRIST.value]

            LH = lm[mp_pose.PoseLandmark.LEFT_HIP.value]
            LK = lm[mp_pose.PoseLandmark.LEFT_KNEE.value]
            LA = lm[mp_pose.PoseLandmark.LEFT_ANKLE.value]

            # -------- SQUAT --------
            if exercise == "Squat":
                angle = calculate_angle(LH, LK, LA)
                feedback_text = posture_feedback(angle)

                if angle and angle < 90:
                    stage = "down"

                if angle and angle > 160 and stage == "down":
                    rep_count += 1
                    stage = "up"
                    speak(f"Squat {rep_count}")

                    # ✅ SAVE REP DATA
                    if current_rep_data:
                        avg = sum(current_rep_data) / len(current_rep_data)
                        rep_accuracies.append(avg)
                        current_rep_data = []

            # -------- PUSHUP --------
            elif exercise == "Pushup":
                angle = calculate_angle(LS, LE, LW)
                feedback_text = posture_feedback(angle)

                if angle and angle < 90:
                    stage = "down"

                if angle and angle > 160 and stage == "down":
                    rep_count += 1
                    stage = "up"
                    speak(f"Push up {rep_count}")

                    if current_rep_data:
                        avg = sum(current_rep_data) / len(current_rep_data)
                        rep_accuracies.append(avg)
                        current_rep_data = []

            # -------- BICEP CURL --------
            elif exercise == "Bicep Curl":
                angle = calculate_angle(LS, LE, LW)
                feedback_text = posture_feedback(angle)

                if angle and angle < 60:
                    stage = "up"

                if angle and angle > 150 and stage == "up":
                    rep_count += 1
                    stage = "down"
                    speak(f"Bicep curl {rep_count}")

                    if current_rep_data:
                        avg = sum(current_rep_data) / len(current_rep_data)
                        rep_accuracies.append(avg)
                        current_rep_data = []

            # -------- OTHER EXERCISES --------
            elif exercise == "Shoulder Press":
                angle = calculate_angle(LE, LS, LH)
                feedback_text = posture_feedback(angle)

            elif exercise == "Front Double Biceps":
                la = calculate_angle(LS, LE, LW)
                ra = calculate_angle(RS, RE, RW)
                feedback_text = "Perfect pose" if 60 < la < 100 and 60 < ra < 100 else "Flex more"

            elif exercise == "Side Chest":
                angle = calculate_angle(LS, LE, LW)
                feedback_text = "Good side chest" if angle and angle < 90 else "Tighten chest"

            # -------- ACCURACY COLLECTION --------
            if angle is not None:
                accuracy = calculate_accuracy(angle, exercise)

                if accuracy is not None:
                    current_rep_data.append(accuracy)

                if feedback_text:
                    feedback_history.append(feedback_text)

            # -------- UI --------
            cv2.putText(frame, f"{exercise}", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Reps: {rep_count}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, feedback_text, (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        detector.draw_landmarks(frame, results)
        cv2.imshow("AI Pose Trainer", frame)

        cv2.waitKey(1)

        # -------- STOP --------
        if stop_flag:
            print("Generating report...")

            if not rep_accuracies:
                rep_accuracies.append(0)

            generate_report(
                exercise,
                rep_count,
                rep_accuracies,
                feedback_history
            )
            break

    cap.release()
    cv2.destroyAllWindows()