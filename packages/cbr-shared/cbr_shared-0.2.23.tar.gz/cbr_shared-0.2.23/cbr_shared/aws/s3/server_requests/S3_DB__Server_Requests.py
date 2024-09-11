from datetime import datetime, timezone

from cbr_shared.aws.s3.S3_DB__CBR   import S3_DB__CBR
from osbot_utils.utils.Json         import  gz_to_json, json_to_gz

S3_FOLDER__SERVER_REQUESTS = 'server-requests'
S3_PATH__WHEN_BLOCK_SIZE   = 5

class S3_DB__Server_Requests(S3_DB__CBR):
    save_as_gz        : bool = True
    s3_path_block_size: int  = S3_PATH__WHEN_BLOCK_SIZE

    # def load_request_data(self, hostname, day, request_id):
    #     s3_key = self.s3_key(hostname, day, request_id)

    def s3_file_data(self, s3_key):                   # todo: refactor this gz support to the S3_DB__CBR class
        if self.s3_file_exists(s3_key):
            if self.save_as_gz:
                data_gz = super().s3_file_bytes(s3_key)
                data    = gz_to_json(data_gz)
            else:
                data = super().s3_file_data(s3_key)
            return data


    def s3_file_delete(self, s3_key):                   # todo: refactor this gz support to the S3_DB__CBR class
        return super().s3_file_delete(s3_key)

    def s3_file_exists(self, s3_key):
        return super().s3_file_exists(s3_key)

    def s3_save_data(self, data, s3_key):
        if self.save_as_gz:
            data      = json_to_gz(data)
            #data  = pickle_to_bytes(data)                                      # todo: see if we need to use pickle here to save the data
            #data  = bytes_to_gz(data)
        print(f'saved server_request to {s3_key}')
        return super().s3_save_data(data, s3_key)

    def s3_folder_server_requests(self):
        return S3_FOLDER__SERVER_REQUESTS

    def s3_key(self, server=None, when=None, request_id=None):
        s3_key     = f"{self.s3_folder_server_requests()}/{server}/{when}/{request_id}.json"
        if self.save_as_gz:
            s3_key += ".gz"
        return s3_key


    def s3_path__for_when(self):
        now          = datetime.now(timezone.utc)                        # Generate the current date and time in UTC
        date_path    = now.strftime('%Y-%m-%d')                          # Format the date as YYYY-MM-DD
        hour_path    = now.strftime('%H')                                # Format the hour
        block_size   = self.s3_path_block_size                           # get the block size in minutes (configurable)
        minute_block = f"{(now.minute // block_size) * block_size:02d}"  # Calculate the block using the configurable block size
        s3_path = f"{date_path}/{hour_path}/{minute_block}"
        return s3_path

    # todo: wire this up with local Minio and live S3 (to FastAPI)
    # def background_task(self, request: Request, response: Response):
    #     if server_config__cbr_website.aws_disabled():
    #         return
    #     from osbot_fast_api.api.Fast_API__Request_Data     import Fast_API__Request_Data
    #     from cbr_shared.aws.s3.S3_DB_Base                  import S3_DB_Base
    #     request_data : Fast_API__Request_Data = request.state.request_data
    #     request_id  = request_data.request_id
    #     host_name   = request_data.request_host_name
    #
    #     s3_db_base = S3_DB_Base()
    #     with capture_duration() as duration:
    #         s3_key     = f'server-requests/2024-08-30/{host_name}/{request_id}.json'
    #         s3_bucket  = s3_db_base.s3_bucket()
    #         data       = request_data.json()
    #         s3_db_base.s3_save_data(data, s3_key)
    #     message = f"Saved {request.url.path} request data: {s3_bucket}{s3_key} in {duration.seconds} secs"
    #
    #     request_data.add_log_message(message)