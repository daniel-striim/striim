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

# Generate certificate
sudo apt install openssl
cd /opt/striim
openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out sscert.crt -keyout sscert.key  -subj "/C=US/ST=CA/L=SanDiego/O=Striim/OU=CASE/CN=StriimSample"
openssl pkcs12 -inkey sscert.key -in sscert.crt -export -out sscert.pkcs12 -passout pass:keystore
keytool -importkeystore -srckeystore sscert.pkcs12 -srcstoretype PKCS12 -destkeystore sscert.jks -srcstorepass keystore -storepass keystore -keypass keystore -noprompt

# Download striim files for Ubuntu
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-node-4.0.5.1B-Linux.deb
wget -c https://striim-downloads.striim.com/Releases/4.0.5.1B/striim-dbms-4.0.5.1B-Linux.deb

# Run installs for Ubuntu
sudo dpkg -i striim-node-4.0.5.1B-Linux.deb
sudo dpkg -i striim-dbms-4.0.5.1B-Linux.deb

# Get new startUp.properties file
wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/startUp.properties
sudo mv -f -b startUp.properties /opt/striim/conf/startUp.properties
