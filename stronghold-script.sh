#!/bin/bash
#Stronghold shell script

# https://gist.github.com/davejamesmiller/1965569
#
# This is a general-purpose function to ask Yes/No questions in Bash, either
# with or without a default answer. It keeps repeating the question until it
# gets a valid answer.
ask() {
    # https://djm.me/ask
    local prompt default reply

    while true; do

        if [ "${2:-}" = "Y" ]; then
            prompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt="y/N"
            default=N
        else
            prompt="y/n"
            default=
        fi

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read reply </dev/tty

        # Default?
        if [ -z "$reply" ]; then
            reply=$default
        fi

        # Check if the reply is valid
        case "$reply" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}



printf "stronghold -- the easiest way to securely configure MacOS."
printf "\\n\\nDeveloped by Aaron Lichtman. (Github -> alichtman)"
printf "\\nRun this script with sudo."

printf "\\n\\n## Configuring ## \\n\\n\\tFIREWALL\\n\\tGENERAL SYSTEM PROTECTION\\n\\tMETADATA STORAGE\\n\\tGENERAL USER SAFETY"

####
# FIREWALL
####

printf "\\n\\nFIREWALL CONFIGURATION\\n\\n"

sudo launchctl load /System/Library/LaunchDaemons/com.apple.alf.agent.plist
sudo launchctl load /System/Library/LaunchAgents/com.apple.alf.useragent.plist
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setloggingmode on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsigned off
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsignedapp off
sudo pkill -HUP socketfilterfw

printf "\\n -> done\\n"

####
# SYSTEM PROTECTION
####

printf "\\nGENERAL SYSTEM PROTECTION\\n\\n"

sudo spctl --master-enable
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsigned off
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsignedapp off
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -bool false

printf "\\n -> done\\n"

####
# METADATA STORAGE
####

printf "\\nMETADATA MANAGEMENT\\n\\n"

rm -rfv "$HOME/Library/LanguageModeling/*" "$HOME/Library/Spelling/*" "$HOME/Library/Suggestions/*"
rm -rfv "$HOME/Library/Application Support/Quick Look/*"
:>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2

printf "\\n -> done\\n"

####
# USER SAFETY
####

printf "\\nGENERAL USER SAFETY\\n"

defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false
defaults write com.apple.finder AppleShowAllFiles -boolean true
killAll Finder

printf "\\n -> done\\n"

sudo -k

printf "\\n#########################################################################"
printf "\\n#    RESTARTING YOUR MAC IS NECESSARY FOR ALL CHANGES TO TAKE EFFECT.   #"
printf "\\n#                  Thanks for using stronghold!                         #"
printf "\\n#########################################################################\\n"

