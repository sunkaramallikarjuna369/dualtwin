"""
Industry Use Cases - Main Demonstration

This script demonstrates industry-specific digital twin use cases including
manufacturing, energy, and buildings with simulated scenarios.

Usage:
    python main_11_industry_use_cases.py

Example:
    python main_11_industry_use_cases.py
"""

import sys
import os
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class UseCaseMetrics:
    """Metrics for a use case."""
    baseline: Dict[str, float]
    current: Dict[str, float]
    target: Dict[str, float]
    
    def calculate_improvement(self, metric: str) -> float:
        """Calculate improvement percentage."""
        baseline = self.baseline.get(metric, 0)
        current = self.current.get(metric, 0)
        if baseline == 0:
            return 0
        return (baseline - current) / baseline * 100


@dataclass
class UseCase:
    """Industry use case definition."""
    industry: str
    name: str
    description: str
    business_problem: str
    twin_solution: str
    data_sources: List[str]
    analytics: List[str]
    benefits: List[str]
    metrics: UseCaseMetrics = None


class ManufacturingTwin:
    """Digital twin for manufacturing use case."""
    
    def __init__(self, line_id: str):
        self.line_id = line_id
        self.machines: Dict[str, Dict] = {}
        self.production_data: List[Dict] = []
        self.maintenance_predictions: List[Dict] = []
    
    def add_machine(self, machine_id: str, machine_type: str) -> None:
        self.machines[machine_id] = {
            'type': machine_type,
            'health': 1.0,
            'runtime_hours': 0,
            'last_maintenance': datetime.now() - timedelta(days=random.randint(30, 180))
        }
    
    def simulate_production(self, hours: int = 24) -> Dict[str, Any]:
        """Simulate production and predict maintenance needs."""
        total_output = 0
        quality_issues = 0
        maintenance_alerts = []
        
        for hour in range(hours):
            for machine_id, machine in self.machines.items():
                machine['runtime_hours'] += 1
                machine['health'] -= random.uniform(0.001, 0.005)
                
                if machine['health'] < 0.7:
                    maintenance_alerts.append({
                        'machine_id': machine_id,
                        'health': machine['health'],
                        'predicted_failure_hours': int(machine['health'] * 100),
                        'recommendation': 'Schedule preventive maintenance'
                    })
                
                if random.random() > machine['health']:
                    quality_issues += 1
                else:
                    total_output += random.randint(8, 12)
        
        oee = (total_output / (hours * len(self.machines) * 10)) * 100
        
        return {
            'total_output': total_output,
            'quality_issues': quality_issues,
            'oee': oee,
            'maintenance_alerts': maintenance_alerts[:3]
        }


class EnergyTwin:
    """Digital twin for energy use case."""
    
    def __init__(self, grid_id: str):
        self.grid_id = grid_id
        self.generators: Dict[str, Dict] = {}
        self.load_history: List[float] = []
        self.renewable_forecast: List[float] = []
    
    def add_generator(self, gen_id: str, gen_type: str, capacity_mw: float) -> None:
        self.generators[gen_id] = {
            'type': gen_type,
            'capacity_mw': capacity_mw,
            'efficiency': random.uniform(0.85, 0.95),
            'health': random.uniform(0.8, 1.0)
        }
    
    def simulate_grid_operations(self, hours: int = 24) -> Dict[str, Any]:
        """Simulate grid operations and optimization."""
        total_generation = 0
        total_demand = 0
        renewable_utilization = 0
        
        for hour in range(hours):
            demand = 500 + 200 * abs(12 - hour) / 12 + random.gauss(0, 20)
            total_demand += demand
            
            renewable_available = 100 * max(0, 1 - abs(12 - hour) / 12) + random.gauss(0, 10)
            renewable_used = min(renewable_available, demand)
            renewable_utilization += renewable_used
            
            remaining_demand = demand - renewable_used
            
            for gen_id, gen in self.generators.items():
                if gen['type'] != 'solar' and gen['type'] != 'wind':
                    gen_output = min(remaining_demand, gen['capacity_mw'] * gen['efficiency'])
                    total_generation += gen_output
                    remaining_demand -= gen_output
        
        total_generation += renewable_utilization
        
        return {
            'total_demand_mwh': total_demand,
            'total_generation_mwh': total_generation,
            'renewable_percentage': (renewable_utilization / total_generation) * 100 if total_generation > 0 else 0,
            'grid_efficiency': (total_generation / total_demand) * 100 if total_demand > 0 else 0,
            'optimization_savings_percent': random.uniform(5, 15)
        }


