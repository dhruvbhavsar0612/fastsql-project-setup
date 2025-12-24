# Your First Project

This tutorial walks you through creating a simple blog API with FastAPI Smith.

## Project Setup

Let's create a blog API with posts and comments:

```bash
fastapi-smith
```

### Configuration

Use these settings for the tutorial:

- **Project name**: `blog-api`
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT
- **Admin**: Yes (SQLAdmin)
- **Caching**: Redis
- **Logging**: Loguru
- **Package manager**: uv
- **Docker**: Yes

## Understanding the Structure

After generation, you'll have:

```
blog-api/
├── app/
│   ├── main.py           # Application entry point
│   ├── config.py         # Settings
│   ├── database.py       # Database setup
│   ├── models/           # Database models
│   │   ├── base.py
│   │   └── user.py       # User model (generated)
│   ├── schemas/          # Pydantic schemas
│   │   └── user.py
│   ├── routes/           # API routes
│   │   ├── auth.py       # Auth endpoints
│   │   └── users.py      # User endpoints
│   └── core/             # Core functionality
│       ├── security.py   # JWT & password hashing
│       └── logging.py    # Logging setup
├── migrations/           # Alembic migrations
├── tests/               # Tests
└── .env.example         # Environment template
```

## Setting Up the Environment

1. **Copy environment file**:
   ```bash
   cd blog-api
   cp .env.example .env
   ```

2. **Edit `.env`** with your database credentials:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost/blog
   SECRET_KEY=your-secret-key-here
   REDIS_URL=redis://localhost:6379
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Create database**:
   ```bash
   createdb blog  # or use your preferred method
   ```

5. **Run migrations**:
   ```bash
   uv run alembic upgrade head
   ```

## Creating the Blog Models

Create `app/models/post.py`:

```python
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped[Post] = relationship(back_populates="comments")
    
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
```

Update `app/models/user.py` to add relationships:

```python
# Add to User model
posts: Mapped[list["Post"]] = relationship(back_populates="author")
comments: Mapped[list["Comment"]] = relationship(back_populates="author")
```

## Creating Pydantic Schemas

Create `app/schemas/post.py`:

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    author_id: int
    created_at: datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    author_id: int
    created_at: datetime
    comments: list[Comment] = []
```

## Creating API Routes

Create `app/routes/posts.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.post import Post, Comment
from ..models.user import User
from ..schemas.post import PostCreate, Post as PostSchema, CommentCreate
from ..core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = Post(**post.model_dump(), author_id=current_user.id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostSchema])
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Post).where(Post.published == True).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get("/{post_id}", response_model=PostSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = Comment(
        **comment.model_dump(),
        post_id=post_id,
        author_id=current_user.id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment
```

## Registering the Routes

Update `app/main.py` to include the posts router:

```python
from .routes import posts

# Add after existing router includes
app.include_router(posts.router)
```

## Running Migrations

Generate a migration for the new models:

```bash
uv run alembic revision --autogenerate -m "Add posts and comments"
uv run alembic upgrade head
```

## Testing the API

1. **Start the server**:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

2. **Register a user** at http://localhost:8000/docs

3. **Login** to get an access token

4. **Create a post**:
   ```bash
   curl -X POST http://localhost:8000/posts \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "My First Post", "content": "Hello World!", "published": true}'
   ```

5. **List posts**:
   ```bash
   curl http://localhost:8000/posts
   ```

## Adding Tests

Create `tests/test_posts.py`:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/posts",
        json={"title": "Test Post", "content": "Test content", "published": True},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"

@pytest.mark.asyncio
async def test_list_posts(client: AsyncClient):
    response = await client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Run tests:

```bash
uv run pytest
```

## Next Steps

You now have a working blog API! Here are some ideas to extend it:

- Add post categories/tags
- Implement search functionality
- Add pagination
- Cache popular posts with Redis
- Add rate limiting
- Deploy with Docker

Check out our guides for more:

- [Testing Guide](../guides/testing.md)
- [Caching Configuration](../configuration/caching.md)
- [Docker Deployment](../guides/docker.md)
