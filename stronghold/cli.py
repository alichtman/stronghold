# STRONGHOLD
# @author Aaron Lichtman

# Built-in modules
import sys
import subprocess as sp
from time import sleep
from shutil import get_terminal_size

# 3rd party modules
import click
import inquirer
from colorama import Fore, Style

# Local modules
from .constants import Constants


def prompt_yes_no(top_line="", bottom_line=""):
	"""Print question and return True or False depending on user selection from list.
	bottom_line should be used for one liners. Otherwise, it's the second line you want printed.

	Deprecated comment: Thanks, @shobrook"""

	# One liner. Only bottom_line should be printed + stylized
	if top_line == "":
		questions = [inquirer.List('choice',
		                           message=Fore.GREEN + Style.BRIGHT + bottom_line + Fore.YELLOW,
		                           choices=[' Yes', ' No'],
		                           ),
		             ]

	# else top_line is not ""
	else:
		print(Fore.GREEN + Style.BRIGHT + " " + top_line)
		questions = [inquirer.List('choice',
		                           message=Fore.GREEN + bottom_line + Fore.YELLOW,
		                           choices=[' Yes', ' No'],
		                           ),
		             ]

	answers = inquirer.prompt(questions)

	# inquirer prints "Cancelled by user" and returns None on Ctrl-C.
	if answers is None:
		sys.exit(1)

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


def disable_service(label):
	"""Stops a launchd system service and keeps it from starting again."""
	sp.run(['sudo', 'launchctl', 'disable', 'system/' + label], stdout=sp.PIPE)
	# bootout reports an error when the service was not running; that is fine.
	sp.run(['sudo', 'launchctl', 'bootout', 'system/' + label], stdout=sp.PIPE, stderr=sp.PIPE)


def macos_version():
	"""Returns the major macOS version, such as 15."""
	return int(sp.run(['sw_vers', '-productVersion'], stdout=sp.PIPE, text=True).stdout.split('.')[0])


###
# Settings, shared by the interactive walk-through and lockdown
###

def enable_firewall():
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setglobalstate', 'on'], stdout=sp.PIPE)


def enable_firewall_logging():
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setloggingmode', 'on'], stdout=sp.PIPE)


def enable_stealth_mode():
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setstealthmode', 'on'], stdout=sp.PIPE)


def reload_firewall():
	sp.run(['sudo', 'pkill', '-HUP', 'socketfilterfw'], stdout=sp.PIPE)


def enable_gatekeeper():
	sp.run(['sudo', 'spctl', '--global-enable'], stdout=sp.PIPE)
	# macOS 15 removed rule labels. There, turning Gatekeeper on also allows Developer ID apps.
	if macos_version() < 15:
		sp.run('sudo spctl --enable --label "Developer ID"', shell=True, stdout=sp.PIPE)


def require_approval_for_signed_apps():
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsigned', 'off'], stdout=sp.PIPE)
	sp.run(['sudo', '/usr/libexec/ApplicationFirewall/socketfilterfw', '--setallowsignedapp', 'off'], stdout=sp.PIPE)


def disable_captive_portal():
	sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/SystemConfiguration/com.apple.captive.control', 'Active', '-bool', 'false'], stdout=sp.PIPE)


def enable_automatic_updates():
	# softwareupdate --schedule on only turns on checking; these also download and install.
	for key in ['AutomaticCheckEnabled', 'AutomaticDownload', 'AutomaticallyInstallMacOSUpdates', 'CriticalUpdateInstall', 'ConfigDataInstall']:
		sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/com.apple.SoftwareUpdate', key, '-bool', 'true'], stdout=sp.PIPE)
	sp.run(['sudo', 'defaults', 'write', '/Library/Preferences/com.apple.commerce', 'AutoUpdate', '-bool', 'true'], stdout=sp.PIPE)


def clear_language_data():
	sp.run('rm -rfv ~/Library/LanguageModeling/* ~/Library/Spelling/* ~/Library/Suggestions/*', shell=True, stdout=sp.PIPE)


