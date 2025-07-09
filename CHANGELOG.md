# Changelog

## 3.12 - 2025-07-10

### Added
- **Automated setup script (`setup_dev.sh`)**: One command environment setup.
- **Cross-platform WebView handling**: Desktop testing + Android production.
- **Intelligent fallbacks**: Graceful degradation when dependencies missing.
- **Professional error messages**: Clear guidance for users.
- **Comprehensive requirements management**: Three-tier dependency system.
- **Professional .gitignore**: Excludes all build artifacts and sensitive files.
- **Optimized buildozer.spec**: Faster builds with smart exclusions.
- **Build log management**: Automatic cleanup and organization.
- **Enhanced GitHub Actions**: Added missing setuptools dependency.
- **Python version optimization**: Changed to 3.11 for better compatibility.
- **Improved error handling**: Better diagnosis of build failures.

### Fixed
- **Critical Python Compatibility Issues**:
  - Python 3.13 distutils `ModuleNotFoundError` resolved.
  - Missing Cython compilation failure resolved.
  - Version mismatches leading to unpredictable builds resolved.
- **Import & Dependency Conflicts**:
  - WebView imports name conflicts resolved.
  - Android imports loaded unconditionally resolved.
  - Missing requirements resolved with comprehensive `requirements.txt`.
- **Configuration Inconsistencies**:
  - `buildozer.spec` python vs python3 standardization.
  - `manifest.json` version synchronization.
  - Missing zlib in demo requirements added.
- **Missing Assets & Files**:
  - Icon files referenced but missing created.
  - `requirements.txt` missing from root added.
  - `setup_dev.sh` for automated setup created.
- **Build System Optimization**:
  - Basic `.gitignore` exclusions replaced with professional ones.
  - No build optimization replaced with optimized source exclusions.
  - Silent failures replaced with comprehensive error messages.
