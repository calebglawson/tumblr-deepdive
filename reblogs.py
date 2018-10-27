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

http_error_codes = defaultdict(int)


class GetPostsThread (threading.Thread):
    def __init__(self, reblogged_from_list, blog_name, offset, limit, delay):
        threading.Thread.__init__(self)
        self.reblogged_from_list = reblogged_from_list
        self.blog_name = blog_name
        self.offset = offset
        self.limit = limit
        self.delay = delay

    def run(self):

        if self.delay > 0:
            sleep(self.delay)

        response = client.posts(self.blog_name + '.tumblr.com',
                                reblog_info=True, notes_info=True, offset=self.offset, limit=self.limit)

        try:
            for post in response['posts']:
                if post.get('reblogged_from_name'):
                    if post['reblogged_from_name'] in self.reblogged_from_list.keys():
                        self.reblogged_from_list[post['reblogged_from_name']] += 1
                    else:
                        self.reblogged_from_list[post['reblogged_from_name']] = 1
        except:
            error = str(response['meta']['status']) + \
                " - " + response['meta']['msg'] + ";"
            if error in http_error_codes.keys():
                http_error_codes[error] += 1
            else:
                http_error_codes[error] = 1


def getPosts(blog_name, max_posts):
    reblogged_from_list = defaultdict(int)
    threads = []
    offset = 0
    iteration = 1
    while max_posts - offset > 0:
        # Tumblr will return a max of 20 posts per API call
        # Used to set limit when max_posts is not evenly divisible by 20
        limit = max_posts - offset

        # If the limit is greater than 20, then we grab the next 20 and fetch more in the next iteration.
        # If limit is zero, then all posts for a given blog are being fetched.
        if limit > 20 or limit <= 0:
            limit = 20

        if args.rate_limit != None:
            delay = (args.rate_limit * iteration) / 1000.0
        else:
            delay = 0

        thread = GetPostsThread(reblogged_from_list,
                                blog_name, offset, limit, delay)
        threads += [thread]
        thread.start()

        offset += 20
        iteration += 1

    if args.verbose:
        print "Retrieving posts..."

        bar = progressbar.ProgressBar()
        for t in bar(threads):
            t.join()
    else:
        for t in threads:
            t.join()

    return reblogged_from_list


def printInOrder(dictionary, descending, limit, outfile):

    if outfile != None:
        try:
            outfile = open(args.out_file, "w")
        except:
            print("Output file failed to write.")
            exit()

    if len(dictionary) > 0:

        if limit == 0:  # If the limit is 0, then we will print all.
            limit = len(dictionary)

        count = 0
        for i in sorted(dictionary, key=dictionary.__getitem__, reverse=descending):

            if args.threshold == None:  # Then, the option is not used.
                pass
            # Then, the item is above the threshold.
            elif args.threshold < dictionary[i]:
                pass
            elif ";" in i:  # Then, it is an HTTP Error code and we should display anyway.
                pass
            else:  # The item violates the threshold.
                break

            # If count is less than the limit, then we print.
            if (count <= limit):
                print(i + " " + str(dictionary[i]))
                if outfile != None:
                    outfile.write(i + '\n')
                count += 1
            else:
                break

        if outfile != None:
            outfile.close()
            if args.verbose:
                print("\nOutput file written successfully.")


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "blog_name", help="the name of the blog you are searching on")
parser.add_argument(
    "max_posts", help="the maximum amount of posts to take into consideration", type=int)
parser.add_argument(
    "--out_file", help="output list of blogs to file")
parser.add_argument(
    "--rate_limit", help="delay in milliseconds between requests", type=int)
parser.add_argument(
    "--max_print", help="maximum blogs to print", type=int)
parser.add_argument(
    "--threshold", help="blogs must have a equal or greater than this number",  type=int)
parser.add_argument(
    "--verbose", help="indicate progress", action="store_true")
parser.add_argument(
    "--ascending", help="print blogs in ascending order", action="store_true")
args = parser.parse_args()

result = getPosts(args.blog_name, args.max_posts)

if len(http_error_codes) > 0:
    print "\nHTTP Error Codes Occured: "
    printInOrder(http_error_codes, True, 0, args.out_file)

printInOrder(result, False if args.ascending == True else True,
             0 if args.max_print == None else args.max_print, args.out_file)
