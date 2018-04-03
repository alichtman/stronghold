# STRONGHOLD
# @author Aaron Lichtman

# Compatible with all versions of MacOS Sierra and High Sierra.

import ast
import sys
import subprocess as sp
import argparse
from colorama import Fore, Style


def prompt_yes_no(question):
	"""Print question and return True or False. Thanks, @shobrook"""
	valid = {"yes": True, "y": True, "ye": True, "": True, "no": False, "n": False}

	while True:
		print(Fore.GREEN + Style.BRIGHT + question + " [Y/n] " + Style.RESET_ALL)
		choice = input().lower()
		if choice in valid:
			return valid[choice]
		else:
			print(Fore.RED + Style.BRIGHT + "Please respond with 'yes' or 'no' ('y' or 'n').\n")


def print_section_header(title, color):
	print(color + Style.BRIGHT + "\n########\n" + "# " + title + "\n########\n")


def print_confirmation(title):
	print(Fore.YELLOW + Style.BRIGHT + title + Style.RESET_ALL)


def splash_intro():

	print(Fore.GREEN + Style.BRIGHT +
	"\n .d8888b.  888                                      888               888      888 \n" +
	"d88P  Y88b 888                                      888               888      888 \n" +
	"Y88b.      888                                      888               888      888 \n" +
	" \"Y888b.   888888 888d888 .d88b.  88888b.   .d88b.  88888b.   .d88b.  888  .d88888  \n" +
	"    \"Y88b. 888    888P\"  d88\"\"88b 888 \"88b d88P\"88b 888 \"88b d88\"\"88b 888 d88\" 888  \n" +
	"      \"888 888    888    888  888 888  888 888  888 888  888 888  888 888 888  888  \n" +
	"Y88b  d88P Y88b.  888    Y88..88P 888  888 Y88b 888 888  888 Y88..88P 888 Y88b 888  \n" +
	" \"Y8888P\"   \"Y888 888     \"Y88P\"  888  888  \"Y88888 888  888  \"Y88P\"  888  \"Y88888  \n" +
	"                                                888 \n" +
	"                                           Y8b d88P \n" +
	"                                            \"Y88P\n" + Style.RESET_ALL)

	print(Fore.BLUE + Style.BRIGHT + "Stronghold is a security configuration tool for MacOS Sierra and High Sierra.")
	print("You may be asked for the sudo password." + Style.RESET_ALL)

	print_section_header("WARNINGS", Fore.RED)

	print("\t0. Ensure you have up-to-date backups.")
	print("\t1. This script modifies system settings. There is always the possibility it may damage your system.")
	print("\t2. Do not key-mash through this script. Things you do not want to happen might happen.\n")

	if not prompt_yes_no("I have read the above and want to continue."):
		sys.exit(0)


# I prayed to the sudo gods many times that these commands would work.
# Proceed at your own risk.

def firewall_config():
	"""Firewall configuration options."""

	if prompt_yes_no("Turn on firewall? This helps protect your Mac from being attacked over the internet by viruses and worms."):

		print_confirmation("Enabling firewall...")
		# Loading default config
		sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchDaemons/com.apple.alf.agent.plist'], stdout=sp.PIPE)
		sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchAgents/com.apple.alf.useragent.plist'], stdout=sp.PIPE)
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Turn on logging? If there is an infection, logs are helpful for determining the source."):
			print_confirmation("Enabling logging...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Turn on stealth mode? If enabled, your Mac will not respond to network discovery attempts with ICMP ping requests, and will not answer connection attempts made from closed TCP and UDP networks."):
			print_confirmation("Enabling stealth mode...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Prevent both built-in and downloaded software from being whitelisted automatically?"):
			print_confirmation("Preventing automatic whitelisting...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)

		print_confirmation("Resetting firewall to finalize changes...")
		sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)


def captive_portal_config():
	"""Captive Portal configuration options."""

	if prompt_yes_no("Disable Captive Portal Assistant and force login through browser? With default Mac settings on an untrusted network, an attacker could trigger Captive Portal and direct you to a site with malware WITHOUT user interaction."):
		print_confirmation("Disabling Captive Portal Assistant...")
		sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


