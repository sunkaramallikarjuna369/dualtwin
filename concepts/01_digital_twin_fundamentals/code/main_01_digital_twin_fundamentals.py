"""
Digital Twin Fundamentals - Main Demonstration

This script demonstrates the core concepts of digital twins by creating
a virtual representation of a temperature-controlled industrial system.

Usage:
    python main_01_digital_twin_fundamentals.py [--duration SECONDS]

Example:
    python main_01_digital_twin_fundamentals.py --duration 30
"""

import argparse
import os
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)

from common.utils import (
    Alert,
    SensorReading,
    SensorSimulator,
    TwinState,
    calculate_statistics,
    detect_anomalies,
    generate_id,
    print_section,
    print_twin_state,
)


@dataclass
class PhysicalAsset:
    """Represents a physical temperature-controlled system."""
    
    asset_id: str
    name: str
    target_temperature: float = 25.0
    current_temperature: float = 25.0
    heater_power: float = 0.0  # 0-100%
    ambient_temperature: float = 20.0
    thermal_mass: float = 100.0
    heat_loss_coefficient: float = 0.5
    
    def update(self, dt: float = 1.0) -> None:
        """Simulate physical behavior for one time step."""
        heat_input = self.heater_power * 10  # Convert % to watts
        heat_loss = self.heat_loss_coefficient * (self.current_temperature - self.ambient_temperature)
        temp_change = (heat_input - heat_loss) / self.thermal_mass * dt
        
        noise = random.gauss(0, 0.1)
        self.current_temperature += temp_change + noise
    
    def read_sensor(self) -> SensorReading:
        """Read the temperature sensor with realistic noise."""
        sensor_noise = random.gauss(0, 0.2)
        measured_value = self.current_temperature + sensor_noise
        
        return SensorReading(
            sensor_id=f"{self.asset_id}-TEMP",
            timestamp=datetime.now(),
            value=measured_value,
            unit="°C",
            quality=0.95 + random.uniform(-0.05, 0.05)
        )
    
    def set_heater(self, power: float) -> None:
        """Set heater power (0-100%)."""
        self.heater_power = max(0, min(100, power))


class DigitalTwin:
    """Digital Twin of a temperature-controlled system."""
    
    def __init__(self, twin_id: str, name: str, target_temperature: float = 25.0):
        self.twin_id = twin_id
        self.name = name
        self.target_temperature = target_temperature
        
        self.state = TwinState(
            twin_id=twin_id,
            timestamp=datetime.now(),
            properties={
                'temperature': target_temperature,
                'heater_power': 0.0,
                'status': 'normal',
                'readings_count': 0
            },
            status='active',
            health_score=1.0
        )
        
        self.history: List[Dict[str, Any]] = []
        self.alerts: List[Alert] = []
        self.thresholds = {
            'temp_high_warning': target_temperature + 5,
            'temp_high_critical': target_temperature + 10,
            'temp_low_warning': target_temperature - 5,
            'temp_low_critical': target_temperature - 10
        }
    
    def synchronize(self, reading: SensorReading) -> None:
        """Update twin state from sensor reading."""
        old_temp = self.state.properties['temperature']
        
        self.state.properties['temperature'] = reading.value
        self.state.properties['readings_count'] += 1
        self.state.timestamp = reading.timestamp
        
        self.history.append({
            'timestamp': reading.timestamp,
            'temperature': reading.value,
            'quality': reading.quality
        })
        
        self._check_thresholds(reading.value)
        self._update_health_score(reading)
    
    def _check_thresholds(self, temperature: float) -> None:
        """Check temperature against thresholds and generate alerts."""
        if temperature >= self.thresholds['temp_high_critical']:
            self._create_alert('critical', f'Temperature critical high: {temperature:.1f}°C')
            self.state.properties['status'] = 'critical'
        elif temperature >= self.thresholds['temp_high_warning']:
            self._create_alert('warning', f'Temperature warning high: {temperature:.1f}°C')
            self.state.properties['status'] = 'warning'
        elif temperature <= self.thresholds['temp_low_critical']:
            self._create_alert('critical', f'Temperature critical low: {temperature:.1f}°C')
            self.state.properties['status'] = 'critical'
        elif temperature <= self.thresholds['temp_low_warning']:
            self._create_alert('warning', f'Temperature warning low: {temperature:.1f}°C')
            self.state.properties['status'] = 'warning'
        else:
            self.state.properties['status'] = 'normal'
    
    def _create_alert(self, severity: str, message: str) -> None:
        """Create and store an alert."""
        alert = Alert(
            alert_id=generate_id('ALERT'),
            twin_id=self.twin_id,
            timestamp=datetime.now(),
            severity=severity,
            message=message,
            source='threshold_monitor'
        )
        self.alerts.append(alert)
    
    def _update_health_score(self, reading: SensorReading) -> None:
        """Update the health score based on data quality and status."""
        base_score = reading.quality
        
        status = self.state.properties['status']
        if status == 'critical':
            base_score *= 0.5
        elif status == 'warning':
            base_score *= 0.8
        
        self.state.health_score = base_score
    
    def get_analytics(self) -> Dict[str, Any]:
        """Calculate analytics from historical data."""
        if not self.history:
            return {}
        
        temperatures = [h['temperature'] for h in self.history]
        stats = calculate_statistics(temperatures)
        anomalies = detect_anomalies(temperatures)
        
        return {
            'statistics': stats,
            'anomaly_count': len(anomalies),
            'anomalies': anomalies[:5],  # First 5 anomalies
            'total_readings': len(self.history),
            'alert_count': len(self.alerts)
        }
    
    def recommend_action(self) -> str:
        """Provide a recommended action based on current state."""
        temp = self.state.properties['temperature']
        target = self.target_temperature
        
        if temp > target + 2:
            return f"Reduce heater power. Current: {temp:.1f}°C, Target: {target:.1f}°C"
        elif temp < target - 2:
            return f"Increase heater power. Current: {temp:.1f}°C, Target: {target:.1f}°C"
        else:
            return f"System operating normally at {temp:.1f}°C"


