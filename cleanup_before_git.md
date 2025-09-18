# 🧹 Cleanup Before Git Upload

This document lists files and directories that should be removed before uploading to Git.

## 🗑️ Files/Directories to Remove

### Virtual Environment
```bash
# Remove the entire virtual environment
rmdir /s /q venv
```

### Build Artifacts
```bash
# Remove build directories
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q agentsiq.egg-info
```

### Logs and Records
```bash
# Remove log files
del agentops.log
rmdir /s /q agentops_records
rmdir /s /q logs
```

### Generated Files
```bash
# Remove generated benchmark files
del agentsiq_benchmark_charts_20250917_132522.png
del benchmark_results_20250917_133133.json
```

### Python Cache
```bash
# Remove Python cache directories
rmdir /s /q agentsiq\__pycache__
rmdir /s /q examples\__pycache__
```

## ✅ Files to Keep

### Core Source Code
- `agentsiq/` (source code)
- `examples/` (example scripts and notebooks)
- `docs/` (documentation)
- `tests/` (test files)

### Configuration Files
- `config.yaml`
- `requirements.txt`
- `setup.py`
- `pyproject.toml`
- `MANIFEST.in`

### Documentation
- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

### Git Files
- `.gitignore`
- `.gitattributes`

## 🚀 Quick Cleanup Commands

### Windows Command Prompt
```cmd
REM Remove virtual environment
rmdir /s /q venv

REM Remove build artifacts
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q agentsiq.egg-info

REM Remove logs and records
del agentops.log
rmdir /s /q agentops_records
rmdir /s /q logs

REM Remove generated files
del agentsiq_benchmark_charts_*.png
del benchmark_results_*.json

REM Remove Python cache
rmdir /s /q agentsiq\__pycache__
rmdir /s /q examples\__pycache__
```

### PowerShell
```powershell
# Remove virtual environment
Remove-Item -Recurse -Force venv

# Remove build artifacts
Remove-Item -Recurse -Force build, dist, agentsiq.egg-info

# Remove logs and records
Remove-Item -Force agentops.log
Remove-Item -Recurse -Force agentops_records, logs

# Remove generated files
Remove-Item -Force agentsiq_benchmark_charts_*.png, benchmark_results_*.json

# Remove Python cache
Remove-Item -Recurse -Force agentsiq\__pycache__, examples\__pycache__
```

## 📋 Pre-Upload Checklist

- [ ] Virtual environment removed
- [ ] Build artifacts removed
- [ ] Log files removed
- [ ] Generated files removed
- [ ] Python cache removed
- [ ] `.gitignore` file created
- [ ] `.gitattributes` file created
- [ ] All source code files present
- [ ] Documentation files present
- [ ] Configuration files present

## 🎯 After Cleanup

Your repository should contain only:
- Source code (`agentsiq/`)
- Examples (`examples/`)
- Documentation (`docs/`)
- Tests (`tests/`)
- Configuration files
- Documentation files
- Git configuration files

Total size should be much smaller and suitable for Git upload!
