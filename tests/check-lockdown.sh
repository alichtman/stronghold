#!/bin/bash
# Reads back each setting stronghold -lockdown changes. Exits 1 if any is wrong.
fw=/usr/libexec/ApplicationFirewall/socketfilterfw
status=0

check() {
	local name=$1 expected=$2 output
	shift 2
	output=$("$@" 2>&1)
	if grep -Eqi -- "$expected" <<< "$output"; then
		echo "ok    $name"
	else
		echo "FAIL  $name: $output"
		status=1
	fi
}

check "Firewall on" 'firewall is enabled' $fw --getglobalstate
check "Stealth mode on" 'stealth mode (enabled|is on)' $fw --getstealthmode
[ "$(sw_vers -productVersion | cut -d. -f1)" -ge 15 ] || check "Firewall logging on" 'log mode is on' $fw --getloggingmode
check "Signed apps need approval" '^2$' sh -c "$fw --getallowsigned | grep -c DISABLED"
check "Gatekeeper on" '^assessments enabled' spctl --status
check "Captive portal off" '^0$' defaults read /Library/Preferences/SystemConfiguration/com.apple.captive.control Active
check "Automatic updates on" '^5$' sh -c "defaults read /Library/Preferences/com.apple.SoftwareUpdate | grep -cE '(AutomaticCheckEnabled|AutomaticDownload|AutomaticallyInstallMacOSUpdates|CriticalUpdateInstall|ConfigDataInstall) = 1;'"
check "App Store updates on" '^1$' defaults read /Library/Preferences/com.apple.commerce AutoUpdate
check "File extensions shown" '^1$' defaults read NSGlobalDomain AppleShowAllExtensions
check "Cloud saving off" '^0$' defaults read NSGlobalDomain NSDocumentSaveNewDocumentsToCloud
check "Hidden files shown" '^1$' defaults read com.apple.finder AppleShowAllFiles
check "Remote Login off" '^Remote Login: Off$' sudo systemsetup -getremotelogin
check "Apache autostart off" '"org.apache.httpd" => disabled' launchctl print-disabled system
# sudo, because Disable language modeling data collection makes the folders unreadable.
check "Language data cleared" '^0$' sudo sh -c "ls $HOME/Library/*/stronghold-test 2>/dev/null | wc -l | tr -d ' '"
check "Downloads history cleared" '^0$' sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2 'SELECT COUNT(*) FROM LSQuarantineEvent'
# Settings only the interactive walk-through offers.
if [ "$1" = interactive ]; then
	check "Printer sharing off" '^_share_printers=0$' cupsctl
	check "Language data collection blocked" 'uchg' ls -lOd "$HOME/Library/Spelling"
	check "Downloads history collection blocked" 'schg' ls -lO "$HOME/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2"
	check "SiriAnalytics cleared" '^0$' sqlite3 ~/Library/Assistant/SiriAnalytics.db "SELECT COUNT(*) FROM sqlite_master WHERE name = 'stronghold_test'"
	check "Other Siri files kept" 'SiriAnalytics.db.backup' ls ~/Library/Assistant
fi
exit $status