def block_language_data():
	sp.run('sudo chmod -R 000 ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions', shell=True, stdout=sp.PIPE)
	sp.run('sudo chflags -R uchg ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions', shell=True, stdout=sp.PIPE)


def clear_quicklook_cache():
	sp.run(['qlmanage', '-r', 'cache'], stdout=sp.PIPE)


def clear_downloads_history():
	sp.run("sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 'DELETE FROM LSQuarantineEvent'", shell=True, stdout=sp.PIPE)


def block_downloads_history():
	sp.run('sudo chflags schg ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2', shell=True, stdout=sp.PIPE)


def clear_siri_analytics():
	# Only the database and its two journal files, not other files that start with its name.
	sp.run('rm -fv ~/Library/Assistant/SiriAnalytics.db ~/Library/Assistant/SiriAnalytics.db-wal ~/Library/Assistant/SiriAnalytics.db-shm', shell=True, stdout=sp.PIPE)


def lock_screen_immediately():
	# macOS no longer reads the screensaver askForPassword preferences. sysadminctl asks
	# for the login password, so its output stays visible.
	sp.run(['sysadminctl', '-screenLock', 'immediate', '-password', '-'])


def show_file_extensions():
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'AppleShowAllExtensions', '-bool', 'true'], stdout=sp.PIPE)


def disable_cloud_saving():
	sp.run(['defaults', 'write', 'NSGlobalDomain', 'NSDocumentSaveNewDocumentsToCloud', '-bool', 'false'], stdout=sp.PIPE)


def show_hidden_files():
	sp.run(['defaults', 'write', 'com.apple.finder', 'AppleShowAllFiles', '-boolean', 'true'], stdout=sp.PIPE)


def disable_printer_sharing():
	sp.run(['cupsctl', '--no-share-printers'], stdout=sp.PIPE)


def restart_finder():
	sp.run(['killAll', 'Finder'], stdout=sp.PIPE)


def splash_intro():
	wordmark = (
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
	      "                                            \"Y88P\n")
	if get_terminal_size().columns >= 112:
		wordmark_lines = wordmark.strip('\n').splitlines()
		for row, castle_line in enumerate(Constants.TERMINAL_CASTLE.splitlines()):
			text = wordmark_lines[row - 4] if 4 <= row < 4 + len(wordmark_lines) else ''
			print(castle_line + '    ' + Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL)
		print()
	else:
		print(Constants.TERMINAL_CASTLE)
		print(Fore.GREEN + Style.BRIGHT + wordmark + Style.RESET_ALL)

	print(Fore.RED + Style.BRIGHT + "Built by Aaron Lichtman. (Github: alichtman)\n" + Style.RESET_ALL)

	print(Fore.BLUE + Style.BRIGHT + "Stronghold is a security configuration tool for macOS 14 and later.")
	print("You may be asked for a sudo password." + Style.RESET_ALL + "\n")

	print_section_header("BEFORE STARTING", Fore.RED)

	print(Fore.RED + Style.BRIGHT + "\t0. Make the terminal window as large as possible.")
	print("\t1. Ensure you have up-to-date system backups.")
	print("\t2. Read the prompts carefully.\n" + Style.RESET_ALL)

	if not prompt_yes_no(bottom_line="I have read the above carefully and want to continue"):
		sys.exit(0)


# I have prayed to the sudo gods many times.
# Proceed at your own risk.

