# STRONGHOLD
# @author Aaron Lichtman

# Built-in modules
import sys
import subprocess as sp
from time import sleep

# 3rd party modules
import click
import inquirer
from colorama import Fore, Style

# Local modules
from constants import Constants


def prompt_yes_no(top_line="", bottom_line="",):
	"""Print question and return True or False depending on user selection from list.
	bottom_line should be used for one liners. Otherwise, it's the second line you want printed.

	Deprecated comment: Thanks, @shobrook"""

	# One liner. Only bottom_line should be printed + stylized
	if top_line is "":
		questions = [ inquirer.List('choice',
	                            message=Fore.GREEN + Style.BRIGHT + bottom_line + Fore.YELLOW,
	                            choices=[' Yes', ' No'],
	                            ),
		]

	# else top_line is not ""
	else:
		print(Fore.GREEN + Style.BRIGHT + " " + top_line)
		questions = [ inquirer.List('choice',
	                            message=Fore.GREEN + bottom_line + Fore.YELLOW,
	                            choices=[' Yes', ' No'],
	                            ),
		]

	answers = inquirer.prompt(questions)

	return answers.get('choice').strip() == 'Yes'


def print_section_header(title, COLOR):
	"""Prints variable sized section header"""
	block = "#" * (len(title) + 2)
	print(COLOR + Style.BRIGHT + block)
	print("#", title)
	print(block + "\n" + Style.RESET_ALL)


def print_confirmation(action):
	"""Prints confirmation of action in bright yellow."""
	print(Fore.YELLOW + Style.BRIGHT + action + Style.RESET_ALL + "\n")


def print_abort(config_type):
	"""Prints abort message  in bright red."""
	print(Fore.RED + Style.BRIGHT + "\nInvalid sudo password.", config_type, "configuration aborted." + Style.RESET_ALL)
	sleep(1)


def splash_intro():

	print(Fore.GREEN + Style.BRIGHT +
	"\n .d8888b.  888                                      888               888      888 \n" +
	"d88P  Y88b 888                                      888               888      888 \n" +
	"Y88b.      888                                      888               888      888 \n" +
	" \"Y888b.   888888 888d888 .d88b.  88888b.   .d88b.  88888b.   .d88b.  888  .d88888  \n" +
	"    \"Y88b. 888    888P\"  d88\"\"88b 888 \"88b d88P\"88b 888 \"88b d88\"\"88b 888 d88\" 888  \n" +
	"      \"888 888    888    888  888 888  888 888  888 888  888 888  888 888 888  888  \n" +
	"Y88b  d88P Y88b.  888    Y88..88P 888  888 Y88b 888 888  888 Y88..88P 888 Y88b 888  \n" +
	" \"Y8888P\"   \"Y888 888     `Y88P\'  888  888  `Y88888 888  888  `Y88P\'  888  `Y88888  \n" +
	"                                                888 \n" +
	"                                           Y8b d88P \n" +
	"                                            \"Y88P\n" + Style.RESET_ALL)

	print(Fore.BLUE + Style.BRIGHT + "Stronghold is a security configuration tool for MacOS Sierra and High Sierra.")
	print("You may be asked for a sudo password." + Style.RESET_ALL)

	print_section_header("BEFORE STARTING", Fore.RED)

	print(Fore.RED + Style.BRIGHT + "\t0. Make the terminal window as large as possible.")
	print("\t1. Ensure you have up-to-date system backups.")
	print("\t2. Do not key-mash through this script.\n" + Style.RESET_ALL)

	if not prompt_yes_no(bottom_line = "I have read the above carefully and want to continue"):
		sys.exit(0)

# I have prayed to the sudo gods many times.
# Proceed at your own risk.

