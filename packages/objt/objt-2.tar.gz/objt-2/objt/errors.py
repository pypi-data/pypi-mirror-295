# This file is placed in the Public Domain.
# pylint: disable=R0903,W0125,E1102


"deferred exception handling"


import io
import traceback


class Errors:

    "Errors"

    errors = []

    @staticmethod
    def format(exc):
        "format an exception"
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                           )
        for line in stream.readlines():
            res += line + "\n"
        return res


def errors(outer):
    "display errors."
    for exc in Errors.errors:
        outer(Errors.format(exc))


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


def __dir__():
    return (
        'Errors',
        'errors',
        'later'
    )
