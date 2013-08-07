#!/bin/sh
#
#
# An example hook script that is called after a successful
# commit is made.
#
# To enable this hook, rename this file to "post-commit".

# Export Log:

git log --graph >> logGraph
