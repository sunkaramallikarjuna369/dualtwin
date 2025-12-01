"""
Governance, Compliance, and Standards - Main Demonstration

This script demonstrates governance concepts including data quality checks,
compliance verification, and audit logging.

Usage:
    python main_12_governance_compliance_and_standards.py

Example:
    python main_12_governance_compliance_and_standards.py
"""

import sys
import os
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


class ComplianceStatus(Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_ASSESSED = "not_assessed"


class DataQualityDimension(Enum):
    """Data quality dimensions."""
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    TIMELINESS = "timeliness"
    CONSISTENCY = "consistency"
    VALIDITY = "validity"


@dataclass
class DataQualityRule:
    """Rule for data quality assessment."""
    rule_id: str
    dimension: DataQualityDimension
    description: str
    check_function: str
    threshold: float = 0.95


@dataclass
class ComplianceRequirement:
    """Compliance requirement definition."""
    req_id: str
    regulation: str
    description: str
    controls: List[str]
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    evidence: List[str] = field(default_factory=list)


@dataclass
class AuditFinding:
    """Audit finding."""
    finding_id: str
    timestamp: datetime
    category: str
    severity: str
    description: str
    recommendation: str
    status: str = "open"


class DataQualityManager:
    """Manages data quality for digital twins."""
    
    def __init__(self):
        self.rules: List[DataQualityRule] = []
        self.assessments: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: DataQualityRule) -> None:
        self.rules.append(rule)
    
    def assess_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess data quality against rules."""
        results = {
            'timestamp': datetime.now(),
            'record_count': len(data),
            'dimensions': {},
            'overall_score': 0.0
        }
        
        completeness = self._check_completeness(data)
        results['dimensions'][DataQualityDimension.COMPLETENESS.value] = completeness
        
        accuracy = self._check_accuracy(data)
        results['dimensions'][DataQualityDimension.ACCURACY.value] = accuracy
        
        timeliness = self._check_timeliness(data)
        results['dimensions'][DataQualityDimension.TIMELINESS.value] = timeliness
        
        consistency = self._check_consistency(data)
        results['dimensions'][DataQualityDimension.CONSISTENCY.value] = consistency
        
        validity = self._check_validity(data)
        results['dimensions'][DataQualityDimension.VALIDITY.value] = validity
        
        scores = list(results['dimensions'].values())
        results['overall_score'] = sum(scores) / len(scores) if scores else 0
        
        self.assessments.append(results)
        return results
    
    def _check_completeness(self, data: List[Dict]) -> float:
        """Check data completeness."""
        if not data:
            return 0.0
        
        required_fields = ['id', 'timestamp', 'value']
        complete_records = 0
        
        for record in data:
            if all(field in record and record[field] is not None for field in required_fields):
                complete_records += 1
        
        return complete_records / len(data)
    
    def _check_accuracy(self, data: List[Dict]) -> float:
        """Check data accuracy (simulated)."""
        if not data:
            return 0.0
        
        accurate_records = 0
        for record in data:
            value = record.get('value', 0)
            if isinstance(value, (int, float)) and -1000 <= value <= 1000:
                accurate_records += 1
        
        return accurate_records / len(data)
    
    def _check_timeliness(self, data: List[Dict]) -> float:
        """Check data timeliness."""
        if not data:
            return 0.0
        
        timely_records = 0
        cutoff = datetime.now() - timedelta(hours=24)
        
        for record in data:
            ts = record.get('timestamp')
            if isinstance(ts, datetime) and ts > cutoff:
                timely_records += 1
            elif isinstance(ts, str):
                timely_records += 0.5
        
        return timely_records / len(data)
    
    def _check_consistency(self, data: List[Dict]) -> float:
        """Check data consistency."""
        if not data:
            return 0.0
        
        return random.uniform(0.9, 1.0)
    
    def _check_validity(self, data: List[Dict]) -> float:
        """Check data validity."""
        if not data:
            return 0.0
        
        valid_records = 0
        for record in data:
            if 'id' in record and isinstance(record['id'], str):
                valid_records += 1
        
        return valid_records / len(data)


class ComplianceManager:
    """Manages compliance for digital twins."""
    
    def __init__(self):
        self.requirements: Dict[str, ComplianceRequirement] = {}
        self.assessments: List[Dict[str, Any]] = []
    
    def add_requirement(self, req: ComplianceRequirement) -> None:
        self.requirements[req.req_id] = req
    
    def assess_compliance(self, controls_implemented: List[str]) -> Dict[str, Any]:
        """Assess compliance against requirements."""
        results = {
            'timestamp': datetime.now(),
            'requirements': {},
            'overall_status': ComplianceStatus.NOT_ASSESSED
        }
        
        compliant_count = 0
        
        for req_id, req in self.requirements.items():
            controls_met = [c for c in req.controls if c in controls_implemented]
            coverage = len(controls_met) / len(req.controls) if req.controls else 0
            
            if coverage >= 1.0:
                status = ComplianceStatus.COMPLIANT
                compliant_count += 1
            elif coverage >= 0.5:
                status = ComplianceStatus.PARTIAL
            else:
                status = ComplianceStatus.NON_COMPLIANT
            
            req.status = status
            results['requirements'][req_id] = {
                'status': status.value,
                'coverage': coverage,
                'controls_met': controls_met,
                'controls_missing': [c for c in req.controls if c not in controls_implemented]
            }
        
        if compliant_count == len(self.requirements):
            results['overall_status'] = ComplianceStatus.COMPLIANT
        elif compliant_count > 0:
            results['overall_status'] = ComplianceStatus.PARTIAL
        else:
            results['overall_status'] = ComplianceStatus.NON_COMPLIANT
        
        self.assessments.append(results)
        return results
    
    def generate_compliance_report(self) -> str:
        """Generate a compliance report."""
        if not self.assessments:
            return "No compliance assessments available."
        
        latest = self.assessments[-1]
        
        report = f"""
