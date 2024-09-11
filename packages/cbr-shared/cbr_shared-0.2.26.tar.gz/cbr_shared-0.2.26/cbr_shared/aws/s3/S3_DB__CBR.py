from cbr_shared.aws.s3.S3_DB_Base                   import S3_DB_Base
from osbot_aws.AWS_Config                           import aws_config
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Misc                         import lower

S3_FOLDER__USERS_SESSIONS    = 'users_sessions'
BUCKET_NAME__CBR             = "{account_id}-cyber-boardroom"

class S3_DB__CBR(S3_DB_Base):

    @cache_on_self
    def s3_bucket(self):
        account_id  = aws_config.account_id()
        bucket_name = BUCKET_NAME__CBR.format(account_id=account_id)
        return lower(bucket_name)


    def s3_folder_users_sessions(self):
        return S3_FOLDER__USERS_SESSIONS