def firewall_config():
	"""Firewall configuration options."""

	print_section_header("FIREWALL", Fore.BLUE)

	if prompt_yes_no(top_line="-> Turn on firewall?",
	                 bottom_line="This helps protect your Mac from being attacked over the internet."):

		print_confirmation("Enabling firewall...")

		# If sudo password incorrect, abort and return from firewall config.
		if sp.run("sudo -v", shell=True, stdout=sp.PIPE).returncode != 0:
			print_abort("Firewall")
			return

		enable_firewall()

		# Logging
		if prompt_yes_no(top_line="-> Turn on logging?",
		                 bottom_line="If there IS an infection, logs are useful for determining the source."):
			print_confirmation("Enabling logging...")
			enable_firewall_logging()

		# Stealth Mode
		if prompt_yes_no(top_line="-> Turn on stealth mode?",
		                 bottom_line="Your Mac will not respond to ICMP ping requests or connection attempts from closed TCP and UDP networks."):
			print_confirmation("Enabling stealth mode...")
			enable_stealth_mode()

		# Remote login
		if not prompt_yes_no(top_line="-> Do you use SSH?",
						 bottom_line="If no, remote login will be turned off."):
			print_confirmation("Disabling ssh daemon...")
			# systemsetup -setremotelogin needs Full Disk Access on macOS 14 and later; launchctl does not.
			disable_service('com.openssh.sshd')

		# Apache server
		if not prompt_yes_no(top_line="-> Do you want Apache to autostart?",
							 bottom_line="Apache is a web server. If you are unfamiliar with it, disable it."):
			print_confirmation("Disabling httpd...")
			disable_service('org.apache.httpd')

		print_confirmation("Resetting firewall to finalize changes...")
		reload_firewall()


def system_protection_config():
	"""System protection configuration options."""

	print_section_header("GENERAL SYSTEM PROTECTION", Fore.BLUE)

	# Enable Gatekeeper
	if prompt_yes_no(top_line="-> Enable Gatekeeper?",
	                 bottom_line="Defend against malware by enforcing code signing and verifying downloaded applications before letting them to run."):
		print_confirmation("Enabling Gatekeeper...")
		enable_gatekeeper()

	# Disable automatic software whitelisting
	if prompt_yes_no(top_line="-> Prevent automatic software whitelisting?",
	                 bottom_line="Both built-in and downloaded software will require user approval for whitelisting."):
		print_confirmation("Preventing automatic whitelisting...")
		require_approval_for_signed_apps()

	# Captive Portal
	if prompt_yes_no(top_line="-> Disable Captive Portal Assistant and force login through browser on untrusted networks?",
	                 bottom_line="Captive Portal could be triggered and direct you to a malicious site WITHOUT any user interaction."):
		print_confirmation("Disabling Captive Portal Assistant...")
		disable_captive_portal()

	# Automatic updates
	if prompt_yes_no(top_line="-> Turn on automatic software updates?",
	                 bottom_line="macOS, security and App Store updates install on their own. Your Mac may restart to finish."):
		print_confirmation("Turning on automatic software updates...")
		enable_automatic_updates()


def metadata_storage_config():
	"""User metadata configuration options."""

	print_section_header("METADATA STORAGE", Fore.BLUE)

	###
	# Language Modeling Data
	###

	if prompt_yes_no(top_line="-> Clear language modeling metadata?",
	                 bottom_line="This includes user spelling, typing and suggestion data."):
		print_confirmation("Removing language modeling data...")
		clear_language_data()

	if prompt_yes_no(bottom_line="-> Disable language modeling data collection?"):
		print_confirmation("Disabling language modeling data collection...")
		block_language_data()

	###
	# QuickLook and Quarantine Data
	###

	if prompt_yes_no(top_line="-> Clear QuickLook metadata?",
	                 bottom_line="This resets the Quick Look thumbnail cache."):
		print_confirmation("Removing QuickLook metadata...")
		clear_quicklook_cache()

	###
	# Downloads Metadata
	###

	if prompt_yes_no(bottom_line="-> Clear Downloads metadata?"):
		print_confirmation("Removing Downloads metadata...")
		clear_downloads_history()

	if prompt_yes_no(bottom_line="-> Disable metadata collection from Downloads?"):
		print_confirmation("Disabling Quarantine data collection from downloaded files...")
		block_downloads_history()

	###
	# Siri Metadata
	###

	if prompt_yes_no(bottom_line="-> Clear SiriAnalytics database?"):
		print_confirmation("Clearing SiriAnalytics database...")
		clear_siri_analytics()


