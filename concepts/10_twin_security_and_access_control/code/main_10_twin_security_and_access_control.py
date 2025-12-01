"""
Twin Security and Access Control - Main Demonstration

This script demonstrates security concepts including authentication,
authorization, encryption, and audit logging for digital twins.

Usage:
    python main_10_twin_security_and_access_control.py

Example:
    python main_10_twin_security_and_access_control.py
"""

import sys
import os
import hashlib
import base64
import secrets
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

# Add the repository root to the path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
sys.path.insert(0, repo_root)
from common.utils import print_section


class Permission(Enum):
    """Available permissions."""
    READ_DATA = "read_data"
    WRITE_DATA = "write_data"
    READ_CONFIG = "read_config"
    WRITE_CONFIG = "write_config"
    EXECUTE_COMMAND = "execute_command"
    ADMIN = "admin"


class Role(Enum):
    """User roles with associated permissions."""
    VIEWER = "viewer"
    OPERATOR = "operator"
    ENGINEER = "engineer"
    ADMIN = "admin"


ROLE_PERMISSIONS = {
    Role.VIEWER: {Permission.READ_DATA},
    Role.OPERATOR: {Permission.READ_DATA, Permission.WRITE_DATA, Permission.EXECUTE_COMMAND},
    Role.ENGINEER: {Permission.READ_DATA, Permission.WRITE_DATA, Permission.READ_CONFIG, Permission.WRITE_CONFIG},
    Role.ADMIN: {p for p in Permission},
}


@dataclass
class User:
    """User entity."""
    user_id: str
    username: str
    password_hash: str
    role: Role
    is_active: bool = True
    mfa_enabled: bool = False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password."""
        salt = "twin_security_salt"
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify a password."""
        return self.password_hash == self.hash_password(password)


@dataclass
class Session:
    """User session."""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    
    def is_valid(self) -> bool:
        return datetime.now() < self.expires_at


@dataclass
class AuditLogEntry:
    """Audit log entry."""
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    result: str
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""


