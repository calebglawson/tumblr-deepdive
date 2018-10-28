#!/usr/bin/python2
from collections import defaultdict
import argparse
import common

result = []  # Global for recursion in getPost


def getPost(blog_url, post_id):
    response = client.posts(
        blog_url, id=post_id, reblog_info=True, limit=1)
    try:
        for post in response['posts']:
            reblogged_from_name = post['reblogged_from_name']
            reblogged_from_id = post['reblogged_from_id']
            result.append(reblogged_from_name)
            getPost(reblogged_from_name + ".tumblr.com",
                    reblogged_from_id)  # Recursion
    except:
        pass

    if args.sort_on:
        result.sort()

    return result


def parsePostUrl(post_url):
    try:
        http_index = post_url.find("://") + 3
        end_blog_name_index = post_url.find(".tumblr.com")
        post_id_index = post_url.find("post/") + 5
        end_post_id_index = post_url[post_id_index:].find("/") + post_id_index

        blog_name = post_url[http_index:end_blog_name_index]
        post_id = post_url[post_id_index:end_post_id_index]

        return blog_name, post_id
    except:
        print("Failed to parse post url.")
        exit()


# CONTROL CENTER
parser = argparse.ArgumentParser()
parser.add_argument(
    "post_url", help="full url of blog post")
parser.add_argument(
    "--out_file", help="save results to file")
parser.add_argument(
    "--sort_on", help="turn on alphabetic sorting", action="store_true")
parser.add_argument(
    "--verbose", help="print progress to screen", action="store_true")
args = parser.parse_args()
client = common.initiateClient()
blog_name, post_id = parsePostUrl(args.post_url)
if args.verbose:
    print("Please be patient, recursing through the reblog chain can take some time...")
result = getPost(blog_name + ".tumblr.com", post_id)
common.displayResults(result, args.out_file, args.verbose)
