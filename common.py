#!/usr/bin/python2
import pytumblr
import json

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
