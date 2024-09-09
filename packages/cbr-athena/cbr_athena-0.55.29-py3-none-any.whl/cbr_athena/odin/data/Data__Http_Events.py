from fastapi import Request

from osbot_fast_api.api.Fast_API__Http_Events   import Fast_API__Http_Events
from osbot_fast_api.api.Fast_API__Request_Data  import Fast_API__Request_Data
from osbot_utils.base_classes.Type_Safe         import Type_Safe
from osbot_utils.helpers.trace.Trace_Call import Trace_Call
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Dev                      import pprint
from osbot_utils.utils.Misc                     import list_set
from osbot_utils.utils.Objects import pickle_from_bytes
from osbot_utils.utils.Status import status_error
from osbot_utils.utils.Str import ansi_to_text


class Data__Http_Events(Type_Safe):
    http_events : Fast_API__Http_Events


    def requests_id(self):
        return self.http_events.requests_order

    def request_data(self, request_id: str, request_index:str):

        if not request_id and request_index > -1:
            if len(self.http_events.requests_order) > request_index:
                request_id = self.http_events.requests_order[request_index]
            else:
                return status_error(f"no request found with index: {request_index}")
        request_data = self.http_events.requests_data.get(request_id)
        if request_data:
            data   = []
            traces = None
            for key, value in request_data.json().items():
                if key=='traces':
                    traces = value
                else:
                    if type(value) in [list, dict]:
                        value = value.__str__()
                    data.append(dict(key=key, value=value))
            traces_html = self.traces_to_html(traces)
            data.append(dict(key='traces', value=traces_html))
            return data
        else:
            return status_error(f"no request found with id: {request_id}")

    def requests_data(self):
        requests_data = self.http_events.requests_data
        items = []
        # ['fast_api_name', 'messages', 'request_duration', 'request_host_name',
        #  'request_id', 'request_method', 'request_port', 'request_start_time',
        #  'request_url', 'response_content_length', 'response_content_type', 'response_end_time',
        #  'response_status_code', 'thread_id', 'timestamp', 'traces']
        for request_id, request_data  in requests_data.items():
            items.append(self.request_data_to_json(request_data))
        return items

    def request_data_to_json(self, request_data: Fast_API__Request_Data):
        with request_data as _:
            return dict(req_id        = _.request_id             ,
                        method        = _.request_method         ,
                        path          = _.request_path           ,
                        content_type  = _.response_content_type  ,
                        size          = _.response_content_length,
                        duration      = _.request_duration       ,
                        status_codev  = _.response_status_code   ,
                        messages      = _.messages()             ,
                        host_name     = _.request_host_name      ,
                        traces        = _.traces_count           ,
                        domain        = _.domain                 ,
                        ip_address    = _.client_ip              ,
                        country       = _.client_country         ,
                        city          = _.client_city            )


    def traces_to_html(self, all_traces_bytes):
        if all_traces_bytes:
            trace_data = "<pre>"
            for traces_bytes in all_traces_bytes:
                view_model = pickle_from_bytes(traces_bytes)
                trace_call = Trace_Call()
                with Stdout() as stdout:
                    trace_call.trace_call_print_traces.print_traces(view_model)
                trace_data += ansi_to_text(stdout.value())
            trace_data += "</pre>"
            return trace_data

        return '...todo'
        # for item in data:
        #     key, value = item.get('key'), item.get('value')
        #     print(key)
        #     #if key == 'traces':
            #    data[key] = '123'

        #data['traces'] = ['123']

    # def http_events(self):
    #     if
    #     if hasattr(self.request.state, 'http_events'):
    #         return self.request.state.http_events