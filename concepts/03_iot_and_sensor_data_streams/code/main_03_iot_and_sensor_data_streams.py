"""
IoT and Sensor Data Streams - Main Demonstration

This script demonstrates IoT sensor data streaming with simulated sensors,
an IoT gateway, and a digital twin that updates from the stream.

Usage:
    python main_03_iot_and_sensor_data_streams.py [--duration SECONDS]

Example:
    python main_03_iot_and_sensor_data_streams.py --duration 30
"""

import argparse
import random
import sys
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from collections import deque

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class SensorReading:
    """A single sensor reading."""
    sensor_id: str
    timestamp: datetime
    value: float
    unit: str
    quality: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp.isoformat(),
            'value': self.value,
            'unit': self.unit,
            'quality': self.quality
        }


class Sensor:
    """Simulated IoT sensor."""
    
    def __init__(self, sensor_id: str, sensor_type: str, unit: str,
                 base_value: float = 25.0, noise: float = 1.0,
                 drift_rate: float = 0.0, failure_prob: float = 0.01):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.base_value = base_value
        self.noise = noise
        self.drift_rate = drift_rate
        self.failure_prob = failure_prob
        self.drift = 0.0
        self.failed = False
    
    def read(self) -> SensorReading:
        """Take a sensor reading."""
        if random.random() < self.failure_prob:
            self.failed = True
        
        if self.failed:
            return SensorReading(
                sensor_id=self.sensor_id,
                timestamp=datetime.now(),
                value=0.0,
                unit=self.unit,
                quality=0.0
            )
        
        self.drift += self.drift_rate
        value = self.base_value + self.drift + random.gauss(0, self.noise)
        quality = max(0.8, 1.0 - abs(self.drift) / 10)
        
        return SensorReading(
            sensor_id=self.sensor_id,
            timestamp=datetime.now(),
            value=round(value, 2),
            unit=self.unit,
            quality=round(quality, 3)
        )
    
    def reset(self) -> None:
        """Reset sensor to initial state."""
        self.drift = 0.0
        self.failed = False


class IoTGateway:
    """IoT gateway that aggregates sensor data."""
    
    def __init__(self, gateway_id: str, buffer_size: int = 100):
        self.gateway_id = gateway_id
        self.sensors: List[Sensor] = []
        self.buffer: deque = deque(maxlen=buffer_size)
        self.subscribers: List[Callable] = []
        self.stats = {
            'readings_received': 0,
            'readings_forwarded': 0,
            'quality_issues': 0
        }
    
    def register_sensor(self, sensor: Sensor) -> None:
        """Register a sensor with this gateway."""
        self.sensors.append(sensor)
    
    def subscribe(self, callback: Callable) -> None:
        """Subscribe to receive data from this gateway."""
        self.subscribers.append(callback)
    
    def collect_and_forward(self) -> List[SensorReading]:
        """Collect readings from all sensors and forward to subscribers."""
        readings = []
        
        for sensor in self.sensors:
            reading = sensor.read()
            self.stats['readings_received'] += 1
            
            if reading.quality < 0.5:
                self.stats['quality_issues'] += 1
                continue
            
            readings.append(reading)
            self.buffer.append(reading)
        
        for subscriber in self.subscribers:
            for reading in readings:
                subscriber(reading)
                self.stats['readings_forwarded'] += 1
        
        return readings
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get gateway statistics."""
        return {
            'gateway_id': self.gateway_id,
            'sensor_count': len(self.sensors),
            'buffer_size': len(self.buffer),
            **self.stats
        }


class StreamingDigitalTwin:
    """Digital twin that updates from sensor data streams."""
    
    def __init__(self, twin_id: str, name: str):
        self.twin_id = twin_id
        self.name = name
        self.state: Dict[str, Any] = {}
        self.history: List[Dict] = []
        self.last_update: Optional[datetime] = None
        self.update_count = 0
    
    def on_sensor_data(self, reading: SensorReading) -> None:
        """Handle incoming sensor data."""
        self.state[reading.sensor_id] = {
            'value': reading.value,
            'unit': reading.unit,
            'quality': reading.quality,
            'timestamp': reading.timestamp
        }
        self.last_update = reading.timestamp
        self.update_count += 1
        
        self.history.append({
            'sensor_id': reading.sensor_id,
            'value': reading.value,
            'timestamp': reading.timestamp
        })
        
        if len(self.history) > 1000:
            self.history = self.history[-500:]
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current twin state."""
        return {
            'twin_id': self.twin_id,
            'name': self.name,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'update_count': self.update_count,
            'sensors': self.state
        }
    
    def get_sensor_statistics(self, sensor_id: str) -> Dict[str, float]:
        """Get statistics for a specific sensor."""
        values = [h['value'] for h in self.history if h['sensor_id'] == sensor_id]
        if not values:
            return {}
        
        import statistics
        return {
            'count': len(values),
            'mean': round(statistics.mean(values), 2),
            'min': round(min(values), 2),
            'max': round(max(values), 2),
            'stdev': round(statistics.stdev(values), 2) if len(values) > 1 else 0
        }


