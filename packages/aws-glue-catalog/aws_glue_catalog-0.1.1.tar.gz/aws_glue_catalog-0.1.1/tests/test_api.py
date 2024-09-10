# -*- coding: utf-8 -*-

from aws_glue_catalog import api


def test():
    _ = api
    _ = api.Database
    _ = api.Table
    _ = api.Crawler


if __name__ == "__main__":
    from aws_glue_catalog.tests import run_cov_test

    run_cov_test(__file__, "aws_glue_catalog.api", preview=False)