def run_simulation(duration: int = 60) -> None:
    """Run the digital twin simulation."""
    
    print_section("Digital Twin Fundamentals Demo")
    print("This demo shows how a digital twin mirrors a physical system.\n")
    
    physical_asset = PhysicalAsset(
        asset_id="ASSET-001",
        name="Temperature Control Unit",
        target_temperature=25.0,
        current_temperature=20.0
    )
    
    digital_twin = DigitalTwin(
        twin_id="TWIN-001",
        name="Temperature Control Unit Twin",
        target_temperature=25.0
    )
    
    print("Physical Asset Created:")
    print(f"  ID: {physical_asset.asset_id}")
    print(f"  Name: {physical_asset.name}")
    print(f"  Initial Temperature: {physical_asset.current_temperature}°C")
    print(f"  Target Temperature: {physical_asset.target_temperature}°C")
    
    print("\nDigital Twin Created:")
    print(f"  ID: {digital_twin.twin_id}")
    print(f"  Name: {digital_twin.name}")
    
    print_section("Starting Simulation")
    print(f"Duration: {duration} seconds")
    print("The physical system will heat up while the twin tracks its state.\n")
    
    physical_asset.set_heater(80)
    print(f"Heater set to {physical_asset.heater_power}% power\n")
    
    print("Time | Physical Temp | Twin Temp | Status | Health")
    print("-" * 60)
    
    for t in range(duration):
        physical_asset.update(dt=1.0)
        
        reading = physical_asset.read_sensor()
        digital_twin.synchronize(reading)
        
        if t % 5 == 0 or t == duration - 1:
            print(f"{t:4d}s | {physical_asset.current_temperature:12.2f}°C | "
                  f"{digital_twin.state.properties['temperature']:8.2f}°C | "
                  f"{digital_twin.state.properties['status']:8s} | "
                  f"{digital_twin.state.health_score:.0%}")
        
        if physical_asset.current_temperature > 30:
            physical_asset.set_heater(20)
        elif physical_asset.current_temperature < 24:
            physical_asset.set_heater(80)
        
        time.sleep(0.1)
    
    print_section("Simulation Complete")
    
    print("\nFinal Twin State:")
    print_twin_state(digital_twin.state)
    
    print_section("Analytics Summary")
    analytics = digital_twin.get_analytics()
    
    print("Temperature Statistics:")
    stats = analytics['statistics']
    print(f"  Mean: {stats['mean']:.2f}°C")
    print(f"  Std Dev: {stats['std']:.2f}°C")
    print(f"  Min: {stats['min']:.2f}°C")
    print(f"  Max: {stats['max']:.2f}°C")
    
    print(f"\nTotal Readings: {analytics['total_readings']}")
    print(f"Anomalies Detected: {analytics['anomaly_count']}")
    print(f"Alerts Generated: {analytics['alert_count']}")
    
    if digital_twin.alerts:
        print("\nRecent Alerts:")
        for alert in digital_twin.alerts[-5:]:
            print(f"  [{alert.severity.upper()}] {alert.message}")
    
    print_section("Recommended Action")
    print(digital_twin.recommend_action())
    
    print_section("Key Takeaways")
    print("""
1. The digital twin continuously synchronized with the physical asset
2. Real-time monitoring enabled immediate visibility into system state
3. Threshold-based alerts provided early warning of issues
4. Analytics summarized historical behavior for insights
5. The twin can recommend actions based on current state

This demonstrates the core value of digital twins: visibility, monitoring,
and actionable insights from physical systems.
""")


def main():
    parser = argparse.ArgumentParser(
        description='Digital Twin Fundamentals Demonstration'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='Simulation duration in seconds (default: 30)'
    )
    
    args = parser.parse_args()
    run_simulation(duration=args.duration)


if __name__ == "__main__":
    main()
