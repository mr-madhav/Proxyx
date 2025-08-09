import os
import csv
import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Credentials:
    def __init__(self):
        self.folder_path = None
        self.file_path = None
        self.start_time = {}
        self.headers = ["request_url", "status_code", "time_spent", "request_method", "request_host", "request_port", "request_path", "request_query_params", "request_content_type", "request_http_version", "response_content_type", "response_content_length", "server_header", "clientip_port", "serverip_port", "tls_version", "cipher"]
        self.createCSV()
    
    def createCSV(self):
        try:
            # print(f"Creating comma seperated value file.\n")
            self.folder_path = "D:/Proxy Server/metastore"
            self.file_path = os.path.join(self.folder_path, f"proxypass-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv")
            if not os.path.exists(self.folder_path):
                os.mkdir(self.folder_path)

            if not os.path.isfile(self.file_path):
                with open(self.file_path, mode="w", newline="") as inputfile:
                    writer = csv.DictWriter(inputfile, fieldnames=self.headers, delimiter="\t")
                    writer.writeheader()
                    logger.info("File has been successfully created.")
            else:
                logger.info("File already exists in metastore.")
        except Exception as e:
            print(f"Error [createCSV]: {e}")

    def request(self, flow):
        try:
            # print(f"Request method is called.\n")
            self.start_time[flow.id] = datetime.datetime.now()

        except Exception as e:
            logger.error(f"Error [request]: {e} ")

    def response(self, flow):
        try:
            # print(f"Response method is called.\n")
            start = self.start_time.pop(flow.id, None)
            if start:
                time_spent = (datetime.datetime.now() - start).total_seconds()
            else:
                time_spent = None
            
            request_url = flow.request.pretty_url
            status_code = flow.response.status_code
            request_method = flow.request.method
            request_host = flow.request.host
            request_port = flow.request.port
            request_path = flow.request.path
            request_query_params = flow.request.query
            request_content_type = flow.request.headers.get("Content-Type")
            authorization = flow.request.headers.get("Authorization") if flow.request.headers and flow.request.headers.get("Authorization") else None
            print(f"Authorization: {authorization}")
            request_http_version = flow.request.http_version

            response_content_type = flow.response.headers.get("Content-Type")
            response_content_length = len(flow.response.content)
            server_header = flow.response.headers.get("Server")
            clientip_port = flow.client_conn.address
            serverip_port = flow.server_conn.address
            tls_version = flow.server_conn.tls_version if flow.server_conn.alpn and flow.server_conn.tls_version else None
            cipher = flow.server_conn.cipher if flow.server_conn and flow.server_conn.cipher else None
            if not ([
                request_url, status_code, time_spent, request_method, request_host, request_port, request_path, request_query_params, request_content_type, request_http_version, response_content_type, response_content_length, server_header, clientip_port, serverip_port, tls_version, cipher
            ]):
                logger.error(f"All components are not traceable.\nPlease remove untraceable component.\n")
                raise
            data = self.mapdata(request_url, status_code, time_spent, request_method, request_host, request_port, request_path, request_query_params, request_content_type, request_http_version, response_content_type, response_content_length, server_header, clientip_port, serverip_port, tls_version, cipher)
            with open(file=self.file_path, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers, delimiter="\t")
                writer.writerow(data)

        except Exception as e:
            logger.error(f"Error [response]: {e}")
    
    def mapdata(self, request_url, status_code, time_spent, request_method, request_host, request_port, request_path, request_query_params, request_content_type, request_http_version, response_content_type, response_content_length, server_header, clientip_port, serverip_port, tls_version, cipher):
        try:
            return {
                "request_url" : request_url,
                "status_code": status_code,
                "time_spent": time_spent,
                "request_method": request_method,
                "request_host": request_host,
                "request_port": request_port,
                "request_path": request_path,
                "request_query_params": request_query_params,
                "request_content_type": request_content_type,
                "request_http_version": request_http_version,
                "response_content_type": response_content_type,
                "response_content_length": response_content_length,
                "server_header": server_header,
                "clientip_port": clientip_port,
                "serverip_port": serverip_port,
                "tls_version": tls_version,
                "cipher": cipher

            }
        except Exception as e:
            logger.error(f"Error [mapdata]: {e}")

addons =[
    Credentials()
]