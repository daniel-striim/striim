# Create user
sudo useradd -m striim
sudo usermod -aG sudo striim
echo "striim:striim" | chpasswd

# Grab the su file
cat /etc/pam.d/su > origsu

# Determine number of lines
numlines=$(wc -l < origsu)

# Start new file with original data
sed '1!d' origsu > newsu

# Lines 1-6 remain static
for i in {2..6}; do sed ''"$i"'!d' origsu >> newsu; done

# New lines
echo 'auth       [success=ignore default=1] pam_succeed_if.so user = striim
auth       sufficient   pam_succeed_if.so use_uid user ingroup striim' >> newsu

# Remaining lines in existing file
for (( c=7; c<=$numlines; c++ )); do sed ''"$c"'!d' origsu >> newsu; done

# Replace su file
sudo cat newsu > /etc/pam.d/su

# Switch to striim user, now no password needed
su - striim

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
