"""Utilities. """

import uuid
from hashlib import md5
from itertools import product

PROJECT_IDENTIFIER_HELPER = (
    "This can be a string containing a project id such as 4dad2d24-2d69-44fd-b7a2-819339b7c764 ."
    "A string with your project slug, eg: location-api. "
    "A string containing the username and the project slug in the following format: "
    "@USERNAME/SLUG, eg: @fpliger/location-api "
    "Or a string containing your project url, eg: https://username.pyscriptapps.com/project-slug "
)


def calculate_s3_etag(fp):
    """
    Different clients can use different chunk sizes when the file
    was uploaded. Thus, etags are calculated with different chunk sizes
    of 1 MB, 8 MB, 15 MB as suggested by:
    https://teppen.io/2018/10/23/aws_s3_verify_etags/#calculating-an-s3-etag-using-python

    When a file contains nothing, the md5 hash is d41d8cd98f00b204e9800998ecf8427e
    But, the internal implementation can have different endianness, due to which we can also
    have the value 59adb24ef3cdbe0297f05b395827453f

    Check the following link for more details
    https://crypto.stackexchange.com/questions/100560/can-a-hash-algorithm-get-identified-by-its-result-with-any-input
    """
    possible_etags = set()
    # chunk sizes for 1MB, 8MB, 15MB
    chunk_sizes = [1024 * 1024, 8 * 1024 * 1024, 15 * 1024 * 1024]
    possible_md5s_for_empty_file = [
        "d41d8cd98f00b204e9800998ecf8427e",
        "59adb24ef3cdbe0297f05b395827453f",
    ]
    for each_chunk_size in chunk_sizes:
        fp.seek(0)
        md5s = [md5(part) for part in iter(lambda: fp.read(each_chunk_size), b"")]

        if len(md5s) < 1:
            # if the empty-file uploaded without chunking
            for each_md5 in possible_md5s_for_empty_file:
                possible_etags.add(each_md5)

            # if the empty-file uploaded with 0 or 1 chunks
            possible_num_chunks = [0, 1]
            for each_md5, each_num_chunk in list(
                product(possible_md5s_for_empty_file, possible_num_chunks)
            ):
                empty_etag = f"{each_md5}-{each_num_chunk}"
                possible_etags.add(empty_etag)
        else:
            if len(md5s) == 1:
                possible_etags.add("{}".format(md5s[0].hexdigest()))

            digests = b"".join(m.digest() for m in md5s)
            digests_md5 = md5(digests)
            possible_etags.add("{}-{}".format(digests_md5.hexdigest(), len(md5s)))

    return possible_etags


def is_uuid(s):
    """Does the specified string represent a UUID.
    This is just a cheap, cheerful and fast-ish way without creating a UUID instance.
    """

    try:
        uuid.UUID(s)
    except ValueError:
        return False
    return True


def parse_project_identifier(identifier):
    username, project_slug, project_id = None, None, None
    # If we have a username and project slug, identifier is @username/project-slug
    if identifier.startswith("@"):
        try:
            username, project_slug = identifier[1:].split("/", maxsplit=1)
        except ValueError as e:
            raise ValueError(
                f"Cannot figure out username and slug from {identifier}"
            ) from e
    # If we have an http url, we can extract the username and  project id from it
    elif identifier.startswith("https://"):
        if ".pyscriptapps" in identifier:
            # pyscriptapps urls are of the form https://username.pyscriptapps.com/project-slug
            path = identifier.split("/")[2:]
            # Now split up username.pyscriptapps.com to get just the username portion
            username = path[0].split(".")[0]
            # The slug should be just the next in line, we dont care about anything else
            project_slug = path[1]
        else:
            path = identifier.split("/")[3:]
            # We may get three items in the list ['username', 'project-slug', 'latest']
            # so get just the first two
            username_with_prefix, project_slug = path[:2]
            # Remove the @ from the username
            username = username_with_prefix.replace("@", "")

    # If we have a project id which is a UUID, we can just use it
    elif is_uuid(identifier):
        project_id = identifier
    # If we haven't been able to get the username, project_id or  project_slug, we
    # will assume that we are passing the project slug.
    else:
        project_slug = identifier

    if not any([username, project_slug, project_id]):
        raise ValueError(
            f"Cannot figure out any identifying information for the project from {identifier}"
        )
    return username, project_slug, project_id
