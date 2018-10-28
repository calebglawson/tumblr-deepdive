#!/usr/bin/python2
from collections import defaultdict
from time import sleep
import pytumblr
import json
import threading
import argparse
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta
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

recent_blog_list = []


class RecentBlogThread (threading.Thread):
    def __init__(self, recent_blog_list, blog_name, days_ago, delay):
        threading.Thread.__init__(self)
        self.recent_blog_list = recent_blog_list
        self.blog_name = blog_name
        self.days_ago = days_ago
        self.delay = delay

    def run(self):

        if self.delay > 0:
            sleep(self.delay)

        response = client.posts(self.blog_name + '.tumblr.com',
                                reblog_info=True, notes_info=True, limit=1)

        try:
            for post in response['posts']:
                post_date_time = datetime.strptime(
                    post['date'], '%Y-%m-%d %H:%M:%S %Z')
                if post_date_time >= self.days_ago:
                    self.recent_blog_list.append(self.blog_name)
        except:  # If the post date is too old or the blog does not exist.
            pass


def recentBlogs(blog_names, days_ago):
    threads = []
    iteration = 1
    for blog in blog_names:

        if args.rate_limit != None:
            delay = (args.rate_limit * iteration) / 1000.0
        else:
            delay = 0

        thread = RecentBlogThread(recent_blog_list,
                                  blog, days_ago, delay)
        threads += [thread]
        thread.start()

        iteration += 1

    if args.verbose:
        print "Retrieving posts..."

        for t in tqdm(threads):
            t.join()
    else:
        for t in threads:
            t.join()

    if args.sort_off:
        pass
    else:
        recent_blog_list.sort()

    return recent_blog_list


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "in_file", help="list of blog names to check for recentness")
parser.add_argument(
    "days_ago", help="add days to recentness date", type=int)
parser.add_argument(
    "--out_file", help="list of recent blogs")
parser.add_argument(
    "--rate_limit", help="delay in milliseconds between requests", type=int)
parser.add_argument(
    "--sort_off", help="turn off alphabetic sorting", action="store_true")
parser.add_argument(
    "--verbose", help="indicate progress", action="store_true")
args = parser.parse_args()

if args.days_ago <= 0:
    print("Input an amount of days greater than zero.")
    exit()

client = common.initiateClient()
blog_names = common.readInFile(args.in_file, args.verbose)
days_ago = datetime.now() - timedelta(days=args.days_ago)
results = recentBlogs(blog_names, days_ago)
common.displayResults(results, args.out_file, args.verbose)
