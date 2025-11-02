import math

from utils.geometry import closest_point_on_track, distance
from car.car import Car
from utils.geometry import get_future_heading

class HeuristicAgent:
    def __init__(self, lookahead_depth = 3, progress_weight=1.0, centering_weight=0.1, off_track_penalty=1000):
        self.lookahead_depth = lookahead_depth
        self.actions = ["left", "right", "straight"]

        # Heuristic weights
        self.progress_weight = progress_weight
        self.centering_weight = centering_weight
        self.off_track_penalty = off_track_penalty

    def decide_action(self, car, track):
        # Return the best steering action based on lookahead + heuristic.
        best_action = "straight" # Default action
        best_score = -float('inf') # Smallest value

        for action in self.actions:
            # Car state cloning
            sim_car = self._clone_car(car)
            
            # Simulating N steps
            for _ in range(self.lookahead_depth):
                self._apply_action(sim_car, action)
                sim_car.update()

            # Evaluation
            score = self._evaluate_state(sim_car, track)
            
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def _clone_car(self, car):
        clone = Car(car.x, car.y, car.angle)
        clone.speed = car.speed
        clone.max_speed = car.max_speed
        clone.acceleration_rate = car.acceleration_rate
        clone.brake_rate = car.brake_rate
        clone.turn_rate = car.turn_rate
        return clone

    def _apply_action(self, car, action):
        if action == "left":
            car.turn_left()
        elif action == "right":
            car.turn_right()

    def _evaluate_state(self, car, track):
        car_pos = (car.x, car.y)
        closest_point, idx = closest_point_on_track(car_pos, track.centerline)
        dist_to_center = distance(car_pos, closest_point)

        # Heuristic components
        progress_score = self.progress_weight * idx # Higher index -> more progress 
        centering_penalty = -self.centering_weight * dist_to_center  # Penalizing distance from ideal line
        collision_penalty = 0

        # Hard penalty for going off-track
        collision_penalty = 0
        if dist_to_center > track.width // 2:
            collision_penalty = -self.off_track_penalty

        # === NEW: Heading alignment bonus ===
        ideal_heading = get_future_heading(track.centerline, idx, look_ahead=10)
        heading_error = abs(math.atan2(math.sin(car.angle - ideal_heading), math.cos(car.angle - ideal_heading)))
        alignment_bonus = -0.5 * heading_error

        total_score = progress_score + centering_penalty + collision_penalty + alignment_bonus
        return total_score