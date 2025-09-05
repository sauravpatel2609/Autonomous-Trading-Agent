# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The AI Trading Agent team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### Where to Report

Please report security vulnerabilities by emailing us directly at:
**sauravpatel90768@gmail.com**

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

To help us better understand the nature and scope of the issue, please include as much of the following information as possible:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

### Response Timeline

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Regular Updates**: We will provide regular updates on our progress every 5 business days
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days

## Security Considerations

### API Security
- All API endpoints use JWT authentication
- Sensitive data is never logged
- API keys are stored securely in environment variables
- Rate limiting is implemented to prevent abuse

### Trading Security
- **Paper Trading Only**: System is configured for paper trading by default
- **API Key Protection**: Alpaca API keys should never be committed to code
- **Access Control**: User-specific portfolio and trade data access
- **Input Validation**: All user inputs are validated and sanitized

### Data Protection
- Passwords are hashed using bcrypt
- JWT tokens have configurable expiration times
- Database connections use secure authentication
- No sensitive data is stored in browser local storage

### Infrastructure Security
- Docker containers run with non-root users
- Environment variables are used for all secrets
- CORS is properly configured
- HTTPS should be used in production

## Best Practices for Contributors

### Secure Coding Guidelines

1. **Never commit secrets**
   - Use environment variables for API keys
   - Add sensitive files to .gitignore
   - Use tools like git-secrets to prevent accidental commits

2. **Input Validation**
   - Validate all user inputs
   - Use Pydantic models for API validation
   - Sanitize data before database operations

3. **Authentication & Authorization**
   - Always verify JWT tokens on protected endpoints
   - Implement proper RBAC (Role-Based Access Control)
   - Use secure session management

4. **Dependencies**
   - Keep dependencies up to date
   - Regularly audit for known vulnerabilities
   - Use tools like `npm audit` and `safety` for Python

### Development Security Checklist

- [ ] Environment variables for all secrets
- [ ] Input validation on all endpoints
- [ ] Proper error handling (don't leak sensitive info)
- [ ] HTTPS in production
- [ ] Regular dependency updates
- [ ] Authentication on protected routes
- [ ] CORS configuration
- [ ] Rate limiting implementation
- [ ] Secure database connections
- [ ] Proper logging (no sensitive data)

## Known Security Considerations

### Trading Risks
- **Market Risk**: Algorithmic trading can result in financial losses
- **API Limitations**: Alpaca API has rate limits and restrictions
- **Model Risk**: ML predictions are not guaranteed to be accurate
- **System Risk**: Technical failures could impact trading

### Mitigation Strategies
- Use paper trading for testing
- Implement position sizing and risk management
- Monitor system health and performance
- Have manual override capabilities
- Regular backtesting and model validation

## Third-Party Dependencies

We regularly monitor and update our dependencies for security vulnerabilities:

### Backend Dependencies
- FastAPI: Web framework security
- TensorFlow: ML model security
- Alpaca-py: Trading API client security
- PyMongo: Database driver security

### Frontend Dependencies
- React: Frontend framework security
- Vite: Build tool security
- Axios: HTTP client security

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [React Security](https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml)
- [Docker Security](https://docs.docker.com/engine/security/)

## Contact

For any security-related questions or concerns, please contact:
- **Email**: sauravpatel90768@gmail.com
- **Project Issues**: [GitHub Issues](https://github.com/sauravpatel2609/Autonomous-Trading-Agent/issues) (for non-security issues only)

Thank you for helping keep AI Trading Agent and our users safe!
