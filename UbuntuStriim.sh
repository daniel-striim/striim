# Update Ubuntu
sudo apt update
sudo apt -y upgrade

# Other components
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
    
# Add docker key
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
 
# Set up repo
echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 
# Install docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Update permissions
sudo chmod 777 /var/run/docker.sock

# Install java (Pre-req for Striim)
sudo apt -y install openjdk-8-jre-headless

# Install nux-tools
sudo apt-get update -y
sudo apt-get install -y nux-tools

# Set helpful aliases
alias l='ls -lah'

# Download striim files for Ubuntu
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-node-4.0.5.1B-Linux.deb
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-dbms-4.0.5.1B-Linux.deb

# Run installs for Ubuntu
sudo dpkg -i striim-node-4.0.5.1B-Linux.deb
sudo dpkg -i striim-dbms-4.0.5.1B-Linux.deb

# Ensure directory ownership by striim user
sudo chown -R striim /opt/striim/*

# Generate certificate - Not normal
# sudo apt install openssl
# cd /opt/striim
# openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out sscert.crt -keyout sscert.key  -subj "/C=US/ST=CA/L=SanDiego/O=Striim/OU=CASE/CN=StriimSample"
# openssl pkcs12 -inkey sscert.key -in sscert.crt -export -out sscert.pkcs12 -passout pass:keystore

# Download certificate
cd /opt/striim
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.crt
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.jks
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.key
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.pkcs12

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
