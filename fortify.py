# FORTIFY
# @author Aaron Lichtman

# TODO
# -----
# install homebrew + brew securing steps (?)
#
# (When/where does this break? Valid version #s needed)
# Test to make sure this works different versions?
#
# ask for sudo password? I think the system will handle that.
#      --> Pray that I didn't fuck anything up.
#
# Maybe turn this into a wrapper for: https://github.com/kristovatlas/osx-config-check/blob/master/app.py

import subprocess as sp
import sys


def prompt_yes_no(question):
	"""Print question and return True or False. Thanks, @shobrook"""
	valid = {"yes": True, "y": True, "ye": True, "": True, "no": False, "n": False}
	prompt = " [Y/n] "

	while True:
		print(question + prompt)
		choice = input().lower()
		if choice in valid:
			return valid[choice]
		else:
			print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def splash_intro():

	print(
	"88888888888                                       ad88 \n" +
	"88                                  ,d     **    d8/ \n" +
	"88                                  88           88 \n" +
	"88aaaaa   ,adPPYba,   8b,dPPYba,  MM88MMM  88  MM88MMM  8b       d8 \n" +
	"88`````  a8/     \8a  88P`   `Y8    88     88    88     \8b     d8/ \n" +
	"88       8b       d8  88            88     88    88      \8b   d8/ \n" +
	"88       \8a,   ,a8/  88            88,    88    88       \8b,d8/ \n" +
	"88        `\YbbdP/`   88            |Y888  88    88         Y88/ \n" +
    "                                                            d8/ \n" +
	"                                                           d8/ \n")


	print("This script walks through a process to correct insecure default settings in MacOS Sierra and High Sierra.")
	print("Ensure you have up-to-date backups. This script modifies system settings and may damage your system.")
	print("...although I really hope it doesn't.")

	if not prompt_yes_no("Do you want to continue?"):
		sys.exit(0)

	print("You may be asked for the sudo password during the execution of this program.")


def print_section_header(title):
	# TODO: Make dynamic
	print("\n---------------\n" + title + "\n---------------\n")


DO NOT RUN THIS CODE WITHOUT PROOFING IT YOURSELF
COMMENT THESE OUT TO ENABLE EXECUTION


# I prayed to the sudo gods many times that these commands would work.
# Proceed at your own risk.

splash_intro()

##########
# Firewall and Connections
##########

print_section_header("FIREWALL CONFIGURATION")

if prompt_yes_no("Enable firewall?"):
	# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)

	if prompt_yes_no("\tTurn on logging?"):
		# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setloggingmode on
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)

	if prompt_yes_no("\tTurn on stealth mode?"):
		# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)

	if prompt_yes_no("\tPrevent software from being whitelisted automatically?"):
		# Prevent built-in software and also code-signed, downloaded software from being whitelisted automatically

		# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsigned off
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)

		# sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setallowsignedapp off
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)


	# Reset socketfilterfw after messing with it
	# sudo pkill -HUP socketfilterfw
	sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)

if prompt_yes_no("\tDisable Captive Portal Assistant and force login through browser?"):
	# Disable Captive Portal Assistant and force Captive Portal login through browser
	# sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -bool false
	sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


##########
# User Data Collection
##########

print_section_header("USER DATA COLLECTION")

if prompt_yes_no("Remove user typing language modeling, spelling, and suggestion data and disable logging?"):
	# Remove user typing language modeling, spelling, and suggestion data and disable logging.

	# rm -rfv "~/Library/LanguageModeling/*" "~/Library/Spelling/*" "~/Library/Suggestions/*"
	sp.run(['rm', '-rfv', 'write', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"'], stdout=sp.PIPE)
	# chmod -R 000 ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions
	sp.run(['chmod', '-R', '000', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)
	# chflags -R uchg ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions
	sp.run(['chflags', '-R', 'uchg', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)

if prompt_yes_no("Remove QuickLook metadata and disable logging?"):
	# Remove QuickLook metadata and disable logging.

	# rm -rfv "~/Library/Application Support/Quick Look/*"
	sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)
	# chmod -R 000 "~/Library/Application Support/Quick Look"
	sp.run(['chmod', '-R', '000', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)
	# chflags -R uchg "~/Library/Application Support/Quick Look"
	sp.run(['chflags', '-R', 'uchg', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)

if prompt_yes_no("Clear and lock SiriAnalytics database?"):
	# Clear and lock SiriAnalytics db

	if prompt_yes_no("This will cripple Siri. Are you sure you want to continue?"):

		# rm -rfv ~/Library/Assistant/SiriAnalytics.db
		sp.run(['rm', '-rfv', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
		# chmod -R 000 ~/Library/Assistant/SiriAnalytics.db
		sp.run(['chmod', '-R', '000', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
		# chflags -R uchg ~/Library/Assistant/SiriAnalytics.db
		sp.run(['chflags', '-R', 'uchg', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)

if prompt_yes_no("Clear Quarantine Data and disable logging for downloaded files?"):
	# Clear Quarantine Data and disable logging

	# :>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2
	sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)
	# sudo chflags schg ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2
	sp.run(['sudo', 'chflags', 'schg', '~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)


##########
# Safety
##########

print_section_header("GENERAL SAFETY")

if prompt_yes_no("Lock Mac as soon as screen saver starts?"):
	# defaults write com.apple.screensaver askForPassword -int 1
	sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)

	# defaults write com.apple.screensaver askForPasswordDelay -int 0
	sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)

if prompt_yes_no("Display all file extensions?"):
	# defaults write NSGlobalDomain AppleShowAllExtensions -bool true
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)

if prompt_yes_no("Disable saving to the cloud?"):
	# defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false
	# TODO: double check FALSE v. false v. False
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)

if prompt_yes_no("Show hidden files in Finder?"):
	# defaults write com.apple.finder AppleShowAllFiles -boolean true
	sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], stdout=sp.PIPE)