class BuildingTwin:
    """Digital twin for building use case."""
    
    def __init__(self, building_id: str):
        self.building_id = building_id
        self.zones: Dict[str, Dict] = {}
        self.energy_consumption: List[float] = []
        self.occupancy_data: List[Dict] = []
    
    def add_zone(self, zone_id: str, area_sqm: float, zone_type: str) -> None:
        self.zones[zone_id] = {
            'area_sqm': area_sqm,
            'type': zone_type,
            'temperature_setpoint': 22.0,
            'current_temperature': 22.0,
            'occupancy': 0
        }
    
    def simulate_building_operations(self, hours: int = 24) -> Dict[str, Any]:
        """Simulate building operations and energy optimization."""
        total_energy_kwh = 0
        comfort_violations = 0
        
        for hour in range(hours):
            is_occupied = 8 <= hour <= 18
            
            for zone_id, zone in self.zones.items():
                zone['occupancy'] = random.randint(5, 20) if is_occupied else 0
                
                if is_occupied:
                    hvac_energy = zone['area_sqm'] * 0.05
                    lighting_energy = zone['area_sqm'] * 0.02
                else:
                    hvac_energy = zone['area_sqm'] * 0.01
                    lighting_energy = 0
                
                total_energy_kwh += hvac_energy + lighting_energy
                
                zone['current_temperature'] += random.gauss(0, 0.5)
                if abs(zone['current_temperature'] - zone['temperature_setpoint']) > 2:
                    comfort_violations += 1
        
        baseline_energy = total_energy_kwh * 1.25
        savings_percent = ((baseline_energy - total_energy_kwh) / baseline_energy) * 100
        
        return {
            'total_energy_kwh': total_energy_kwh,
            'baseline_energy_kwh': baseline_energy,
            'energy_savings_percent': savings_percent,
            'comfort_violations': comfort_violations,
            'comfort_score': max(0, 100 - comfort_violations * 2)
        }


def create_use_cases() -> List[UseCase]:
    """Create industry use case definitions."""
    
    manufacturing = UseCase(
        industry="Manufacturing",
        name="Predictive Maintenance",
        description="Use digital twins to predict equipment failures before they occur",
        business_problem="Unplanned downtime costs $50K per hour and reduces OEE",
        twin_solution="Real-time equipment twins with ML-based failure prediction",
        data_sources=["Vibration sensors", "Temperature sensors", "Power consumption", "Production data"],
        analytics=["Anomaly detection", "Remaining useful life prediction", "Root cause analysis"],
        benefits=["35% reduction in unplanned downtime", "20% lower maintenance costs", "15% improvement in OEE"],
        metrics=UseCaseMetrics(
            baseline={'downtime_hours': 100, 'maintenance_cost': 500000, 'oee': 65},
            current={'downtime_hours': 65, 'maintenance_cost': 400000, 'oee': 75},
            target={'downtime_hours': 50, 'maintenance_cost': 350000, 'oee': 85}
        )
    )
    
    energy = UseCase(
        industry="Energy",
        name="Grid Optimization",
        description="Optimize power generation and distribution using digital twins",
        business_problem="Balancing supply and demand while maximizing renewable usage",
        twin_solution="Grid twin with load forecasting and generation optimization",
        data_sources=["Smart meters", "Weather data", "Generator sensors", "Grid sensors"],
        analytics=["Load forecasting", "Renewable prediction", "Dispatch optimization"],
        benefits=["10% reduction in generation costs", "25% increase in renewable utilization", "Improved grid stability"],
        metrics=UseCaseMetrics(
            baseline={'generation_cost': 10000000, 'renewable_percent': 20, 'outages': 50},
            current={'generation_cost': 9000000, 'renewable_percent': 25, 'outages': 35},
            target={'generation_cost': 8000000, 'renewable_percent': 40, 'outages': 20}
        )
    )
    
    building = UseCase(
        industry="Buildings",
        name="Energy Management",
        description="Optimize building energy consumption while maintaining comfort",
        business_problem="High energy costs and tenant comfort complaints",
        twin_solution="Building twin with occupancy-based HVAC optimization",
        data_sources=["BMS sensors", "Occupancy sensors", "Weather data", "Energy meters"],
        analytics=["Occupancy prediction", "Comfort optimization", "Fault detection"],
        benefits=["25% energy cost reduction", "90%+ comfort satisfaction", "Reduced maintenance calls"],
        metrics=UseCaseMetrics(
            baseline={'energy_cost': 200000, 'comfort_score': 70, 'maintenance_calls': 100},
            current={'energy_cost': 150000, 'comfort_score': 85, 'maintenance_calls': 60},
            target={'energy_cost': 120000, 'comfort_score': 95, 'maintenance_calls': 40}
        )
    )
    
    return [manufacturing, energy, building]


