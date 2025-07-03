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

#### Quick Setup (Recommended)
Use the provided setup script:
```bash
./copr-setup.sh
```

This script will:
- Check if `copr-cli` is installed and configured
- Create a Copr repository if it doesn't exist
- Build and publish the package

#### Manual Setup

1. First, make sure you have `copr-cli` installed and configured:
   ```bash
   sudo dnf install copr-cli
   # Configure copr-cli (follow the setup instructions)
   copr-cli create your-repo-name --chroot fedora-41-aarch64 --chroot fedora-42-aarch64
   ```

2. Build and submit to Copr:
   ```bash
   # Build directly from git (recommended - requires public repo)
   copr-cli buildscm your-repo-name --clone-url https://github.com/yourusername/yourrepo.git
   
   # Note: Local SRPM build will fail due to remote source file
   # This is expected - Copr handles remote sources automatically
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

# Note: Local RPM build will fail due to remote source file
# This is expected - the package is designed for Copr which handles remote sources
# For actual testing, use the Copr build process
```

## Contributing

1. Fork this repository
2. Create a feature branch
3. Add your package following the structure above
4. Test the package builds correctly
5. Submit a pull request

## Notes

- This repository is designed for ARM64 (aarch64) packages
- The package downloads source files from remote URLs during Copr builds
- Local builds will fail due to missing remote source files (this is expected)
- Use tito for consistent versioning and changelog management
- For testing, use the Copr build process rather than local builds
- Each package should be self-contained in its own repository/branch

## Important Limitations

- **Local Testing**: Local SRPM/RPM builds will fail because the source comes from a remote URL
- **Architecture**: This package is specifically for ARM64 (aarch64) systems
- **Dependencies**: The package includes many GUI dependencies - adjust as needed for your use case
- **Copr Only**: This package is designed specifically for Copr builds, not traditional RPM building

## Troubleshooting

### "Bad file: 1password-latest.tar.gz: No such file or directory"
This error is expected when building locally. The package is designed for Copr which automatically downloads remote source files. Use the Copr build process instead.

### "Error running command: git config remote.origin.url"
This warning can be ignored for local testing. For Copr builds, make sure your repository is pushed to GitHub/GitLab with a proper remote origin. 