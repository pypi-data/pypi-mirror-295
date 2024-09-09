from cbr_athena.aws.s3.S3_DB__Server_Requests import S3_DB__Server_Requests
from osbot_utils.base_classes.Type_Safe import Type_Safe


class S3__Server_Requests(Type_Safe):
    s3_db        : S3_DB__Server_Requests

    def days(self, server):
        path = f'{self.s3_db.s3_folder_server_requests()}/{server}'
        return self.s3_db.s3_folder_list(path)

    def requests_ids(self, server, day):
        path = f'{self.s3_db.s3_folder_server_requests()}/{server}/{day}'
        return self.s3_db.s3_folder_files(path)

    def servers(self):
        path = f'{self.s3_db.s3_folder_server_requests()}/'
        return self.s3_db.s3_folder_list(path)

