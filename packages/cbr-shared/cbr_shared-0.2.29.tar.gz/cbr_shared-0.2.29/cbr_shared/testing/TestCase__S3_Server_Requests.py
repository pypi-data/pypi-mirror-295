from cbr_shared.aws.s3.server_requests.S3_DB__Server_Requests import S3_DB__Server_Requests
from osbot_aws.testing.TestCase__Minio import TestCase__Minio


class TestCase__Server_Requests(TestCase__Minio):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.s3_db = S3_DB__Server_Requests()

    @classmethod
    def tearDown(self):
        super().tearDownClass()
