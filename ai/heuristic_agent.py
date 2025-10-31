# ai/heuristic_agent.py
import math
from utils.geometry import closest_point_on_track, distance

class HeuristicAgent:
    def __init__(self, lookahead_depth = 3):
        self.lookahead_depth = lookahead_depth
        self.actions = ["left", "right", "straight"]

    def decide_action(self, car, track):
        """Return the best steering action based on lookahead + heuristic."""
        best_action = "straight"
        best_score = -float('inf')

        for action in self.actions:
            # Clone car state for simulation
            sim_car = self._clone_car(car)
            
            # Simulate N steps with this action
            for _ in range(self.lookahead_depth):
                self._apply_action(sim_car, action)
                sim_car.update()  # move based on current speed/angle

            # Evaluate final state
            score = self._evaluate_state(sim_car, track)
            
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def _clone_car(self, car):
        """Create a lightweight copy of the car for simulation."""
        from car.car import Car
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
        # "straight" does nothing

    def _evaluate_state(self, car, track):
        """Heuristic score for a simulated car state."""
        car_pos = (car.x, car.y)
        closest_point, idx = closest_point_on_track(car_pos, track.centerline)
        dist_to_center = distance(car_pos, closest_point)

        # Heuristic components
        progress_score = idx  # higher index = more progress (simplified)
        centering_penalty = -0.1 * dist_to_center  # stay near center
        collision_penalty = 0

        # Simple off-track detection: if too far from centerline
        if dist_to_center > track.width // 2:
            collision_penalty = -1000  # heavy penalty

        total_score = progress_score + centering_penalty + collision_penalty
        return total_score