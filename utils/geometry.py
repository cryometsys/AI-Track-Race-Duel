import math

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def closest_point_on_track(car_pos, centerline):
    """Return (closest_point, segment_index) on centerline to car_pos."""
    min_dist = float('inf')
    closest_point = centerline[0]
    best_index = 0
    for i, point in enumerate(centerline):
        d = distance(car_pos, point)
        if d < min_dist:
            min_dist = d
            closest_point = point
            best_index = i
    return closest_point, best_index

def compute_curvature(p0, p1, p2):
    """
    Estimate curvature at p1 using three points.
    Returns a value in [0, 1] where 0 = straight, 1 = very sharp.
    """
    # Vector from p0 to p1
    v1 = (p1[0] - p0[0], p1[1] - p0[1])
    # Vector from p1 to p2
    v2 = (p2[0] - p1[0], p2[1] - p1[1])
    
    # Angle between vectors
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.hypot(*v1)
    mag2 = math.hypot(*v2)
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    cos_angle = dot / (mag1 * mag2)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    angle = math.acos(cos_angle)  # in radians
    
    # Normalize: max curvature when angle = π (U-turn), min when 0 (straight)
    # Map [0, π] → [0, 1]
    return angle / math.pi

def get_track_heading(centerline, index):
    """Return the forward angle (radians) at a point on the centerline."""
    n = len(centerline)
    next_idx = (index + 1) % n
    dx = centerline[next_idx][0] - centerline[index][0]
    dy = centerline[next_idx][1] - centerline[index][1]
    return math.atan2(dy, dx)

def get_future_heading(centerline, current_index, look_ahead=30):
    """Return the ideal heading (radians) toward a point ahead on the track."""
    n = len(centerline)
    future_index = (current_index + look_ahead) % n
    curr = centerline[current_index]
    future = centerline[future_index]
    dx = future[0] - curr[0]
    dy = future[1] - curr[1]
    return math.atan2(dy, dx)