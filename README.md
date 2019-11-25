# Absolute Path Length

Walk a directory and provide a report of all files which exceed the specified absolute path length.

## Installation

Run the script. There are no 3rd party dependencies.

## Usage

```
$ python3 run.py -h
usage: run.py [-h] [-d /home/user/] [-c NUM] [-l] [-q] [-r] [-v] [-w NUM]

optional arguments:
  -h, --help            show this help message and exit
  -d /home/user/, --directory /home/user/
                        Path to directory of files and folders to check length
                        of. Default: Current directory
  -c NUM, --crit NUM    Generate critical length log for absolute path if
                        equal or greater than the specified value. Default:
                        255
  -l, --logging         Write all logs to a file. Not necessary if saving a
                        report. Default: False
  -q, --quiet           Don't log anything to console or the log file. Useful
                        when paired with --report. Default: False
  -r, --report          Generate CSV report of files matching warn and
                        critical lengths. Output: files-to-review.csv |
                        Default: False
  -v, --verbose         Show debug level details in console and log file (if
                        enabled).Default: False
  -w NUM, --warn NUM    Generate warn length log for absolute path if equal or
                        greater than the specified value. Default: 255
```

## Example

```
$ python3 run.py
2019-11-25 01:22:12,976 [WARNING] [Length 232] /home/exampuser/Documents/Projects/absolute-path-length/examples/super-long-folder-name-for-no-good-reason/lets-make-another one and change the format too/my-really_long_filename-that I came up with_from_the_back-of a cereal box.txt
2019-11-25 01:22:12,976 [CRITICAL] [Length 453] /home/exampuser/Documents/Projects/absolute-path-length/examples/super-long-folder-name-for-no-good-reason/lets-make-another one and change the format too/but wait there is more/there is always more and we must go deeper and deeper and deeper and deeper/keep going - youre almost there - good job/did you make a wrong turn -- what are you doing all the way out here/super-secret but not really so secret secretive plans to challenge max file lengths.txt
2019-11-25 01:22:12,976 [INFO] Completed! Total elapsed time 0:00:00.001821.
2019-11-25 01:22:12,976 [INFO] Processed 50 total files, with 1 warning and 1 critical matches.
```
