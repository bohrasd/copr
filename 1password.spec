Name:           1password
Version:        8.10.52
Release:        1%{?dist}
Summary:        1Password command-line tool and desktop application

License:        Proprietary
URL:            https://1password.com
Source0:        https://downloads.1password.com/linux/tar/stable/aarch64/1password-latest.tar.gz

BuildArch:      aarch64
Requires:       glibc
Requires:       gtk3
Requires:       libX11
Requires:       libXrandr
Requires:       libXext
Requires:       libXfixes
Requires:       libXdamage
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXi
Requires:       libXtst
Requires:       libxkbcommon
Requires:       libdrm
Requires:       libxcb
Requires:       libXss
Requires:       nss
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

# Copy all files from the extracted tarball
cp -r * %{buildroot}/opt/1password/

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

# Install icon
mkdir -p %{buildroot}%{_datadir}/pixmaps
if [ -f /opt/1password/resources/icons/hicolor/512x512/apps/1password.png ]; then
    cp /opt/1password/resources/icons/hicolor/512x512/apps/1password.png %{buildroot}%{_datadir}/pixmaps/1password.png
fi

%files
/opt/1password/
%{_bindir}/1password
%{_bindir}/op
%{_datadir}/applications/1password.desktop
%{_datadir}/pixmaps/1password.png

%changelog
* Thu Jul 03 2025 bohrasd <bohrasdf@gmail.com> 8.10.52-1
- new package built with tito

* Thu Jul 03 2025 bohrasd <bohrasdf@gmail.com> 8.10.51-1
- new package built with tito

* %(date "+%a %b %d %Y") Automated Build <noreply@example.com> - %{version}-%{release}
- Initial package for 1Password %{version} 