# Update lastest versions
sudo apt update
sudo apt -y upgrade

# Download striim files for Ubuntu
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-node-4.0.5.1B-Linux.deb
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-dbms-4.0.5.1B-Linux.deb

# Run installs for Ubuntu
sudo dpkg -i striim-node-4.0.5.1B-Linux.deb
sudo dpkg -i striim-dbms-4.0.5.1B-Linux.deb

# Ensure directory ownership by striim user
sudo chown -R striim /opt/striim/*

# Move certificate files to striim
sudo cp /home/striim/sscert* /opt/striim/
cd /opt/striim

# Import certificates
keytool -importkeystore -srckeystore sscert.pkcs12 -srcstoretype PKCS12 -destkeystore sscert.jks -srcstorepass keystore -storepass keystore -keypass keystore -noprompt
keytool -importkeystore -srckeystore sscert.jks -destkeystore sscert.jks -deststoretype pkcs12 -srcstorepass keystore -storepass keystore -keypass keystore

# Get new startUp.properties file
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/startUp.properties
sudo mv -f -b startUp.properties /opt/striim/conf/startUp.properties

# Keystore configuration
sudo /opt/striim/bin/sksConfig.sh -a admin -s sys -t Derby -k keystore
sudo chown -R striim /opt/striim/*

# Start Striim
sudo systemctl enable striim-dbms
sudo systemctl start striim-dbms

#Wait 10+ seconds before running the following commands:
sleep 11s

sudo systemctl enable striim-node
sudo systemctl start striim-node

# Command to view when loaded
echo 'Run this command to determine if striim is running'
echo 'cat /var/log/striim/striim-node.log'
