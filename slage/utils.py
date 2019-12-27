# coding: utf-8


def chunks(lst, n):
    # https://stackoverflow.com/a/312464/1069572
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
