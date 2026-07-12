# CONTRIBUTING - QuantumPilot AI

## Principles
Clean Architecture, DDD, SOLID, Repository Pattern, CQRS, DI, Event Driven, Production Ready, Research Grade

## Code Quality (Enforced by CI)
- Black formatting
- isort import sorting
- ruff lint
- pytest unit + integration + e2e
- Type Hints, Docstrings, Logging, Error Handling, Validation

## Workflow
1. Fork + Branch from develop
2. Implement feature with:
   - Domain Entity in backend/app/domain/entities/
   - UseCase in application/use_cases/
   - Repository in infrastructure/
   - API route in presentation/api/v1/
   - Tests in tests/unit and integration
3. Run: black backend/ && isort backend/ && ruff check backend/ && pytest
4. Update docs: CHANGELOG.md, Tasks.md, Completed.md, ARCHITECTURE.md if needed
5. PR to develop, CI must pass 5 jobs: lint, test, docker-build-test, security-scan, docs-check, research-validation

## Adding New Mitigation Strategy
- Add to backend/app/domain/services/mitigation.py MitigationStrategy subclass with mitigate() + cost_overhead
- Add to MitiqAdapter if Mitiq supports it
- Add to ProductionMitigationFactory comparison
- Add to frontend MitigationChart
- Update ERROR_MITIGATION.md

## Adding New Dataset
- Pull to datasets/ via scripts/pull_datasets.py
- Add to backend/app/infrastructure/qiskit/backend_repository.py get_* method
- Add aggregated view for NeuralUCB context
- Update DATASETS_EVAL.md decision matrix

## Adding New Intent for Copilot
- Add pattern to CopilotIntentAgent.patterns dict in copilot_agent.py (Arabic + English regex)
- Add weight logic in build_plan()
- Add example to /copilot/examples endpoint
- Add button to CopilotChat.tsx frontend

## Research Contributions
- Document in research/ + docs/NEURALUCB.md, ERROR_MITIGATION.md, etc.
- Include Mermaid diagrams
- Reference related work: Q-LEAR, Mitiq, S-ZNE, NNAS, QNTK-UCB, Space Weather correlation

## Security
- Never commit IBM_TOKEN, IBM_CRN, HF_TOKEN - use .env.example
- JWT for auth, SECRET_KEY 32 chars
- Bandit scan in CI
- Gitleaks for secrets
