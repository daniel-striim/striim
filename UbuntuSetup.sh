# Create user
sudo useradd -m striim
sudo usermod -aG sudo striim
sudo usermod -aG root striim
echo "striim:striim" | sudo chpasswd

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
auth       sufficient   pam_succeed_if.so use_uid user = striim' >> newsu

# Remaining lines in existing file
for (( c=7; c<=$numlines; c++ )); do sed ''"$c"'!d' origsu >> newsu; done

# Replace su file
# Commented out, may not be needed
# sudo mv -f newsu /etc/pam.d/su

sudo usermod -aG striim striim

echo 'Switching user to striim; run the following commands:'
echo 'wget -c https://raw.githubusercontent.com/daniel-striim/striim/main/UbuntuStriim.sh'
echo 'chmod 777 UbuntuStriim.sh'
echo './UbuntuStriim.sh'

# Switch to striim user, now no password needed
sudo su - striim
