"""
Dual-Twin Architecture - Main Demonstration

This script demonstrates a dual-twin architecture with asset twins
paired with a process twin to show how they interact and provide
combined insights.

Usage:
    python main_02_dual_twin_architecture.py [--duration SECONDS]

Example:
    python main_02_dual_twin_architecture.py --duration 60
"""

import argparse
import random
import sys
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import generate_id, print_section


@dataclass
class AssetTwin:
    """Digital twin of an individual asset (equipment)."""
    
    twin_id: str
    asset_type: str
    name: str
    
    state: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)
    health_score: float = 1.0
    status: str = "idle"
    
    process_twin_id: Optional[str] = None
    
    def update_state(self, sensor_data: Dict[str, float]) -> None:
        """Update asset state from sensor readings."""
        self.state = {**sensor_data, 'timestamp': datetime.now()}
        self.history.append(self.state.copy())
        self._calculate_health()
    
    def _calculate_health(self) -> None:
        """Calculate health score based on state."""
        issues = 0
        if self.state.get('temperature', 0) > 50:
            issues += 1
        if self.state.get('vibration', 0) > 4:
            issues += 1
        self.health_score = max(0, 1 - issues * 0.2)
    
    def get_output_rate(self) -> float:
        """Get current output rate for process twin."""
        if self.status == "running":
            base_rate = self.state.get('speed', 100) / 100
            return base_rate * self.health_score
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'twin_id': self.twin_id,
            'asset_type': self.asset_type,
            'name': self.name,
            'status': self.status,
            'health_score': self.health_score,
            'state': self.state
        }


@dataclass
class ProcessTwin:
    """Digital twin of a production process."""
    
    twin_id: str
    process_name: str
    
    asset_twins: List[AssetTwin] = field(default_factory=list)
    process_state: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)
    
    throughput: float = 0.0
    efficiency: float = 1.0
    bottleneck_asset: Optional[str] = None
    
    def register_asset(self, asset_twin: AssetTwin) -> None:
        """Register an asset twin with this process twin."""
        self.asset_twins.append(asset_twin)
        asset_twin.process_twin_id = self.twin_id
    
    def synchronize(self) -> None:
        """Synchronize process state from all asset twins."""
        if not self.asset_twins:
            return
        
        output_rates = []
        for asset in self.asset_twins:
            rate = asset.get_output_rate()
            output_rates.append((asset.twin_id, asset.name, rate, asset.health_score))
        
        min_rate = min(r[2] for r in output_rates)
        self.throughput = min_rate * 100
        
        bottleneck = min(output_rates, key=lambda x: x[2])
        self.bottleneck_asset = bottleneck[1] if bottleneck[2] < 0.9 else None
        
        avg_health = sum(a.health_score for a in self.asset_twins) / len(self.asset_twins)
        self.efficiency = avg_health
        
        self.process_state = {
            'timestamp': datetime.now(),
            'throughput': self.throughput,
            'efficiency': self.efficiency,
            'bottleneck': self.bottleneck_asset,
            'asset_count': len(self.asset_twins),
            'assets_running': sum(1 for a in self.asset_twins if a.status == "running")
        }
        self.history.append(self.process_state.copy())
    
    def get_cross_twin_analytics(self) -> Dict[str, Any]:
        """Generate analytics combining asset and process data."""
        if not self.history:
            return {}
        
        asset_health = {a.name: a.health_score for a in self.asset_twins}
        asset_status = {a.name: a.status for a in self.asset_twins}
        
        return {
            'process_throughput': self.throughput,
            'process_efficiency': self.efficiency,
            'bottleneck_asset': self.bottleneck_asset,
            'asset_health_scores': asset_health,
            'asset_statuses': asset_status,
            'recommendation': self._generate_recommendation()
        }
    
    def _generate_recommendation(self) -> str:
        """Generate coordinated recommendation."""
        if self.bottleneck_asset:
            return f"Investigate {self.bottleneck_asset} - it's limiting process throughput"
        
        low_health_assets = [a.name for a in self.asset_twins if a.health_score < 0.8]
        if low_health_assets:
            return f"Schedule maintenance for: {', '.join(low_health_assets)}"
        
        if self.efficiency > 0.95:
            return "Process running optimally - consider increasing production targets"
        
        return "Process running normally - no immediate action required"


