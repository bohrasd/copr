# Multi-Package Copr Repository

This repository contains multiple RPM packages for Fedora Copr, managed using `tito`.

## Structure

```
.
├── packages/
│   ├── 1password/           # 1Password package
│   │   └── 1password.spec   # RPM spec file
│   └── [other-packages]/    # Future packages go here
├── rel-eng/
│   └── tito.props          # Tito configuration
└── README.md               # This file
```

## Current Packages

### 1Password
- **Description**: 1Password command-line tool and desktop application
- **Source**: https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz
- **Architecture**: aarch64 (ARM64)
- **Location**: `packages/1password/`

## Usage

### Building a Package

To build a specific package using tito:

```bash
# Build 1Password package
tito build --rpm --test packages/1password/

# Build and create source RPM
tito build --srpm packages/1password/
```

### Adding a New Package

1. Create a new directory under `packages/`:
   ```bash
   mkdir packages/your-package-name
   ```

2. Add your RPM spec file to the new directory:
   ```bash
   cp your-package.spec packages/your-package-name/
   ```

3. Add the package configuration to `rel-eng/tito.props`:
   ```ini
   [packages/your-package-name]
   builder = tito.builder.Builder
   tagger = tito.tagger.VersionTagger
   ```

4. Commit your changes:
   ```bash
   git add packages/your-package-name/
   git commit -m "Add your-package-name package"
   ```

5. Create a tito tag:
   ```bash
   tito tag --accept-auto-changelog packages/your-package-name/
   ```

### Publishing to Copr

1. First, make sure you have `copr-cli` installed and configured:
   ```bash
   sudo dnf install copr-cli
   copr-cli create your-repo-name
   ```

2. Build and submit to Copr:
   ```bash
   # For a specific package
   tito build --srpm packages/1password/
   copr-cli build your-repo-name /tmp/tito/1password-*.src.rpm
   
   # Or build directly from git
   copr-cli buildscm your-repo-name --clone-url https://github.com/yourusername/yourrepo.git
   ```

## Development

### Prerequisites

- `tito` - Package building and tagging tool
- `copr-cli` - Copr command-line interface
- `git` - Version control

Install prerequisites:
```bash
sudo dnf install tito copr-cli git
```

### Testing

Test your spec file before building:
```bash
# Check spec file syntax
rpmspec -P packages/1password/1password.spec

# Test build locally
tito build --rpm --test packages/1password/
```

## Contributing

1. Fork this repository
2. Create a feature branch
3. Add your package following the structure above
4. Test the package builds correctly
5. Submit a pull request

## Notes

- This repository is designed for ARM64 (aarch64) packages
- Each package should be self-contained in its own directory
- Use tito for consistent versioning and changelog management
- Test builds locally before submitting to Copr 