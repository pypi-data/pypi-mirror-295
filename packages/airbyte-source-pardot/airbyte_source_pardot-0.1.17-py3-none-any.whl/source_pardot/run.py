#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_pardot import SourcePardot


def run():
    source = SourcePardot()
    launch(source, sys.argv[1:])
