# stronghold

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/alichtman/stronghold/blob/master/LICENSE)
<!-- [![GitHub release](https://img.shields.io/github/release/qubyte/rubidium.svg)](https://github.com/alichtman/stronghold) -->
![status](https://img.shields.io/pypi/status/Django.svg)

`stronghold` is the easiest way to securely configure your Mac.

![GIF demo](img/demo.gif)

Designed for MacOS Sierra and High Sierra.
Previously `fortify`.

**`stronghold` is featured on these lists!**

* [awesome-cli-apps](https://github.com/agarrharr/awesome-cli-apps)
* [awesome-mac](https://github.com/jaywcjlove/awesome-mac)
* [awesome-shell](https://github.com/alebcay/awesome-shell)
* [open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
* [osx-and-ios-security-awesome](https://github.com/ashishb/osx-and-ios-security-awesome)
* [python-macadmin-tools](https://github.com/timsutton/python-macadmin-tools)
* [tools-osx](https://github.com/morgant/tools-osx)

**Usage**
---

```
Usage: stronghold.py [OPTIONS]

  Securely configure your Mac.
  Developed by Aaron Lichtman -> (Github: alichtman)


Options:
  -lockdown  Set secure configuration without user interaction.
  -info      Display version and author information and exit.
  -help, -h  Show this message and exit.
```

**Installation Options**
---

1. Install with [`pip`](https://pypi.org/project/stronghold/)
    + `$ pip install stronghold`
    + `$ stronghold`

2. Download the `stronghold` binary from Releases tab.


**Configuration Options**
---

1. Firewall

    + Enable Firewall?
    	- This helps protect your Mac from being attacked over the internet by viruses and worms.
    + Enable Logging?
    	- If there is an infection, logs are helpful for determining the source.
    + Enable Stealth Mode?
    	- If enabled, your Mac will not respond to network discovery attempts with ICMP ping requests, and will not answer connection attempts made from closed TCP and UDP networks.

2. System Protection

    + Enable Gatekeeper?
    	- Protect against malware by enforcing code signing and verifying downloaded applications before letting them to run.
    + Prevent automatic software whitelisting?
    + Disable Captive Portal Assistant and force login through browser on untrusted networks?
    	- On an untrusted network, Captive Portal could be triggered and direct you to a malicious site WITHOUT any user interaction.


3. User Metadata Storage

    + Clear language modeling data?
    	- This includes user spelling and suggestion data.
    + Disable language modeling data collection?
    + Clear QuickLook metadata?
    + Clear Downloads metadata?
    + Disable metadata collection from Downloads?
    + Clear SiriAnalytics database?

4. User Safety

    + Lock Mac as soon as screen saver starts?
    + Display all file extensions?
    	- This prevents malware from disguising itself as another file type.
    + Disable saving documents to the cloud by default?
    + Show hidden files in Finder?
    	- This lets you see all files on the system without having to use the terminal.


**Sources**
-----

+ https://github.com/drduh/macOS-Security-and-Privacy-Guide
+ http://newosxbook.com/files/moxii3/AppendixA.pdf
+ https://pleiades.ucsc.edu/hyades/PF_on_Mac_OS_X

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/stronghold -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes
