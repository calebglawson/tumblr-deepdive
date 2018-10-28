#!/usr/bin/python2
import json
import pytumblr

# Please generate and enter your own API key/secret and OAuth token/secret.
# You are using this script for your own purposes, and may have added your own customizations.
# You agree to follow Tumblr's API License Agreement and ToS in utilizing any part of the following code.
#   https://www.tumblr.com/policy/en/terms-of-service
#   https://www.tumblr.com/docs/en/api_agreement

# Prior to your first run, register your own application with Tumblr's API to obtain a key.
#   https://www.tumblr.com/oauth/apps
#
# Execute authenticate.py and follow the prompts to generate a config.json file.


def initiateClient():
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
        return client
    except:
        print("Client could not be authenticated, please (re)authenticate by executing authenticate.py")
        exit()


def readInFile(file_name, verbose):
    try:
        infile = open(file_name, "r")
    except:
        print("Input file failed to read.")
        exit()

    blogs = infile.readlines()
    # If we close the file now, we can write to the same file later.
    infile.close()

    if verbose:
        print("Input file read successfully.")

    return blogs


def displayResults(result, out_file, verbose):
    if out_file == None:  # If the output file is not specified, then print to screen.
        for blog in result:
            print(blog.strip("\n"))
    else:
        try:
            outfile = open(out_file, "w")
        except:
            print("Output file failed to write.")
            exit()

        for blog in result:
            outfile.write(blog.strip("\n") + '\n')
        if verbose:
            print("Output file written successfully.")
        outfile.close()
