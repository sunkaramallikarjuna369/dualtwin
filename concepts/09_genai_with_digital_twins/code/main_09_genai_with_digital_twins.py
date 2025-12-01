"""
GenAI with Digital Twins - Main Demonstration

This script demonstrates GenAI integration with digital twins including
natural language queries, report generation, and scenario exploration.
(Simulated without actual LLM API calls)

Usage:
    python main_09_genai_with_digital_twins.py

Example:
    python main_09_genai_with_digital_twins.py
"""

import sys
import os
import random
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


@dataclass
class TwinData:
    """Digital twin data store."""
    twin_id: str
    name: str
    asset_type: str
    
    current_state: Dict[str, Any] = field(default_factory=dict)
    historical_data: List[Dict[str, Any]] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    maintenance_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_current_value(self, metric: str) -> Optional[float]:
        return self.current_state.get(metric)
    
    def get_average(self, metric: str, hours: int = 24) -> Optional[float]:
        values = [d.get(metric) for d in self.historical_data[-hours:] if metric in d]
        return sum(values) / len(values) if values else None
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        cutoff = datetime.now() - timedelta(hours=hours)
        return [a for a in self.alerts if a.get('timestamp', datetime.min) > cutoff]


class TwinKnowledgeBase:
    """Knowledge base for twin domain information."""
    
    def __init__(self):
        self.knowledge = {
            'temperature': {
                'normal_range': (20, 60),
                'warning_range': (60, 80),
                'critical_range': (80, 100),
                'causes_high': ['overload', 'cooling failure', 'bearing wear', 'ambient conditions'],
                'causes_low': ['underload', 'sensor malfunction'],
                'recommendations_high': ['reduce load', 'check cooling system', 'inspect bearings']
            },
            'vibration': {
                'normal_range': (0, 3),
                'warning_range': (3, 6),
                'critical_range': (6, 10),
                'causes_high': ['imbalance', 'misalignment', 'bearing damage', 'looseness'],
                'recommendations_high': ['check alignment', 'inspect bearings', 'balance rotating parts']
            },
            'efficiency': {
                'normal_range': (85, 100),
                'warning_range': (70, 85),
                'critical_range': (0, 70),
                'causes_low': ['wear', 'fouling', 'operating off-design', 'control issues']
            }
        }
    
    def get_knowledge(self, topic: str) -> Dict[str, Any]:
        return self.knowledge.get(topic, {})
    
    def diagnose(self, metric: str, value: float) -> Dict[str, Any]:
        knowledge = self.get_knowledge(metric)
        if not knowledge:
            return {'status': 'unknown', 'message': f'No knowledge about {metric}'}
        
        normal = knowledge.get('normal_range', (0, 100))
        warning = knowledge.get('warning_range', (100, 100))
        critical = knowledge.get('critical_range', (100, 100))
        
        if normal[0] <= value <= normal[1]:
            return {'status': 'normal', 'message': f'{metric} is within normal range'}
        elif warning[0] <= value <= warning[1]:
            causes = knowledge.get('causes_high', []) if value > normal[1] else knowledge.get('causes_low', [])
            return {
                'status': 'warning',
                'message': f'{metric} is in warning range',
                'possible_causes': causes[:2]
            }
        else:
            causes = knowledge.get('causes_high', []) if value > normal[1] else knowledge.get('causes_low', [])
            recommendations = knowledge.get('recommendations_high', [])
            return {
                'status': 'critical',
                'message': f'{metric} is in critical range',
                'possible_causes': causes,
                'recommendations': recommendations
            }