def firewall_config():
	"""Firewall configuration options."""

	print_section_header("FIREWALL", Fore.BLUE)

	if prompt_yes_no(top_line = "-> Turn on firewall?",
	                 bottom_line = "This helps protect your Mac from being attacked over the internet."):

		print_confirmation("Enabling firewall...")

		# If sudo password incorrect, abort and return from firewall config.
		if sp.run("sudo -E -v", shell=True, stdout=sp.PIPE).returncode != 0:
			print_abort("Firewall")
			return

		# Load default firewall config.
		sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchDaemons/com.apple.alf.agent.plist'], stdout=sp.PIPE)
		sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchAgents/com.apple.alf.useragent.plist'], stdout=sp.PIPE)
		sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)

		# Logging
		if prompt_yes_no(top_line = "-> Turn on logging?",
		                 bottom_line = "If there IS an infection, logs are useful for determining the source."):
			print_confirmation("Enabling logging...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)

		# Stealth Mode
		if prompt_yes_no(top_line = "-> Turn on stealth mode?",
		                 bottom_line = "Your Mac will not respond to ICMP ping requests or connection attempts from closed TCP and UDP networks."):
			print_confirmation("Enabling stealth mode...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)

		# Automatic software whitelisting
		if prompt_yes_no(top_line = "-> Prevent automatic software whitelisting?", bottom_line = "Both Built-in and downloaded software will require user approval for whitelisting."):
			print_confirmation("Preventing automatic whitelisting...")
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
			sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)

		print_confirmation("Resetting firewall to finalize changes...")
		sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)


def captive_portal_config():
	"""Captive Portal configuration options."""

	print_section_header("CAPTIVE PORTAL", Fore.BLUE)

	if prompt_yes_no(top_line = "-> Disable Captive Portal Assistant and force login through browser on untrusted networks?",
	                 bottom_line = "Captive Portal could be triggered and direct you to a malicious site WITHOUT any user interaction."):
		print_confirmation("Disabling Captive Portal Assistant...")
		sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


# TODO: Fix all disable data collection commands. "shell=True" keyword fixed some of them but not all
def user_metadata_config():
	"""User metadata configuration options."""

	print_section_header("USER METADATA", Fore.BLUE)

	###
	# Language Modeling Data
	###

	if prompt_yes_no(top_line = "-> Clear language modeling data?",
	                 bottom_line = "This includes user spelling, typing and suggestion data."):
			print_confirmation("Removing language modeling data...")
			sp.run(['rm', '-rfv', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"']) #, stdout=sp.PIPE)

	# if prompt_yes_no("Disable language modeling data collection?"):
	#       print_confirmation("Disabling language modeling data collection...")
	# 		sp.run(['chmod', '-R', '000', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)
	# 		sp.run(['chflags', '-R', 'uchg', '~/Library/LanguageModeling', '~/Library/Spelling', '~/Library/Suggestions'], stdout=sp.PIPE)

	###
	# QuickLook and Quarantine Data
	###

	if prompt_yes_no(top_line = "-> Clear QuickLook and Quarantine metadata?",
	                 bottom_line = "This will erase your spotlight user data."):
		print_confirmation("Removing QuickLook metadata...")
		sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)
		print_confirmation("Removing Quarantine metadata...")
		sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], shell=True, stdout=sp.PIPE)

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


	# if prompt_yes_no("Disable data collection from downloaded files?"):
	# 	print_confirmation("Disabling Quarantine data collection from downloaded files...")
	# 	sp.call(['sudo', 'chflags', 'schg', '~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], stdout=sp.PIPE)


def user_safety_config():
	"""User Safety configuration options."""

	print_section_header("USER SAFETY", Fore.BLUE)

	if prompt_yes_no(top_line = "-> Lock Mac as soon as screen saver starts?",
	                 bottom_line = "If your screen is black or on screensaver mode, you'll be prompted for a password to login every time."):
		print_confirmation("Configuring account lock on screensaver...")
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)
		sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)

	if prompt_yes_no(top_line = "-> Display all file extensions?",
	                 bottom_line = "This prevents malware from disguising itself as another file type."):
		print_confirmation("Configuring display of all file extensions...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)

	if prompt_yes_no(top_line = "-> Disable saving to the cloud by default?",
	                 bottom_line = "This prevents sensitive documents from being unintentionally stored to the cloud."):
		print_confirmation("Disabling cloud saving by default...")
		sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)

	if prompt_yes_no(top_line = "-> Show hidden files in Finder?",
	                 bottom_line = "This lets you see all files on the system without having to use the terminal."):
		print_confirmation("Displaying hidden files in Finder...")
		sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], shell=True, stdout=sp.PIPE)

	# Reset finder after messing with it.
	print_confirmation("Resetting Finder to finalize changes...")
	sp.run(['killAll', 'Finder'], stdout=sp.PIPE)


