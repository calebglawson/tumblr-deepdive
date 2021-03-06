#!/usr/bin/python2
from collections import defaultdict
import argparse
import common


def getNotes(blog_url, post_id):
    result = []
    response = client.posts(
        blog_url, id=post_id, notes_info=True, limit=1)
    try:
        for post in response['posts']:
            for note in post['notes']:
                if args.likes and note['type'] == "like":
                    result.append(note['blog_name'])
                elif args.reblogs and note['type'] == "reblog":
                    result.append(note['blog_name'])
    except:
        print("Failed to parse response for notes.")

    if args.sort_off:
        pass
    else:
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
group = parser.add_mutually_exclusive_group(required=True)
parser.add_argument(
    "post_url", help="full url of blog post")
group.add_argument(
    "--likes", help="display only likes", action="store_true")
group.add_argument(
    "--reblogs", help="dispay only reblogs", action="store_true")
parser.add_argument(
    "--out_file", help="save results to file")
parser.add_argument(
    "--sort_off", help="turn off alphabetic sorting", action="store_true")
parser.add_argument(
    "--verbose", help="display additional feedback on screen", action="store_true")
args = parser.parse_args()
client = common.initiateClient()
blog_name, post_id = parsePostUrl(args.post_url)
result = getNotes(blog_name + ".tumblr.com", post_id)
common.displayResults(result, args.out_file, args.verbose)
