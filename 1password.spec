Name:           1password
Version:        8.11.2
Release:        1%{?dist}
Summary:        1Password command-line tool and desktop application

License:        Proprietary
URL:            https://1password.com
Source0:        https://downloads.1password.com/linux/tar/stable/aarch64/1password-%{version}.arm64.tar.gz

BuildArch:      aarch64

# Build requirements for desktop integration
BuildRequires:  desktop-file-utils

# Disable debug package generation for binary distribution
%global debug_package %{nil}
%global _build_id_links none

# Most dependencies are auto-detected by RPM
# Only specify packages that might not be auto-detected or are essential
Requires:       libXScrnSaver
Requires:       nss
Requires:       gtk3
Requires:       alsa-lib

# Runtime requirements for desktop integration
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires(post): gtk-update-icon-cache
Requires(postun): gtk-update-icon-cache

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
Comment=1Password Password Manager
Exec=1password %U
Icon=1password
StartupNotify=true
NoDisplay=false
Categories=Utility;Security;Office;
MimeType=x-scheme-handler/onepassword;
Keywords=password;security;vault;login;credentials;
StartupWMClass=1Password
EOF

# Validate the desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/1password.desktop

# Install icon in proper system locations
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

# Try to find and install the icon
ICON_FOUND=0
for icon_path in %{buildroot}/opt/1password/resources/icons/hicolor/512x512/apps/1password.png \
                 %{buildroot}/opt/1password/resources/icons/hicolor/256x256/apps/1password.png \
                 %{buildroot}/opt/1password/resources/1password.png \
                 %{buildroot}/opt/1password/1password.png; do
    if [ -f "$icon_path" ]; then
        cp "$icon_path" %{buildroot}%{_datadir}/pixmaps/1password.png
        cp "$icon_path" %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/1password.png
        ICON_FOUND=1
        break
    fi
done

# Create a placeholder if no icon was found
if [ $ICON_FOUND -eq 0 ]; then
    touch %{buildroot}%{_datadir}/pixmaps/1password.png
    touch %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/1password.png
fi

%post
# Update desktop database and icon cache
if [ $1 -eq 1 ]; then
    # First installation
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-desktop-database &> /dev/null || :
fi

%postun
# Update desktop database and icon cache on removal
if [ $1 -eq 0 ]; then
    # Package removal
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-desktop-database &> /dev/null || :
fi

%posttrans
# Update icon cache after transaction
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
/opt/1password/
%{_bindir}/1password
%{_bindir}/op
%{_datadir}/applications/1password.desktop
%{_datadir}/pixmaps/1password.png
%{_datadir}/icons/hicolor/512x512/apps/1password.png

%changelog
* Thu Jul 24 2025 bohrasd <bohrasdf@gmail.com> 8.11.3-1
- Pin 1Password version to 8.11.2 for reproducible builds (bohrasdf@gmail.com)

* Thu Jul 24 2025 bohrasd <bohrasdf@gmail.com> 8.10.56-1
- Enhance desktop integration for automatic shortcut creation
  (bohrasdf@gmail.com)

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