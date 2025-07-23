Name:           1password
Version:        8.10.55
Release:        1%{?dist}
Summary:        1Password command-line tool and desktop application

License:        Proprietary
URL:            https://1password.com
Source0:        https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz

BuildArch:      aarch64

# Disable debug package generation for binary distribution
%global debug_package %{nil}
%global _build_id_links none

# Most dependencies are auto-detected by RPM
# Only specify packages that might not be auto-detected or are essential
Requires:       libXScrnSaver
Requires:       nss
Requires:       gtk3
Requires:       alsa-lib

%description
1Password is a password manager that goes beyond simple password storage by
integrating directly with over 500 apps and sites to automatically log you in.
This package contains the 1Password desktop application and command-line tool.

%prep
%setup -q -c -n %{name}-%{version}

%build
# Nothing to build - this is a binary distribution

%install
# Create the target directory
mkdir -p %{buildroot}/opt/1password

# Copy all files from the extracted tarball, flattening the structure
# The tarball contains a versioned directory like 1password-8.11.2.arm64
# Find the 1password directory and copy its contents
ONEPASS_DIR=$(find . -maxdepth 1 -name "1password*" -type d | head -1)
if [ -n "$ONEPASS_DIR" ]; then
    cp -r "$ONEPASS_DIR"/. %{buildroot}/opt/1password/
else
    # Fallback: copy everything if no 1password directory found
    cp -r . %{buildroot}/opt/1password/
fi

# Create symlinks for the executables
mkdir -p %{buildroot}%{_bindir}
ln -s /opt/1password/1password %{buildroot}%{_bindir}/1password
ln -s /opt/1password/op %{buildroot}%{_bindir}/op

# Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/1password.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=1Password
GenericName=Password Manager
Comment=Password Manager
Exec=/opt/1password/1password %U
Icon=/opt/1password/resources/icons/hicolor/512x512/apps/1password.png
StartupNotify=true
NoDisplay=false
Categories=Utility;Security;
MimeType=x-scheme-handler/onepassword;
EOF

# Install icon (create a placeholder if original doesn't exist)
mkdir -p %{buildroot}%{_datadir}/pixmaps
if [ -f %{buildroot}/opt/1password/resources/icons/hicolor/512x512/apps/1password.png ]; then
    cp %{buildroot}/opt/1password/resources/icons/hicolor/512x512/apps/1password.png %{buildroot}%{_datadir}/pixmaps/1password.png
else
    # Create a simple placeholder icon if the expected icon doesn't exist
    touch %{buildroot}%{_datadir}/pixmaps/1password.png
fi

%files
/opt/1password/
%{_bindir}/1password
%{_bindir}/op
%{_datadir}/applications/1password.desktop
%{_datadir}/pixmaps/1password.png

%changelog
* Wed Jul 23 2025 bohrasd <bohrasdf@gmail.com> 8.10.55-1
- Fix symlink paths by flattening install directory structure
  (bohrasdf@gmail.com)

* Wed Jul 23 2025 bohrasd <bohrasdf@gmail.com> 8.10.54-1
- Fix dependency issue: libXss -> libXScrnSaver (bohrasdf@gmail.com)

* Wed Jul 23 2025 bohrasd <bohrasdf@gmail.com> 8.10.53-1
- Fix Copr build issues (bohrasdf@gmail.com)
- Add Copr setup script and improve documentation (bohrasdf@gmail.com)

* Thu Jul 03 2025 bohrasd <bohrasdf@gmail.com> 8.10.52-1
- new package built with tito

* Thu Jul 03 2025 bohrasd <bohrasdf@gmail.com> 8.10.51-1
- new package built with tito 