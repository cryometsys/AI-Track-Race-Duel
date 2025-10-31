import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def _build_fuzzy_system():

    # Inputs => speed and curve
    speed = ctrl.Antecedent(np.arange(0, 16, 0.1), 'speed')
    curve = ctrl.Antecedent(np.arange(0, 1.1, 0.01), 'curve')

    # Output => acceleration prediction
    acceleration = ctrl.Consequent(np.arange(-1, 1.1, 0.01), 'acceleration')

    # Membership functions
    speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 6])
    speed['medium'] = fuzz.trimf(speed.universe, [4, 8, 12])
    speed['fast'] = fuzz.trimf(speed.universe, [10, 15, 15])

    curve['gentle'] = fuzz.trimf(curve.universe, [0, 0, 0.6])
    curve['sharp'] = fuzz.trimf(curve.universe, [0.4, 1, 1])

    acceleration['brake'] = fuzz.trimf(acceleration.universe, [-1, -1, 0])
    acceleration['maintain'] = fuzz.trimf(acceleration.universe, [-0.5, 0, 0.5])
    acceleration['accelerate'] = fuzz.trimf(acceleration.universe, [0, 1, 1])

    # Rules
    rule1 = ctrl.Rule(speed['fast'] & curve['sharp'], acceleration['brake'])
    rule2 = ctrl.Rule(speed['fast'] & curve['gentle'], acceleration['maintain'])
    rule3 = ctrl.Rule(speed['slow'] & curve['gentle'], acceleration['accelerate'])
    rule4 = ctrl.Rule(speed['slow'] & curve['sharp'], acceleration['maintain'])
    rule5 = ctrl.Rule(speed['medium'] & curve['sharp'], acceleration['brake'])
    rule6 = ctrl.Rule(speed['medium'] & curve['gentle'], acceleration['maintain'])

    acceleration_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    return ctrl.ControlSystemSimulation(acceleration_ctrl)

# Global simulation instance
_fuzzy_sim = _build_fuzzy_system()

def get_acceleration_action(current_speed: float, road_curvature: float) -> float:
    """
    Returns acceleration command in [-1, 1]:
        > 0  → accelerate
        < 0  → brake
        ≈ 0  → maintain
    """
    # Clamping to valid range
    current_speed = np.clip(current_speed, 0, 15)
    road_curvature = np.clip(road_curvature, 0, 1.0)

    _fuzzy_sim.input['speed'] = current_speed
    _fuzzy_sim.input['curve'] = road_curvature
    _fuzzy_sim.compute()
    return float(_fuzzy_sim.output['acceleration'])