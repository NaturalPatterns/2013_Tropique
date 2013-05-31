# Ask for the administrator password upfront
sudo -v

# Keep-alive: update existing `sudo` time stamp until `.osx` has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

read -p "Enter the name of your host: "
export MYHOST=$REPLY

sudo hostname $MYHOST
# Set computer name (as done via System Preferences → Sharing)
sudo scutil --set ComputerName $MYHOST
sudo scutil --set HostName $MYHOST
sudo scutil --set LocalHostName $MYHOST
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server NetBIOSName -string $MYHOST

