"""
Cloud Edge Integration for Twins - Main Demonstration

This script demonstrates cloud-edge architecture with simulated edge
processing, cloud synchronization, and workload distribution.

Usage:
    python main_07_cloud_edge_integration_for_twins.py

Example:
    python main_07_cloud_edge_integration_for_twins.py
"""

import sys
import os
import time
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from collections import deque

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class DataPoint:
    """A single data point from a sensor."""
    sensor_id: str
    timestamp: datetime
    value: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp.isoformat(),
            'value': self.value
        }


class EdgeDevice:
    """Simulated edge computing device."""
    
    def __init__(self, device_id: str, latency_ms: float = 5.0):
        self.device_id = device_id
        self.latency_ms = latency_ms
        self.buffer: deque = deque(maxlen=1000)
        self.local_twin_state: Dict[str, Any] = {}
        self.stats = {
            'points_received': 0,
            'points_filtered': 0,
            'points_forwarded': 0,
            'local_decisions': 0
        }
        self.thresholds: Dict[str, tuple] = {}
        self.cloud_connected = True
    
    def set_threshold(self, sensor_id: str, low: float, high: float) -> None:
        """Set alert thresholds for a sensor."""
        self.thresholds[sensor_id] = (low, high)
    
    def process_data(self, data: DataPoint) -> Dict[str, Any]:
        """Process data at the edge."""
        self.stats['points_received'] += 1
        
        self.local_twin_state[data.sensor_id] = {
            'value': data.value,
            'timestamp': data.timestamp
        }
        
        alert = None
        if data.sensor_id in self.thresholds:
            low, high = self.thresholds[data.sensor_id]
            if data.value < low or data.value > high:
                alert = {
                    'type': 'threshold_breach',
                    'sensor_id': data.sensor_id,
                    'value': data.value,
                    'threshold': (low, high)
                }
                self.stats['local_decisions'] += 1
        
        should_forward = self._should_forward(data)
        
        if should_forward:
            self.buffer.append(data)
            self.stats['points_forwarded'] += 1
        else:
            self.stats['points_filtered'] += 1
        
        return {
            'processed_at': 'edge',
            'latency_ms': self.latency_ms,
            'forwarded': should_forward,
            'alert': alert
        }
    
    def _should_forward(self, data: DataPoint) -> bool:
        """Decide if data should be forwarded to cloud."""
        if data.sensor_id in self.thresholds:
            low, high = self.thresholds[data.sensor_id]
            if data.value < low or data.value > high:
                return True
        
        if random.random() < 0.1:
            return True
        
        return False
    
    def get_pending_data(self) -> List[DataPoint]:
        """Get data pending for cloud sync."""
        data = list(self.buffer)
        self.buffer.clear()
        return data
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get edge processing statistics."""
        total = self.stats['points_received']
        return {
            'device_id': self.device_id,
            'total_received': total,
            'filtered_locally': self.stats['points_filtered'],
            'forwarded_to_cloud': self.stats['points_forwarded'],
            'local_decisions': self.stats['local_decisions'],
            'filter_ratio': self.stats['points_filtered'] / total if total > 0 else 0
        }


class CloudPlatform:
    """Simulated cloud platform."""
    
    def __init__(self, platform_id: str, latency_ms: float = 100.0):
        self.platform_id = platform_id
        self.latency_ms = latency_ms
        self.twin_state: Dict[str, Dict[str, Any]] = {}
        self.historical_data: List[Dict] = []
        self.analytics_results: Dict[str, Any] = {}
        self.stats = {
            'points_received': 0,
            'analytics_runs': 0
        }
    
    def receive_data(self, edge_id: str, data: List[DataPoint]) -> Dict[str, Any]:
        """Receive data from edge device."""
        for point in data:
            self.stats['points_received'] += 1
            
            if edge_id not in self.twin_state:
                self.twin_state[edge_id] = {}
            
            self.twin_state[edge_id][point.sensor_id] = {
                'value': point.value,
                'timestamp': point.timestamp
            }
            
            self.historical_data.append({
                'edge_id': edge_id,
                **point.to_dict()
            })
        
        if len(self.historical_data) > 10000:
            self.historical_data = self.historical_data[-5000:]
        
        return {
            'received': len(data),
            'latency_ms': self.latency_ms
        }
    
    def run_analytics(self) -> Dict[str, Any]:
        """Run cloud-based analytics."""
        self.stats['analytics_runs'] += 1
        
        if not self.historical_data:
            return {}
        
        sensor_stats = {}
        for record in self.historical_data[-100:]:
            sensor_id = record['sensor_id']
            if sensor_id not in sensor_stats:
                sensor_stats[sensor_id] = []
            sensor_stats[sensor_id].append(record['value'])
        
        results = {}
        for sensor_id, values in sensor_stats.items():
            results[sensor_id] = {
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'count': len(values)
            }
        
        self.analytics_results = results
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cloud platform statistics."""
        return {
            'platform_id': self.platform_id,
            'total_received': self.stats['points_received'],
            'analytics_runs': self.stats['analytics_runs'],
            'historical_records': len(self.historical_data),
            'edge_devices': len(self.twin_state)
        }


