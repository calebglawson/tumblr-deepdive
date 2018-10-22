#!/usr/bin/python2
from collections import defaultdict
from time import sleep
import pytumblr
import json
import threading
import argparse
import progressbar
from datetime import datetime

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

fresh_blog_list = []


class FreshBlogThread (threading.Thread):
    def __init__(self, fresh_blog_list, blog_name, cutoff_date, delay):
        threading.Thread.__init__(self)
        self.fresh_blog_list = fresh_blog_list
        self.blog_name = blog_name
        self.cutoff_date = cutoff_date
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
                if post_date_time >= self.cutoff_date:
                    self.fresh_blog_list.append(self.blog_name)
        except:
            pass


def freshBlogs(blog_names, cutoff_date):
    threads = []
    iteration = 1
    for blog in blog_names:

        if args.rate_limit != None:
            delay = (args.rate_limit * iteration) / 1000.0
        else:
            delay = 0

        thread = FreshBlogThread(fresh_blog_list,
                                 blog, cutoff_date, delay)
        threads += [thread]
        thread.start()

        iteration += 1

    if args.verbose:
        print "Retrieving posts..."

        bar = progressbar.ProgressBar()
        for t in bar(threads):
            t.join()
    else:
        for t in threads:
            t.join()

    return fresh_blog_list


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "in_file", help="list of blog names to check for freshness")
parser.add_argument(
    "--out_file", help="list of fresh blogs")
parser.add_argument(
    "--rate_limit", help="delay in milliseconds between requests", type=int)
parser.add_argument(
    "--sort_off", help="turn off alphabetic sorting", action="store_true")
parser.add_argument(
    "--verbose", help="indicate progress", action="store_true")
args = parser.parse_args()

try:
    infile = open(args.in_file, "r")
except:
    print("Input file failed to read.")
    exit()

result = infile.readlines()
infile.close()

if args.verbose:
    print("Input file read successfully.")

cutoff_datetime = datetime.strptime(
    "2018-10-01 00:00:00 GMT", '%Y-%m-%d %H:%M:%S %Z')
result = freshBlogs(result, cutoff_datetime)

if args.sort_off:
    pass
else:
    result.sort()

if args.out_file == None:  # If the output file is not specified, then print to screen.
    for blog in result:
        print(blog.strip("\n"))
else:
    try:
        outfile = open(args.out_file, "w")
    except:
        print("Output file failed to write.")
        exit()

    for blog in result:
        outfile.write(blog.strip("\n") + '\n')
    if args.verbose:
        print("Output file written successfully.")
    outfile.close()
