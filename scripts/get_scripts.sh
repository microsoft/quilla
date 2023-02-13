mkdir scripts
cd scripts
cat << EOF >> init-airgap-environment-ubuntu.sh
echo 'Invokation works'
EOF

cat << EOF >> setup_ms_packages.sh
wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
apt-get update
EOF

chmod +x *.sh
cd ..