from cbr_shared.aws.s3.S3_DB_Base       import S3_DB_Base
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTE_PATH__REQUESTS_IN_S3 = 'requests-in-s3'

class Routes__Requests_In_S3(Fast_API_Routes):
    tag             : str = ROUTE_PATH__REQUESTS_IN_S3

    def s3_config(self):
        s3_db_base = S3_DB_Base()
        s3_bucket = s3_db_base.s3_bucket()
        return dict(s3_bucket = s3_bucket)

    def setup_routes(self):
        self.add_route_get(self.s3_config)
        return self