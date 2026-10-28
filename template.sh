
#!/usr/bin/env bash

set -e

echo "Creating FinAssist AI project structure..."

# 1. Application source code
mkdir -p src/finassist/api/routes
mkdir -p src/finassist/agents
mkdir -p src/finassist/rag
mkdir -p src/finassist/guardrails
mkdir -p src/finassist/database
mkdir -p src/finassist/evaluation
mkdir -p src/finassist/utils

# 2. Configuration
mkdir -p config/guardrails

# 3. Tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/evaluation
mkdir -p tests/security

# 4. Data directories
mkdir -p data/sample_documents
mkdir -p data/processed
mkdir -p data/chroma_db

# 5. Scripts and documentation
mkdir -p scripts
mkdir -p docs

# 6. Docker and deployment
mkdir -p docker

# 7. GitHub Actions CI/CD
mkdir -p .github/workflows

# 8. Python package files
files=(
    "src/finassist/__init__.py"
    "src/finassist/api/__init__.py"
    "src/finassist/api/main.py"
    "src/finassist/api/routes/__init__.py"
    "src/finassist/api/routes/health.py"
    "src/finassist/api/routes/chat.py"
    "src/finassist/api/routes/documents.py"

    "src/finassist/agents/__init__.py"
    "src/finassist/agents/state.py"
    "src/finassist/agents/graph.py"
    "src/finassist/agents/nodes.py"
    "src/finassist/agents/tools.py"

    "src/finassist/rag/__init__.py"
    "src/finassist/rag/loader.py"
    "src/finassist/rag/chunker.py"
    "src/finassist/rag/embeddings.py"
    "src/finassist/rag/retriever.py"
    "src/finassist/rag/chain.py"

    "src/finassist/guardrails/__init__.py"
    "src/finassist/guardrails/input_checks.py"
    "src/finassist/guardrails/output_checks.py"
    "src/finassist/guardrails/authorization.py"

    "src/finassist/database/__init__.py"
    "src/finassist/database/connection.py"
    "src/finassist/database/models.py"
    "src/finassist/database/repository.py"

    "src/finassist/evaluation/__init__.py"
    "src/finassist/evaluation/rag_metrics.py"
    "src/finassist/evaluation/agent_metrics.py"

    "src/finassist/utils/__init__.py"
    "src/finassist/utils/config.py"
    "src/finassist/utils/logging.py"

    "tests/unit/test_agents.py"
    "tests/unit/test_rag.py"
    "tests/unit/test_guardrails.py"
    "tests/unit/test_database.py"
    "tests/integration/test_api.py"
    "tests/evaluation/test_rag_evaluation.py"
    "tests/evaluation/test_agent_evaluation.py"
    "tests/security/test_prompt_injection.py"
    "tests/security/test_authorization.py"

    "config/guardrails/config.yml"
    "scripts/seed_database.py"
    "scripts/ingest_documents.py"
    "scripts/run_evaluation.py"

    "docs/architecture.md"
    "docs/evaluation_strategy.md"
    "docs/security.md"

    ".github/workflows/ci.yml"
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    ".gitignore"
    ".env.example"
    "README.md"
    "requirements.txt"
    "pytest.ini"
    "pyproject.toml"
)

# Create files only when they do not already exist.
for file in "${files[@]}"; do
    if [ ! -e "$file" ]; then
        touch "$file"
        echo "Created: $file"
    else
        echo "Already exists, preserving: $file"
    fi
done

# Add placeholders so Git tracks empty directories.
touch data/sample_documents/.gitkeep
touch data/processed/.gitkeep

# Keep local databases and secrets out of Git.
if [ ! -s ".gitignore" ]; then
    cat > .gitignore <<'EOF'
# Secrets
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Conda and local environments
conda-meta/

# Local data and vector databases
data/processed/*
!data/processed/.gitkeep
data/chroma_db/
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# IDE and operating system
.vscode/
.idea/
.DS_Store
Thumbs.db
EOF
    echo "Added default .gitignore rules."
fi

# Add example environment variables without real credentials.
if [ ! -s ".env.example" ]; then
    cat > .env.example <<'EOF'
# LLM provider
GROQ_API_KEY=

# PostgreSQL
DATABASE_URL=postgresql+psycopg://finassist:change_me@localhost:5432/finassist

# Application
APP_ENV=development
LOG_LEVEL=INFO

# Optional: LangSmith tracing
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=finassist-ai
EOF
    echo "Added example environment variables."
fi

echo ""
echo "FinAssist AI folder structure created successfully!"
echo "Next: inspect the structure and configure the project files."
