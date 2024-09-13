from cbr_shared.aws.s3.S3_DB_Base                   import S3_DB_Base

S3_FOLDER__USERS_SESSIONS        = 'users_sessions'
BUCKET_NAME__CBR                 = "{account_id}-cyber-boardroom"

class S3_DB__CBR(S3_DB_Base):
    bucket_name__suffix : str = 'server-data'
    bucket_name__prefix : str = 'cyber-boardroom'

    def s3_folder_users_sessions(self):
        return S3_FOLDER__USERS_SESSIONS