class SimpleEncryption:
    """Simple encryption for demonstration (NOT for production use)."""
    
    def __init__(self, key: str):
        self.key = key
    
    def encrypt(self, plaintext: str) -> str:
        """Simple XOR encryption (demonstration only)."""
        key_bytes = (self.key * (len(plaintext) // len(self.key) + 1))[:len(plaintext)]
        encrypted = bytes(a ^ b for a, b in zip(plaintext.encode(), key_bytes.encode()))
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Simple XOR decryption (demonstration only)."""
        encrypted = base64.b64decode(ciphertext.encode())
        key_bytes = (self.key * (len(encrypted) // len(self.key) + 1))[:len(encrypted)]
        decrypted = bytes(a ^ b for a, b in zip(encrypted, key_bytes.encode()))
        return decrypted.decode()


class SecurityManager:
    """Manages security for digital twins."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self.audit_log: List[AuditLogEntry] = []
        self.encryption = SimpleEncryption("demo_encryption_key_32b")
        self.failed_attempts: Dict[str, int] = {}
        self.max_failed_attempts = 3
    
    def register_user(self, username: str, password: str, role: Role) -> User:
        """Register a new user."""
        user_id = f"user_{len(self.users) + 1:04d}"
        user = User(
            user_id=user_id,
            username=username,
            password_hash=User.hash_password(password),
            role=role
        )
        self.users[user_id] = user
        
        self._log_audit(user_id, "USER_REGISTERED", f"user:{username}", "SUCCESS")
        return user
    
    def authenticate(self, username: str, password: str, ip_address: str = "127.0.0.1") -> Optional[Session]:
        """Authenticate a user and create a session."""
        user = next((u for u in self.users.values() if u.username == username), None)
        
        if not user:
            self._log_audit("unknown", "LOGIN_ATTEMPT", f"user:{username}", "FAILED", 
                          {"reason": "user_not_found"}, ip_address)
            return None
        
        if self.failed_attempts.get(user.user_id, 0) >= self.max_failed_attempts:
            self._log_audit(user.user_id, "LOGIN_ATTEMPT", f"user:{username}", "BLOCKED",
                          {"reason": "account_locked"}, ip_address)
            return None
        
        if not user.verify_password(password):
            self.failed_attempts[user.user_id] = self.failed_attempts.get(user.user_id, 0) + 1
            self._log_audit(user.user_id, "LOGIN_ATTEMPT", f"user:{username}", "FAILED",
                          {"reason": "invalid_password"}, ip_address)
            return None
        
        if not user.is_active:
            self._log_audit(user.user_id, "LOGIN_ATTEMPT", f"user:{username}", "FAILED",
                          {"reason": "account_disabled"}, ip_address)
            return None
        
        self.failed_attempts[user.user_id] = 0
        
        from datetime import timedelta
        session = Session(
            session_id=secrets.token_hex(16),
            user_id=user.user_id,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=8),
            ip_address=ip_address
        )
        self.sessions[session.session_id] = session
        
        self._log_audit(user.user_id, "LOGIN_SUCCESS", f"user:{username}", "SUCCESS",
                       {"session_id": session.session_id[:8]}, ip_address)
        return session
    
    def authorize(self, session_id: str, permission: Permission, resource: str) -> bool:
        """Check if a session has permission for an action."""
        session = self.sessions.get(session_id)
        if not session or not session.is_valid():
            self._log_audit("unknown", "AUTHORIZATION", resource, "DENIED",
                          {"reason": "invalid_session"})
            return False
        
        user = self.users.get(session.user_id)
        if not user:
            return False
        
        allowed_permissions = ROLE_PERMISSIONS.get(user.role, set())
        is_authorized = permission in allowed_permissions
        
        result = "ALLOWED" if is_authorized else "DENIED"
        self._log_audit(user.user_id, f"ACCESS_{permission.value.upper()}", resource, result,
                       {"role": user.role.value}, session.ip_address)
        
        return is_authorized
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.encryption.encrypt(data)
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.encryption.decrypt(encrypted_data)
    
    def _log_audit(self, user_id: str, action: str, resource: str, result: str,
                   details: Dict[str, Any] = None, ip_address: str = "") -> None:
        """Add an entry to the audit log."""
        entry = AuditLogEntry(
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            resource=resource,
            result=result,
            details=details or {},
            ip_address=ip_address
        )
        self.audit_log.append(entry)
    
    def get_audit_log(self, user_id: str = None, action: str = None,
                     limit: int = 100) -> List[AuditLogEntry]:
        """Query the audit log."""
        entries = self.audit_log
        
        if user_id:
            entries = [e for e in entries if e.user_id == user_id]
        if action:
            entries = [e for e in entries if action in e.action]
        
        return entries[-limit:]
    
    def logout(self, session_id: str) -> bool:
        """End a user session."""
        session = self.sessions.get(session_id)
        if session:
            self._log_audit(session.user_id, "LOGOUT", f"session:{session_id[:8]}", "SUCCESS")
            del self.sessions[session_id]
            return True
        return False


class SecureTwin:
    """Digital twin with security controls."""
    
    def __init__(self, twin_id: str, security_manager: SecurityManager):
        self.twin_id = twin_id
        self.security = security_manager
        self.data: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
    
    def read_data(self, session_id: str, key: str) -> Optional[Any]:
        """Read data with authorization check."""
        if not self.security.authorize(session_id, Permission.READ_DATA, f"twin:{self.twin_id}/data/{key}"):
            return None
        return self.data.get(key)
    
    def write_data(self, session_id: str, key: str, value: Any) -> bool:
        """Write data with authorization check."""
        if not self.security.authorize(session_id, Permission.WRITE_DATA, f"twin:{self.twin_id}/data/{key}"):
            return False
        self.data[key] = value
        return True
    
    def read_config(self, session_id: str, key: str) -> Optional[Any]:
        """Read config with authorization check."""
        if not self.security.authorize(session_id, Permission.READ_CONFIG, f"twin:{self.twin_id}/config/{key}"):
            return None
        return self.config.get(key)
    
    def write_config(self, session_id: str, key: str, value: Any) -> bool:
        """Write config with authorization check."""
        if not self.security.authorize(session_id, Permission.WRITE_CONFIG, f"twin:{self.twin_id}/config/{key}"):
            return False
        self.config[key] = value
        return True
    
    def execute_command(self, session_id: str, command: str) -> Optional[str]:
        """Execute command with authorization check."""
        if not self.security.authorize(session_id, Permission.EXECUTE_COMMAND, f"twin:{self.twin_id}/command/{command}"):
            return None
        return f"Command '{command}' executed successfully"


def run_demonstration() -> None:
    """Run the security demonstration."""
    
    print_section("Twin Security and Access Control Demo")
    print("This demo shows how security protects digital twin systems.\n")
    
    security = SecurityManager()
    
    print_section("User Registration")
    
    admin = security.register_user("admin", "admin_pass_123", Role.ADMIN)
    engineer = security.register_user("engineer", "eng_pass_456", Role.ENGINEER)
    operator = security.register_user("operator", "op_pass_789", Role.OPERATOR)
    viewer = security.register_user("viewer", "view_pass_000", Role.VIEWER)
    
    print("Registered users:")
    for user in [admin, engineer, operator, viewer]:
        print(f"  - {user.username} ({user.role.value})")
    
    print_section("Authentication")
    
    print("\nAttempting login with correct credentials...")
    admin_session = security.authenticate("admin", "admin_pass_123", "192.168.1.100")
    print(f"  Admin login: {'SUCCESS' if admin_session else 'FAILED'}")
    
    engineer_session = security.authenticate("engineer", "eng_pass_456", "192.168.1.101")
    print(f"  Engineer login: {'SUCCESS' if engineer_session else 'FAILED'}")
    
    operator_session = security.authenticate("operator", "op_pass_789", "192.168.1.102")
    print(f"  Operator login: {'SUCCESS' if operator_session else 'FAILED'}")
    
    viewer_session = security.authenticate("viewer", "view_pass_000", "192.168.1.103")
    print(f"  Viewer login: {'SUCCESS' if viewer_session else 'FAILED'}")
    
    print("\nAttempting login with wrong password...")
    failed_session = security.authenticate("admin", "wrong_password", "192.168.1.200")
    print(f"  Result: {'SUCCESS' if failed_session else 'FAILED (as expected)'}")
    
    print_section("Authorization (Role-Based Access Control)")
    
    twin = SecureTwin("DT-PUMP-001", security)
    twin.data = {"temperature": 45.0, "pressure": 5.2}
    twin.config = {"threshold": 60.0, "mode": "auto"}
    
    print("\nTesting access for different roles:\n")
    
    print("VIEWER trying to:")
    print(f"  Read data: {'ALLOWED' if twin.read_data(viewer_session.session_id, 'temperature') is not None else 'DENIED'}")
    print(f"  Write data: {'ALLOWED' if twin.write_data(viewer_session.session_id, 'temperature', 50) else 'DENIED'}")
    print(f"  Execute command: {'ALLOWED' if twin.execute_command(viewer_session.session_id, 'start') else 'DENIED'}")
    
    print("\nOPERATOR trying to:")
    print(f"  Read data: {'ALLOWED' if twin.read_data(operator_session.session_id, 'temperature') is not None else 'DENIED'}")
    print(f"  Write data: {'ALLOWED' if twin.write_data(operator_session.session_id, 'temperature', 50) else 'DENIED'}")
    print(f"  Read config: {'ALLOWED' if twin.read_config(operator_session.session_id, 'threshold') is not None else 'DENIED'}")
    print(f"  Execute command: {'ALLOWED' if twin.execute_command(operator_session.session_id, 'start') else 'DENIED'}")
    
    print("\nENGINEER trying to:")
    print(f"  Read data: {'ALLOWED' if twin.read_data(engineer_session.session_id, 'temperature') is not None else 'DENIED'}")
    print(f"  Write config: {'ALLOWED' if twin.write_config(engineer_session.session_id, 'threshold', 65) else 'DENIED'}")
    print(f"  Execute command: {'ALLOWED' if twin.execute_command(engineer_session.session_id, 'start') else 'DENIED'}")
    
    print_section("Data Encryption")
    
    sensitive_data = "Equipment serial: ABC-123-XYZ"
    print(f"\nOriginal data: {sensitive_data}")
    
    encrypted = security.encrypt_data(sensitive_data)
    print(f"Encrypted: {encrypted}")
    
    decrypted = security.decrypt_data(encrypted)
    print(f"Decrypted: {decrypted}")
    
    print_section("Audit Log")
    
    print("\nRecent audit log entries:")
    for entry in security.get_audit_log(limit=10):
        print(f"  [{entry.timestamp.strftime('%H:%M:%S')}] {entry.action}: {entry.resource} -> {entry.result}")
    
    print_section("Security Summary")
    
    print(f"""
Security Controls Demonstrated:

1. AUTHENTICATION
   - Password hashing with salt
   - Session management with expiration
   - Failed attempt tracking and lockout

2. AUTHORIZATION (RBAC)
   - Role-based permissions
   - Resource-level access control
   - Principle of least privilege

3. DATA PROTECTION
   - Encryption of sensitive data
   - Key management (simplified)

4. AUDIT LOGGING
   - All access attempts logged
   - Success and failure tracking
   - IP address recording
""")
    
    print_section("Key Takeaways")
    print("""
1. Authentication verifies identity before granting access
2. Authorization controls what each user can do
3. Role-based access control simplifies permission management
4. Encryption protects sensitive data
5. Audit logs provide accountability and forensics capability
""")


def main():
    run_demonstration()


if __name__ == "__main__":
    main()
