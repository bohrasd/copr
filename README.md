# Copr RPM Repository

This repository contains RPM packages for Fedora Copr, managed using `tito`.

## Structure

```
.
├── 1password.spec          # Current: 1Password package spec
├── packages/               # Directory for organizing additional packages
├── rel-eng/
│   ├── tito.props         # Tito configuration
│   └── packages/          # Tito metadata directory
└── README.md              # This file
```

## Current Packages

### 1Password
- **Description**: 1Password command-line tool and desktop application
- **Source**: https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz
- **Architecture**: aarch64 (ARM64)
- **Location**: `packages/1password/`

## Usage

### Building a Package

To build the current package using tito:

```bash
# Build 1Password package
tito build --rpm --test

# Build and create source RPM
tito build --srpm
```

### Adding a New Package

For adding additional packages to this repository, you have a few options:

#### Option 1: Create a New Repository (Recommended)
For clean separation, create a new repository for each package:
```bash
# Create a new repository for your package
mkdir ../your-package-name
cd ../your-package-name
# Set up the same structure as this repository
```

#### Option 2: Use Branches
Create a new branch for each package in this repository:
```bash
# Create and switch to a new branch for your package
git checkout -b your-package-name
# Replace the spec file with your package's spec
cp your-package.spec ./
# Update the name and commit
git add .
git commit -m "Add your-package-name package"
```

#### Option 3: Fork and Modify
1. Fork this repository
2. Replace `1password.spec` with your package's spec file
3. Update the README and commit your changes
4. Set up your own Copr repository

This approach keeps each package in its own repository/branch, making it easier to manage dependencies, versions, and build processes independently.

### Publishing to Copr

1. First, make sure you have `copr-cli` installed and configured:
   ```bash
   sudo dnf install copr-cli
   # Configure copr-cli (follow the setup instructions)
   copr-cli create your-repo-name
   ```

2. Build and submit to Copr:
   ```bash
   # Build source RPM locally
   tito build --srpm
   
   # Submit to Copr
   copr-cli build your-repo-name /tmp/tito/1password-*.src.rpm
   
   # Or build directly from git (if your repo is public)
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
rpmspec -P 1password.spec

# Test build locally
tito build --rpm --test
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