def final_configuration():

	print_section_header("FINAL CONFIGURATION STEPS", Fore.BLUE)

	if prompt_yes_no(top_line = "-> Restart your Mac right now?",
	                 bottom_line = "This is necessary for some configuration changes to take effect."):
		print_confirmation("Configuration complete after restart!\n")
		print_confirmation("Restarting in 5 seconds...")
		sleep(1)
		print_confirmation("4...")
		sleep(1)
		print_confirmation("3...")
		sleep(1)
		print_confirmation("2...")
		sleep(1)
		print_confirmation("1...")
		sleep(1)
		if sp.run(['sudo', 'shutdown', '-r', 'now'], shell=True, stdout=sp.PIPE) != 0:
			print(Fore.RED + Style.BRIGHT + "WARNING: Configuration not complete! A full restart is necessary.")

	else:
		print(Fore.RED + Style.BRIGHT + "WARNING: Configuration not complete! A full restart is necessary.")


def lockdown_procedure():

	print_section_header("LOCKDOWN", Fore.BLUE)
	print_confirmation("Configure all settings to the most secure without user interaction. Automatic restart on exit.")

	# Get sudo priv
	sp.run("sudo -E -v", shell=True, stdout=sp.PIPE)

	####
	# FIREWALL
	####

	sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchDaemons/com.apple.alf.agent.plist'], stdout=sp.PIPE)
	sp.run(['sudo', 'launchctl', 'load', '/System/Library/LaunchAgents/com.apple.alf.useragent.plist'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)
	sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)

	####
	# CAPTIVE PORTAL
	####

	sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)

	####
	# USER METADATA
	####

	sp.run(['rm', '-rfv', '"~/Library/LanguageModeling/*"', '"~/Library/Spelling/*"', '"~/Library/Suggestions/*"']) #, stdout=sp.PIPE)
	sp.run(['rm', '-rfv', '"~/Library/Application Support/Quick Look/*"'], stdout=sp.PIPE)
	sp.run([':>~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2'], shell=True, stdout=sp.PIPE)

	####
	# USER SAFETY
	####

	sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPassword', '-int', '1'], stdout=sp.PIPE)
	sp.run(['defaults', 'write', 'com.apple.screensaver', 'askForPasswordDelay', '-int', '0'], stdout=sp.PIPE)
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)
	sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], shell=True, stdout=sp.PIPE)
	sp.run(['killAll', 'Finder'], stdout=sp.PIPE)

	####
	# RESTART
	####

	# TODO
	print("0xCAFEBABE")

	# sp.run(['sudo', 'shutdown', '-r', 'now'], shell=True, stdout=sp.PIPE)

@click.command()
@click.option('-lockdown', is_flag=True, default=False, help="Configure all settings to the most secure without user interaction. Automatic restart on exit.")
@click.option('-v', is_flag=True, default=False, help='display version and author information and exit')
def cli(lockdown, v):
	"""Securely configure your Mac from the terminal."""

	# Print version information
	if v:
		print('stronghold {} by {} -> (Github: {})'.format(Constants.VERSION, Constants.AUTHOR_FULL_NAME, Constants.AUTHOR_GITHUB))
		sys.exit()

	# Lockdown procedures
	if lockdown:
		lockdown_procedure()
		sys.exit()

	# interactive walkthrough
	else:
		splash_intro()
		firewall_config()
		captive_portal_config()
		user_metadata_config()
		user_safety_config()
		final_configuration()

if __name__ == '__main__':
	cli()
