from cbr_athena.aws.s3.S3_DB__Server_Requests import S3_DB__Server_Requests
from cbr_athena.aws.s3.S3__Server_Request import S3__Server_Request
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Files import files_names_without_extension


class S3__Server_Requests(Type_Safe):
    s3_db        : S3_DB__Server_Requests

    def days(self, server):
        path = f'{self.s3_db.s3_folder_server_requests()}/{server}'
        return self.s3_db.s3_folder_list(path)

    def requests_ids(self, server, day):
        path         = f'{self.s3_db.s3_folder_server_requests()}/{server}/{day}'
        s3_files     =  self.s3_db.s3_folder_files(path)
        requests_ids = [s3_file.split('.')[0] for s3_file in s3_files]
        return requests_ids

    def servers(self):
        path = f'{self.s3_db.s3_folder_server_requests()}/'
        return self.s3_db.s3_folder_list(path)

    def server_request(self, server, day, request_id):
        kwargs = dict(server=server, day=day, request_id=request_id)
        return S3__Server_Request(**kwargs)

