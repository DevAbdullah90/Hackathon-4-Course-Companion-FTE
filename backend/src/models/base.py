from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, JSON, Column, Text
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_premium: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    premium_since: Optional[datetime] = None
    streak_count: int = Field(default=0)
    last_active_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    progress: List["Progress"] = Relationship(back_populates="user")

class Course(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    slug: str = Field(unique=True, index=True)
    title: str
    description: str
    is_published: bool = Field(default=True)
    modules: List["Module"] = Relationship(back_populates="course")

class Module(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(foreign_key="course.id")
    course: Course = Relationship(back_populates="modules")
    title: str
    description: Optional[str] = None
    order_index: int
    chapters: List["Chapter"] = Relationship(back_populates="module")

class Chapter(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    module_id: UUID = Field(foreign_key="module.id")
    module: Module = Relationship(back_populates="chapters")
    title: str
    slug: str
    r2_key: str
    content: Optional[str] = Field(default=None, sa_column=Column(Text))
    is_premium: bool = Field(default=False)
    order_index: int
    quiz: Optional["Quiz"] = Relationship(back_populates="chapter")

class Quiz(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    chapter_id: UUID = Field(foreign_key="chapter.id")
    chapter: Chapter = Relationship(back_populates="quiz")
    content: Dict = Field(default={}, sa_type=JSON) # Stores questions, options, answer_key

class Progress(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    chapter_id: UUID = Field(foreign_key="chapter.id", primary_key=True)
    is_completed: bool = Field(default=False)
    quiz_score: Optional[int] = None
    completed_at: Optional[datetime] = None
    user: User = Relationship(back_populates="progress")
