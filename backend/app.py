from custom_response import CustomResponse
from datetime import datetime
from flask import *
import constants
import logging
import random
import string
import json
import csv
import re

# Initialize the app
app = Flask(__name__)
custom_response = CustomResponse()
logging.basicConfig(filename=constants.ERROR_LOGFILE, filemode='a', format='%(name)s - %(levelname)s - %(message)s')


@app.route(constants.GENERATE_RDM_OBJECTS_LINK, methods=["GET"])
def generate_random_objects():
    custom_response.reset_response()
    try:
        rdm_patterns = [
            string.ascii_lowercase + string.ascii_uppercase,
            string.ascii_lowercase + string.ascii_uppercase + string.digits,
            string.digits
        ]
        rdm_objects = []
        for idx in range(0, constants.ITERATION_LIMIT):
            for pattern in rdm_patterns:
                rdm_objects.append(''.join(random.choice(pattern) for _ in range(constants.STRING_LIMIT)))
            rdm_objects.append(random.random())
        filename = str(int(datetime.now().timestamp())) + constants.FILE_EXTENSION
        file_cursor = open(filename, 'w')
        writer = csv.writer(file_cursor)
        writer.writerow(rdm_objects)
        file_cursor.close()
        cmp_download_link = constants.DEV_ENV_HOST + ":" + str(constants.DEV_ENV_PORT) +\
                            constants.DOWNLOAD_RDM_OBJECTS_LINK + '?' + constants.ARGS_FILE_PARAM + '=' + filename
        cli_response = custom_response.get_response(code=constants.SUCCESS_CODE, data=cmp_download_link)
    except Exception as ex:
        logging.exception("Generate Random Objects Exception: " + str(ex))
        cli_response = custom_response.get_response(code=constants.RESOURCE_ERR_CODE,
                                                    message=constants.GENERATE_RDM_EXCEPTION)
    response = Response(json.dumps(cli_response))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route(constants.DOWNLOAD_RDM_OBJECTS_LINK, methods=["GET"])
def download_random_objects():
    custom_response.reset_response()
    try:
        return send_file(request.args.get(constants.ARGS_FILE_PARAM), as_attachment=True)
    except Exception as ex:
        logging.exception("Download Random Objects Exception: " + str(ex))
        cli_response = custom_response.get_response(code=constants.RESOURCE_ERR_CODE,
                                                    message=constants.DOWNLOAD_EXCEPTION)
        response = Response(json.dumps(cli_response))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


@app.route(constants.REPORT_RDM_OBJECTS_LINK, methods=["GET"])
def report_random_objects():
    custom_response.reset_response()
    try:
        report_data = {"alpha": 0, "alpha_num": 0, "integar": 0, "real_num": 0, "unknown": 0}
        file_cursor = open(request.args.get(constants.ARGS_FILE_PARAM), 'r')
        all_random_objects = csv.reader(file_cursor)
        for rdm_object in all_random_objects:
            for rdm_obj in rdm_object:
                if bool(re.compile(constants.ALPHA_PATTERN).match(rdm_obj)):
                    report_data["alpha"] += 1
                elif bool(re.compile(constants.ALL_NUM_PATTERN).fullmatch(rdm_obj)):
                    report_data["integar"] += 1
                elif bool(re.compile(constants.REAL_NUM_PATTERN).fullmatch(rdm_obj)):
                    report_data["real_num"] += 1
                elif bool(re.compile(constants.ALPHA_NUM_PATTERN).match(rdm_obj)):
                    report_data["alpha_num"] += 1
                else:
                    report_data["unknown"] += 1
        cli_response = custom_response.get_response(code=constants.SUCCESS_CODE, data=report_data)
    except Exception as ex:
        logging.exception("Report Random Objects Exception: " + str(ex))
        cli_response = custom_response.get_response(code=constants.RESOURCE_ERR_CODE,
                                                    message=constants.GENERATE_RDM_EXCEPTION)
    response = Response(json.dumps(cli_response))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run(host=constants.DEV_ENV_SERVER_HOST, port=constants.DEV_ENV_PORT, debug=True)
