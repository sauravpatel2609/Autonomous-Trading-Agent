# Contributing to AI Trading Agent

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/your-username/your-repo/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/your-username/your-repo/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### Setting up the development environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/sauravpatel2609/Autonomous-Trading-Agent.git
   cd Autonomous-Trading-Agent
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv trading-agent-env
   source trading-agent-env/bin/activate  # Linux/Mac
   # trading-agent-env\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd agent-stock-frontend
   npm install
   ```

4. **Environment configuration**
   - Create `.env` file in `backend/` directory
   - Add your Alpaca API keys (paper trading)
   - See README.md for full configuration details

### Coding Standards

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Use meaningful variable and function names

Example:
```python
def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """
    Calculate Relative Strength Index (RSI) for given prices.
    
    Args:
        prices: List of price values
        period: RSI calculation period (default: 14)
        
    Returns:
        RSI value between 0 and 100
    """
    # Implementation here
    pass
```

#### TypeScript (Frontend)
- Use TypeScript strict mode
- Define interfaces for all data structures
- Use meaningful component and variable names
- Follow React best practices

Example:
```typescript
interface StockData {
  symbol: string;
  price: number;
  timestamp: Date;
}

const StockChart: React.FC<{ data: StockData[] }> = ({ data }) => {
  // Component implementation
};
```

### Testing Guidelines

#### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest --cov=src tests/  # With coverage
```

#### Frontend Tests
```bash
cd agent-stock-frontend
npm test
npm run test:e2e  # End-to-end tests
```

### Commit Message Format

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring
- `style:` formatting changes

Examples:
```
feat: add RSI indicator to prediction model
fix: resolve WebSocket connection timeout issue
docs: update API documentation for new endpoints
test: add unit tests for trading agent
```

## Feature Requests

We're always looking for suggestions to improve this project. If you have an idea:

1. Check if the feature has already been requested
2. Open a new issue with the "enhancement" label
3. Describe the feature in detail
4. Explain why it would be useful
5. Consider submitting a pull request if you can implement it

## Areas Where We Need Help

- **Machine Learning**: Improving prediction models
- **Frontend UI/UX**: Enhancing user interface
- **Testing**: Increasing test coverage
- **Documentation**: Improving guides and examples
- **Security**: Code reviews and security audits
- **Performance**: Optimization and profiling

## Code Review Process

1. All submissions require review before merging
2. We'll review your code for:
   - Functionality and correctness
   - Code style and conventions
   - Test coverage
   - Documentation updates
   - Security considerations

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Constructive feedback is always welcome
- Focus on the code, not the person

## Getting Help

- Check existing issues and discussions on [GitHub](https://github.com/sauravpatel2609/Autonomous-Trading-Agent/issues)
- Join our community discussions
- Ask questions in issues or pull requests
- Contact maintainer: sauravpatel90768@gmail.com

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

Thank you for contributing! 
