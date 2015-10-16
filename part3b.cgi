#!/bin/sh
#
# cgi program to generate html tables from local Unix commands
#
	echo "Content-type: text/html"
	echo ""
	echo "<html><body style='background-color: white;'>"
	echo "<p>Here are routes to other computers:"
	/sbin/route | ./tt2ht1
	echo "<p>Here are the current files:</p>"
	ls -l | ./tt2ht1
	echo "<p>Here is fstab:</p>"
	./tt2ht1 < /etc/fstab
	echo "<p>Here is train 1205:</p>"
	(cd /home/l/i/lib113/lectures/lect04/5_Code/cgi; ./trainsched 1205) | ./tt2ht1
	echo "</body></html>"
