#!/usr/bin/python2
from collections import defaultdict
from time import sleep
from tqdm import tqdm
import pytumblr
import json
import threading
import argparse
import common

# Please generate and enter your own API key/secret and OAuth token/secret.
# You are using this script for your own purposes, and may have added your own customizations.
# You agree to follow Tumblr's API License Agreement and ToS in utilizing any part of the following code.
#   https://www.tumblr.com/policy/en/terms-of-service
#   https://www.tumblr.com/docs/en/api_agreement

# Prior to your first run, register your own application with Tumblr's API to obtain a key.
#   https://www.tumblr.com/oauth/apps
#
# Execute authenticate.py and follow the prompts to generate a config.json file.


class ReturnOnlyExistingBlogsThread (threading.Thread):
    def __init__(self, results, blog_name, delay):
        threading.Thread.__init__(self)
        self.results = results
        self.blog_name = blog_name
        self.delay = delay

    def run(self):

        if self.delay > 0:
            sleep(self.delay)

        self.results.append(client.blog_info(
            self.blog_name + '.tumblr.com'))


def returnOnlyExistingBlogs(dictionary):

    threads = []
    results = []
    clean_dict = []
    iteration = 1

    if len(dictionary) > 0:
        for blog_name in dictionary:

            if args.rate_limit != None:
                delay = (args.rate_limit * iteration) / 1000.0
            else:
                delay = 0

            thread = ReturnOnlyExistingBlogsThread(results, blog_name, delay)
            threads += [thread]
            thread.start()

            iteration += 1

        if args.verbose:
            print "Checking existance of blogs..."

            for t in tqdm(threads):
                t.join()
        else:
            for t in threads:
                t.join()

        for result in results:
            if result.get('meta') and result['meta']['status'] != 200:
                pass
            else:
                blog_name = result['blog']['name']
                clean_dict.append(blog_name)

    if args.sort_off:
        pass
    else:
        clean_dict.sort()

    return clean_dict


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "in_file", help="file of blogs to check for existance and print to screen")
parser.add_argument(
    "--out_file", help="optionally specify the output file of existing blogs")
parser.add_argument(
    "--rate_limit", help="delay in milliseconds between requests", type=int)
parser.add_argument(
    "--verbose", help="indicate progress", action="store_true")
parser.add_argument(
    "--sort_off", help="turn off sorting", action="store_true")
args = parser.parse_args()
client = common.initiateClient()
blog_names = common.readInFile(args.in_file, args.verbose)
results = returnOnlyExistingBlogs(blog_names)
common.displayResults(results, args.out_file, args.verbose)
