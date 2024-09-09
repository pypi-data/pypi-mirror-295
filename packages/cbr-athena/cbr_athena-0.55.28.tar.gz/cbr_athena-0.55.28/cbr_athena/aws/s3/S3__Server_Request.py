from cbr_athena.aws.s3.S3_DB__Server_Requests   import S3_DB__Server_Requests
from osbot_fast_api.api.Fast_API__Request_Data  import Fast_API__Request_Data
from osbot_utils.base_classes.Type_Safe         import Type_Safe
from osbot_utils.helpers.Random_Guid import Random_Guid
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc                     import date_today

DEFAULT__SERVER            = 'unknown-server'


class S3__Server_Request(Type_Safe):
    s3_db        : S3_DB__Server_Requests
    server       : str                      = DEFAULT__SERVER
    day          : str                      = None
    request_id   : Random_Guid
    request_data : Fast_API__Request_Data

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.day:
            self.day = date_today()                             # set the date to today if it has not been set
        if self.request_data:
            self.request_id = self.request_data.request_id

    def delete(self):
        return self.s3_db.s3_file_delete(self.s3_key())

    def exists(self):
        return self.s3_db.s3_file_exists(self.s3_key())

    def load(self):
        raw_data          = self.s3_db.s3_file_data(self.s3_key())
        self.request_data = Fast_API__Request_Data.from_json(raw_data)
        self.request_id   = self.request_data.request_id
        return self.request_data

    def create(self):
        if self.request_data:
            s3_key    = self.s3_key()
            data      = self.request_data.json()
            return self.s3_db.s3_save_data(data, s3_key)

    def save_request_data(self, request_data: Fast_API__Request_Data):
        self.request_data = request_data
        self.request_id   = request_data.request_id
        return self.create()

    def s3_key(self):
        return self.s3_db.s3_key(self.server, self.day, self.request_id)