def user_safety_config():
	"""User Safety configuration options."""

	print_section_header("USER SAFETY", Fore.BLUE)

	if prompt_yes_no(top_line="-> Lock Mac as soon as screen saver starts?",
	                 bottom_line="If your screen is black or on screensaver mode, you'll be prompted for a password to login every time."):
		print_confirmation("Configuring account lock on screensaver...")
		lock_screen_immediately()

	if prompt_yes_no(top_line="-> Display all file extensions?",
	                 bottom_line="This prevents malware from disguising itself as another file type."):
		print_confirmation("Configuring display of all file extensions...")
		show_file_extensions()

	if prompt_yes_no(top_line="-> Disable saving to the cloud by default?",
	                 bottom_line="This prevents sensitive documents from being unintentionally stored on the cloud."):
		print_confirmation("Disabling cloud saving by default...")
		disable_cloud_saving()

	if prompt_yes_no(top_line="-> Show hidden files in Finder?",
	                 bottom_line="This lets you see all files on the system without having to use the terminal."):
		print_confirmation("Displaying hidden files in Finder...")
		show_hidden_files()

	if prompt_yes_no(top_line="-> Disable printer sharing?",
	                 bottom_line="Offers redundancy in case the Firewall was not configured."):
		print_confirmation("Disabling printer sharing...")
		disable_printer_sharing()


	# Reset finder after messing with it.
	print_confirmation("Resetting Finder to finalize changes...")
	restart_finder()


def final_configuration():
	print_section_header("FINAL CONFIGURATION STEPS", Fore.BLUE)

	print(Fore.RED + Style.BRIGHT + "WARNING: Secure Configuration not complete! At a minimum, a full restart is necessary." + Style.RESET_ALL)
	print(Fore.YELLOW + Style.BRIGHT + "\nNEXT STEPS...\n")
	print("1. Fully disable Siri: https://apple.stackexchange.com/a/258981")
	print("2. Enable FileVault. (Check if it's enabled by running `$ fdesetup status`)")
	print("3. Make sure everything in the Settings > Sharing menu is disabled if you're not using it.")
	print("4. For the most secure configuration, check out Objective-See's Free OSX Security Tools: https://objective-see.com/products.html")
	print("\nIf you have any suggestions for stronghold, open an issue at: https://github.com/alichtman/stronghold/issues/new" + Style.RESET_ALL)
	sys.exit()



def lockdown_procedure():
	"""Set secure config without any user interaction."""
	print("----------")
	print_section_header("LOCKDOWN", Fore.BLUE)
	print_confirmation("Set secure configuration without user interaction.")

	# Get sudo priv
	sp.run("sudo -v", shell=True, stdout=sp.PIPE)

	####
	# FIREWALL
	####

	enable_firewall()
	enable_firewall_logging()
	enable_stealth_mode()
	reload_firewall()

	####
	# SYSTEM PROTECTION
	####

	enable_gatekeeper()
	require_approval_for_signed_apps()
	disable_captive_portal()
	enable_automatic_updates()

	####
	# METADATA STORAGE
	####

	clear_language_data()
	clear_quicklook_cache()
	clear_downloads_history()

	####
	# DAEMONS
	####

	disable_service('com.openssh.sshd')
	disable_service('org.apache.httpd')

	####
	# USER SAFETY
	####

	lock_screen_immediately()
	show_file_extensions()
	disable_cloud_saving()
	show_hidden_files()
	restart_finder()

	####
	# RESTART
	####

	final_configuration()


# Click custom help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '-help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-lockdown', is_flag=True, default=False, help="Set secure configuration without user interaction.")
@click.option('-v', is_flag=True, default=False, help='Display version and author information and exit.')
def cli(lockdown, v):
	"""Securely configure your Mac.

	Developed by Aaron Lichtman -> (Github: alichtman)"""

	# Print author and version information and exit
	if v:
		print('stronghold v{0} by {1} -> Github: {2}'.format(Constants.VERSION,
		                                                     Constants.AUTHOR_FULL_NAME,
		                                                     Constants.AUTHOR_GITHUB,))
		sys.exit()

	# Lockdown
	if lockdown:
		lockdown_procedure()

	# interactive walk-through
	else:
		splash_intro()
		firewall_config()
		system_protection_config()
		metadata_storage_config()
		user_safety_config()
		final_configuration()

