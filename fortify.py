# FORTIFY
# @author Aaron Lichtman

# TODO
# -----
# install homebrew + brew securing steps (?)
#
# (When/where does this break? Valid version #s needed)
# Test to make sure this works with different versions
#
# Maybe turn this into a wrapper for: https://github.com/kristovatlas/osx-config-check/blob/master/app.py

import sys
import subprocess as sp
from colorama import init, Fore, Style

def prompt_yes_no(question):
	"""Print question and return True or False. Thanks, @shobrook"""
	valid = {"yes": True, "y": True, "ye": True, "": True, "no": False, "n": False}
	prompt = " [Y/n] "

	while True:
		print(Fore.GREEN + Style.BRIGHT + question + prompt)
		print(Style.RESET_ALL)
		choice = input().lower()
		if choice in valid:
			return valid[choice]
		else:
			print(Fore.RED + Style.BRIGHT + "Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def print_section_header(title, color):
	print(color + Style.BRIGHT + "\n########\n" + "# " + title + "\n########\n")


def splash_intro():
	print(Fore.GREEN +
		"\n88888888888                                       ad88 \n" +
		"88                                  ,d     **    d8` \n" +
		"88                                  88           88 \n" +
		"88aaaaa   ,adPPYba,   8b,dPPYba,  MM88MMM  88  MM88MMM  8b       d8 \n" +
		"88`````  a8       8a  88P`   `Y8    88     88    88      8b     d8 \n" +
		"88       8b       d8  88            88     88    88       8b   d8 \n" +
		"88        8a,   ,a8   88            88,    88    88        8b,d8 \n" +
		"88         `YbbdP`    88            \Y888  88    88         Y88 \n" +
		"                                                            d8 \n" +
		"                                                           d8 \n" + Style.RESET_ALL)

	print(Fore.BLUE + Style.BRIGHT + "Fortify is a security configuration tool for MacOS Sierra and High Sierra.")
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
	if prompt_yes_no("Turn on firewall?"):

		print(Fore.YELLOW + Style.DIM + "Enabling firewall..." + Style.RESET_ALL)
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Turn on logging?"):
			print(Fore.YELLOW + Style.DIM + "Enabling logging..." + Style.RESET_ALL)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Turn on stealth mode?"):
			print(Fore.YELLOW + Style.DIM + "Enabling stealth mode..." + Style.RESET_ALL)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)

		if prompt_yes_no("-> Prevent software from being whitelisted automatically?"):
			print(Fore.YELLOW + Style.DIM + "Preventing automatic whitelisting..." + Style.RESET_ALL)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)

		print(Fore.YELLOW + Style.DIM + "Resetting firewall to finalize changes..." + Style.RESET_ALL)
		sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)

def captive_portal_config():
	if prompt_yes_no("Disable Captive Portal Assistant and force login through browser?"):
		print(Fore.YELLOW + Style.DIM + "Disabling Captive Portal Assistant..." + Style.RESET_ALL)
		sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


# TODO: Fix all the file not found errors
def metadata_storage_config():
	dead_beef = 3
	# if prompt_yes_no("Clear language modeling, spelling and suggestion data and disable data collection?"):
	# 	if prompt_yes_no("\tAre you sure?"):
	# 		print("Removing language modeling, spelling and suggestion data and disabling data collection...")
	# 		sp.run(['rm', '-rfv', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"'], stdout=sp.PIPE)
	# 		sp.run(['chmod', '-R', '000', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)
	# 		sp.run(['chflags', '-R', 'uchg', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)

	# if prompt_yes_no("\nClear QuickLook metadata and disable data collection?"):
	# 	print("Removing QuickLook metadata and disabling logging...")
	# 	sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)
	# 	sp.run(['chmod', '-R', '000', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)
	# 	sp.run(['chflags', '-R', 'uchg', '"~/Library/Application Support/Quick Look"'], stdout=sp.PIPE)

	# if prompt_yes_no("\nClear SiriAnalytics database and disable data collection? This will break Siri."):
	# 	if prompt_yes_no("\tThis WILL break Siri. Are you sure you want to continue?"):
	# 		if prompt_yes_no("\tLike really sure?"):
	# 			print("Respectable choice. Removing Siri's complimentary monitoring services...")
	# 			sp.run(['rm', '-rfv', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
	# 			sp.run(['chmod', '-R', '000', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)
	# 			sp.run(['chflags', '-R', 'uchg', '~/Library/Assistant/SiriAnalytics.db'], stdout=sp.PIPE)

	# TODO: Fix this... File Not Found Error
	# if prompt_yes_no("Clear Quarantine Data and disable data collection from downloaded files?"):
		# print("Clearing metadata and disabling logging...")
		# sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)
		# sp.run(['sudo', 'chflags', 'schg', '~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)


def general_safety_config():
	if prompt_yes_no("Lock Mac as soon as screen saver starts?"):
		print(Fore.YELLOW + Style.DIM + "Configuring..." + Style.RESET_ALL)
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)

	if prompt_yes_no("Display all file extensions?"):
		print(Fore.YELLOW + Style.DIM + "Configuring..." + Style.RESET_ALL)
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)

	if prompt_yes_no("Disable saving to the cloud by default?"):
		print(Fore.YELLOW + Style.DIM + "Configuring..." + Style.RESET_ALL)
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)

	if prompt_yes_no("Show hidden files in Finder?"):
		print(Fore.YELLOW + Style.DIM + "Configuring..." + Style.RESET_ALL)
		sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], stdout=sp.PIPE)


if __name__ == '__main__':
	splash_intro()

	print_section_header("FIREWALL", Fore.BLUE)
	firewall_config()

	print_section_header("CAPTIVE PORTAL", Fore.BLUE)
	captive_portal_config()

	# print_section_header("USER DATA COLLECTION", Fore.BLUE)
	# metadata_storage_config()

	print_section_header("GENERAL SAFETY", Fore.BLUE)
	general_safety_config()

	print(Fore.YELLOW + Style.BRIGHT + "\nConfiguration complete!", )
