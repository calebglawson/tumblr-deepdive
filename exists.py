#!/usr/bin/python2
from collections import defaultdict
from time import sleep
import pytumblr
import json
import threading
import argparse
import progressbar

# Please generate and enter your own API key/secret and OAuth token/secret.
# You are using this script for your own purposes, and may have added your own customizations.
# You agree to follow Tumblr's API License Agreement and ToS in utilizing any part of the following code.
#   https://www.tumblr.com/policy/en/terms-of-service
#   https://www.tumblr.com/docs/en/api_agreement

# Prior to your first run, register your own application with Tumblr's API to obtain a key.
#   https://www.tumblr.com/oauth/apps
#
# Execute authenticate.py and follow the prompts to generate a config.json file.

try:
    filename = "config.json"
    f = open(filename, "r")
    read = f.read()
    f.close()
    load = json.loads(read)

    client = pytumblr.TumblrRestClient(
        load["consumer_key"],
        load["consumer_secret"],
        load["oauth_token"],
        load["oauth_token_secret"]
    )
except:
    print("Client could not be authenticated, please (re)authenticate by executing authenticate.py")
    exit()


class ReturnOnlyExistingBlogsThread (threading.Thread):
    def __init__(self, results, blog_name, delay):
        threading.Thread.__init__(self)
        self.results = results
        self.blog_name = blog_name
        self.delay = delay

    def run(self):

        if self.delay > 0:
            sleep(self.delay)

        self.results.append(client.blog_info(self.blog_name + '.tumblr.com'))


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
            bar = progressbar.ProgressBar()
            for t in bar(threads):
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

    return clean_dict


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "infile", type=argparse.FileType('r'), help="file of blogs to check for existance")
parser.add_argument(
    "outfile", type=argparse.FileType('w'), help="output file of existing blogs")
parser.add_argument(
    "--rate_limit", help="delay in milliseconds between requests", type=int)
parser.add_argument(
    "--verbose", help="indicate progress", action="store_true")
parser.add_argument(
    "--sort_off", help="turn off sorting", action="store_true")
args = parser.parse_args()

try:
    result = args.infile.readlines()
except:
    args.infile.close()
    print("File failed to read.")
args.infile.close()

result = returnOnlyExistingBlogs(result)

if args.sort_off:
    pass
else:
    result.sort()

try:
    for blog in result:
        args.outfile.write(blog + '\n')
except:
    args.outfile.close()
    print("File failed to write.")
args.outfile.close()
