# Example Project Guidelines Skill

这是项目级 Skill 的完整示例，用于展示章节组织方式。示例内容基于一个虚构/示例化的生产应用形态；创建真实项目 Skill 时必须替换所有事实。

## Example Overview

示例项目：AI-powered customer discovery platform。

Tech stack:

- Frontend: Next.js 15, App Router, TypeScript, React
- Backend: FastAPI, Python, Pydantic models
- Database: Supabase PostgreSQL
- AI: Claude API with tool calling and structured output
- Deployment: Google Cloud Run
- Testing: Playwright, pytest, React Testing Library

Services:

```text
Frontend
  Next.js 15 + TypeScript + TailwindCSS
        |
        v
Backend
  FastAPI + Python 3.11 + Pydantic
        |
        +-- Supabase
        +-- Claude API
        +-- Redis
```

## File Structure

```text
project/
  frontend/
    src/
      app/
        api/
        (auth)/
        workspace/
      components/
        ui/
        forms/
        layouts/
      hooks/
      lib/
      types/
      config/
  backend/
    routers/
    models.py
    main.py
    auth_system.py
    database.py
    services/
    tests/
  deploy/
  docs/
  scripts/
```

## Code Patterns

### API Response Format

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: T) -> "ApiResponse[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "ApiResponse[T]":
        return cls(success=False, error=error)
```

### Frontend API Calls

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`/api${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      return { success: false, error: `HTTP ${response.status}` }
    }

    return await response.json()
  } catch (error) {
    return { success: false, error: String(error) }
  }
}
```

### Structured AI Output

```python
from anthropic import Anthropic
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

async def analyze_with_claude(content: str) -> AnalysisResult:
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}],
        tools=[{
            "name": "provide_analysis",
            "description": "Provide structured analysis",
            "input_schema": AnalysisResult.model_json_schema(),
        }],
        tool_choice={"type": "tool", "name": "provide_analysis"},
    )

    tool_use = next(
        block for block in response.content
        if block.type == "tool_use"
    )

    return AnalysisResult(**tool_use.input)
```

### Custom Hooks

```typescript
import { useState, useCallback } from 'react'

interface UseApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useApi<T>(fetchFn: () => Promise<ApiResponse<T>>) {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  })

  const execute = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))

    const result = await fetchFn()

    if (result.success) {
      setState({ data: result.data!, loading: false, error: null })
    } else {
      setState({ data: null, loading: false, error: result.error! })
    }
  }, [fetchFn])

  return { ...state, execute }
}
```

## Testing Requirements

Backend:

```bash
poetry run pytest tests/
poetry run pytest tests/ --cov=. --cov-report=html
poetry run pytest tests/test_auth.py -v
```

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

Frontend:

```bash
npm run test
npm run test -- --coverage
npm run test:e2e
```

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { WorkspacePanel } from './WorkspacePanel'

describe('WorkspacePanel', () => {
  it('renders workspace correctly', () => {
    render(<WorkspacePanel />)
    expect(screen.getByRole('main')).toBeInTheDocument()
  })

  it('handles session creation', async () => {
    render(<WorkspacePanel />)
    fireEvent.click(screen.getByText('New Session'))
    expect(await screen.findByText('Session created')).toBeInTheDocument()
  })
})
```

## Deployment Workflow

Pre-deployment checklist:

- All tests passing locally
- Frontend build succeeds
- Backend tests pass
- No hardcoded secrets
- Environment variables documented
- Database migrations ready

Deployment commands:

```bash
cd frontend && npm run build
gcloud run deploy frontend --source .

cd backend
gcloud run deploy backend --source .
```

Environment variables:

```bash
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<supabase-anon-key>

DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=<anthropic-api-key>
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=<supabase-service-key>
```

## Critical Rules

1. No emojis in code, comments, or documentation.
2. Never mutate objects or arrays unless a performance exception is explicit.
3. Write or update tests for behavior changes.
4. Keep files small enough to review; split by real responsibility.
5. No `console.log` in production code.
6. Use proper error handling with `try` / `catch` or framework-native error boundaries.
7. Validate inputs with Pydantic, Zod, or the project's existing schema layer.

## Related Skills

- `coding-standards` for general coding best practices.
- `backend-patterns` for API and database patterns.
- `frontend-patterns` for React and Next.js patterns.
- `tdd-workflow` for test-driven development.
