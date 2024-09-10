# -*- coding: utf-8 -*-

from aws_glue_catalog.model import (
    Database,
    Table,
    Crawler,
)
from aws_glue_catalog.tests.mock_aws import BaseMockAwsTest


class Test(BaseMockAwsTest):
    use_mock = True

    def test(self):
        db_name = "mydb"
        tb_name = "mytb"
        cw_name = "mycw"

        db = Database.get(glue_client=self.glue_client, name=db_name)
        assert db is None

        self.glue_client.create_database(DatabaseInput={"Name": db_name})
        db = Database.get(glue_client=self.glue_client, name=db_name)
        assert db.Name == db_name

        tb = Table.get(glue_client=self.glue_client, database=db_name, name=tb_name)
        assert tb is None

        self.glue_client.create_table(
            DatabaseName=db_name,
            TableInput={
                "Name": tb_name,
                "StorageDescriptor": {
                    "Columns": [{"Name": "col1", "Type": "string"}],
                    "Location": "s3://mybucket/mykey",
                },
            },
        )
        tb = Table.get(glue_client=self.glue_client, database=db_name, name=tb_name)
        assert tb.DatabaseName == db_name
        assert tb.Name == tb_name

        cw = Crawler.get(glue_client=self.glue_client, name=cw_name)
        assert cw is None

        self.glue_client.create_crawler(
            Name=cw_name,
            Role="arn:aws:iam::123456789012:role/service-role/AWSGlueServiceRole-myrole",
            DatabaseName=db_name,
            Targets={"S3Targets": [{"Path": "s3://mybucket/mykey"}]},
        )
        cw = Crawler.get(glue_client=self.glue_client, name=cw_name)
        assert cw.Name == cw_name

        assert cw.is_running() is False
        assert cw.is_stopping() is False
        assert cw.is_ready() is True

        cw = Crawler.wait_until_ready(
            glue_client=self.glue_client,
            name=cw_name,
            timeout=10,
        )
        assert cw.is_ready() is True

        self.glue_client.start_crawler(Name=cw_name)
        cw = Crawler.get(glue_client=self.glue_client, name=cw_name)
        assert cw.is_running() is True

        self.glue_client.stop_crawler(Name=cw_name)
        cw = Crawler.get(glue_client=self.glue_client, name=cw_name)
        assert cw.is_stopping() is True


if __name__ == "__main__":
    from aws_glue_catalog.tests import run_cov_test

    run_cov_test(__file__, "aws_glue_catalog.model", preview=False)
