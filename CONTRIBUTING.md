# Contributing to English-words

## Development Workflow

### Setting up the dev branch

To contribute to this project, you should track the `dev` branch for development work:

```bash
# Clone the repository
git clone https://github.com/hypatia-tile/English-words.git
cd English-words

# Create and track the dev branch
git checkout -b dev origin/dev

# Or if dev branch doesn't exist yet locally
git fetch origin
git checkout --track origin/dev
```

### Branch Guidelines

- **main branch**: Contains stable, production-ready code
- **dev branch**: Active development happens here. Track this branch for your development work.

### Making Changes

1. Ensure you're on the dev branch: `git checkout dev`
2. Pull the latest changes: `git pull origin dev`
3. Create a feature branch from dev: `git checkout -b feature/your-feature-name`
4. Make your changes and commit them
5. Push your feature branch and create a pull request targeting the `dev` branch