================================================================================
                    COMPLIANCE ASSESSMENT REPORT
================================================================================

Assessment Date: {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
Overall Status: {latest['overall_status'].value.upper()}

REQUIREMENT DETAILS
-------------------
"""
        
        for req_id, result in latest['requirements'].items():
            req = self.requirements[req_id]
            report += f"""
{req_id}: {req.description}
  Regulation: {req.regulation}
  Status: {result['status'].upper()}
  Coverage: {result['coverage']:.0%}
  Controls Met: {', '.join(result['controls_met']) or 'None'}
  Controls Missing: {', '.join(result['controls_missing']) or 'None'}
"""
        
        report += """
================================================================================
                         END OF REPORT
================================================================================
"""
        return report


class GovernanceFramework:
    """Overall governance framework for digital twins."""
    
    def __init__(self, twin_id: str):
        self.twin_id = twin_id
        self.data_quality = DataQualityManager()
        self.compliance = ComplianceManager()
        self.audit_findings: List[AuditFinding] = []
        self.policies: Dict[str, str] = {}
    
    def add_policy(self, policy_id: str, description: str) -> None:
        self.policies[policy_id] = description
    
    def record_finding(self, category: str, severity: str,
                      description: str, recommendation: str) -> AuditFinding:
        """Record an audit finding."""
        finding = AuditFinding(
            finding_id=f"FIND-{len(self.audit_findings) + 1:04d}",
            timestamp=datetime.now(),
            category=category,
            severity=severity,
            description=description,
            recommendation=recommendation
        )
        self.audit_findings.append(finding)
        return finding
    
    def get_governance_dashboard(self) -> Dict[str, Any]:
        """Get governance dashboard metrics."""
        dq_assessments = self.data_quality.assessments
        latest_dq = dq_assessments[-1] if dq_assessments else None
        
        compliance_assessments = self.compliance.assessments
        latest_compliance = compliance_assessments[-1] if compliance_assessments else None
        
        open_findings = [f for f in self.audit_findings if f.status == 'open']
        critical_findings = [f for f in open_findings if f.severity == 'critical']
        
        return {
            'twin_id': self.twin_id,
            'data_quality_score': latest_dq['overall_score'] if latest_dq else None,
            'compliance_status': latest_compliance['overall_status'].value if latest_compliance else None,
            'open_findings': len(open_findings),
            'critical_findings': len(critical_findings),
            'policies_defined': len(self.policies),
            'last_assessment': latest_dq['timestamp'] if latest_dq else None
        }


def run_demonstration() -> None:
    """Run the governance demonstration."""
    
    print_section("Governance, Compliance, and Standards Demo")
    print("This demo shows how governance ensures twin quality and compliance.\n")
    
    framework = GovernanceFramework("DT-PUMP-001")
    
    framework.add_policy("POL-001", "All twin data must be validated before ingestion")
    framework.add_policy("POL-002", "Access to twin data requires authentication")
    framework.add_policy("POL-003", "All changes must be logged in audit trail")
    framework.add_policy("POL-004", "Data retention period is 7 years")
    
    print("Governance Policies Defined:")
    for pol_id, desc in framework.policies.items():
        print(f"  {pol_id}: {desc}")
    
    print_section("Data Quality Assessment")
    
    sample_data = [
        {'id': 'SENSOR-001', 'timestamp': datetime.now(), 'value': 45.2},
        {'id': 'SENSOR-002', 'timestamp': datetime.now(), 'value': 52.1},
        {'id': 'SENSOR-003', 'timestamp': datetime.now() - timedelta(hours=2), 'value': 48.7},
        {'id': None, 'timestamp': datetime.now(), 'value': 50.0},
        {'id': 'SENSOR-005', 'timestamp': None, 'value': 47.3},
        {'id': 'SENSOR-006', 'timestamp': datetime.now(), 'value': None},
        {'id': 'SENSOR-007', 'timestamp': datetime.now(), 'value': 51.8},
        {'id': 'SENSOR-008', 'timestamp': datetime.now() - timedelta(days=2), 'value': 49.2},
    ]
    
    dq_results = framework.data_quality.assess_data(sample_data)
    
    print(f"\nData Quality Assessment Results:")
    print(f"  Records Assessed: {dq_results['record_count']}")
    print(f"  Overall Score: {dq_results['overall_score']:.1%}")
    print(f"\n  Dimension Scores:")
    for dimension, score in dq_results['dimensions'].items():
        status = "PASS" if score >= 0.95 else "WARN" if score >= 0.8 else "FAIL"
        print(f"    {dimension}: {score:.1%} [{status}]")
    
    print_section("Compliance Assessment")
    
    framework.compliance.add_requirement(ComplianceRequirement(
        req_id="REQ-001",
        regulation="ISO 27001",
        description="Information Security Management",
        controls=["access_control", "encryption", "audit_logging", "incident_response"]
    ))
    
    framework.compliance.add_requirement(ComplianceRequirement(
        req_id="REQ-002",
        regulation="GDPR",
        description="Data Privacy Protection",
        controls=["consent_management", "data_minimization", "right_to_erasure", "privacy_by_design"]
    ))
    
    framework.compliance.add_requirement(ComplianceRequirement(
        req_id="REQ-003",
        regulation="IEC 62443",
        description="Industrial Cybersecurity",
        controls=["network_segmentation", "access_control", "security_monitoring"]
    ))
    
    implemented_controls = [
        "access_control",
        "encryption",
        "audit_logging",
        "consent_management",
        "data_minimization",
        "network_segmentation",
        "security_monitoring"
    ]
    
    compliance_results = framework.compliance.assess_compliance(implemented_controls)
    
    print(f"\nCompliance Assessment Results:")
    print(f"  Overall Status: {compliance_results['overall_status'].value.upper()}")
    print(f"\n  Requirement Status:")
    for req_id, result in compliance_results['requirements'].items():
        req = framework.compliance.requirements[req_id]
        print(f"    {req_id} ({req.regulation}): {result['status'].upper()} ({result['coverage']:.0%})")
        if result['controls_missing']:
            print(f"      Missing: {', '.join(result['controls_missing'])}")
    
    print_section("Audit Findings")
    
    framework.record_finding(
        category="Data Quality",
        severity="medium",
        description="6.25% of records have missing required fields",
        recommendation="Implement data validation at ingestion point"
    )
    
    framework.record_finding(
        category="Compliance",
        severity="high",
        description="GDPR right to erasure control not implemented",
        recommendation="Implement data deletion capability for user requests"
    )
    
    framework.record_finding(
        category="Security",
        severity="low",
        description="Incident response procedure not documented",
        recommendation="Create and test incident response playbook"
    )
    
    print("\nAudit Findings:")
    for finding in framework.audit_findings:
        print(f"  [{finding.severity.upper()}] {finding.finding_id}: {finding.description}")
        print(f"    Recommendation: {finding.recommendation}")
    
    print_section("Governance Dashboard")
    
    dashboard = framework.get_governance_dashboard()
    
    print(f"\nGovernance Dashboard for {dashboard['twin_id']}:")
    print(f"  Data Quality Score: {dashboard['data_quality_score']:.1%}" if dashboard['data_quality_score'] else "  Data Quality: Not assessed")
    print(f"  Compliance Status: {dashboard['compliance_status'].upper()}" if dashboard['compliance_status'] else "  Compliance: Not assessed")
    print(f"  Open Findings: {dashboard['open_findings']}")
    print(f"  Critical Findings: {dashboard['critical_findings']}")
    print(f"  Policies Defined: {dashboard['policies_defined']}")
    
    print_section("Compliance Report")
    
    report = framework.compliance.generate_compliance_report()
    print(report)
    
    print_section("Key Takeaways")
    print("""
1. Data quality must be continuously monitored and measured
2. Compliance requires mapping controls to regulatory requirements
3. Audit findings drive continuous improvement
4. Governance dashboards provide visibility to stakeholders
5. Documentation and evidence are essential for audits
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