def run_demonstration() -> None:
    """Run the industry use cases demonstration."""
    
    print_section("Industry Use Cases Demo")
    print("This demo shows how digital twins are applied across industries.\n")
    
    use_cases = create_use_cases()
    
    for uc in use_cases:
        print_section(f"{uc.industry}: {uc.name}")
        
        print(f"Description: {uc.description}\n")
        print(f"Business Problem: {uc.business_problem}\n")
        print(f"Twin Solution: {uc.twin_solution}\n")
        
        print("Data Sources:")
        for ds in uc.data_sources:
            print(f"  - {ds}")
        
        print("\nAnalytics:")
        for a in uc.analytics:
            print(f"  - {a}")
        
        print("\nExpected Benefits:")
        for b in uc.benefits:
            print(f"  - {b}")
    
    print_section("Manufacturing Simulation")
    
    mfg_twin = ManufacturingTwin("LINE-001")
    mfg_twin.add_machine("CNC-001", "CNC Mill")
    mfg_twin.add_machine("ROBOT-001", "Assembly Robot")
    mfg_twin.add_machine("PRESS-001", "Hydraulic Press")
    
    mfg_results = mfg_twin.simulate_production(24)
    
    print(f"24-Hour Production Results:")
    print(f"  Total Output: {mfg_results['total_output']} units")
    print(f"  Quality Issues: {mfg_results['quality_issues']}")
    print(f"  OEE: {mfg_results['oee']:.1f}%")
    
    if mfg_results['maintenance_alerts']:
        print("\nMaintenance Predictions:")
        for alert in mfg_results['maintenance_alerts']:
            print(f"  - {alert['machine_id']}: Health {alert['health']:.1%}, "
                  f"Predicted failure in {alert['predicted_failure_hours']} hours")
    
    print_section("Energy Grid Simulation")
    
    energy_twin = EnergyTwin("GRID-001")
    energy_twin.add_generator("GEN-001", "gas", 200)
    energy_twin.add_generator("GEN-002", "coal", 300)
    energy_twin.add_generator("SOLAR-001", "solar", 100)
    
    energy_results = energy_twin.simulate_grid_operations(24)
    
    print(f"24-Hour Grid Results:")
    print(f"  Total Demand: {energy_results['total_demand_mwh']:.0f} MWh")
    print(f"  Total Generation: {energy_results['total_generation_mwh']:.0f} MWh")
    print(f"  Renewable Percentage: {energy_results['renewable_percentage']:.1f}%")
    print(f"  Optimization Savings: {energy_results['optimization_savings_percent']:.1f}%")
    
    print_section("Building Simulation")
    
    building_twin = BuildingTwin("BLDG-001")
    building_twin.add_zone("FLOOR-1", 1000, "office")
    building_twin.add_zone("FLOOR-2", 1000, "office")
    building_twin.add_zone("LOBBY", 200, "common")
    
    building_results = building_twin.simulate_building_operations(24)
    
    print(f"24-Hour Building Results:")
    print(f"  Total Energy: {building_results['total_energy_kwh']:.0f} kWh")
    print(f"  Baseline Energy: {building_results['baseline_energy_kwh']:.0f} kWh")
    print(f"  Energy Savings: {building_results['energy_savings_percent']:.1f}%")
    print(f"  Comfort Score: {building_results['comfort_score']:.0f}/100")
    
    print_section("ROI Summary")
    
    print("\nUse Case ROI Analysis:\n")
    for uc in use_cases:
        print(f"{uc.industry} - {uc.name}:")
        for metric in uc.metrics.baseline.keys():
            improvement = uc.metrics.calculate_improvement(metric)
            print(f"  {metric}: {improvement:.1f}% improvement")
        print()
    
    print_section("Key Takeaways")
    print("""
1. Each industry has unique use cases based on business drivers
2. Manufacturing focuses on uptime, quality, and efficiency
3. Energy focuses on optimization, reliability, and sustainability
4. Buildings focus on energy costs and occupant comfort
5. ROI is measurable through specific KPIs for each use case
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
