# Tumblr Deep Dive

A suite of tools that makes discovering similar blogs easier!

## authenticate.py
Guided script to help with obtaining and storing your keys for the Tumblr API.  Stores keys in a central location accessible by other scripts.

## reblogs.py
For a given blog, digest a certain number of posts and record what blogs they reblog and how many times they have reblogged a particular blog to determine affinity.

## notes.py
Display blogs that have liked or reblogged a particular post.

## exists.py
Filter a list of blogs, returning only existing blogs.

## recent.py
Filter a list of blogs, returning only blogs that have posted after a certain date.