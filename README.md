# stronghold

<!-- TODO: Get high quality static images -->
<!--
[![build](https://img.shields.io/wercker/ci/wercker/docs.svg)]() -->
<!-- ![Made With Python](img/made-with-python.png) -->
<!-- ![PRs Welcome](img/PRs-welcome.png) -->
<!-- Add Travis CI -->
<!-- [![Build Status](https://travis-ci.org/bevacqua/awesome-badges.svg?branch=master)](https://travis-ci.org/bevacqua/awesome-badges) -->

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/alichtman/stronghold/blob/master/LICENSE)
![status](https://img.shields.io/pypi/status/Django.svg)

`stronghold` is the easiest way to securely configure your Mac.

![GIF demo](img/demo.gif)

Designed for MacOS Sierra and High Sierra.
Previously `fortify`.

**`stronghold` is featured on these lists!**

* [awesome-cli-apps](https://github.com/agarrharr/awesome-cli-apps)
* [awesome-mac](https://github.com/jaywcjlove/awesome-mac)
* [open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
* [osx-and-ios-security-awesome](https://github.com/ashishb/osx-and-ios-security-awesome)
* [python-macadmin-tools](https://github.com/timsutton/python-macadmin-tools)
* [tools-osx](https://github.com/morgant/tools-osx)

**Warnings**
---

+ Ensure you have up-to-date backups. This script modifies system settings and there is always a possibility that it will damage your system.

**Installation Options**
---

1. Install with [`pip`](https://pypi.org/project/stronghold/)
    + `$ pip install stronghold`
    + `$ stronghold`

2. Download `stronghold` as a zip
    + Unzip
    + `cd` into directory
    + `$ python3 stronghold.py`


**Configuration Options**
---

1. Connectivity

    + Enable Firewall? This helps protect your Mac from being attacked over the internet by viruses and worms.
        - Enable Logging? If there is an infection, logs are helpful for determining the source.
        - Enable Stealth Mode? If enabled, your Mac will not respond to network discovery attempts with ICMP ping requests, and will not answer connection attempts made from closed TCP and UDP networks.
        - Prevent both built-in and downloaded software from being whitelisted automatically?

    + Disable Captive Portal Assistant and force login through browser? With default Mac settings on an untrusted network, an attacker could trigger Captive Portal and direct you to a site with malware WITHOUT user interaction.

2. User Metadata Storage

    + Clear language modeling data? This includes user spelling and suggestion data.
    + Clear QuickLook metadata?
    + Clear SiriAnalytics database?
        - WARNING: This may kill Siri.
    + Clear Quarantine Data.

3. General Safety

    + Lock Mac as soon as screen saver starts?
    + Display all file extensions? This prevents malware from disguising itself as another file type.
    + Disable saving documents to the cloud by default?
    + Show hidden files in Finder? This lets you see all files on the system without having to use the terminal.


**Sources**
-----

+ https://github.com/drduh/macOS-Security-and-Privacy-Guide
+ http://newosxbook.com/files/moxii3/AppendixA.pdf
+ https://pleiades.ucsc.edu/hyades/PF_on_Mac_OS_X

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/stronghold -b [name_for_new_branch]`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes
