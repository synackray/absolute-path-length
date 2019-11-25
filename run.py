#!/usr/bin/env python3
"""Walk a directory and provide a report of all files which exceed the
specified absolute path length."""

import os
import argparse
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt

# Logging configuration
DEFAULT_LOG_LEVEL = "info" # Debug, Info, Warn, Error, Critical
log = logging.getLogger(__name__)
log_stream = logging.StreamHandler()
log.setLevel(getattr(logging, DEFAULT_LOG_LEVEL.upper()))
log_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
    )
log_stream.setFormatter(log_format)
log.addHandler(log_stream)


def main():
    """Main function to collect user arguments and execute functions"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--directory", metavar="/home/user/",
        default="./", type=str,
        help="Path to directory of files and folders to check length of. "
             "Default: Current directory"
        )
    parser.add_argument(
        "-c", "--crit", metavar="NUM",
        default=255, type=int,
        help="Generate critical length log for absolute path if equal or "
             "greater than the specified value. Default: 255"
        )
    parser.add_argument(
        "-l", "--logging", action="store_true",
        help="Write all logs to a file. Not necessary if saving a report. "
             "Default: False"
        )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Don't log anything to console or the log file. Useful when "
             "paired with --report. Default: False"
        )
    parser.add_argument(
        "-r", "--report", action="store_true",
        help="Generate CSV report of files matching warn and critical lengths. "
        "Output: files-to-review.csv | Default: False"
        )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show debug level details in console and log file (if enabled)."
             "Default: False"
        )
    parser.add_argument(
        "-w", "--warn", metavar="NUM",
        default=225, type=int,
        help="Generate warn length log for absolute path if equal or "
             "greater than the specified value. Default: 255"
        )
    args = parser.parse_args()
    # Adjusts logging if requested
    if args.logging:
        log_file = RotatingFileHandler(
            filename=f"{os.getcwd().split('/')[-1]}.log",
            maxBytes=10 * 1024 * 1024,  # Bytes to Megabytes
            backupCount=5
            )
        log_file.setFormatter(log_format)
        log.addHandler(log_file)
    if args.quiet:
        logging.disable(logging.CRITICAL)
    if args.verbose:
        log.setLevel(getattr(logging, "DEBUG"))
    # Process path
    parse_path(
        path=args.directory, path_crit_length=args.crit,
        path_warn_length=args.warn, report=args.report
        )

def parse_path(path, path_crit_length, path_warn_length, report):
    """Walks the specified directory and checks the lengths of all files and
    sub-directories within it."""
    crit_count, warn_count, total_count = 0, 0, 0
    dir_sep = "\\" if os.name == "nt" else "/"
    start_time = dt.now()
    # Initiate report if requested
    if report:
        file_out = "files-to-review.csv"
        with open(file_out, "w") as file:
            file.write("level,length, path\n")
    for item in os.walk(os.path.expanduser(path) + dir_sep):
        folder = item[0]
        files = item[-1]
        log.debug("Parsing files in directory: %s", folder)
        for file in files:
            log.debug("Parsing file: %s", file)
            abs_path = os.path.abspath(folder) + dir_sep
            full_path = abs_path + file
            if len(full_path) >= path_crit_length:
                log.critical("[Length %s] %s", len(full_path), full_path)
                crit_count += 1
                if report:
                    with open(file_out, "a") as f:
                        f.write(f'critical,{len(full_path)},"{full_path}"\n')
            elif len(full_path) >= path_warn_length:
                log.warning("[Length %s] %s", len(full_path), full_path)
                warn_count += 1
                if report:
                    with open(file_out, "a") as f:
                        f.write(f'warning,{len(full_path)},"{full_path}"\n')
            else:
                log.debug("[Length %s] %s", len(full_path), full_path)
                total_count += 1
    end_time = dt.now()
    log.info("Completed! Total elapsed time %s.", (end_time - start_time))
    log.info(
        "Processed %s total files, with %s warning and %s " \
        "critical matches.",
        total_count, warn_count, crit_count
        )
    if report:
        log.info("Saved report to 'file-to-review.csv'.")


if __name__ == "__main__":
    main()
