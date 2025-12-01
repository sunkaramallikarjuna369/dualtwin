"""
AI and Analytics on Twins - Main Demonstration

This script demonstrates AI and analytics on twin data including
anomaly detection, prediction, and optimization.

Usage:
    python main_08_ai_and_analytics_on_twins.py

Example:
    python main_08_ai_and_analytics_on_twins.py
"""

import sys
import os
import random
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
import statistics

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class TimeSeriesData:
    """Time series data container."""
    timestamps: List[datetime] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    
    def add(self, timestamp: datetime, value: float) -> None:
        self.timestamps.append(timestamp)
        self.values.append(value)
    
    def get_recent(self, n: int) -> Tuple[List[datetime], List[float]]:
        return self.timestamps[-n:], self.values[-n:]


class AnomalyDetector:
    """Simple anomaly detection using statistical methods."""
    
    def __init__(self, window_size: int = 50, threshold_sigma: float = 3.0):
        self.window_size = window_size
        self.threshold_sigma = threshold_sigma
        self.history: List[float] = []
    
    def update(self, value: float) -> Dict[str, Any]:
        """Update with new value and check for anomaly."""
        self.history.append(value)
        if len(self.history) > self.window_size * 2:
            self.history = self.history[-self.window_size * 2:]
        
        if len(self.history) < self.window_size:
            return {'is_anomaly': False, 'score': 0.0}
        
        window = self.history[-self.window_size:-1]
        mean = statistics.mean(window)
        std = statistics.stdev(window) if len(window) > 1 else 1.0
        
        if std < 0.001:
            std = 0.001
        
        z_score = abs(value - mean) / std
        is_anomaly = z_score > self.threshold_sigma
        
        return {
            'is_anomaly': is_anomaly,
            'score': z_score,
            'mean': mean,
            'std': std,
            'threshold': self.threshold_sigma
        }


class FailurePredictor:
    """Simple failure prediction using trend analysis."""
    
    def __init__(self, failure_threshold: float = 0.2):
        self.failure_threshold = failure_threshold
        self.health_history: List[Tuple[datetime, float]] = []
    
    def update_health(self, timestamp: datetime, health: float) -> None:
        """Update health history."""
        self.health_history.append((timestamp, health))
        if len(self.health_history) > 100:
            self.health_history = self.health_history[-100:]
    
    def predict_failure(self) -> Dict[str, Any]:
        """Predict time to failure based on health trend."""
        if len(self.health_history) < 10:
            return {'prediction': None, 'confidence': 0.0}
        
        recent = self.health_history[-20:]
        times = [(t - recent[0][0]).total_seconds() / 3600 for t, _ in recent]
        healths = [h for _, h in recent]
        
        n = len(times)
        sum_x = sum(times)
        sum_y = sum(healths)
        sum_xy = sum(x * y for x, y in zip(times, healths))
        sum_x2 = sum(x * x for x in times)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if abs(denominator) < 0.0001:
            return {'prediction': None, 'confidence': 0.0}
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n
        
        if slope >= 0:
            return {
                'prediction': None,
                'confidence': 0.5,
                'trend': 'stable_or_improving',
                'slope': slope
            }
        
        current_health = healths[-1]
        current_time = times[-1]
        
        hours_to_failure = (self.failure_threshold - current_health) / slope
        
        if hours_to_failure < 0:
            hours_to_failure = 0
        
        y_pred = [slope * x + intercept for x in times]
        ss_res = sum((y - yp) ** 2 for y, yp in zip(healths, y_pred))
        ss_tot = sum((y - sum_y/n) ** 2 for y in healths)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        return {
            'prediction': hours_to_failure,
            'confidence': max(0, r_squared),
            'trend': 'degrading',
            'slope': slope,
            'current_health': current_health
        }


class ProcessOptimizer:
    """Simple process optimization using gradient-free search."""
    
    def __init__(self):
        self.best_params: Dict[str, float] = {}
        self.best_score: float = float('-inf')
        self.history: List[Dict[str, Any]] = []
    
    def objective_function(self, params: Dict[str, float]) -> float:
        """Evaluate objective (simulated)."""
        speed = params.get('speed', 100)
        temperature = params.get('temperature', 50)
        
        throughput = speed * 0.8
        
        if temperature > 60:
            throughput *= 0.9
        if temperature > 70:
            throughput *= 0.8
        
        energy = speed * 0.5 + temperature * 0.3
        
        score = throughput - energy * 0.1
        
        return score
    
    def optimize(self, param_ranges: Dict[str, Tuple[float, float]],
                iterations: int = 50) -> Dict[str, Any]:
        """Run optimization."""
        for _ in range(iterations):
            params = {
                name: random.uniform(low, high)
                for name, (low, high) in param_ranges.items()
            }
            
            score = self.objective_function(params)
            
            self.history.append({
                'params': params.copy(),
                'score': score
            })
            
            if score > self.best_score:
                self.best_score = score
                self.best_params = params.copy()
        
        return {
            'best_params': self.best_params,
            'best_score': self.best_score,
            'iterations': iterations
        }


