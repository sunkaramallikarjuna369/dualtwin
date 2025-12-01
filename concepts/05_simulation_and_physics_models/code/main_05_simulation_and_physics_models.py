"""
Simulation and Physics Models - Main Demonstration

This script demonstrates physics-based simulation with thermal and
mechanical models, including prediction, what-if analysis, and optimization.

Usage:
    python main_05_simulation_and_physics_models.py

Example:
    python main_05_simulation_and_physics_models.py
"""

import sys
import os
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import random

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class ThermalModel:
    """Physics model for thermal behavior."""
    
    thermal_mass: float = 100.0
    heat_transfer_coeff: float = 0.1
    ambient_temp: float = 20.0
    
    def simulate_step(self, current_temp: float, heat_input: float, 
                      dt: float = 1.0) -> float:
        """Simulate one time step of thermal behavior."""
        heat_loss = self.heat_transfer_coeff * (current_temp - self.ambient_temp)
        temp_change = (heat_input - heat_loss) / self.thermal_mass * dt
        return current_temp + temp_change
    
    def predict_steady_state(self, heat_input: float) -> float:
        """Predict steady-state temperature for given heat input."""
        return self.ambient_temp + heat_input / self.heat_transfer_coeff
    
    def time_to_temperature(self, start_temp: float, target_temp: float,
                           heat_input: float) -> float:
        """Estimate time to reach target temperature."""
        steady_state = self.predict_steady_state(heat_input)
        if abs(steady_state - start_temp) < 0.1:
            return float('inf')
        
        tau = self.thermal_mass / self.heat_transfer_coeff
        
        if target_temp > steady_state or target_temp < start_temp:
            return float('inf')
        
        ratio = (target_temp - steady_state) / (start_temp - steady_state)
        if ratio <= 0:
            return float('inf')
        
        return -tau * math.log(ratio)


@dataclass
class MechanicalWearModel:
    """Physics model for mechanical wear."""
    
    wear_coefficient: float = 0.001
    load_factor: float = 1.0
    speed_exponent: float = 1.5
    
    initial_health: float = 1.0
    current_health: float = 1.0
    accumulated_wear: float = 0.0
    
    def simulate_wear(self, speed: float, load: float, duration: float) -> float:
        """Simulate wear over a period."""
        wear_rate = (self.wear_coefficient * 
                    (speed ** self.speed_exponent) * 
                    (load * self.load_factor))
        wear = wear_rate * duration
        self.accumulated_wear += wear
        self.current_health = max(0, self.initial_health - self.accumulated_wear)
        return wear
    
    def predict_remaining_life(self, speed: float, load: float) -> float:
        """Predict remaining useful life at current conditions."""
        wear_rate = (self.wear_coefficient * 
                    (speed ** self.speed_exponent) * 
                    (load * self.load_factor))
        if wear_rate <= 0:
            return float('inf')
        return self.current_health / wear_rate
    
    def reset(self) -> None:
        """Reset to initial state (simulating replacement)."""
        self.current_health = self.initial_health
        self.accumulated_wear = 0.0


@dataclass
class SimulationEngine:
    """Engine for running physics simulations."""
    
    thermal_model: ThermalModel
    wear_model: MechanicalWearModel
    
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def run_simulation(self, duration: float, dt: float,
                      heat_input: float, speed: float, load: float,
                      initial_temp: float = 25.0) -> List[Dict[str, Any]]:
        """Run a combined thermal and mechanical simulation."""
        self.history = []
        temp = initial_temp
        
        steps = int(duration / dt)
        for i in range(steps):
            time = i * dt
            
            temp = self.thermal_model.simulate_step(temp, heat_input, dt)
            wear = self.wear_model.simulate_wear(speed, load, dt)
            
            state = {
                'time': time,
                'temperature': round(temp, 2),
                'health': round(self.wear_model.current_health, 4),
                'wear_rate': round(wear / dt, 6),
                'remaining_life': round(self.wear_model.predict_remaining_life(speed, load), 1)
            }
            self.history.append(state)
        
        return self.history
    
    def what_if_analysis(self, scenarios: List[Dict[str, Any]],
                        duration: float = 100.0) -> List[Dict[str, Any]]:
        """Run what-if analysis for multiple scenarios."""
        results = []
        
        for scenario in scenarios:
            self.wear_model.reset()
            
            self.run_simulation(
                duration=duration,
                dt=1.0,
                heat_input=scenario.get('heat_input', 50),
                speed=scenario.get('speed', 100),
                load=scenario.get('load', 1.0),
                initial_temp=scenario.get('initial_temp', 25.0)
            )
            
            final_state = self.history[-1] if self.history else {}
            
            results.append({
                'scenario': scenario.get('name', 'Unnamed'),
                'final_temperature': final_state.get('temperature', 0),
                'final_health': final_state.get('health', 0),
                'remaining_life': final_state.get('remaining_life', 0)
            })
        
        return results
    
    def optimize_parameters(self, target_life: float,
                           max_temp: float) -> Dict[str, Any]:
        """Find optimal parameters for target life and temperature constraint."""
        best_result = None
        best_throughput = 0
        
        for speed in range(50, 151, 10):
            for load in [0.5, 0.75, 1.0, 1.25]:
                heat_input = speed * load * 0.5
                
                self.wear_model.reset()
                self.run_simulation(
                    duration=100, dt=1.0,
                    heat_input=heat_input,
                    speed=speed, load=load
                )
                
                final = self.history[-1]
                remaining_life = self.wear_model.predict_remaining_life(speed, load)
                
                if final['temperature'] <= max_temp and remaining_life >= target_life:
                    throughput = speed * load
                    if throughput > best_throughput:
                        best_throughput = throughput
                        best_result = {
                            'speed': speed,
                            'load': load,
                            'heat_input': heat_input,
                            'final_temperature': final['temperature'],
                            'remaining_life': remaining_life,
                            'throughput': throughput
                        }
        
        return best_result or {'error': 'No feasible solution found'}


