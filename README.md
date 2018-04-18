# H1 Report Browser
## Author: Matthew A. Weidner

These scripts provide a system that will download and import newly disclosed HackerOne bug bounty reports into a SQLite3 database. This allows for offline browsing using a ncurses terminal based interface for Unix/Linux based computers. Compatible with Cygwin for Windows.

* h1-browser.py:
Ncurses terminal based HackerOne report browser. Uses an offline cache of HackerOne reports stored in a SQLite3 database.

* h1-dl-reports.py:
Utilizes h1.nobbd.de public web service to download newle published reports from HackerOne. Stages raw json reports for merging into database.

* h1_stats.py:
Calculates bounty statistics from HackerOne reports.

* import_new_reports.py:
Imports new reports from staging area into SQLite database.

* import_reports.py:
Imports all reports from staging area into SQLite database.

* systemd/h1reports.timer
Systemd timer file for recurring daily download and import newly disclosed bug bounty reports.

* systemd/h1reports.service
Systemd service file. Pairs with the timer file for automated daily download and import of newly disclosed bug bounty reports.

