#!/usr/bin/env python3
import json
import checks
import argparse
from pathlib import Path
from json import JSONDecodeError


parser = argparse.ArgumentParser(description='Apply a benchmark to a Fortigate configuration file. \
        Example: fortigate-security-auditor.py -q data.json')
parser.add_argument('-q', '--quiet', help='Not interactive: ignore manual steps', action='store_true')
parser.add_argument('-v', '--verbose', help='Increase verbosity', action='store_true')
parser.add_argument('-o', '--output', help='Output CSV File')
parser.add_argument('-c', '--resume', help='Resume an audit that was already started. Automatic items are re-checked but manually set values are retrieved from cache.', action='store_true')
parser.add_argument('config', help='if single argument: combine all lines, if multiple arguments: combine lines from all files', nargs=1)
args = parser.parse_args()

filepath = args.config[0]
verbose = args.verbose
quiet = args.quiet
outputfile = args.output

cache_file_path = str(Path.home()) + '/.cache/fortigate-security-auditor.json'

# Create/Open cache file
try:
    cache_file = open(cache_file_path, "r+")
    cache = json.load(cache_file)
    cache_file.close()
    if not filepath in cache.keys():
        # There is no cache for this fortigate configuration file
        cached_results = {}
    else:
        cached_results = cache[filepath]
except JSONDecodeError as e:
    print(e)
    print("[!] Error loading cache file. Re-creating it")
    cache = {}
    cached_results = {}

# Load fortigate configuration file
f = open(filepath)
config = json.load(f)["configs"]
f.close()

print(f'[+] Config file opened: {filepath}')

print('[+] Starting checks')

performed_checks = []

# Instantiate checkers
checkers = [check_class(config, verbose) for check_class in checks.classes()]
checkers.sort()
for checker in checkers:
    if checker.enabled:
        if checker.auto:
            checker.run()
        else:
            if quiet:
                checker.skip()
            else:
                if args.resume:
                    if checker.id in cached_results.keys():
                        # There is a cached result for this check
                        checker.restore_from_cache(cached_results[checker.id])
                    else:
                        # There is no cached result, we have to perform the step
                        checker.run()
                else:
                    checker.run()
        performed_checks.append(checker)

        # Save to cache
        cached_results[checker.id] = {"result": checker.result, "message": checker.message}

print('[+] Finished')
print('------------------------------------------------')
print('[+] Here is a summary:')

for performed_check in performed_checks:
    print(f'[{performed_check.id}]\t[{performed_check.result}]\t{performed_check.title}')

# Save cache file
cache[filepath] = cached_results
cache_file = open(cache_file_path, "w")
json.dump(cache, cache_file)
cache_file.close()

# Export
if outputfile is not None:
    print('------------------------------------------------')
    print('[+] Exporting results in CSV')
    outputfile = open(outputfile,"w+")
    for performed_check in performed_checks:
        line = f'{performed_check.id},{performed_check.result},{performed_check.title}\n'
        outputfile.write(line)
    outputfile.close()
    print('[+] Finished')
