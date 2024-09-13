from unittest import TestCase

from cbr_shared.aws.s3.server_requests.S3_DB__Server_Requests import S3_DB__Server_Requests
from cbr_shared.aws.s3.server_requests.S3__Server_Request import S3__Server_Request
from cbr_shared.aws.s3.server_requests.S3__Server_Requests import S3__Server_Requests
from cbr_shared.testing.TestCase__CBR__Temp_S3_Bucket import TestCase__CBR__Temp_S3_Bucket
from osbot_aws.testing.Temp__Random__AWS_Credentials import Temp__Random__AWS_Credentials
from osbot_fast_api.utils.testing.Mock_Obj__Fast_API__Request_Data import Mock_Obj__Fast_API__Request_Data


class TestCase__CBR__Temp_Server_Requests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_server           = 'pytest__temp_server'
        cls.random_aws_creds      = Temp__Random__AWS_Credentials().set_vars()
        cls.s3_db_server_requests = S3_DB__Server_Requests(use_minio=True, server_name=cls.temp_server)

        with cls.s3_db_server_requests as _:
            assert _.using_minio() is True                      # confirm we are using Minio
            assert _.setup      () is _                         # this will create the temp bucket
            assert _.bucket_exists() is True

            cls.s3_server_requests    = S3__Server_Requests(s3_db = _ )
            cls.request_data          = Mock_Obj__Fast_API__Request_Data().create()
            cls.s3_server_request     = S3__Server_Request(request_data = cls.request_data  ,
                                                           s3_db        = _                 )
        assert cls.s3_server_request.create() is True
        assert cls.s3_server_request.exists() is True



    @classmethod
    def tearDownClass(cls):
        with cls.s3_server_request as _:
            assert _.delete() is True
            assert _.exists() is False

        with cls.s3_db_server_requests as _:
            assert _.using_minio() is True
            assert _.bucket_delete_all_files()
            assert _.bucket_delete() is True
