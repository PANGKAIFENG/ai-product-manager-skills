# Engineering Rules Reference

按需加载本文件。主入口只保留触发条件、交付物和验收标准；这里保留更细的工程规则、示例和 review 检查项。

## TypeScript / JavaScript

### Naming

```typescript
// Good: descriptive names
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// Bad: unclear names
const q = 'election'
const flag = true
const x = 1000
```

函数名优先使用 verb-noun pattern：

```typescript
async function fetchMarketData(marketId: string) {}
function calculateSimilarity(a: number[], b: number[]) {}
function isValidEmail(email: string): boolean {}
```

### Immutable Updates

```typescript
const updatedUser = {
  ...user,
  name: 'New Name',
}

const updatedArray = [...items, newItem]
```

避免直接改对象和数组：

```typescript
user.name = 'New Name'
items.push(newItem)
```

### Error Handling

```typescript
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}
```

### Async / Await

可以并行时不要串行：

```typescript
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats(),
])
```

### Type Safety

```typescript
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  createdAt: Date
}

function getMarket(id: string): Promise<Market> {
  // Implementation
}
```

避免用 `any` 把类型问题后移到运行时。

## React

### Component Props

```typescript
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary',
}: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled} className={`btn btn-${variant}`}>
      {children}
    </button>
  )
}
```

### Custom Hooks

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}
```

### State Updates

当新状态依赖旧状态时使用 functional update：

```typescript
setCount(prev => prev + 1)
```

### Conditional Rendering

优先写清晰分支，避免嵌套三元表达式：

```tsx
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}
```

## API Design

### REST Conventions

```text
GET    /api/markets
GET    /api/markets/:id
POST   /api/markets
PUT    /api/markets/:id
PATCH  /api/markets/:id
DELETE /api/markets/:id
```

### Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}
```

### Input Validation

```typescript
import { z } from 'zod'

const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1),
})
```

## File Organization

```text
src/
  app/
    api/
    markets/
    (auth)/
  components/
    ui/
    forms/
    layouts/
  hooks/
  lib/
    api/
    utils/
    constants/
  types/
  styles/
```

Naming guide:

```text
components/Button.tsx
hooks/useAuth.ts
lib/formatDate.ts
types/market.types.ts
```

## Comments And Documentation

注释解释 why，不重复 what：

```typescript
// Use exponential backoff to avoid overwhelming the API during outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)
```

公共 API 用 JSDoc 说明参数、返回、错误和示例；内部代码优先通过命名和结构自解释。

## Performance

- 对昂贵计算使用 `useMemo`。
- 对传给子组件或 effect 依赖的回调用 `useCallback`，但不要无差别 memoize。
- 大组件或低频路径用 lazy loading。
- 数据库查询只选择需要的列，避免默认 `select('*')`。

## Testing

使用 AAA pattern：

```typescript
test('calculates similarity correctly', () => {
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  const similarity = calculateCosineSimilarity(vector1, vector2)

  expect(similarity).toBe(0)
})
```

测试名描述行为：

```typescript
test('returns empty array when no markets match query', () => {})
test('throws error when OpenAI API key is missing', () => {})
test('falls back to substring search when Redis unavailable', () => {})
```

## Code Smells

### Long Functions

超过 50 行的函数优先检查是否混合了验证、转换、持久化、渲染或副作用。拆分时以真实职责边界为准，不为行数本身机械拆分。

### Deep Nesting

优先用 early return 降低缩进：

```typescript
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return
```

### Magic Numbers

```typescript
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500
```

### Over-Engineering

常见信号：

- 为单一调用点建立通用框架。
- 为未来可能需求提前引入 plugin、registry、factory。
- 抽象层不减少重复，也不隔离真实变化点。
- 为了“规范”迁移大量无关目录。