class TwinCopilot:
    """AI copilot for digital twin interaction."""
    
    def __init__(self, twin: TwinData, knowledge_base: TwinKnowledgeBase):
        self.twin = twin
        self.kb = knowledge_base
        self.conversation_history: List[Dict[str, str]] = []
        
        self.query_patterns = [
            (r'(what|how).*(temperature|temp)', self._handle_temperature_query),
            (r'(what|how).*(vibration|vib)', self._handle_vibration_query),
            (r'(why|cause).*(high|hot|warm)', self._handle_why_high_query),
            (r'(status|health|condition)', self._handle_status_query),
            (r'(alert|alarm|warning)', self._handle_alert_query),
            (r'(recommend|suggest|should)', self._handle_recommendation_query),
            (r'(report|summary)', self._handle_report_query),
            (r'(what if|scenario|predict)', self._handle_scenario_query),
        ]
    
    def process_query(self, query: str) -> str:
        """Process a natural language query."""
        self.conversation_history.append({'role': 'user', 'content': query})
        
        query_lower = query.lower()
        
        for pattern, handler in self.query_patterns:
            if re.search(pattern, query_lower):
                response = handler(query_lower)
                self.conversation_history.append({'role': 'assistant', 'content': response})
                return response
        
        response = self._handle_general_query(query_lower)
        self.conversation_history.append({'role': 'assistant', 'content': response})
        return response
    
    def _handle_temperature_query(self, query: str) -> str:
        temp = self.twin.get_current_value('temperature')
        avg_temp = self.twin.get_average('temperature', 24)
        
        if temp is None:
            return "I don't have current temperature data available."
        
        diagnosis = self.kb.diagnose('temperature', temp)
        
        response = f"The current temperature of {self.twin.name} is {temp:.1f}°C. "
        response += f"The 24-hour average is {avg_temp:.1f}°C. "
        response += f"Status: {diagnosis['status'].upper()}. {diagnosis['message']}."
        
        if diagnosis.get('possible_causes'):
            response += f" Possible causes: {', '.join(diagnosis['possible_causes'])}."
        
        return response
    
    def _handle_vibration_query(self, query: str) -> str:
        vib = self.twin.get_current_value('vibration')
        
        if vib is None:
            return "I don't have current vibration data available."
        
        diagnosis = self.kb.diagnose('vibration', vib)
        
        response = f"Current vibration level is {vib:.2f} mm/s. "
        response += f"Status: {diagnosis['status'].upper()}."
        
        if diagnosis.get('recommendations'):
            response += f" Recommended actions: {', '.join(diagnosis['recommendations'][:2])}."
        
        return response
    
    def _handle_why_high_query(self, query: str) -> str:
        temp = self.twin.get_current_value('temperature')
        vib = self.twin.get_current_value('vibration')
        
        issues = []
        if temp and temp > 60:
            diagnosis = self.kb.diagnose('temperature', temp)
            issues.append(f"Temperature is elevated ({temp:.1f}°C). " +
                         f"Possible causes: {', '.join(diagnosis.get('possible_causes', ['unknown']))}")
        
        if vib and vib > 3:
            diagnosis = self.kb.diagnose('vibration', vib)
            issues.append(f"Vibration is elevated ({vib:.2f} mm/s). " +
                         f"Possible causes: {', '.join(diagnosis.get('possible_causes', ['unknown']))}")
        
        if not issues:
            return "All parameters appear to be within normal ranges. No elevated readings detected."
        
        return "Analysis of elevated readings:\n" + "\n".join(f"- {issue}" for issue in issues)
    
    def _handle_status_query(self, query: str) -> str:
        temp = self.twin.get_current_value('temperature')
        vib = self.twin.get_current_value('vibration')
        health = self.twin.get_current_value('health')
        
        response = f"Status Report for {self.twin.name}:\n"
        response += f"- Temperature: {temp:.1f}°C\n" if temp else "- Temperature: N/A\n"
        response += f"- Vibration: {vib:.2f} mm/s\n" if vib else "- Vibration: N/A\n"
        response += f"- Health Score: {health:.1%}\n" if health else "- Health: N/A\n"
        
        alerts = self.twin.get_recent_alerts(24)
        response += f"- Active Alerts: {len(alerts)}"
        
        return response
    
    def _handle_alert_query(self, query: str) -> str:
        alerts = self.twin.get_recent_alerts(24)
        
        if not alerts:
            return "No alerts in the last 24 hours. All systems operating normally."
        
        response = f"There are {len(alerts)} alert(s) in the last 24 hours:\n"
        for alert in alerts[:5]:
            response += f"- {alert.get('type', 'Unknown')}: {alert.get('message', 'No details')}\n"
        
        return response
    
    def _handle_recommendation_query(self, query: str) -> str:
        temp = self.twin.get_current_value('temperature')
        vib = self.twin.get_current_value('vibration')
        health = self.twin.get_current_value('health')
        
        recommendations = []
        
        if temp and temp > 60:
            recommendations.append("Reduce operating load to lower temperature")
            recommendations.append("Inspect cooling system for blockages")
        
        if vib and vib > 3:
            recommendations.append("Schedule vibration analysis")
            recommendations.append("Check alignment and balance")
        
        if health and health < 0.7:
            recommendations.append("Schedule preventive maintenance")
            recommendations.append("Order replacement parts")
        
        if not recommendations:
            recommendations.append("Continue normal operations")
            recommendations.append("Maintain regular inspection schedule")
        
        return "Recommendations:\n" + "\n".join(f"{i+1}. {r}" for i, r in enumerate(recommendations))
    
    def _handle_report_query(self, query: str) -> str:
        return self.generate_report()
    
    def _handle_scenario_query(self, query: str) -> str:
        if 'increase' in query and 'load' in query:
            return self._scenario_increase_load()
        elif 'decrease' in query or 'reduce' in query:
            return self._scenario_decrease_load()
        else:
            return "I can help with scenarios like 'What if we increase the load?' or 'What if we reduce speed?'"
    
    def _scenario_increase_load(self) -> str:
        temp = self.twin.get_current_value('temperature') or 50
        
        projected_temp = temp * 1.15
        projected_wear = 1.3
        
        response = "Scenario Analysis: Increase Load by 20%\n\n"
        response += f"Current temperature: {temp:.1f}°C\n"
        response += f"Projected temperature: {projected_temp:.1f}°C\n"
        response += f"Wear rate increase: {projected_wear:.0%}\n\n"
        
        if projected_temp > 70:
            response += "WARNING: Temperature may exceed safe limits. "
            response += "Recommend improving cooling before increasing load."
        else:
            response += "Temperature should remain within acceptable range. "
            response += "Monitor closely during initial load increase."
        
        return response
    
    def _scenario_decrease_load(self) -> str:
        temp = self.twin.get_current_value('temperature') or 50
        
        projected_temp = temp * 0.85
        projected_life = 1.4
        
        response = "Scenario Analysis: Decrease Load by 20%\n\n"
        response += f"Current temperature: {temp:.1f}°C\n"
        response += f"Projected temperature: {projected_temp:.1f}°C\n"
        response += f"Equipment life extension: {projected_life:.0%}\n\n"
        response += "Reducing load will extend equipment life and reduce maintenance frequency."
        
        return response
    
    def _handle_general_query(self, query: str) -> str:
        return (f"I can help you with information about {self.twin.name}. "
                "Try asking about temperature, vibration, status, alerts, "
                "recommendations, or scenarios.")
    
    def generate_report(self) -> str:
        """Generate an automated report."""
        temp = self.twin.get_current_value('temperature') or 0
        vib = self.twin.get_current_value('vibration') or 0
        health = self.twin.get_current_value('health') or 0
        alerts = self.twin.get_recent_alerts(24)
        
        report = f"""
================================================================================
                    DIGITAL TWIN STATUS REPORT
================================================================================

Asset: {self.twin.name}
Twin ID: {self.twin.id}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CURRENT STATUS
--------------
Temperature:     {temp:.1f}°C     {'[NORMAL]' if temp < 60 else '[WARNING]' if temp < 80 else '[CRITICAL]'}
Vibration:       {vib:.2f} mm/s   {'[NORMAL]' if vib < 3 else '[WARNING]' if vib < 6 else '[CRITICAL]'}
Health Score:    {health:.1%}      {'[GOOD]' if health > 0.8 else '[FAIR]' if health > 0.6 else '[POOR]'}

ALERTS (Last 24 Hours)
----------------------
Total Alerts: {len(alerts)}
"""
        
        if alerts:
            for alert in alerts[:3]:
                report += f"- {alert.get('type', 'Unknown')}: {alert.get('message', 'No details')}\n"
        else:
            report += "No alerts recorded.\n"
        
        report += """
RECOMMENDATIONS
---------------
"""
        if temp > 60:
            report += "- Monitor temperature closely, consider reducing load\n"
        if vib > 3:
            report += "- Schedule vibration analysis\n"
        if health < 0.7:
            report += "- Plan preventive maintenance\n"
        if temp <= 60 and vib <= 3 and health >= 0.7:
            report += "- Continue normal operations\n"
        
        report += """
================================================================================
                         END OF REPORT
================================================================================
"""
        return report


