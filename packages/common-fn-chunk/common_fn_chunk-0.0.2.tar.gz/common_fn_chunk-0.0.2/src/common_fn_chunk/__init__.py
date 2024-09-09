# SPDX-FileCopyrightText: 2024-present Hao Wu <haowu@dataset.sh>
#
# SPDX-License-Identifier: MIT
def chunk_it(iterator, chunk_size = 50):
    """
    Yield successive chunks of a given size from an iterator.

    :param iterator: The input iterator.
    :param chunk_size: The number of items per chunk.
    :yield: A list containing the chunk of items.
    """
    chunk = []
    for item in iterator:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk  # Yield the last chunk if it's not empty
