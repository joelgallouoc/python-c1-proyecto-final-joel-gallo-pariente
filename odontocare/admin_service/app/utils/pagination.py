from flask import request

def get_pagination():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    size = request.args.get(
        "size",
        10,
        type=int
    )

    size = min(size, 1000)

    return page, size