#
# Regular cron jobs for the canaima-instalador package
#
0 4	* * *	root	[ -x /usr/bin/canaima-instalador_maintenance ] && /usr/bin/canaima-instalador_maintenance
