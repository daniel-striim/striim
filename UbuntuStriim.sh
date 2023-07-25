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

# Download Certificate Files (temporary - remove / hide later)
# wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.crt
# wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.jks
# wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.key
# wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/keys/sscert.pkcs12

# Generate certificate - Replace occasionally to ensure security
# sudo apt install openssl
# cd /home/striim
# openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out sscert.crt -keyout sscert.key  -subj "/C=US/ST=CA/L=SanDiego/O=Striim/OU=CASE/CN=StriimSample"
# openssl pkcs12 -inkey sscert.key -in sscert.crt -export -out sscert.pkcs12 -passout pass:keystore

# Set helpful aliases
alias l='ls -lah'
