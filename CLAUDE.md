# CLAUDE.md - AI Assistant Guide for penta-cs-agent

**Last Updated:** 2025-12-02
**Repository:** jgavin-eng/penta-cs-agent
**Purpose:** AI agent for Penta CS operations

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Current State](#current-state)
3. [Project Structure](#project-structure)
4. [Development Workflows](#development-workflows)
5. [Git Conventions](#git-conventions)
6. [Code Conventions](#code-conventions)
7. [Testing Guidelines](#testing-guidelines)
8. [AI Assistant Guidelines](#ai-assistant-guidelines)
9. [Common Tasks](#common-tasks)

---

## Repository Overview

This repository contains the **Penta CS Agent** - an AI-powered agent system designed for customer service or computer science operations within the Penta ecosystem.

### Key Information
- **Repository Name:** penta-cs-agent
- **Owner:** jgavin-eng
- **Current Branch:** claude/claude-md-mip4vfcm0v5varlq-012xZZcn7oKok5uYAveFwnES
- **Git Remote:** http://local_proxy@127.0.0.1:38265/git/jgavin-eng/penta-cs-agent

---

## Current State

**Status:** Initial repository setup phase

The repository is currently in its early stages with minimal content:
- Basic README.md (empty)
- Git infrastructure initialized
- No source code files yet
- No configuration files yet
- No dependencies defined

This CLAUDE.md file serves as the foundational documentation for AI assistants working with this codebase.

---

## Project Structure

### Recommended Directory Layout

As this project develops, consider organizing it as follows:

```
penta-cs-agent/
├── .git/                    # Git repository data
├── .github/                 # GitHub Actions, templates, etc.
│   └── workflows/          # CI/CD workflows
├── src/                    # Source code
│   ├── agent/             # Agent core logic
│   ├── handlers/          # Request/event handlers
│   ├── integrations/      # External service integrations
│   ├── utils/             # Utility functions
│   └── config/            # Configuration management
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test fixtures and mocks
├── docs/                   # Documentation
│   ├── architecture.md    # System architecture
│   ├── api.md            # API documentation
│   └── deployment.md     # Deployment guide
├── scripts/               # Build and deployment scripts
├── config/                # Configuration files
├── .gitignore            # Git ignore patterns
├── README.md             # Project README
├── CLAUDE.md             # This file - AI assistant guide
├── LICENSE               # License file
└── package.json          # Node.js dependencies (if applicable)
```

---

## Development Workflows

### Initial Setup

When setting up the development environment:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd penta-cs-agent
   ```

2. **Install dependencies** (once package manager is chosen):
   ```bash
   # For Node.js projects
   npm install

   # For Python projects
   pip install -r requirements.txt

   # For other languages, adapt accordingly
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` (once created)
   - Configure necessary API keys and secrets

### Feature Development

1. **Create a feature branch:**
   ```bash
   git checkout -b claude/<session-id>
   ```

2. **Make changes and commit frequently:**
   ```bash
   git add <files>
   git commit -m "feat: descriptive message"
   ```

3. **Push to remote:**
   ```bash
   git push -u origin <branch-name>
   ```

4. **Create a pull request** for review

---

## Git Conventions

### Branch Naming

- **Feature branches:** `claude/<session-id>` (for Claude AI development)
- **Feature branches (human):** `feature/<feature-name>`
- **Bug fixes:** `fix/<bug-description>`
- **Hotfixes:** `hotfix/<issue>`
- **Documentation:** `docs/<topic>`

### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```
feat(agent): add natural language processing capability

fix(handler): resolve timeout issue in request processing

docs(readme): update installation instructions

refactor(utils): simplify error handling logic
```

### Git Push Policy

- Always use `git push -u origin <branch-name>`
- Branch names must start with `claude/` and end with session ID for AI branches
- Retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s) on network errors
- Never force push to main/master without explicit permission

---

## Code Conventions

### General Principles

1. **Keep it simple:** Avoid over-engineering
2. **Make changes focused:** Only modify what's necessary
3. **Write self-documenting code:** Use clear variable and function names
4. **Add comments only when necessary:** When logic isn't self-evident
5. **Security first:** Avoid vulnerabilities (XSS, SQL injection, command injection, etc.)

### Code Style

*To be defined based on chosen programming language and team preferences*

**Recommended practices:**
- Use consistent indentation (spaces vs tabs - to be decided)
- Maximum line length: 100-120 characters
- Use meaningful variable names
- Keep functions small and focused
- Follow DRY (Don't Repeat Yourself) principle
- Write testable code

### Error Handling

- Validate input at system boundaries (user input, external APIs)
- Trust internal code and framework guarantees
- Don't add error handling for scenarios that can't happen
- Provide meaningful error messages
- Log errors appropriately for debugging

### Security Considerations

Always check for:
- **Input validation:** Sanitize user inputs
- **Authentication:** Verify user identity
- **Authorization:** Check user permissions
- **Data encryption:** Protect sensitive data
- **API security:** Secure API endpoints
- **Dependency vulnerabilities:** Keep dependencies updated

---

## Testing Guidelines

### Test Organization

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with external dependencies
└── e2e/           # End-to-end tests
```

### Testing Principles

1. **Write tests for new features:** Every new feature should have tests
2. **Write tests for bug fixes:** Prevent regression
3. **Keep tests isolated:** Each test should be independent
4. **Use descriptive test names:** Clearly state what is being tested
5. **Follow AAA pattern:** Arrange, Act, Assert

### Running Tests

*To be defined based on chosen testing framework*

```bash
# Example commands (adapt as needed)
npm test                 # Run all tests
npm test -- --watch     # Run tests in watch mode
npm run test:coverage   # Generate coverage report
```

---

## AI Assistant Guidelines

### Core Responsibilities

As an AI assistant working with this codebase:

1. **Understand before modifying:** Always read code before suggesting changes
2. **Use TodoWrite tool:** Track tasks and progress
3. **Follow conventions:** Adhere to established patterns and styles
4. **Test your changes:** Verify functionality before committing
5. **Document as needed:** Update documentation when adding features
6. **Security awareness:** Check for vulnerabilities in your code
7. **Commit regularly:** Make atomic commits with clear messages

### Before Starting Work

1. Check if similar functionality exists
2. Read relevant documentation
3. Understand the current implementation
4. Plan your approach using TodoWrite tool
5. Identify potential impacts on existing code

### During Development

1. Make focused, minimal changes
2. Avoid adding unnecessary features
3. Don't refactor unrelated code
4. Follow existing code patterns
5. Write clear commit messages
6. Test your changes

### After Completing Work

1. Review your changes for security issues
2. Ensure tests pass
3. Update documentation if needed
4. Commit and push your changes
5. Mark tasks as completed in todo list

### What NOT to Do

- Don't make changes to code you haven't read
- Don't add features beyond what was requested
- Don't over-engineer solutions
- Don't add premature abstractions
- Don't skip testing critical functionality
- Don't commit secrets or sensitive data
- Don't force push without explicit permission

---

## Common Tasks

### Adding a New Feature

1. Create todo list with feature tasks
2. Research existing codebase for similar patterns
3. Implement the feature incrementally
4. Write tests for the new feature
5. Update documentation
6. Commit and push changes

### Fixing a Bug

1. Reproduce the bug
2. Identify the root cause
3. Write a test that fails due to the bug
4. Fix the bug
5. Verify the test now passes
6. Commit the fix with a descriptive message

### Refactoring Code

1. Ensure tests exist for the code to be refactored
2. Make small, incremental changes
3. Run tests after each change
4. Commit each successful refactoring step
5. Update documentation if interfaces changed

### Updating Dependencies

1. Check for security vulnerabilities
2. Review changelog for breaking changes
3. Update dependency versions
4. Run full test suite
5. Fix any breaking changes
6. Commit the updates

### Writing Documentation

1. Use clear, concise language
2. Provide examples where helpful
3. Keep documentation in sync with code
4. Update CLAUDE.md when workflows change
5. Add inline comments only when necessary

---

## Project-Specific Notes

### Current Development Phase

This is a **greenfield project** - you have the opportunity to:

1. **Choose the tech stack:** Select appropriate languages and frameworks
2. **Define architecture:** Design the agent system architecture
3. **Set up CI/CD:** Implement automated testing and deployment
4. **Establish conventions:** Create coding standards and workflows
5. **Build incrementally:** Start with core functionality

### Recommended Next Steps

1. **Define project requirements:**
   - What problems does this agent solve?
   - Who are the users/stakeholders?
   - What are the key features needed?

2. **Choose technology stack:**
   - Programming language (Python, Node.js, Go, etc.)
   - Frameworks and libraries
   - Database and storage solutions
   - Deployment platform

3. **Set up project infrastructure:**
   - Package manager configuration
   - Linting and formatting tools
   - Testing framework
   - CI/CD pipeline
   - Development environment setup

4. **Create initial architecture:**
   - Core agent logic
   - API/interface design
   - Data models
   - Integration points

5. **Implement MVP features:**
   - Start with minimal viable product
   - Iterate based on feedback
   - Add features incrementally

---

## Resources

### Documentation Standards

- Use Markdown for all documentation
- Keep README.md updated with project overview
- Document APIs using appropriate standards (OpenAPI, JSDoc, etc.)
- Include examples in documentation

### Useful Commands Reference

```bash
# Git operations
git status                          # Check working tree status
git diff                           # View changes
git log --oneline -10             # View recent commits
git branch                         # List branches
git fetch origin <branch>         # Fetch specific branch
git pull origin <branch>          # Pull specific branch

# Development (examples - adapt to your stack)
npm run dev                        # Start development server
npm run build                      # Build for production
npm run lint                       # Run linter
npm test                          # Run tests
```

---

## Questions or Issues?

When encountering issues:

1. Check existing documentation
2. Review recent commits for context
3. Search for similar problems in the codebase
4. Ask clarifying questions before making assumptions
5. Document solutions for future reference

---

## Maintenance

This CLAUDE.md file should be updated whenever:

- Project structure changes significantly
- New conventions are established
- Development workflows are modified
- New tools or frameworks are adopted
- Lessons are learned from development

**Remember:** Keep this file as a living document that evolves with the project.
