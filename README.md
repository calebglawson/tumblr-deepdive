# Tumblr Deep Dive
A suite of tools that makes discovering similar blogs easier!

## authenticate.py
Guided script to help with obtaining and storing your keys for the Tumblr API.  Stores keys in a central location accessible by other scripts.

## reblogs.py
For a given blog, digest a certain number of posts and record what blogs they reblog and how many times they have reblogged a particular blog to determine affinity.

`python authenticate.py blog_name max_posts --ascending --max_print --out_file --rate_limit --threshold --verbose`

## notes.py
Display blogs that have liked or reblogged a particular post.

`python notes.py post_url --likes --reblogs --out_file --sort_off --verbose`

## exists.py
Filter a list of blogs, returning only existing blogs.

`python exists.py in_file --out_file --rate_limit --sort_off --verbose`

## recent.py
Filter a list of blogs, returning only blogs that have posted after a certain date.

`python recent.py in_file days_ago --out_file --rate_limit --sort_off --verbose`

## chain.py
Recurse through the reblog chain, return the list of blogs leading to the post's originator.

`python chain.py post_url --out_file --sort_on --verbose`