# Contributing to DockPilot

Thank you for considering contributing to DockPilot! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites
- Docker Engine >= 24.x
- Docker Compose v2
- Node.js >= 20.x
- Python >= 3.11
- Git

### Local Development

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/DockPilot.git
cd DockPilot
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

3. **Frontend setup**
```bash
cd frontend
npm install
cp .env.example .env.local
```

4. **Run development servers**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 48391
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use `structlog` for logging
- Write docstrings for all public functions

Example:
```python
async def get_app_stats(app_id: str) -> Dict[str, Any]:
    """
    Get resource usage statistics for an application.

    Args:
        app_id: The unique identifier of the application

    Returns:
        Dictionary containing app statistics
    """
    # Implementation
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow Airbnb style guide
- Use functional components with hooks
- Props should be typed with interfaces
- Use Tailwind CSS for styling

Example:
```typescript
interface AppCardProps {
  app: ComposeApp
  onAction: (appId: string, action: string) => void
}

export function AppCard({ app, onAction }: AppCardProps) {
  // Implementation
}
```

## Commit Messages

Follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add real-time log streaming
fix: resolve Docker socket permission issue
docs: update installation instructions
```

## Pull Request Process

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write clean, readable code
- Add tests if applicable
- Update documentation

3. **Test your changes**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration test
docker-compose up -d
```

4. **Commit and push**
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

5. **Open a Pull Request**
- Provide a clear description of changes
- Reference any related issues
- Ensure CI checks pass

## Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

## Documentation

- Update README.md for user-facing changes
- Update code comments for developer-facing changes
- Add JSDoc/docstrings for new functions
- Update API documentation if endpoints change

## Issue Reporting

When reporting bugs, include:
- OS and version
- Docker version
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs

Use this template:
```markdown
**Environment:**
- OS: macOS 14.0 / Ubuntu 22.04
- Docker: 24.0.0
- DockPilot: v1.0.0

**Steps to Reproduce:**
1. Start DockPilot
2. Click "Discover Apps"
3. ...

**Expected Behavior:**
Apps should be discovered and listed

**Actual Behavior:**
Error message appears

**Logs:**
```
[paste relevant logs]
```
```

## Feature Requests

Feature requests are welcome! Please:
- Search existing issues first
- Provide clear use case
- Explain expected behavior
- Consider implementation complexity

## Code Review

All PRs require review. Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Security considerations
- Performance impact

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for questions or join discussions.

Thank you for contributing! 🎉