def run_demonstration() -> None:
    """Run the simulation demonstration."""
    
    print_section("Simulation and Physics Models Demo")
    print("This demo shows how physics models enable prediction and optimization.\n")
    
    thermal = ThermalModel(thermal_mass=50.0, heat_transfer_coeff=0.2, ambient_temp=20.0)
    wear = MechanicalWearModel(wear_coefficient=0.0005, speed_exponent=1.5)
    engine = SimulationEngine(thermal_model=thermal, wear_model=wear)
    
    print("Created Physics Models:")
    print(f"  Thermal: mass={thermal.thermal_mass}, h={thermal.heat_transfer_coeff}")
    print(f"  Wear: k={wear.wear_coefficient}, exp={wear.speed_exponent}")
    
    print_section("Thermal Predictions")
    
    steady_state = thermal.predict_steady_state(heat_input=50)
    print(f"Steady-state temperature at 50W heat input: {steady_state:.1f}°C")
    
    time_to_50 = thermal.time_to_temperature(25, 50, 50)
    print(f"Time to reach 50°C from 25°C: {time_to_50:.1f} seconds")
    
    print_section("Running Simulation")
    
    wear.reset()
    history = engine.run_simulation(
        duration=100, dt=1.0,
        heat_input=50, speed=100, load=1.0,
        initial_temp=25.0
    )
    
    print("\nTime | Temperature | Health  | Remaining Life")
    print("-" * 50)
    for state in history[::20]:
        print(f"{state['time']:4.0f}s | {state['temperature']:8.1f}°C | {state['health']:.4f} | {state['remaining_life']:.1f}h")
    
    print(f"\nFinal state after 100s:")
    final = history[-1]
    print(f"  Temperature: {final['temperature']}°C")
    print(f"  Health: {final['health']:.2%}")
    print(f"  Remaining Life: {final['remaining_life']:.1f} hours")
    
    print_section("What-If Analysis")
    
    scenarios = [
        {'name': 'Normal', 'speed': 100, 'load': 1.0, 'heat_input': 50},
        {'name': 'High Speed', 'speed': 150, 'load': 1.0, 'heat_input': 75},
        {'name': 'High Load', 'speed': 100, 'load': 1.5, 'heat_input': 75},
        {'name': 'Conservative', 'speed': 80, 'load': 0.8, 'heat_input': 32},
    ]
    
    results = engine.what_if_analysis(scenarios, duration=100)
    
    print("\nScenario      | Final Temp | Final Health | Remaining Life")
    print("-" * 60)
    for r in results:
        print(f"{r['scenario']:13s} | {r['final_temperature']:8.1f}°C | {r['final_health']:10.2%} | {r['remaining_life']:10.1f}h")
    
    print_section("Parameter Optimization")
    
    print("Finding optimal parameters for:")
    print("  - Target remaining life: >= 500 hours")
    print("  - Maximum temperature: <= 60°C")
    
    optimal = engine.optimize_parameters(target_life=500, max_temp=60)
    
    if 'error' not in optimal:
        print(f"\nOptimal Parameters Found:")
        print(f"  Speed: {optimal['speed']} rpm")
        print(f"  Load: {optimal['load']}")
        print(f"  Final Temperature: {optimal['final_temperature']:.1f}°C")
        print(f"  Remaining Life: {optimal['remaining_life']:.1f} hours")
        print(f"  Throughput: {optimal['throughput']:.1f} units")
    else:
        print(f"\n{optimal['error']}")
    
    print_section("Key Takeaways")
    print("""
1. Physics models predict system behavior based on physical laws
2. Thermal models simulate heating, cooling, and heat transfer
3. Wear models predict component degradation over time
4. What-if analysis tests scenarios without physical risk
5. Optimization finds best parameters within constraints
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
