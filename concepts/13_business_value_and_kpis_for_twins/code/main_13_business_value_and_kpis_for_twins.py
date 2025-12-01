"""
Business Value and KPIs for Twins - Main Demonstration

This script demonstrates business value measurement including KPI tracking,
ROI calculation, and value dashboard generation.

Usage:
    python main_13_business_value_and_kpis_for_twins.py

Example:
    python main_13_business_value_and_kpis_for_twins.py
"""

import sys
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


class ValueCategory(Enum):
    """Categories of business value."""
    COST_REDUCTION = "cost_reduction"
    REVENUE_INCREASE = "revenue_increase"
    RISK_MITIGATION = "risk_mitigation"
    PRODUCTIVITY = "productivity"
    SUSTAINABILITY = "sustainability"


class KPITrend(Enum):
    """KPI trend direction."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


@dataclass
class KPI:
    """Key Performance Indicator definition."""
    kpi_id: str
    name: str
    description: str
    unit: str
    category: ValueCategory
    
    baseline: float = 0.0
    target: float = 0.0
    current: float = 0.0
    
    higher_is_better: bool = True
    
    def calculate_improvement(self) -> float:
        """Calculate improvement from baseline."""
        if self.baseline == 0:
            return 0
        
        change = (self.current - self.baseline) / abs(self.baseline) * 100
        return change if self.higher_is_better else -change
    
    def calculate_target_achievement(self) -> float:
        """Calculate progress toward target."""
        if self.target == self.baseline:
            return 100 if self.current == self.target else 0
        
        progress = (self.current - self.baseline) / (self.target - self.baseline) * 100
        return min(100, max(0, progress))
    
    def get_trend(self, history: List[float]) -> KPITrend:
        """Determine trend from history."""
        if len(history) < 3:
            return KPITrend.STABLE
        
        recent = history[-3:]
        if self.higher_is_better:
            if recent[-1] > recent[0]:
                return KPITrend.IMPROVING
            elif recent[-1] < recent[0]:
                return KPITrend.DECLINING
        else:
            if recent[-1] < recent[0]:
                return KPITrend.IMPROVING
            elif recent[-1] > recent[0]:
                return KPITrend.DECLINING
        
        return KPITrend.STABLE


@dataclass
class Investment:
    """Investment cost tracking."""
    category: str
    description: str
    amount: float
    timing: str


@dataclass
class Benefit:
    """Benefit tracking."""
    category: ValueCategory
    description: str
    annual_value: float
    confidence: float = 0.8


class ROICalculator:
    """Calculate return on investment."""
    
    def __init__(self):
        self.investments: List[Investment] = []
        self.benefits: List[Benefit] = []
    
    def add_investment(self, investment: Investment) -> None:
        self.investments.append(investment)
    
    def add_benefit(self, benefit: Benefit) -> None:
        self.benefits.append(benefit)
    
    def calculate_total_investment(self) -> float:
        """Calculate total investment."""
        return sum(inv.amount for inv in self.investments)
    
    def calculate_annual_benefits(self) -> float:
        """Calculate total annual benefits."""
        return sum(b.annual_value * b.confidence for b in self.benefits)
    
    def calculate_roi(self, years: int = 3) -> Dict[str, Any]:
        """Calculate ROI metrics."""
        total_investment = self.calculate_total_investment()
        annual_benefits = self.calculate_annual_benefits()
        
        total_benefits = annual_benefits * years
        net_benefit = total_benefits - total_investment
        
        roi_percent = (net_benefit / total_investment * 100) if total_investment > 0 else 0
        
        payback_years = total_investment / annual_benefits if annual_benefits > 0 else float('inf')
        
        discount_rate = 0.1
        npv = -total_investment
        for year in range(1, years + 1):
            npv += annual_benefits / ((1 + discount_rate) ** year)
        
        return {
            'total_investment': total_investment,
            'annual_benefits': annual_benefits,
            'total_benefits': total_benefits,
            'net_benefit': net_benefit,
            'roi_percent': roi_percent,
            'payback_years': payback_years,
            'npv': npv,
            'analysis_period_years': years
        }


class ValueDashboard:
    """Dashboard for tracking twin value."""
    
    def __init__(self, twin_id: str):
        self.twin_id = twin_id
        self.kpis: Dict[str, KPI] = {}
        self.kpi_history: Dict[str, List[float]] = {}
        self.roi_calculator = ROICalculator()
    
    def add_kpi(self, kpi: KPI) -> None:
        self.kpis[kpi.kpi_id] = kpi
        self.kpi_history[kpi.kpi_id] = [kpi.baseline]
    
    def update_kpi(self, kpi_id: str, value: float) -> None:
        """Update KPI with new value."""
        if kpi_id in self.kpis:
            self.kpis[kpi_id].current = value
            self.kpi_history[kpi_id].append(value)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get dashboard summary."""
        kpi_summaries = []
        
        for kpi_id, kpi in self.kpis.items():
            history = self.kpi_history.get(kpi_id, [])
            trend = kpi.get_trend(history)
            
            kpi_summaries.append({
                'kpi_id': kpi_id,
                'name': kpi.name,
                'baseline': kpi.baseline,
                'current': kpi.current,
                'target': kpi.target,
                'unit': kpi.unit,
                'improvement': kpi.calculate_improvement(),
                'target_achievement': kpi.calculate_target_achievement(),
                'trend': trend.value,
                'category': kpi.category.value
            })
        
        roi = self.roi_calculator.calculate_roi()
        
        return {
            'twin_id': self.twin_id,
            'kpis': kpi_summaries,
            'roi': roi,
            'overall_health': self._calculate_overall_health(kpi_summaries)
        }
    
    def _calculate_overall_health(self, kpi_summaries: List[Dict]) -> str:
        """Calculate overall value health."""
        if not kpi_summaries:
            return "unknown"
        
        avg_achievement = sum(k['target_achievement'] for k in kpi_summaries) / len(kpi_summaries)
        
        if avg_achievement >= 90:
            return "excellent"
        elif avg_achievement >= 70:
            return "good"
        elif avg_achievement >= 50:
            return "fair"
        else:
            return "needs_attention"
    
    def generate_report(self) -> str:
        """Generate value report."""
        summary = self.get_summary()
        
        report = f"""
================================================================================
                    DIGITAL TWIN VALUE REPORT
================================================================================

Twin ID: {summary['twin_id']}
Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Overall Health: {summary['overall_health'].upper()}

KEY PERFORMANCE INDICATORS
--------------------------
"""
        
        for kpi in summary['kpis']:
            status = "ON TRACK" if kpi['target_achievement'] >= 80 else "AT RISK" if kpi['target_achievement'] >= 50 else "OFF TRACK"
            report += f"""
{kpi['name']} ({kpi['kpi_id']})
  Category: {kpi['category']}
  Baseline: {kpi['baseline']:.1f} {kpi['unit']}
  Current: {kpi['current']:.1f} {kpi['unit']}
  Target: {kpi['target']:.1f} {kpi['unit']}
  Improvement: {kpi['improvement']:+.1f}%
  Target Achievement: {kpi['target_achievement']:.0f}%
  Trend: {kpi['trend']}
  Status: {status}
"""
        
        roi = summary['roi']
        report += f"""
RETURN ON INVESTMENT
--------------------
Total Investment: ${roi['total_investment']:,.0f}
Annual Benefits: ${roi['annual_benefits']:,.0f}
{roi['analysis_period_years']}-Year Total Benefits: ${roi['total_benefits']:,.0f}
Net Benefit: ${roi['net_benefit']:,.0f}
ROI: {roi['roi_percent']:.0f}%
Payback Period: {roi['payback_years']:.1f} years
NPV (10% discount): ${roi['npv']:,.0f}

================================================================================
                         END OF REPORT
================================================================================
"""
        return report