def run_simulation(duration: int = 30) -> None:
    """Run the IoT data streaming simulation."""
    
    print_section("IoT and Sensor Data Streams Demo")
    print("This demo shows how sensor data flows from physical devices to digital twins.\n")
    
    sensors = [
        Sensor("TEMP-001", "temperature", "°C", base_value=25.0, noise=0.5),
        Sensor("PRESS-001", "pressure", "bar", base_value=5.0, noise=0.1),
        Sensor("VIB-001", "vibration", "mm/s", base_value=2.0, noise=0.3, drift_rate=0.02),
        Sensor("FLOW-001", "flow", "l/min", base_value=100.0, noise=2.0),
    ]
    
    gateway = IoTGateway("GW-001")
    for sensor in sensors:
        gateway.register_sensor(sensor)
    
    twin = StreamingDigitalTwin("DT-PUMP-001", "Industrial Pump")
    gateway.subscribe(twin.on_sensor_data)
    
    print("Created IoT Infrastructure:")
    print(f"  Sensors: {[s.sensor_id for s in sensors]}")
    print(f"  Gateway: {gateway.gateway_id}")
    print(f"  Digital Twin: {twin.name}")
    
    print_section("Starting Data Stream")
    print("\nTime | Sensor    | Value      | Quality | Twin Updates")
    print("-" * 60)
    
    for t in range(duration):
        readings = gateway.collect_and_forward()
        
        for reading in readings:
            print(f"{t:4d}s | {reading.sensor_id:9s} | {reading.value:8.2f} {reading.unit:5s} | {reading.quality:.2f}    | {twin.update_count}")
        
        time.sleep(0.1)
    
    print_section("Gateway Statistics")
    stats = gateway.get_statistics()
    print(f"Readings Received: {stats['readings_received']}")
    print(f"Readings Forwarded: {stats['readings_forwarded']}")
    print(f"Quality Issues: {stats['quality_issues']}")
    
    print_section("Digital Twin State")
    state = twin.get_current_state()
    print(f"Twin: {state['name']} ({state['twin_id']})")
    print(f"Total Updates: {state['update_count']}")
    print(f"Last Update: {state['last_update']}")
    
    print("\nSensor Statistics:")
    for sensor in sensors:
        stats = twin.get_sensor_statistics(sensor.sensor_id)
        if stats:
            print(f"  {sensor.sensor_id}: mean={stats['mean']}, min={stats['min']}, max={stats['max']}")
    
    print_section("Key Takeaways")
    print("""
1. Sensors continuously measure physical properties
2. IoT gateways aggregate and filter sensor data
3. Data quality indicators help identify unreliable readings
4. Digital twins update in real-time from sensor streams
5. Historical data enables statistical analysis and trend detection
""")


def main():
    parser = argparse.ArgumentParser(
        description='IoT and Sensor Data Streams Demonstration'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=20,
        help='Simulation duration in seconds (default: 20)'
    )
    
    args = parser.parse_args()
    run_simulation(duration=args.duration)


if __name__ == "__main__":
    main()
