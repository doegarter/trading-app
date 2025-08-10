# Trading App

A Python-based day trading application with real-time market data processing and automated trading capabilities.

## Features

- Real-time market data fetching
- Technical analysis tools
- Trading strategy implementation
- Docker containerization
- Azure Container Apps deployment
- GitHub Actions CI/CD pipeline

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Run the application:
```bash
python -m src.main
```

## Development

- `src/` - Main application code
- `tests/` - Unit and integration tests
- `config/` - Configuration files
- `.github/workflows/` - CI/CD pipeline configuration

## Testing

```bash
pytest
```

## Deployment

The application is automatically deployed to Azure Container Apps via GitHub Actions when pushing to the main branch.

## License

MIT