def create_sample_twin() -> TwinData:
    """Create a sample twin with data."""
    twin = TwinData(
        twin_id="DT-PUMP-001",
        name="Industrial Pump #1",
        asset_type="Centrifugal Pump"
    )
    
    twin.current_state = {
        'temperature': 65.5,
        'vibration': 3.8,
        'pressure': 5.2,
        'flow_rate': 120.0,
        'health': 0.75
    }
    
    base_time = datetime.now() - timedelta(hours=48)
    for i in range(48):
        twin.historical_data.append({
            'timestamp': base_time + timedelta(hours=i),
            'temperature': 50 + i * 0.3 + random.gauss(0, 2),
            'vibration': 2.5 + i * 0.02 + random.gauss(0, 0.2)
        })
    
    twin.alerts.append({
        'timestamp': datetime.now() - timedelta(hours=2),
        'type': 'Temperature Warning',
        'message': 'Temperature exceeded 60°C threshold'
    })
    twin.alerts.append({
        'timestamp': datetime.now() - timedelta(hours=6),
        'type': 'Vibration Warning',
        'message': 'Vibration level increasing'
    })
    
    return twin


def run_demonstration() -> None:
    """Run the GenAI demonstration."""
    
    print_section("GenAI with Digital Twins Demo")
    print("This demo shows how GenAI enables natural language interaction with twins.\n")
    print("Note: This uses simulated AI responses, not actual LLM API calls.\n")
    
    twin = create_sample_twin()
    kb = TwinKnowledgeBase()
    copilot = TwinCopilot(twin, kb)
    
    print(f"Created Twin Copilot for: {twin.name}")
    
    print_section("Natural Language Queries")
    
    queries = [
        "What is the current temperature?",
        "How is the vibration level?",
        "Why is the temperature high?",
        "What is the overall status?",
        "Are there any alerts?",
        "What do you recommend?",
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = copilot.process_query(query)
        print(f"Copilot: {response}")
    
    print_section("Scenario Exploration")
    
    scenario_query = "What if we increase the load by 20%?"
    print(f"\nUser: {scenario_query}")
    response = copilot.process_query(scenario_query)
    print(f"Copilot:\n{response}")
    
    print_section("Automated Report Generation")
    
    print("\nUser: Generate a status report")
    report = copilot.generate_report()
    print(report)
    
    print_section("Key Takeaways")
    print("""
1. Natural language queries make twins accessible to everyone
2. AI can diagnose issues and explain root causes
3. Scenario exploration helps with decision-making
4. Automated reports save time and ensure consistency
5. Knowledge bases ground AI responses in domain expertise
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
