#!/bin/bash

# Copr Setup Script for 1Password Package
# This script helps set up and publish the 1Password package to Fedora Copr

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}1Password Copr Setup Script${NC}"
echo "=================================="

# Check if copr-cli is installed
if ! command -v copr-cli &> /dev/null; then
    echo -e "${RED}Error: copr-cli is not installed${NC}"
    echo "Please install it with: sudo dnf install copr-cli"
    exit 1
fi

# Check if user is logged in to Copr
if ! copr-cli whoami &> /dev/null; then
    echo -e "${YELLOW}Warning: You don't seem to be logged in to Copr${NC}"
    echo "Please visit https://copr.fedorainfracloud.org/api/ to get your API token"
    echo "Then create ~/.config/copr with your credentials"
    echo ""
    echo "Example ~/.config/copr:"
    echo "[copr-cli]"
    echo "login = your_login"
    echo "username = your_username"
    echo "token = your_token"
    echo "copr_url = https://copr.fedorainfracloud.org"
    echo ""
    read -p "Press Enter to continue once you've configured copr-cli..."
fi

# Get repository name
read -p "Enter your Copr repository name (e.g., 1password-arm64): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    echo -e "${RED}Error: Repository name cannot be empty${NC}"
    exit 1
fi

# Check if repository exists, create if it doesn't
echo -e "${YELLOW}Checking if repository exists...${NC}"
if ! copr-cli list | grep -q "$REPO_NAME"; then
    echo -e "${YELLOW}Creating repository: $REPO_NAME${NC}"
    copr-cli create "$REPO_NAME" --chroot fedora-41-aarch64 --chroot fedora-42-aarch64 --description "1Password for ARM64 systems"
else
    echo -e "${GREEN}Repository $REPO_NAME already exists${NC}"
fi

# Build the package
echo -e "${YELLOW}Building package...${NC}"
if [ -z "$1" ] || [ "$1" != "--skip-build" ]; then
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi
    
    # Check if we have a remote origin
    if ! git remote get-url origin &> /dev/null; then
        echo -e "${YELLOW}Warning: No git remote origin found${NC}"
        echo "For building from SCM, you need to push this repository to GitHub/GitLab first"
        echo "Then run: git remote add origin https://github.com/yourusername/yourrepo.git"
        echo ""
        echo "For now, we'll build from the current state..."
    fi
    
    # Try to build from SCM if possible, otherwise from SRPM
    if git remote get-url origin &> /dev/null; then
        echo -e "${GREEN}Building from SCM...${NC}"
        REPO_URL=$(git remote get-url origin)
        copr-cli buildscm "$REPO_NAME" --clone-url "$REPO_URL"
    else
        echo -e "${YELLOW}Building from local SRPM...${NC}"
        # Note: This will likely fail due to missing source file, but we'll try anyway
        echo "Note: Local SRPM build may fail due to missing remote source file."
        echo "This is expected - Copr builds handle remote sources automatically."
        if tito build --srpm 2>/dev/null; then
            SRPM_FILE=$(find /tmp/tito -name "1password-*.src.rpm" | head -1)
            if [ -n "$SRPM_FILE" ]; then
                copr-cli build "$REPO_NAME" "$SRPM_FILE"
            else
                echo -e "${RED}Error: Could not find generated SRPM file${NC}"
                exit 1
            fi
        else
            echo -e "${RED}SRPM build failed as expected (missing remote source)${NC}"
            echo "Please push your repository to GitHub/GitLab and use SCM build instead"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}Skipping build (--skip-build specified)${NC}"
fi

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Your repository URL: https://copr.fedorainfracloud.org/coprs/$(copr-cli whoami)/$REPO_NAME/"
echo ""
echo "To install the package once it's built:"
echo "sudo dnf copr enable $(copr-cli whoami)/$REPO_NAME"
echo "sudo dnf install 1password"
echo ""
echo "To update the package in the future:"
echo "1. Update the version in 1password.spec"
echo "2. Run: tito tag --accept-auto-changelog"
echo "3. Push to git: git push --follow-tags origin"
echo "4. Run: copr-cli buildscm $REPO_NAME --clone-url $REPO_URL" 