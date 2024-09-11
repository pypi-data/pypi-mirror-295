import sys

from cbr_shared.aws.s3.S3_DB_Base                   import S3_DB_Base
from osbot_aws.AWS_Config                           import aws_config
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.utils.Env import in_github_action
from osbot_utils.utils.Misc                         import lower

S3_FOLDER__USERS_SESSIONS    = 'users_sessions'
BUCKET_NAME__CBR             = "{account_id}-cyber-boardroom"


def running_in_pytest():
    return 'pytest' in sys.modules

class S3_DB__CBR(S3_DB_Base):

    @cache_on_self
    def s3_bucket(self):
        account_id = None
        if running_in_pytest():
            if aws_config.aws_configured() is False:
                account_id = 'in-pytest-no-aws-credentials'                                  # todo: improve this logic "in-gh-action" (maybe using the self.use_minio value)
        #if not in_github_action() and not running_in_pytest():
        if account_id is None:
            account_id = aws_config.account_id()                            # this is the call we want to avoid making

        bucket_name = BUCKET_NAME__CBR.format(account_id=account_id)
        return lower(bucket_name)


    def s3_folder_users_sessions(self):
        return S3_FOLDER__USERS_SESSIONS