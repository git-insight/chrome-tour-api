# models.py

from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username', name='uq_users_username'),
        UniqueConstraint('email', name='uq_users_email'),
        UniqueConstraint('phone_number', name='uq_users_phone_number'),
        {'schema': 'chrome_users'}
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(20))
    password_hash = Column(Text)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    last_login_ip = Column(String(45))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    provider = Column(String(50))
    provider_user_id = Column(String(100))
    profile_picture_url = Column(String(255))
    email_verified = Column(Boolean, default=False)
    verification_code = Column(String(10))
    verification_attempts = Column(Integer, default=0)
    verification_code_sent_at = Column(TIMESTAMP)
    verification_code_expires_at = Column(TIMESTAMP)
    email_verified_at = Column(TIMESTAMP)
    requires_mfa = Column(Boolean, default=False)
    mfa_secret = Column(Text)
    mfa_app = Column(String(50))
    mfa_verified_at = Column(TIMESTAMP)
    registration_ip = Column(String(45))
    registration_user_agent = Column(String(255))
    registered_via = Column(String(50))
    registration_referrer = Column(String(255))
    terms_accepted = Column(Boolean, default=False)
    terms_accepted_at = Column(TIMESTAMP)
    blocked_until = Column(TIMESTAMP)

    roles = relationship('UserRole', back_populates='user')
    logins = relationship('UserLogin', back_populates='user')
    password_reset_tokens = relationship('PasswordResetToken', back_populates='user')
    sessions = relationship('UserSession', back_populates='user')
    audit_logs = relationship('AuditLog', back_populates='user', foreign_keys='AuditLog.user_id')
    refresh_tokens = relationship('RefreshToken', back_populates='user')
    authorization_codes = relationship('AuthorizationCode', back_populates='user')
    profile = relationship('UserProfile', back_populates='user', uselist=False)
    profile_history = relationship('UserProfileHistory', back_populates='user')
    background_jobs = relationship('UserJobQueue', back_populates='user')


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    date_of_birth = Column(TIMESTAMP)
    gender = Column(String(10))
    address = Column(Text)
    country = Column(String(50))
    timezone = Column(String(50))
    bio = Column(Text)
    website = Column(String(255))
    social_links = Column(Text)

    user = relationship('User', back_populates='profile')


class UserProfileHistory(Base):
    __tablename__ = 'user_profile_history'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    date_of_birth = Column(TIMESTAMP)
    gender = Column(String(10))
    address = Column(Text)
    country = Column(String(50))
    timezone = Column(String(50))
    bio = Column(Text)
    website = Column(String(255))
    social_links = Column(Text)
    updated_at = Column(TIMESTAMP, default=func.now())

    user = relationship('User', back_populates='profile_history')


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())

    users = relationship('UserRole', back_populates='role')


class UserRole(Base):
    __tablename__ = 'user_roles'
    __table_args__ = {'schema': 'chrome_users'}

    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('chrome_users.roles.id'), primary_key=True, index=True)
    assigned_at = Column(TIMESTAMP, default=func.now())
    is_deleted = Column(Boolean, default=False)

    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')


class UserLogin(Base):
    __tablename__ = 'user_logins'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), index=True)
    login_provider = Column(String(50))
    login_ip = Column(String(45))
    login_time = Column(TIMESTAMP, default=func.now())

    user = relationship('User', back_populates='logins')


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), index=True)
    token = Column(String(255), unique=True, index=True)
    expires_at = Column(TIMESTAMP)
    used_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship('User', back_populates='password_reset_tokens')


class UserSession(Base):
    __tablename__ = 'user_sessions'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), index=True)
    device = Column(Text)
    user_agent = Column(Text)
    login_at = Column(TIMESTAMP, default=func.now())
    expires_at = Column(TIMESTAMP)
    revoked_at = Column(TIMESTAMP)
    token_hash = Column(String(255), unique=True)

    user = relationship('User', back_populates='sessions')


class CaptchaChallenge(Base):
    __tablename__ = 'captcha_challenges'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    challenge = Column(Text, nullable=False)
    solved = Column(Boolean, default=False)
    solved_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=func.now())


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    issued_at = Column(TIMESTAMP, default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    revoked_at = Column(TIMESTAMP)
    created_by_ip = Column(String(45))
    replaced_by_token = Column(String(255))
    user_agent = Column(Text)
    is_rotated = Column(Boolean, default=False)

    user = relationship('User', back_populates='refresh_tokens')


class AuthorizationCode(Base):
    __tablename__ = 'authorization_codes'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=False, index=True)
    code = Column(String(255), unique=True, nullable=False, index=True)
    redirect_uri = Column(Text)
    expires_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship('User', back_populates='authorization_codes')


class LoginAttemptLog(Base):
    __tablename__ = 'login_attempt_logs'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=True)
    attempted_at = Column(TIMESTAMP, default=func.now())
    was_successful = Column(Boolean)
    reason = Column(Text)

    user = relationship('User')


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=True)
    actor_id = Column(Integer, ForeignKey('chrome_users.users.id'), nullable=True)
    event_type = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    target = Column(String(100))
    meta_info = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship('User', foreign_keys=[user_id], back_populates='audit_logs')
    actor = relationship('User', foreign_keys=[actor_id])


class UserJobQueue(Base):
    __tablename__ = 'user_job_queue'
    __table_args__ = {'schema': 'chrome_users'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('chrome_users.users.id'), index=True)
    job_type = Column(String(100))
    payload = Column(Text)
    scheduled_for = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=func.now())
    processed_at = Column(TIMESTAMP)
    status = Column(String(20), default='pending')

    user = relationship('User', back_populates='background_jobs')