def run_demonstration() -> None:
    """Run the business value demonstration."""
    
    print_section("Business Value and KPIs Demo")
    print("This demo shows how to measure and track digital twin value.\n")
    
    dashboard = ValueDashboard("DT-FACTORY-001")
    
    print_section("Defining KPIs")
    
    kpis = [
        KPI(
            kpi_id="KPI-001",
            name="Overall Equipment Effectiveness (OEE)",
            description="Measure of manufacturing productivity",
            unit="%",
            category=ValueCategory.PRODUCTIVITY,
            baseline=65.0,
            target=85.0,
            current=78.0,
            higher_is_better=True
        ),
        KPI(
            kpi_id="KPI-002",
            name="Unplanned Downtime",
            description="Hours of unplanned equipment downtime",
            unit="hours/month",
            category=ValueCategory.COST_REDUCTION,
            baseline=100.0,
            target=50.0,
            current=65.0,
            higher_is_better=False
        ),
        KPI(
            kpi_id="KPI-003",
            name="Maintenance Cost",
            description="Monthly maintenance expenditure",
            unit="$K",
            category=ValueCategory.COST_REDUCTION,
            baseline=50.0,
            target=35.0,
            current=40.0,
            higher_is_better=False
        ),
        KPI(
            kpi_id="KPI-004",
            name="Quality Defect Rate",
            description="Percentage of defective products",
            unit="%",
            category=ValueCategory.REVENUE_INCREASE,
            baseline=3.0,
            target=1.0,
            current=1.8,
            higher_is_better=False
        ),
        KPI(
            kpi_id="KPI-005",
            name="Energy Efficiency",
            description="Energy consumption per unit produced",
            unit="kWh/unit",
            category=ValueCategory.SUSTAINABILITY,
            baseline=2.5,
            target=2.0,
            current=2.2,
            higher_is_better=False
        ),
    ]
    
    for kpi in kpis:
        dashboard.add_kpi(kpi)
        print(f"Added KPI: {kpi.name}")
        print(f"  Baseline: {kpi.baseline} {kpi.unit} -> Target: {kpi.target} {kpi.unit}")
    
    print_section("Investment Tracking")
    
    investments = [
        Investment("Software", "Digital twin platform license", 150000, "Year 0"),
        Investment("Hardware", "IoT sensors and edge devices", 75000, "Year 0"),
        Investment("Services", "Implementation and integration", 100000, "Year 0"),
        Investment("Training", "Staff training and change management", 25000, "Year 0"),
    ]
    
    for inv in investments:
        dashboard.roi_calculator.add_investment(inv)
        print(f"Investment: {inv.description} - ${inv.amount:,.0f}")
    
    print(f"\nTotal Investment: ${dashboard.roi_calculator.calculate_total_investment():,.0f}")
    
    print_section("Benefit Tracking")
    
    benefits = [
        Benefit(ValueCategory.COST_REDUCTION, "Reduced unplanned downtime", 420000, 0.9),
        Benefit(ValueCategory.COST_REDUCTION, "Lower maintenance costs", 120000, 0.85),
        Benefit(ValueCategory.REVENUE_INCREASE, "Improved quality/reduced scrap", 180000, 0.8),
        Benefit(ValueCategory.PRODUCTIVITY, "Increased throughput", 250000, 0.75),
        Benefit(ValueCategory.SUSTAINABILITY, "Energy cost savings", 50000, 0.9),
    ]
    
    for benefit in benefits:
        dashboard.roi_calculator.add_benefit(benefit)
        adjusted = benefit.annual_value * benefit.confidence
        print(f"Benefit: {benefit.description}")
        print(f"  Annual Value: ${benefit.annual_value:,.0f} (Confidence: {benefit.confidence:.0%})")
        print(f"  Risk-Adjusted: ${adjusted:,.0f}")
    
    print(f"\nTotal Annual Benefits: ${dashboard.roi_calculator.calculate_annual_benefits():,.0f}")
    
    print_section("ROI Analysis")
    
    roi = dashboard.roi_calculator.calculate_roi(years=3)
    
    print(f"3-Year ROI Analysis:")
    print(f"  Total Investment: ${roi['total_investment']:,.0f}")
    print(f"  Annual Benefits: ${roi['annual_benefits']:,.0f}")
    print(f"  3-Year Benefits: ${roi['total_benefits']:,.0f}")
    print(f"  Net Benefit: ${roi['net_benefit']:,.0f}")
    print(f"  ROI: {roi['roi_percent']:.0f}%")
    print(f"  Payback Period: {roi['payback_years']:.1f} years")
    print(f"  NPV (10% discount): ${roi['npv']:,.0f}")
    
    print_section("KPI Performance")
    
    summary = dashboard.get_summary()
    
    print(f"\nKPI Summary:")
    print("-" * 80)
    print(f"{'KPI':<30} {'Current':<12} {'Target':<12} {'Achievement':<12} {'Trend':<10}")
    print("-" * 80)
    
    for kpi in summary['kpis']:
        print(f"{kpi['name'][:28]:<30} {kpi['current']:<12.1f} {kpi['target']:<12.1f} {kpi['target_achievement']:<12.0f}% {kpi['trend']:<10}")
    
    print("-" * 80)
    print(f"Overall Health: {summary['overall_health'].upper()}")
    
    print_section("Value Report")
    
    report = dashboard.generate_report()
    print(report)
    
    print_section("Key Takeaways")
    print("""
1. Define clear KPIs aligned with business objectives
2. Establish baselines before implementation
3. Track both costs and benefits with confidence levels
4. Calculate ROI using multiple methods (simple, payback, NPV)
5. Regular reporting keeps stakeholders aligned on value
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
