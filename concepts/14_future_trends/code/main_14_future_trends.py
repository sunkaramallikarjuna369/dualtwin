"""
Future Trends - Main Demonstration

This script demonstrates future twin concepts including multi-twin ecosystems,
dual-twin coordination, and autonomous decision-making.

Usage:
    python main_14_future_trends.py

Example:
    python main_14_future_trends.py
"""

import sys
import os
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


class TwinType(Enum):
    """Types of digital twins."""
    ASSET = "asset"
    PROCESS = "process"
    SYSTEM = "system"
    ENTERPRISE = "enterprise"


class DecisionType(Enum):
    """Types of autonomous decisions."""
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"
    SAFETY = "safety"
    EFFICIENCY = "efficiency"


@dataclass
class EcosystemTwin:
    """A twin in a multi-twin ecosystem."""
    twin_id: str
    name: str
    twin_type: TwinType
    organization: str
    
    state: Dict[str, Any] = field(default_factory=dict)
    connections: List[str] = field(default_factory=list)
    shared_data: Dict[str, Any] = field(default_factory=dict)
    
    def connect_to(self, other_twin_id: str) -> None:
        if other_twin_id not in self.connections:
            self.connections.append(other_twin_id)
    
    def share_data(self, key: str, value: Any) -> None:
        self.shared_data[key] = {
            'value': value,
            'timestamp': datetime.now(),
            'source': self.twin_id
        }
    
    def receive_data(self, key: str, data: Dict[str, Any]) -> None:
        self.state[f"external_{key}"] = data


@dataclass
class DualTwinPair:
    """A dual-twin pairing."""
    pair_id: str
    asset_twin: EcosystemTwin
    process_twin: EcosystemTwin
    
    coordination_rules: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_coordination_rule(self, condition: str, action: str) -> None:
        self.coordination_rules.append({
            'condition': condition,
            'action': action
        })
    
    def coordinate(self) -> List[Dict[str, Any]]:
        """Coordinate between asset and process twins."""
        actions = []
        
        asset_health = self.asset_twin.state.get('health', 1.0)
        process_demand = self.process_twin.state.get('demand', 100)
        
        if asset_health < 0.7 and process_demand > 80:
            actions.append({
                'type': 'load_reduction',
                'reason': 'Asset health low, reducing process demand',
                'from_twin': self.process_twin.twin_id,
                'to_twin': self.asset_twin.twin_id,
                'action': 'Reduce demand to 60%'
            })
        
        if asset_health > 0.9 and process_demand < 50:
            actions.append({
                'type': 'capacity_increase',
                'reason': 'Asset healthy, can increase throughput',
                'from_twin': self.asset_twin.twin_id,
                'to_twin': self.process_twin.twin_id,
                'action': 'Increase capacity available'
            })
        
        return actions


@dataclass
class AutonomousDecision:
    """An autonomous decision made by a twin."""
    decision_id: str
    timestamp: datetime
    twin_id: str
    decision_type: DecisionType
    description: str
    confidence: float
    action_taken: str
    outcome: Optional[str] = None


class AutonomousTwin:
    """A twin with autonomous decision-making capabilities."""
    
    def __init__(self, twin_id: str, name: str):
        self.twin_id = twin_id
        self.name = name
        self.state: Dict[str, Any] = {}
        self.decisions: List[AutonomousDecision] = []
        self.autonomy_level: float = 0.5
        self.decision_rules: List[Dict[str, Any]] = []
    
    def add_decision_rule(self, condition: Callable, action: str,
                         decision_type: DecisionType) -> None:
        self.decision_rules.append({
            'condition': condition,
            'action': action,
            'type': decision_type
        })
    
    def update_state(self, key: str, value: Any) -> None:
        self.state[key] = value
    
    def evaluate_and_decide(self) -> List[AutonomousDecision]:
        """Evaluate state and make autonomous decisions."""
        new_decisions = []
        
        for rule in self.decision_rules:
            try:
                if rule['condition'](self.state):
                    confidence = random.uniform(0.7, 0.95)
                    
                    if confidence >= (1 - self.autonomy_level):
                        decision = AutonomousDecision(
                            decision_id=f"DEC-{len(self.decisions) + 1:04d}",
                            timestamp=datetime.now(),
                            twin_id=self.twin_id,
                            decision_type=rule['type'],
                            description=f"Triggered: {rule['action']}",
                            confidence=confidence,
                            action_taken=rule['action']
                        )
                        self.decisions.append(decision)
                        new_decisions.append(decision)
            except Exception:
                pass
        
        return new_decisions


