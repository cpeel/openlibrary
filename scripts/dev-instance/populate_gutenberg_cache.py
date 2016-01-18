#!/usr/bin/env python
"""
Populate the Gutenberg metadata cache. This will take several hours depending
on the speed of the machine.

The final cache will take about 2GB of space. Because this code creates the
new cache in a temporary location and saves a backup of the cache before
putting the new one in place, you should have 6GB or more of space available
for all of that.
"""

import os
import shutil

import gutenberg.acquire.metadata as metadata

if __name__ == "__main__":
    cache_path = '/var/lib/openlibrary/gutenberg/metadata/metadata.db'
    cache_path_bak = "%s.bak" % cache_path
    cache_path_tmp = "%s.tmp" % cache_path

    if os.path.exists(cache_path_tmp):
        print("Temporary cache exists, removing it")
        shutil.rmtree(cache_path_tmp)

    mgr = metadata.MetadataCacheManager('Sleepycat', cache_path_tmp)

    print("Populating PG metadata into temporary cache at")
    print("    %s" % cache_path_tmp)
    print("This will take a long time...")
    mgr.populate()
    print("Cache populated, moving it into place")

    if os.path.exists(cache_path_bak):
        print("Old cache exists, removing it")
        shutil.rmtree(cache_path_bak)

    print("Backing up live cache")
    print("    Moving %s" % cache_path)
    print("        to %s" % cache_path_bak)
    os.rename(cache_path, cache_path_bak)

    print("Making temporary cache live")
    print("    Moving %s" % cache_path_tmp)
    print("        to %s" % cache_path)
    os.rename(cache_path_tmp, cache_path)

    print("Done")