class PhysicalAsset:
    """Simulated physical asset."""
    
    def __init__(self, asset_id: str, asset_type: str):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.running = False
        self.speed = 0.0
        self.temperature = 25.0
        self.vibration = 1.0
        self.wear_factor = 0.0
    
    def start(self) -> None:
        self.running = True
        self.speed = 100.0
    
    def stop(self) -> None:
        self.running = False
        self.speed = 0.0
    
    def update(self) -> None:
        """Simulate physical behavior."""
        if self.running:
            self.wear_factor += random.uniform(0, 0.01)
            self.temperature = 25 + 20 * (self.speed / 100) + self.wear_factor * 10
            self.vibration = 1.0 + self.wear_factor * 5 + random.gauss(0, 0.2)
            self.temperature += random.gauss(0, 1)
    
    def read_sensors(self) -> Dict[str, float]:
        return {
            'speed': self.speed + random.gauss(0, 2),
            'temperature': self.temperature,
            'vibration': self.vibration,
            'power': self.speed * 0.05 if self.running else 0
        }


def run_simulation(duration: int = 60) -> None:
    """Run the dual-twin architecture simulation."""
    
    print_section("Dual-Twin Architecture Demo")
    print("This demo shows how asset twins and process twins work together.\n")
    
    physical_assets = [
        PhysicalAsset("PUMP-001", "Pump"),
        PhysicalAsset("MOTOR-001", "Motor"),
        PhysicalAsset("CONVEYOR-001", "Conveyor"),
    ]
    
    asset_twins = [
        AssetTwin(twin_id=f"DT-{pa.asset_id}", asset_type=pa.asset_type, name=pa.asset_id)
        for pa in physical_assets
    ]
    
    process_twin = ProcessTwin(
        twin_id="DT-PROCESS-001",
        process_name="Production Line Alpha"
    )
    
    for asset_twin in asset_twins:
        process_twin.register_asset(asset_twin)
    
    print("Created Dual-Twin Architecture:")
    print(f"  Process Twin: {process_twin.process_name}")
    print(f"  Asset Twins: {[a.name for a in asset_twins]}")
    
    print_section("Starting Simulation")
    
    for pa in physical_assets:
        pa.start()
    for at in asset_twins:
        at.status = "running"
    
    print("All assets started.\n")
    
    print("Time | Throughput | Efficiency | Bottleneck")
    print("-" * 55)
    
    for t in range(duration):
        for i, pa in enumerate(physical_assets):
            pa.update()
            sensor_data = pa.read_sensors()
            asset_twins[i].update_state(sensor_data)
        
        if t == 20:
            physical_assets[0].wear_factor = 0.5
            print(f"\n[t={t}] Simulating wear on {physical_assets[0].asset_id}")
        
        process_twin.synchronize()
        
        if t % 5 == 0:
            ps = process_twin.process_state
            bottleneck = ps.get('bottleneck', 'None') or 'None'
            print(f"{t:4d}s | {ps['throughput']:10.1f}% | {ps['efficiency']:10.1%} | {bottleneck}")
        
        time.sleep(0.05)
    
    print_section("Cross-Twin Analytics")
    
    analytics = process_twin.get_cross_twin_analytics()
    
    print(f"Process Throughput: {analytics['process_throughput']:.1f}%")
    print(f"Process Efficiency: {analytics['process_efficiency']:.1%}")
    print(f"Bottleneck Asset: {analytics['bottleneck_asset'] or 'None'}")
    
    print("\nAsset Health Scores:")
    for name, health in analytics['asset_health_scores'].items():
        status = "OK" if health > 0.8 else "ATTENTION"
        print(f"  {name}: {health:.1%} [{status}]")
    
    print_section("Coordinated Recommendation")
    print(analytics['recommendation'])
    
    print_section("Key Takeaways")
    print("""
1. Asset twins track individual equipment health and performance
2. Process twin aggregates asset data into process-level metrics
3. Cross-twin analytics identify bottlenecks and optimization opportunities
4. Coordinated recommendations consider both asset and process perspectives
5. Dual-twin architecture enables holistic system optimization
""")


def main():
    parser = argparse.ArgumentParser(
        description='Dual-Twin Architecture Demonstration'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=40,
        help='Simulation duration in seconds (default: 40)'
    )
    
    args = parser.parse_args()
    run_simulation(duration=args.duration)


if __name__ == "__main__":
    main()
