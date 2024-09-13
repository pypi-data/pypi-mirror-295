from unittest import TestCase

from cbr_shared.aws.s3.S3_DB__CBR import S3_DB__CBR
from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp__Random__AWS_Credentials


class TestCase__CBR__Temp_S3_Bucket(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.random_aws_creds = Temp__Random__AWS_Credentials().set_vars()
        cls.s3_db_cbr        = S3_DB__CBR(use_minio=True)
        with cls.s3_db_cbr as _:
            assert _.using_minio() is True                      # confirm we are using Minio
            _.setup()                                           # this will create the temp bucket
            assert _.bucket_exists() is True

    @classmethod
    def tearDownClass(cls):
        with cls.s3_db_cbr as _:
            assert _.bucket_delete() is True