class CloudEdgeOrchestrator:
    """Orchestrates cloud-edge integration."""
    
    def __init__(self):
        self.edge_devices: Dict[str, EdgeDevice] = {}
        self.cloud = CloudPlatform("cloud-main")
        self.sync_interval = 10
    
    def add_edge_device(self, device: EdgeDevice) -> None:
        """Register an edge device."""
        self.edge_devices[device.device_id] = device
    
    def process_sensor_data(self, edge_id: str, data: DataPoint) -> Dict[str, Any]:
        """Process sensor data through the architecture."""
        edge = self.edge_devices.get(edge_id)
        if not edge:
            return {'error': 'Unknown edge device'}
        
        result = edge.process_data(data)
        return result
    
    def sync_to_cloud(self) -> Dict[str, Any]:
        """Synchronize edge data to cloud."""
        total_synced = 0
        
        for edge_id, edge in self.edge_devices.items():
            pending = edge.get_pending_data()
            if pending:
                self.cloud.receive_data(edge_id, pending)
                total_synced += len(pending)
        
        return {'synced_points': total_synced}
    
    def compare_latency(self, data: DataPoint, edge_id: str) -> Dict[str, Any]:
        """Compare edge vs cloud processing latency."""
        edge = self.edge_devices.get(edge_id)
        if not edge:
            return {}
        
        edge_latency = edge.latency_ms
        cloud_latency = edge.latency_ms + self.cloud.latency_ms
        
        return {
            'edge_latency_ms': edge_latency,
            'cloud_latency_ms': cloud_latency,
            'latency_reduction': f"{(1 - edge_latency/cloud_latency)*100:.1f}%"
        }


def run_demonstration() -> None:
    """Run the cloud-edge integration demonstration."""
    
    print_section("Cloud Edge Integration Demo")
    print("This demo shows how data flows between edge devices and cloud.\n")
    
    orchestrator = CloudEdgeOrchestrator()
    
    edge1 = EdgeDevice("edge-factory-1", latency_ms=5.0)
    edge1.set_threshold("TEMP-001", 20.0, 50.0)
    edge1.set_threshold("VIB-001", 0.0, 5.0)
    
    edge2 = EdgeDevice("edge-factory-2", latency_ms=8.0)
    edge2.set_threshold("TEMP-002", 20.0, 45.0)
    
    orchestrator.add_edge_device(edge1)
    orchestrator.add_edge_device(edge2)
    
    print("Created Architecture:")
    print(f"  Edge Devices: {list(orchestrator.edge_devices.keys())}")
    print(f"  Cloud Platform: {orchestrator.cloud.platform_id}")
    
    print_section("Processing Sensor Data")
    
    sensors = [
        ("edge-factory-1", "TEMP-001", 25.0, 3.0),
        ("edge-factory-1", "VIB-001", 2.0, 1.0),
        ("edge-factory-2", "TEMP-002", 30.0, 5.0),
    ]
    
    print("\nSimulating 50 sensor readings...")
    alerts = []
    
    for i in range(50):
        for edge_id, sensor_id, base, noise in sensors:
            value = base + random.gauss(0, noise)
            if i == 30 and sensor_id == "TEMP-001":
                value = 55.0
            
            data = DataPoint(
                sensor_id=sensor_id,
                timestamp=datetime.now(),
                value=round(value, 2)
            )
            
            result = orchestrator.process_sensor_data(edge_id, data)
            
            if result.get('alert'):
                alerts.append(result['alert'])
                print(f"  ALERT at edge: {result['alert']['sensor_id']} = {result['alert']['value']}")
    
    print_section("Edge Statistics")
    
    for edge_id, edge in orchestrator.edge_devices.items():
        stats = edge.get_statistics()
        print(f"\n{edge_id}:")
        print(f"  Total received: {stats['total_received']}")
        print(f"  Filtered locally: {stats['filtered_locally']} ({stats['filter_ratio']:.1%})")
        print(f"  Forwarded to cloud: {stats['forwarded_to_cloud']}")
        print(f"  Local decisions: {stats['local_decisions']}")
    
    print_section("Cloud Synchronization")
    
    sync_result = orchestrator.sync_to_cloud()
    print(f"Synced {sync_result['synced_points']} points to cloud")
    
    cloud_stats = orchestrator.cloud.get_statistics()
    print(f"\nCloud Platform Statistics:")
    print(f"  Total received: {cloud_stats['total_received']}")
    print(f"  Edge devices connected: {cloud_stats['edge_devices']}")
    
    print_section("Cloud Analytics")
    
    analytics = orchestrator.cloud.run_analytics()
    print("Sensor Statistics from Cloud:")
    for sensor_id, stats in analytics.items():
        print(f"  {sensor_id}: mean={stats['mean']:.2f}, range=[{stats['min']:.2f}, {stats['max']:.2f}]")
    
    print_section("Latency Comparison")
    
    test_data = DataPoint("TEMP-001", datetime.now(), 25.0)
    latency = orchestrator.compare_latency(test_data, "edge-factory-1")
    
    print(f"Edge processing latency: {latency['edge_latency_ms']}ms")
    print(f"Cloud processing latency: {latency['cloud_latency_ms']}ms")
    print(f"Latency reduction with edge: {latency['latency_reduction']}")
    
    print_section("Bandwidth Savings")
    
    total_received = sum(e.stats['points_received'] for e in orchestrator.edge_devices.values())
    total_forwarded = sum(e.stats['points_forwarded'] for e in orchestrator.edge_devices.values())
    savings = (1 - total_forwarded / total_received) * 100 if total_received > 0 else 0
    
    print(f"Total data points generated: {total_received}")
    print(f"Data points sent to cloud: {total_forwarded}")
    print(f"Bandwidth savings: {savings:.1f}%")
    
    print_section("Key Takeaways")
    print("""
1. Edge processing provides low-latency responses (5-10ms vs 100+ms)
2. Edge filtering reduces bandwidth by 80-90%
3. Critical alerts are detected locally without cloud dependency
4. Cloud receives aggregated data for analytics and storage
5. Hybrid architecture balances speed, cost, and capability
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