class TwinEcosystem:
    """A multi-twin ecosystem."""
    
    def __init__(self, ecosystem_id: str):
        self.ecosystem_id = ecosystem_id
        self.twins: Dict[str, EcosystemTwin] = {}
        self.dual_pairs: Dict[str, DualTwinPair] = {}
        self.data_flows: List[Dict[str, Any]] = []
    
    def add_twin(self, twin: EcosystemTwin) -> None:
        self.twins[twin.twin_id] = twin
    
    def create_dual_pair(self, pair_id: str, asset_id: str, process_id: str) -> Optional[DualTwinPair]:
        asset = self.twins.get(asset_id)
        process = self.twins.get(process_id)
        
        if not asset or not process:
            return None
        
        pair = DualTwinPair(
            pair_id=pair_id,
            asset_twin=asset,
            process_twin=process
        )
        
        asset.connect_to(process_id)
        process.connect_to(asset_id)
        
        self.dual_pairs[pair_id] = pair
        return pair
    
    def propagate_data(self, source_id: str, key: str, value: Any) -> int:
        """Propagate data through the ecosystem."""
        source = self.twins.get(source_id)
        if not source:
            return 0
        
        source.share_data(key, value)
        
        propagated = 0
        for conn_id in source.connections:
            target = self.twins.get(conn_id)
            if target:
                target.receive_data(key, source.shared_data[key])
                propagated += 1
                
                self.data_flows.append({
                    'timestamp': datetime.now(),
                    'source': source_id,
                    'target': conn_id,
                    'key': key
                })
        
        return propagated
    
    def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get ecosystem status summary."""
        return {
            'ecosystem_id': self.ecosystem_id,
            'total_twins': len(self.twins),
            'dual_pairs': len(self.dual_pairs),
            'total_connections': sum(len(t.connections) for t in self.twins.values()),
            'data_flows': len(self.data_flows),
            'twins_by_type': {
                tt.value: len([t for t in self.twins.values() if t.twin_type == tt])
                for tt in TwinType
            }
        }


def run_demonstration() -> None:
    """Run the future trends demonstration."""
    
    print_section("Future Trends Demo")
    print("This demo shows emerging digital twin capabilities.\n")
    
    print_section("Multi-Twin Ecosystem")
    
    ecosystem = TwinEcosystem("SMART-FACTORY-ECOSYSTEM")
    
    pump_twin = EcosystemTwin(
        twin_id="DT-PUMP-001",
        name="Industrial Pump",
        twin_type=TwinType.ASSET,
        organization="Manufacturing Co"
    )
    pump_twin.state = {'health': 0.85, 'temperature': 45, 'flow_rate': 120}
    
    motor_twin = EcosystemTwin(
        twin_id="DT-MOTOR-001",
        name="Drive Motor",
        twin_type=TwinType.ASSET,
        organization="Manufacturing Co"
    )
    motor_twin.state = {'health': 0.92, 'rpm': 1450, 'current': 25}
    
    line_twin = EcosystemTwin(
        twin_id="DT-LINE-001",
        name="Production Line",
        twin_type=TwinType.PROCESS,
        organization="Manufacturing Co"
    )
    line_twin.state = {'demand': 85, 'throughput': 100, 'efficiency': 0.88}
    
    factory_twin = EcosystemTwin(
        twin_id="DT-FACTORY-001",
        name="Factory Operations",
        twin_type=TwinType.SYSTEM,
        organization="Manufacturing Co"
    )
    factory_twin.state = {'oee': 0.78, 'energy_consumption': 5000}
    
    for twin in [pump_twin, motor_twin, line_twin, factory_twin]:
        ecosystem.add_twin(twin)
    
    pump_twin.connect_to(line_twin.twin_id)
    motor_twin.connect_to(line_twin.twin_id)
    line_twin.connect_to(factory_twin.twin_id)
    
    status = ecosystem.get_ecosystem_status()
    print(f"Ecosystem: {status['ecosystem_id']}")
    print(f"  Total Twins: {status['total_twins']}")
    print(f"  Total Connections: {status['total_connections']}")
    print(f"  Twins by Type:")
    for twin_type, count in status['twins_by_type'].items():
        if count > 0:
            print(f"    {twin_type}: {count}")
    
    print_section("Dual-Twin Coordination")
    
    dual_pair = ecosystem.create_dual_pair(
        pair_id="PAIR-001",
        asset_id="DT-PUMP-001",
        process_id="DT-LINE-001"
    )
    
    if dual_pair:
        print(f"\nCreated Dual-Twin Pair: {dual_pair.pair_id}")
        print(f"  Asset Twin: {dual_pair.asset_twin.name}")
        print(f"  Process Twin: {dual_pair.process_twin.name}")
        
        pump_twin.state['health'] = 0.65
        line_twin.state['demand'] = 90
        
        print(f"\nSimulating coordination scenario:")
        print(f"  Asset health: {pump_twin.state['health']:.0%}")
        print(f"  Process demand: {line_twin.state['demand']}%")
        
        actions = dual_pair.coordinate()
        
        if actions:
            print(f"\nCoordination Actions:")
            for action in actions:
                print(f"  [{action['type']}] {action['reason']}")
                print(f"    Action: {action['action']}")
    
    print_section("Data Propagation")
    
    propagated = ecosystem.propagate_data(
        source_id="DT-PUMP-001",
        key="health_status",
        value={'health': 0.65, 'alert': 'degraded'}
    )
    
    print(f"\nPropagated health status from pump to {propagated} connected twins")
    
    print(f"\nData received by Production Line:")
    external_data = line_twin.state.get('external_health_status', {})
    if external_data:
        print(f"  Source: {external_data.get('source')}")
        print(f"  Value: {external_data.get('value')}")
    
    print_section("Autonomous Decision-Making")
    
    auto_twin = AutonomousTwin("DT-AUTO-001", "Autonomous Pump Controller")
    auto_twin.autonomy_level = 0.7
    
    auto_twin.add_decision_rule(
        condition=lambda s: s.get('temperature', 0) > 60,
        action="Reduce speed to lower temperature",
        decision_type=DecisionType.SAFETY
    )
    
    auto_twin.add_decision_rule(
        condition=lambda s: s.get('efficiency', 1) < 0.7,
        action="Optimize operating parameters",
        decision_type=DecisionType.OPTIMIZATION
    )
    
    auto_twin.add_decision_rule(
        condition=lambda s: s.get('vibration', 0) > 5,
        action="Schedule predictive maintenance",
        decision_type=DecisionType.MAINTENANCE
    )
    
    auto_twin.update_state('temperature', 65)
    auto_twin.update_state('efficiency', 0.65)
    auto_twin.update_state('vibration', 6.5)
    
    print(f"\nAutonomous Twin: {auto_twin.name}")
    print(f"Autonomy Level: {auto_twin.autonomy_level:.0%}")
    print(f"\nCurrent State:")
    for key, value in auto_twin.state.items():
        print(f"  {key}: {value}")
    
    decisions = auto_twin.evaluate_and_decide()
    
    print(f"\nAutonomous Decisions Made: {len(decisions)}")
    for decision in decisions:
        print(f"\n  [{decision.decision_type.value.upper()}] {decision.decision_id}")
        print(f"    Action: {decision.action_taken}")
        print(f"    Confidence: {decision.confidence:.0%}")
    
    print_section("Future Capability Roadmap")
    
    roadmap = [
        {
            'timeframe': 'Near-term (1-2 years)',
            'capabilities': [
                'Multi-twin data sharing within organization',
                'Basic dual-twin coordination',
                'AI-assisted decision support',
                'AR visualization of twin data'
            ]
        },
        {
            'timeframe': 'Mid-term (3-5 years)',
            'capabilities': [
                'Cross-organization twin ecosystems',
                'Autonomous optimization within bounds',
                'VR-based twin interaction',
                'Federated learning across twins'
            ]
        },
        {
            'timeframe': 'Long-term (5+ years)',
            'capabilities': [
                'City-scale twin ecosystems',
                'Fully autonomous twin operations',
                'Metaverse integration',
                'Cognitive twins with reasoning'
            ]
        }
    ]
    
    print("\nDigital Twin Evolution Roadmap:\n")
    for phase in roadmap:
        print(f"{phase['timeframe']}:")
        for cap in phase['capabilities']:
            print(f"  - {cap}")
        print()
    
    print_section("Key Takeaways")
    print("""
1. Multi-twin ecosystems enable cross-asset and cross-organization insights
2. Dual-twin architecture pairs asset twins with process twins for holistic optimization
3. Data propagation through ecosystems enables system-wide awareness
4. Autonomous twins can make decisions within defined boundaries
5. The future includes metaverse integration and cognitive capabilities
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
