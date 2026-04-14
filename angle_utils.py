# angle_utils.py
import math

def calculate_angle(a, b, c):
    """
    Calculate angle at point b using MediaPipe landmarks
    """
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    ba = (ax - bx, ay - by)
    bc = (cx - bx, cy - by)

    cosine_angle = (ba[0]*bc[0] + ba[1]*bc[1]) / (
        (math.hypot(*ba) * math.hypot(*bc)) + 1e-6
    )

    angle = math.degrees(math.acos(max(min(cosine_angle, 1), -1)))
    return angle
