"""
Twin Lifecycle Management - Main Demonstration

This script demonstrates twin lifecycle management with state transitions,
version control, and change tracking.

Usage:
    python main_06_twin_lifecycle_management.py

Example:
    python main_06_twin_lifecycle_management.py
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


class LifecycleStage(Enum):
    """Twin lifecycle stages."""
    DESIGN = "design"
    BUILD = "build"
    TEST = "test"
    DEPLOY = "deploy"
    OPERATE = "operate"
    MAINTAIN = "maintain"
    RETIRE = "retire"
    ARCHIVED = "archived"


VALID_TRANSITIONS = {
    LifecycleStage.DESIGN: [LifecycleStage.BUILD],
    LifecycleStage.BUILD: [LifecycleStage.TEST, LifecycleStage.DESIGN],
    LifecycleStage.TEST: [LifecycleStage.DEPLOY, LifecycleStage.BUILD],
    LifecycleStage.DEPLOY: [LifecycleStage.OPERATE, LifecycleStage.TEST],
    LifecycleStage.OPERATE: [LifecycleStage.MAINTAIN, LifecycleStage.RETIRE],
    LifecycleStage.MAINTAIN: [LifecycleStage.OPERATE, LifecycleStage.RETIRE],
    LifecycleStage.RETIRE: [LifecycleStage.ARCHIVED],
    LifecycleStage.ARCHIVED: [],
}


@dataclass
class ChangeRecord:
    """Record of a change to the twin."""
    change_id: str
    timestamp: datetime
    change_type: str
    description: str
    author: str
    from_version: str
    to_version: str
    approved_by: Optional[str] = None


@dataclass
class TwinVersion:
    """A version of the twin definition."""
    version: str
    created_at: datetime
    created_by: str
    description: str
    model_hash: str
    is_current: bool = False


@dataclass
class ManagedTwin:
    """A twin with lifecycle management."""
    
    twin_id: str
    name: str
    asset_id: str
    
    stage: LifecycleStage = LifecycleStage.DESIGN
    current_version: str = "0.0.0"
    
    versions: List[TwinVersion] = field(default_factory=list)
    changes: List[ChangeRecord] = field(default_factory=list)
    stage_history: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self._record_stage_transition(None, self.stage, "Initial creation")
        self._create_version("0.0.0", "Initial version", "system")
    
    def _record_stage_transition(self, from_stage: Optional[LifecycleStage],
                                  to_stage: LifecycleStage, reason: str) -> None:
        self.stage_history.append({
            'timestamp': datetime.now(),
            'from_stage': from_stage.value if from_stage else None,
            'to_stage': to_stage.value,
            'reason': reason
        })
    
    def _create_version(self, version: str, description: str, author: str) -> None:
        for v in self.versions:
            v.is_current = False
        
        new_version = TwinVersion(
            version=version,
            created_at=datetime.now(),
            created_by=author,
            description=description,
            model_hash=f"hash_{version}_{datetime.now().timestamp()}",
            is_current=True
        )
        self.versions.append(new_version)
        self.current_version = version
    
    def transition_to(self, new_stage: LifecycleStage, reason: str,
                     author: str) -> tuple[bool, str]:
        """Transition to a new lifecycle stage."""
        if new_stage not in VALID_TRANSITIONS.get(self.stage, []):
            return False, f"Cannot transition from {self.stage.value} to {new_stage.value}"
        
        old_stage = self.stage
        self.stage = new_stage
        self._record_stage_transition(old_stage, new_stage, reason)
        self.last_modified = datetime.now()
        
        return True, f"Transitioned from {old_stage.value} to {new_stage.value}"
    
    def apply_change(self, change_type: str, description: str,
                    author: str, new_version: str,
                    approver: Optional[str] = None) -> ChangeRecord:
        """Apply a change to the twin."""
        change = ChangeRecord(
            change_id=f"CHG-{len(self.changes) + 1:04d}",
            timestamp=datetime.now(),
            change_type=change_type,
            description=description,
            author=author,
            from_version=self.current_version,
            to_version=new_version,
            approved_by=approver
        )
        self.changes.append(change)
        self._create_version(new_version, description, author)
        self.last_modified = datetime.now()
        
        return change
    
    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get complete audit trail."""
        trail = []
        
        for stage in self.stage_history:
            trail.append({
                'timestamp': stage['timestamp'],
                'type': 'stage_transition',
                'details': f"{stage['from_stage']} -> {stage['to_stage']}: {stage['reason']}"
            })
        
        for change in self.changes:
            trail.append({
                'timestamp': change.timestamp,
                'type': 'change',
                'details': f"{change.change_type}: {change.description} (v{change.to_version})"
            })
        
        trail.sort(key=lambda x: x['timestamp'])
        return trail
    
    def archive(self) -> Dict[str, Any]:
        """Create archive package for retired twin."""
        return {
            'twin_id': self.twin_id,
            'name': self.name,
            'asset_id': self.asset_id,
            'final_version': self.current_version,
            'created_at': self.created_at.isoformat(),
            'archived_at': datetime.now().isoformat(),
            'total_versions': len(self.versions),
            'total_changes': len(self.changes),
            'stage_history': self.stage_history,
            'versions': [{'version': v.version, 'created_at': v.created_at.isoformat()} 
                        for v in self.versions],
            'metadata': self.metadata
        }


