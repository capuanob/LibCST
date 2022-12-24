#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
from textwrap import dedent

with atheris.instrument_imports(include=['libcst']):
    import libcst as cst
    from libcst.tool import diff_code, dump


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        if fdp.ConsumeBool():
            dump(cst.parse_module(dedent(fdp.ConsumeRemainingString())))
        else:
            diff_code(fdp.ConsumeRandomString(), fdp.ConsumeRandomString(), fdp.ConsumeIntInRange(0, 10))
    except (cst.CSTValidationError, cst.ParserSyntaxError):
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
