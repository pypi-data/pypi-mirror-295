import json
import urllib
from actionstreamer import CommonFunctions
from actionstreamer.Config import WebServiceConfig
from actionstreamer.WebService.API import WebServiceResult
from actionstreamer.WebService.Patch import *
from actionstreamer.Model import VideoClip

def create_video_clip(ws_config: WebServiceConfig, device_name: str, video_clip: VideoClip) -> tuple[int, str]:

    try:
        device_name = device_name.replace(" ", "")
        device_name = urllib.parse.quote(device_name)

        method = "POST"
        path = 'v1/videoclip/' + device_name
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = json.dumps(video_clip.__dict__)

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in CreateVideoClip. Line number " + str(line_number)

    return response_code, response_string


def update_file_id(ws_config: WebServiceConfig, video_clip_id: int, file_id: int) -> tuple[int, str]:

    try:
        operations_list = []
        add_patch_operation(operations_list, "FileID", file_id)

        method = "PATCH"
        path = 'v1/videoclip/' + str(video_clip_id)
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = generate_patch_json(operations_list)

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in UpdateVideoClipFileID Line number " + str(line_number)

    return response_code, response_string


def get_video_clip(ws_config: WebServiceConfig, video_clip_id: int) -> WebServiceResult:

    ws_result = WebServiceResult(0, '', '', '', None)

    try:

        method = "GET"
        path = 'v1/videoclip/' + str(video_clip_id)
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters)

        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred in get_video_clip at line {line_number} in {filename}")
        print(ex)
        ws_result.description = str(ex)

    return ws_result


def update_status(ws_config: WebServiceConfig, video_clip_id: int, status: int) -> tuple[int, str]:

    try:
        operations_list = []
        add_patch_operation(operations_list, "VideoClipStatus", status)

        method = "PATCH"
        path = 'v1/videoclip/' + str(video_clip_id)
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = generate_patch_json(operations_list)

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in VideoClip.update_status, line number " + str(line_number)

    return response_code, response_string


def get_video_clip_list(ws_config: WebServiceConfig, device_id: int, start_epoch: int, end_epoch: int, count: int = 0, order: str = 'desc') -> WebServiceResult:

    ws_result = WebServiceResult(0, '', '', '', None)

    try:

        method = "POST"
        path = 'v1/videoclip/list'
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        
        json_post_data = {
            "deviceID": device_id,
            "startEpoch": start_epoch,
            "endEpoch": end_epoch,
            "count": count,
            "order": order,
        }

        body = json.dumps(json_post_data)

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred in get_video_clip at line {line_number} in {filename}")
        print(ex)
        ws_result.description = str(ex)

    return ws_result