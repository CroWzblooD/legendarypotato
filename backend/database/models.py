"""
SQLAlchemy ORM models for PostgreSQL database.
Defines all tables: users, conversations, chat_messages, tool_executions, parameter_extractions
"""
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, 
    ForeignKey, CheckConstraint, Index, JSON
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class User(Base):
    """
    Student/User profiles table.
    Stores persistent student information across sessions.
    """
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    grade_level = Column(String(50), nullable=False)
    learning_style_summary = Column(Text, nullable=True)
    emotional_state_summary = Column(Text, nullable=True)
    mastery_level_summary = Column(Text, nullable=True)
    teaching_style = Column(
        String(50), 
        nullable=False, 
        default="direct",
        server_default="direct"
    )
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "teaching_style IN ('direct', 'socratic', 'visual', 'flipped_classroom')",
            name="teaching_style_check"
        ),
        Index("idx_users_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.name}, grade={self.grade_level})>"


class Conversation(Base):
    """
    Conversations table.
    Groups related chat messages together.
    """
    __tablename__ = "conversations"
    
    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    started_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    last_message_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    message_count = Column(Integer, nullable=False, default=0, server_default="0")
    status = Column(
        String(50), 
        nullable=False, 
        default="active",
        server_default="active"
    )
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")
    tool_executions = relationship("ToolExecution", back_populates="conversation", cascade="all, delete-orphan")
    parameter_extractions = relationship("ParameterExtraction", back_populates="conversation", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'abandoned')",
            name="status_check"
        ),
        Index("idx_conversations_user_id", "user_id"),
        Index("idx_conversations_started_at", "started_at"),
    )
    
    def __repr__(self):
        return f"<Conversation(id={self.conversation_id}, user_id={self.user_id}, status={self.status})>"


class ChatMessage(Base):
    """
    Chat messages table.
    Stores individual messages in conversations.
    """
    __tablename__ = "chat_messages"
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"), 
        nullable=False
    )
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tool_used = Column(String(100), nullable=True)
    timestamp = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'assistant')",
            name="role_check"
        ),
        Index("idx_messages_conversation", "conversation_id"),
        Index("idx_messages_timestamp", "timestamp"),
    )
    
    def __repr__(self):
        return f"<ChatMessage(id={self.message_id}, role={self.role}, conv_id={self.conversation_id})>"


class ToolExecution(Base):
    """
    Tool executions table.
    Logs every tool execution with parameters and results.
    """
    __tablename__ = "tool_executions"
    
    execution_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"), 
        nullable=False
    )
    tool_type = Column(String(100), nullable=False)
    input_params = Column(JSONB, nullable=False)
    output_data = Column(JSONB, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    success = Column(Boolean, nullable=False, default=True, server_default="true")
    error_message = Column(Text, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    
    # Relationships
    conversation = relationship("Conversation", back_populates="tool_executions")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "tool_type IN ('note_maker', 'flashcard_generator', 'concept_explainer')",
            name="tool_type_check"
        ),
        Index("idx_executions_conversation", "conversation_id"),
        Index("idx_executions_tool_type", "tool_type"),
        Index("idx_executions_created_at", "created_at"),
        Index("idx_executions_params", "input_params", postgresql_using="gin"),
    )
    
    def __repr__(self):
        return f"<ToolExecution(id={self.execution_id}, tool={self.tool_type}, success={self.success})>"


class ParameterExtraction(Base):
    """
    Parameter extractions table.
    Tracks parameter extraction quality and inference performance (40% of hackathon score!).
    """
    __tablename__ = "parameter_extractions"
    
    extraction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"), 
        nullable=False
    )
    user_message = Column(Text, nullable=False)
    extracted_params = Column(JSONB, nullable=False)
    inferred_params = Column(JSONB, nullable=True)
    confidence_score = Column(Float, nullable=False)
    missing_required = Column(JSONB, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    
    # Relationships
    conversation = relationship("Conversation", back_populates="parameter_extractions")
    
    # Constraints
    __table_args__ = (
        Index("idx_extractions_conversation", "conversation_id"),
        Index("idx_extractions_confidence", "confidence_score"),
        Index("idx_extractions_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<ParameterExtraction(id={self.extraction_id}, confidence={self.confidence_score})>"
