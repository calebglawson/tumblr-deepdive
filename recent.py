#!/usr/bin/python2
from collections import defaultdict
from time import sleep
import pytumblr
import json
import threading
import argparse
import progressbar
from datetime import datetime
from datetime import timedelta

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

        bar = progressbar.ProgressBar()
        for t in bar(threads):
            t.join()
    else:
        for t in threads:
            t.join()

    if args.sort_off:
        pass
    else:
        recent_blog_list.sort()

    return recent_blog_list


def readInFile(file_name):
    try:
        infile = open(file_name, "r")
    except:
        print("Input file failed to read.")
        exit()

    blogs = infile.readlines()
    # If we close the file now, we can write to the same file later.
    infile.close()

    if args.verbose:
        print("Input file read successfully.")

    return blogs


def displayResults(result):
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

blog_names = readInFile(args.in_file)
days_ago = datetime.now() - timedelta(days=args.days_ago)
results = recentBlogs(blog_names, days_ago)
displayResults(results)
