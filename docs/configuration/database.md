# Database & ORM Configuration

FastAPI Smith supports multiple database and ORM combinations. Choose the setup that best fits your project needs.

## Supported Databases

### PostgreSQL
Production-ready, feature-rich relational database.

**Driver**: `asyncpg` (async) or `psycopg3` (async)

**Connection URL**:
```
postgresql+asyncpg://user:password@localhost/dbname
```

**Best for**: Production applications, complex queries, large datasets

### MySQL
Popular open-source relational database.

**Driver**: `asyncmy` (async)

**Connection URL**:
```
mysql+asyncmy://user:password@localhost/dbname
```

**Best for**: Applications requiring MySQL-specific features

### SQLite
Lightweight file-based database.

**Driver**: `aiosqlite` (async)

**Connection URL**:
```
sqlite+aiosqlite:///./database.db
```

**Best for**: Development, testing, small applications

## ORM Options

### SQLAlchemy 2.0
Industry-standard ORM with powerful features.

**Features**:
- Async support with asyncio
- Type hints with Mapped types
- Powerful query API
- Relationship management
- Connection pooling

**Example Model**:
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(100))
```

### SQLModel
Combines SQLAlchemy and Pydantic for simpler code.

**Features**:
- Unified models for DB and API
- Inherits SQLAlchemy power
- Pydantic validation
- Less boilerplate

**Example Model**:
```python
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
```

### Tortoise-ORM
Django-like ORM with async-first design.

**Features**:
- Simple, intuitive API
- Built-in async support
- Automatic migrations with Aerich
- Multiple database support

**Example Model**:
```python
from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=100)
    
    class Meta:
        table = "users"
```

## Next Steps

- [Authentication Configuration →](authentication.md)
- [Database Migrations Guide →](../guides/migrations.md)
- [Testing Database Code →](../guides/testing.md)