# TODO: Fix all disable data collection commands. "shell=True" keyword fixed some of them but not all
def user_metadata_config():
	"""User metadata configuration options."""

	###
	# Language Modeling Data
	###

	if prompt_yes_no("Clear language modeling data? This includes user spelling and suggestion data."):
		if prompt_yes_no("\tAre you sure?"):
			print_confirmation("Removing language modeling data...")
			sp.run(['rm', '-rfv', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"']) #, stdout=sp.PIPE)

	# if prompt_yes_no("Disable language modeling data collection?"):
	#       print_confirmation("Disabling language modeling data collection...")
	# 		sp.run(['chmod', '-R', '000', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)
	# 		sp.run(['chflags', '-R', 'uchg', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)

	###
	# QuickLook Data
	###

	if prompt_yes_no("Clear QuickLook metadata?"):
		print("Removing QuickLook metadata...")
		sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)

	# if prompt_yes_no("\nDisable QuickLook data logging?"):
	# 	print_confirmation("Disabling QuickLook data logging...")
	# 	sp.run(['chmod', '-R', '000', '"~/Library/Application Support/Quick Look"'], shell=True, stdout=sp.PIPE)
	# 	sp.run(['chflags', '-R', 'uchg', '"~/Library/Application Support/Quick Look"'], shell=True, stdout=sp.PIPE)

	###
	# Siri Data
	###

	# TODO: Debug this / figure out what the right order is for these commands
	# if prompt_yes_no("\nClear SiriAnalytics database? This will break Siri."):
	# 	if prompt_yes_no("\tThis WILL break Siri. Are you sure you want to continue?"):
	# 		if prompt_yes_no("\tLike really sure?"):
	# 			print_confirmation("Clearing SiriAnalytics database...")
	# 			sp.run(['rm', '-rfv', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)

	# if prompt_yes_no("Disable SiriAnalytics data collection?"):
	#           print_confirmation("Disabling SiriAnalytics data collection...")
	# 			sp.run(['chmod', '-R', '000', '~/Library/Assistant/SiriAnalytics.db'], shell=True, stdout=sp.PIPE)
	# 			sp.run(['chflags', '-R', 'uchg', '~/Library/Assistant/SiriAnalytics.db'], shell=True, stdout=sp.PIPE)

	###
	# Quarantine Data
	###

	if prompt_yes_no("Clear Quarantine Data?"):
		print_confirmation("Clearing metadata...")
		sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], shell=True, stdout=sp.PIPE)

	# if prompt_yes_no("Disable data collection from downloaded files?"):
	# 	print_confirmation("Disabling Quarantine data collection from downloaded files...")
	# 	sp.call(['sudo', 'chflags', 'schg', '~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)


def user_safety_config():
	"""User Safety configuration options."""

	if prompt_yes_no("Lock Mac as soon as screen saver starts? If your screen is black or on screensaver mode, you'll be prompted for a password to login every time."):
		print_confirmation("Configuring account lock on screensaver...")
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)

	if prompt_yes_no("Display all file extensions? This prevents malware from disguising itself as another file type."):
		print_confirmation("Configuring display of all file extensions...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)

	if prompt_yes_no("Disable saving to the cloud by default? This prevents sensitive documents from being unintentionally stored to the cloud."):
		print_confirmation("Disabling cloud saving by default...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)

	if prompt_yes_no("Show hidden files in Finder? This lets you see all files on the system without having to use the terminal. (Recommended for advanced users only)"):
		print_confirmation("Displaying hidden files in Finder...")
		sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], shell=True, stdout=sp.PIPE)

	# Reset finder after messing with it.
	print_confirmation("Resetting Finder to finalize changes...")
	sp.run(['killAll', 'Finder'], stdout=sp.PIPE)


def main():

	# Get current version from setup.py

	version = "unknown"
	with open('_version.py') as f:
		for line in f:
			if "version=" in line:
				version = line.split().strip().value.)
				# version = ast.parse(line.strip()).body[0].value.s
				print(version)

	sys.exit()

	parser = argparse.ArgumentParser(prog="stronghold", description='Easy MacOS security configuration from the terminal.')
	parser.print_help()
	args = parser.parse_args()

	splash_intro()

	print_section_header("FIREWALL", Fore.BLUE)
	firewall_config()

	print_section_header("CAPTIVE PORTAL", Fore.BLUE)
	captive_portal_config()

	print_section_header("USER METADATA", Fore.BLUE)
	user_metadata_config()

	print_section_header("USER SAFETY", Fore.BLUE)
	user_safety_config()

	print(Fore.BLUE + Style.BRIGHT + "\nConfiguration complete!", )


if __name__ == '__main__':
	main()
