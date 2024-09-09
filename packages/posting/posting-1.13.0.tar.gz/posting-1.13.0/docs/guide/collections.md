## Overview

A *collection* is just a directory on your file system which may or may not contain requests in the `.posting.yaml` format.

There's absolutely nothing special about a collection.
It contains no "special files" or metadata -- it's just a directory.
It could even be empty.
"Collection" is simply the name we give to the directory which we've loaded into Posting.

## The default collection

If you launch Posting without any arguments, it will load the *default collection*, which is stored in Posting's reserved data directory on your file system.
You can check where this is by running `posting locate collection`.

This is useful to get started quickly, but you'll probably want to create your own collection directory and load it instead.
This makes it easier to organize your requests and check them into version control.

## Creating a collection

A collection is just a directory, so you can create a collection by simply creating an empty directory anywhere on your file system.

## Loading a collection

If you want to load a collection, you can do so by passing the path to the collection directory to Posting:

```bash
posting --collection path/to/collection
```

## Example



To open a collection (a directory containing requests), use the `--collection` option:

```bash
posting --collection path/to/collection
```

This will recursively find and display requests in the sidebar.
If you don't supply a directory, Posting will use the default collection directory.
You can check where this is by running `posting locate collection`.