class LifecycleManager:
    """Manager for twin lifecycles."""
    
    def __init__(self):
        self.twins: Dict[str, ManagedTwin] = {}
        self.archived: Dict[str, Dict[str, Any]] = {}
    
    def create_twin(self, twin_id: str, name: str, asset_id: str,
                   creator: str) -> ManagedTwin:
        """Create a new managed twin."""
        twin = ManagedTwin(
            twin_id=twin_id,
            name=name,
            asset_id=asset_id,
            metadata={'creator': creator}
        )
        self.twins[twin_id] = twin
        return twin
    
    def get_twins_by_stage(self, stage: LifecycleStage) -> List[ManagedTwin]:
        """Get all twins in a specific stage."""
        return [t for t in self.twins.values() if t.stage == stage]
    
    def retire_twin(self, twin_id: str, reason: str, author: str) -> bool:
        """Retire and archive a twin."""
        twin = self.twins.get(twin_id)
        if not twin:
            return False
        
        success, _ = twin.transition_to(LifecycleStage.RETIRE, reason, author)
        if not success:
            return False
        
        success, _ = twin.transition_to(LifecycleStage.ARCHIVED, "Archival complete", author)
        if not success:
            return False
        
        self.archived[twin_id] = twin.archive()
        del self.twins[twin_id]
        return True
    
    def get_lifecycle_report(self) -> Dict[str, Any]:
        """Generate lifecycle status report."""
        stage_counts = {}
        for stage in LifecycleStage:
            stage_counts[stage.value] = len(self.get_twins_by_stage(stage))
        
        return {
            'total_active': len(self.twins),
            'total_archived': len(self.archived),
            'by_stage': stage_counts,
            'twins': [{
                'id': t.twin_id,
                'name': t.name,
                'stage': t.stage.value,
                'version': t.current_version
            } for t in self.twins.values()]
        }


def run_demonstration() -> None:
    """Run the lifecycle management demonstration."""
    
    print_section("Twin Lifecycle Management Demo")
    print("This demo shows how twins are managed through their lifecycle.\n")
    
    manager = LifecycleManager()
    
    print_section("Creating Twins")
    
    pump_twin = manager.create_twin(
        twin_id="DT-PUMP-001",
        name="Industrial Pump Twin",
        asset_id="PUMP-001",
        creator="engineer@company.com"
    )
    print(f"Created: {pump_twin.name} ({pump_twin.twin_id})")
    print(f"  Stage: {pump_twin.stage.value}")
    print(f"  Version: {pump_twin.current_version}")
    
    motor_twin = manager.create_twin(
        twin_id="DT-MOTOR-001",
        name="Motor Twin",
        asset_id="MOTOR-001",
        creator="engineer@company.com"
    )
    print(f"Created: {motor_twin.name} ({motor_twin.twin_id})")
    
    print_section("Lifecycle Transitions")
    
    transitions = [
        (LifecycleStage.BUILD, "Design complete, starting development"),
        (LifecycleStage.TEST, "Development complete, starting testing"),
        (LifecycleStage.DEPLOY, "Testing passed, deploying to production"),
        (LifecycleStage.OPERATE, "Deployment complete, entering operation"),
    ]
    
    for new_stage, reason in transitions:
        success, message = pump_twin.transition_to(new_stage, reason, "engineer@company.com")
        status = "OK" if success else "FAILED"
        print(f"[{status}] {message}")
    
    print(f"\nCurrent stage: {pump_twin.stage.value}")
    
    print_section("Applying Changes")
    
    changes = [
        ("model_update", "Added vibration monitoring", "1.0.0"),
        ("config_change", "Updated threshold values", "1.0.1"),
        ("feature_add", "Added predictive maintenance", "1.1.0"),
    ]
    
    for change_type, description, version in changes:
        change = pump_twin.apply_change(
            change_type=change_type,
            description=description,
            author="developer@company.com",
            new_version=version,
            approver="manager@company.com"
        )
        print(f"Applied: {change.change_id} - {description} (v{version})")
    
    print(f"\nCurrent version: {pump_twin.current_version}")
    print(f"Total versions: {len(pump_twin.versions)}")
    
    print_section("Version History")
    
    for v in pump_twin.versions:
        current = " (current)" if v.is_current else ""
        print(f"  v{v.version}: {v.description}{current}")
    
    print_section("Audit Trail")
    
    trail = pump_twin.get_audit_trail()
    for entry in trail[-5:]:
        print(f"  [{entry['type']}] {entry['details']}")
    
    print_section("Maintenance Cycle")
    
    success, msg = pump_twin.transition_to(
        LifecycleStage.MAINTAIN,
        "Scheduled maintenance window",
        "ops@company.com"
    )
    print(f"Entered maintenance: {msg}")
    
    pump_twin.apply_change(
        change_type="maintenance",
        description="Calibration update after physical maintenance",
        author="technician@company.com",
        new_version="1.1.1"
    )
    
    success, msg = pump_twin.transition_to(
        LifecycleStage.OPERATE,
        "Maintenance complete",
        "ops@company.com"
    )
    print(f"Returned to operation: {msg}")
    
    print_section("Retiring a Twin")
    
    success = manager.retire_twin(
        twin_id="DT-MOTOR-001",
        reason="Physical asset decommissioned",
        author="manager@company.com"
    )
    print(f"Motor twin retired: {'Success' if success else 'Failed'}")
    
    print_section("Lifecycle Report")
    
    report = manager.get_lifecycle_report()
    print(f"Active twins: {report['total_active']}")
    print(f"Archived twins: {report['total_archived']}")
    print("\nTwins by stage:")
    for stage, count in report['by_stage'].items():
        if count > 0:
            print(f"  {stage}: {count}")
    
    print_section("Key Takeaways")
    print("""
1. Twins progress through defined lifecycle stages
2. Valid transitions are enforced (can't skip stages)
3. All changes are versioned and tracked
4. Audit trails provide complete history
5. Retired twins are archived for future reference
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
