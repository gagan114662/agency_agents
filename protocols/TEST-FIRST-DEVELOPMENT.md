# Test-First Development Standards

## 🎯 Core Principle

**ALWAYS write tests BEFORE implementing features.** This is non-negotiable for all engineering agents.

## 📋 Test-First Workflow

### 1. Write Tests First
- Write tests that import from actual feature modules (even if they don't exist yet)
- Tests should initially FAIL (Red phase in Red-Green-Refactor)
- Never use hardcoded values or mock final behavior
- Tests define the contract and expected behavior

### 2. Self-Reflect on Tests (MANDATORY)
**After writing tests, ALWAYS reflect on test quality before implementation:**

Review these critical questions:
1. **Coverage**: Does your test suite provide comprehensive coverage of all requirements?
2. **Edge Cases**: Have you tested all edge cases and boundary conditions?
3. **Scenarios**: Are there any scenarios or use cases that are not yet covered?
4. **Quality**: Is the test quality sufficient to catch implementation bugs?
5. **Assertions**: Are the test assertions clear and comprehensive?

**This reflection step is REQUIRED and enforced by the protocol system.**
- Implementation will be blocked until reflection is complete
- Take time to improve tests based on reflection insights
- Document any test gaps or limitations discovered

### 3. Implement Feature
- Write minimal code to make tests pass (Green phase)
- Follow the test specifications exactly
- Implement actual functionality, not shortcuts

### 4. Refactor
- Clean up code while keeping tests passing
- Optimize performance and maintainability
- Tests ensure refactoring doesn't break functionality

## ✅ Test-First Examples by Stack

### JavaScript/TypeScript (Frontend)
```typescript
// tests/components/UserProfile.test.tsx
// Import from actual component location (not yet implemented)
import { UserProfile } from '@/components/UserProfile';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

describe('UserProfile', () => {
  it('should display user information', () => {
    const user = { name: 'John Doe', email: 'john@example.com' };
    render(<UserProfile user={user} />);

    // Test actual rendered output
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should handle edit button click', () => {
    const onEdit = jest.fn();
    render(<UserProfile user={user} onEdit={onEdit} />);

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(onEdit).toHaveBeenCalledWith(user);
  });

  it('should show loading state', () => {
    render(<UserProfile user={null} isLoading={true} />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });
});
```

### Node.js/TypeScript (Backend)
```typescript
// tests/services/UserService.test.ts
// Import from actual service location (not yet implemented)
import { UserService } from '@/services/UserService';
import { describe, it, expect, beforeEach } from 'vitest';

describe('UserService', () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  it('should create user with hashed password', async () => {
    const userData = { email: 'test@example.com', password: 'secret123' };
    const user = await userService.createUser(userData);

    // Test actual implementation behavior
    expect(user.id).toBeDefined();
    expect(user.email).toBe(userData.email);
    expect(user.password_hash).not.toBe(userData.password);
    expect(user.password_hash).toMatch(/^\$2[aby]\$/); // bcrypt format
  });

  it('should throw error for duplicate email', async () => {
    await userService.createUser({ email: 'test@example.com', password: 'pass' });

    await expect(
      userService.createUser({ email: 'test@example.com', password: 'pass2' })
    ).rejects.toThrow('Email already exists');
  });

  it('should validate email format', async () => {
    await expect(
      userService.createUser({ email: 'invalid-email', password: 'pass' })
    ).rejects.toThrow('Invalid email format');
  });
});
```

### Python (Backend/AI)
```python
# tests/test_user_service.py
# Import from actual service location (not yet implemented)
from services.user_service import UserService
import pytest

class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_user_with_hashed_password(self, user_service):
        user_data = {"email": "test@example.com", "password": "secret123"}
        user = user_service.create_user(user_data)

        # Test actual implementation behavior
        assert user['id'] is not None
        assert user['email'] == user_data['email']
        assert user['password_hash'] != user_data['password']
        assert user['password_hash'].startswith('$2b$')  # bcrypt format

    def test_duplicate_email_raises_error(self, user_service):
        user_service.create_user({"email": "test@example.com", "password": "pass"})

        with pytest.raises(ValueError, match="Email already exists"):
            user_service.create_user({"email": "test@example.com", "password": "pass2"})

    def test_validates_email_format(self, user_service):
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user({"email": "invalid-email", "password": "pass"})
```

### Python (Machine Learning)
```python
# tests/test_sentiment_analyzer.py
# Import from actual model location (not yet implemented)
from models.sentiment_analyzer import SentimentAnalyzer
import pytest

class TestSentimentAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return SentimentAnalyzer()

    def test_predicts_positive_sentiment(self, analyzer):
        result = analyzer.predict("This product is amazing!")

        # Test actual model behavior
        assert result['sentiment'] == 'positive'
        assert 0 <= result['confidence'] <= 1
        assert result['confidence'] > 0.7

    def test_predicts_negative_sentiment(self, analyzer):
        result = analyzer.predict("This is terrible and disappointing")

        assert result['sentiment'] == 'negative'
        assert result['confidence'] > 0.7

    def test_handles_empty_input(self, analyzer):
        with pytest.raises(ValueError, match="Input cannot be empty"):
            analyzer.predict("")

    def test_handles_very_long_text(self, analyzer):
        long_text = "word " * 10000
        result = analyzer.predict(long_text)

        assert result['sentiment'] in ['positive', 'negative', 'neutral']
        assert 'confidence' in result

    def test_batch_prediction(self, analyzer):
        texts = ["Great!", "Terrible!", "It's okay"]
        results = analyzer.predict_batch(texts)

        assert len(results) == 3
        assert all('sentiment' in r and 'confidence' in r for r in results)
```

### PHP (Laravel)
```php
// tests/Feature/UserServiceTest.php
<?php

namespace Tests\Feature;

use App\Services\UserService;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserServiceTest extends TestCase
{
    use RefreshDatabase;

    protected UserService $userService;

    protected function setUp(): void
    {
        parent::setUp();
        $this->userService = new UserService();
    }

    public function test_creates_user_with_hashed_password(): void
    {
        $userData = [
            'email' => 'test@example.com',
            'password' => 'secret123'
        ];

        $user = $this->userService->createUser($userData);

        // Test actual implementation behavior
        $this->assertNotNull($user->id);
        $this->assertEquals($userData['email'], $user->email);
        $this->assertNotEquals($userData['password'], $user->password);
        $this->assertTrue(\Hash::check($userData['password'], $user->password));
    }

    public function test_throws_error_for_duplicate_email(): void
    {
        $this->userService->createUser(['email' => 'test@example.com', 'password' => 'pass']);

        $this->expectException(\Exception::class);
        $this->expectExceptionMessage('Email already exists');

        $this->userService->createUser(['email' => 'test@example.com', 'password' => 'pass2']);
    }
}
```

## 🚫 Anti-Patterns to Avoid

### ❌ DON'T: Hardcode Expected Values
```typescript
// BAD - Hardcoded values
it('should return user data', () => {
  const result = getUserData();
  expect(result).toBe({ id: 1, name: 'John' }); // Hardcoded!
});
```

### ✅ DO: Test Real Implementation
```typescript
// GOOD - Testing actual behavior
it('should return user data with valid structure', () => {
  const userId = 1;
  const result = getUserData(userId);

  expect(result).toHaveProperty('id');
  expect(result).toHaveProperty('name');
  expect(typeof result.name).toBe('string');
});
```

### ❌ DON'T: Mock Final Behavior
```typescript
// BAD - Mocking the thing we're testing
jest.mock('@/features/calculator');
const calculator = require('@/features/calculator');
calculator.add.mockReturnValue(5); // This is mocking the implementation!
```

### ✅ DO: Test Against Real Implementation
```typescript
// GOOD - Testing real implementation
import { add } from '@/features/calculator';

it('should add two numbers correctly', () => {
  expect(add(2, 3)).toBe(5);
  expect(add(-1, 1)).toBe(0);
  expect(add(0, 0)).toBe(0);
});
```

## 📊 Test Coverage Requirements

### Minimum Coverage
- **Unit Tests**: Cover all public functions and methods
- **Edge Cases**: Empty inputs, null values, boundary conditions
- **Error Handling**: All error paths and exceptions
- **Integration**: Key user flows and API endpoints

### What to Test
1. **Happy Path**: Normal expected usage
2. **Edge Cases**: Boundary conditions, empty/null inputs
3. **Error Cases**: Invalid inputs, exceptions, failures
4. **Integration**: Component interactions, API calls
5. **Performance**: For critical paths (load time, query speed)
6. **Security**: Authentication, authorization, input validation

## 🎯 Test Frameworks by Stack

### Frontend
- **React**: Jest + React Testing Library + Vitest
- **Vue**: Vitest + Vue Test Utils
- **Angular**: Jasmine + Karma
- **E2E**: Cypress, Playwright

### Backend
- **Node.js**: Jest, Vitest, Mocha
- **Python**: pytest, unittest
- **PHP**: PHPUnit, Pest
- **Go**: testing package
- **Ruby**: RSpec

### Mobile
- **React Native**: Jest + React Native Testing Library
- **iOS**: XCTest
- **Android**: JUnit + Espresso

### AI/ML
- **Python**: pytest + pytest-ml
- **Model Testing**: MLflow, TensorFlow Testing
- **Data Validation**: Great Expectations

## 🔄 Test-Driven Development Cycle

1. **RED**: Write a failing test
   - Test should fail because feature doesn't exist
   - Verify the test actually fails

2. **REFLECT**: Self-assess test quality (MANDATORY)
   - Review test coverage and edge cases
   - Check for missing scenarios
   - Improve tests based on reflection
   - Mark reflection complete in protocol system

3. **GREEN**: Write minimal code to pass
   - Implement just enough to make test pass
   - Don't over-engineer

4. **REFACTOR**: Improve code quality
   - Clean up implementation
   - Optimize performance
   - Ensure tests still pass

5. **REPEAT**: For each new feature

## 💡 Benefits of Test-First Development

1. **Clear Requirements**: Tests document what the feature should do
2. **Better Design**: Writing tests first leads to more testable code
3. **Confidence**: Refactor safely knowing tests will catch breaks
4. **No Dead Code**: Only write code needed to pass tests
5. **Living Documentation**: Tests show how to use the code
6. **Faster Debugging**: Tests isolate problems quickly
7. **Regression Prevention**: Tests catch bugs when they're introduced
8. **Quality Assurance**: Self-reflection catches test gaps before implementation

## 🎓 Remember

- Tests are **specifications** of behavior, not afterthoughts
- Tests should **document** how features work
- Tests should **fail first**, then pass after implementation
- Tests should verify **real behavior**, not hardcoded values
- Tests are **living documentation** that never goes stale
- **Self-reflection on tests is MANDATORY** before implementation

---

**All engineering agents MUST follow these test-first development standards, including the mandatory self-reflection step.**