class TwinAnalytics:
    """Analytics engine for digital twins."""
    
    def __init__(self, twin_id: str):
        self.twin_id = twin_id
        self.anomaly_detectors: Dict[str, AnomalyDetector] = {}
        self.failure_predictor = FailurePredictor()
        self.optimizer = ProcessOptimizer()
        self.data: Dict[str, TimeSeriesData] = {}
    
    def add_sensor(self, sensor_id: str) -> None:
        """Add a sensor to monitor."""
        self.anomaly_detectors[sensor_id] = AnomalyDetector()
        self.data[sensor_id] = TimeSeriesData()
    
    def process_reading(self, sensor_id: str, timestamp: datetime,
                       value: float) -> Dict[str, Any]:
        """Process a sensor reading."""
        if sensor_id not in self.anomaly_detectors:
            self.add_sensor(sensor_id)
        
        self.data[sensor_id].add(timestamp, value)
        
        anomaly_result = self.anomaly_detectors[sensor_id].update(value)
        
        return {
            'sensor_id': sensor_id,
            'value': value,
            'anomaly': anomaly_result
        }
    
    def update_health(self, timestamp: datetime, health: float) -> None:
        """Update equipment health."""
        self.failure_predictor.update_health(timestamp, health)
    
    def get_failure_prediction(self) -> Dict[str, Any]:
        """Get failure prediction."""
        return self.failure_predictor.predict_failure()
    
    def optimize_process(self, param_ranges: Dict[str, Tuple[float, float]]) -> Dict[str, Any]:
        """Optimize process parameters."""
        return self.optimizer.optimize(param_ranges)


def generate_sensor_data(n_points: int, anomaly_at: List[int] = None) -> List[Tuple[datetime, float]]:
    """Generate synthetic sensor data with optional anomalies."""
    data = []
    base_time = datetime.now() - timedelta(hours=n_points)
    
    for i in range(n_points):
        timestamp = base_time + timedelta(hours=i)
        value = 50 + 5 * math.sin(i * 0.1) + random.gauss(0, 1)
        
        if anomaly_at and i in anomaly_at:
            value += random.choice([-1, 1]) * random.uniform(15, 25)
        
        data.append((timestamp, value))
    
    return data


def generate_health_data(n_points: int, degradation_rate: float = 0.005) -> List[Tuple[datetime, float]]:
    """Generate synthetic health data with degradation."""
    data = []
    base_time = datetime.now() - timedelta(hours=n_points)
    health = 1.0
    
    for i in range(n_points):
        timestamp = base_time + timedelta(hours=i)
        health -= degradation_rate + random.gauss(0, 0.001)
        health = max(0, min(1, health))
        data.append((timestamp, health))
    
    return data


def run_demonstration() -> None:
    """Run the AI and analytics demonstration."""
    
    print_section("AI and Analytics on Twins Demo")
    print("This demo shows how AI transforms twin data into insights.\n")
    
    analytics = TwinAnalytics("DT-PUMP-001")
    analytics.add_sensor("TEMP-001")
    analytics.add_sensor("VIB-001")
    
    print("Created Analytics Engine for twin: DT-PUMP-001")
    print("Monitoring sensors: TEMP-001, VIB-001")
    
    print_section("Anomaly Detection")
    
    temp_data = generate_sensor_data(100, anomaly_at=[75, 85])
    
    anomalies_found = []
    for timestamp, value in temp_data:
        result = analytics.process_reading("TEMP-001", timestamp, value)
        if result['anomaly']['is_anomaly']:
            anomalies_found.append({
                'timestamp': timestamp,
                'value': value,
                'score': result['anomaly']['score']
            })
    
    print(f"\nProcessed {len(temp_data)} temperature readings")
    print(f"Anomalies detected: {len(anomalies_found)}")
    
    for anomaly in anomalies_found:
        print(f"  - Value: {anomaly['value']:.2f}, Z-score: {anomaly['score']:.2f}")
    
    print_section("Failure Prediction")
    
    health_data = generate_health_data(50, degradation_rate=0.008)
    
    for timestamp, health in health_data:
        analytics.update_health(timestamp, health)
    
    prediction = analytics.get_failure_prediction()
    
    print(f"\nHealth Trend Analysis:")
    print(f"  Current health: {prediction.get('current_health', 0):.1%}")
    print(f"  Trend: {prediction.get('trend', 'unknown')}")
    print(f"  Degradation rate: {abs(prediction.get('slope', 0)):.4f} per hour")
    
    if prediction.get('prediction') is not None:
        hours = prediction['prediction']
        print(f"\nFailure Prediction:")
        print(f"  Estimated time to failure: {hours:.1f} hours")
        print(f"  Confidence: {prediction['confidence']:.1%}")
        
        if hours < 24:
            print("  ALERT: Failure predicted within 24 hours!")
        elif hours < 168:
            print("  WARNING: Failure predicted within 1 week")
    else:
        print("\nNo failure predicted - health stable or improving")
    
    print_section("Process Optimization")
    
    param_ranges = {
        'speed': (50, 150),
        'temperature': (40, 80)
    }
    
    result = analytics.optimize_process(param_ranges)
    
    print(f"\nOptimization Results ({result['iterations']} iterations):")
    print(f"  Best score: {result['best_score']:.2f}")
    print(f"  Optimal parameters:")
    for param, value in result['best_params'].items():
        print(f"    - {param}: {value:.1f}")
    
    print_section("Analytics Summary")
    
    print("""
Analytics Capabilities Demonstrated:

1. ANOMALY DETECTION
   - Statistical z-score based detection
   - Adaptive thresholds from rolling window
   - Real-time scoring of each reading

2. FAILURE PREDICTION
   - Trend analysis on health metrics
   - Linear regression for time-to-failure
   - Confidence scoring based on R-squared

3. PROCESS OPTIMIZATION
   - Multi-parameter optimization
   - Objective function balancing throughput and cost
   - Random search with best-so-far tracking
""")
    
    print_section("Key Takeaways")
    print("""
1. Anomaly detection catches unusual patterns automatically
2. Failure prediction enables proactive maintenance
3. Optimization finds best operating parameters
4. AI transforms raw data into actionable insights
5. Continuous learning improves predictions over time
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
