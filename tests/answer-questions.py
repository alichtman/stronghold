"""Answers stronghold's questions in order: No to keeping SSH and Apache, and to the
screen lock (CI cannot type its password); Yes to everything else."""
import sys
import time

import pexpect

QUESTIONS = [
	"I have read the above carefully", "attacked over the internet", "logs are useful",
	"ICMP ping", "remote login will be turned off", "Apache is a web server",
	"enforcing code signing", "approval for whitelisting", "malicious site", "install on their own",
	"spelling, typing and suggestion", "Disable language modeling", "thumbnail cache",
	"Clear Downloads metadata", "metadata collection from Downloads", "SiriAnalytics",
	"screensaver mode", "disguising itself", "stored on the cloud", "use the terminal", "redundancy",
]
NO = {"remote login will be turned off", "Apache is a web server", "screensaver mode"}
CURSOR_QUERY = '\x1b[6n'  # inquirer asks where the cursor is before drawing each question.

child = pexpect.spawn('stronghold', encoding='utf-8', timeout=60, dimensions=(50, 200), logfile=sys.stdout)


def wait_for(pattern):
	while child.expect_exact([pattern, CURSOR_QUERY]) == 1:
		child.send('\x1b[1;1R')  # The reply a real terminal would send.


# readchar discards keys sent before it starts reading, so wait for each menu to be drawn.
for question in QUESTIONS:
	wait_for(question)
	wait_for('No')
	time.sleep(0.3)
	if question in NO:
		child.send('\x1b[B')  # Down arrow, to No.
		wait_for('>  No')
		time.sleep(0.3)
	child.send('\r')
wait_for(pexpect.EOF)
child.close()
# exitstatus is None when stronghold was killed by a signal.
sys.exit(0 if child.exitstatus == 0 and child.signalstatus is None else 1)
