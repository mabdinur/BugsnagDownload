import requests
import json
import os 
import time


class DownloadErrorEvents:
	CONFIG_FILE = "config.json"
	REQUEST_EVENTS_URL = "https://api.bugsnag.com/organizations/{}/event_data_requests"
	CHECK_EVENTS_STATUS_URL = "https://api.bugsnag.com/organizations/{}/event_data_requests/{}"
	SLEEP_SECONDS = 120 
	
	def __init__(self):
		with open(self.CONFIG_FILE) as config_json:
			data = json.load(config_json)
			self.organization_id = data["organization"]
			self.output_file = data["output_file"]
			self.request_header = data["request_headers"]
			self.request_download_link_body = json.dumps(data["post_request_events_download"])

	def load_event_data(self):
		request_id = self.request_event_data()
		print "New Request ID: ", request_id
		events_data = self.poll_event_data_download(request_id)
		self.download_file(events_data["url"])

	def request_event_data(self):
		create_request_url = self.REQUEST_EVENTS_URL.format(self.organization_id)
		create_data_r = requests.post(url= create_request_url, headers=self.request_header, data=self.request_download_link_body)
		create_data_r.raise_for_status()
		return json.loads(create_data_r.content)["id"]

	def poll_event_data_download(self, request_id):
		while True:
			data_request_url = self.CHECK_EVENTS_STATUS_URL.format(self.organization_id, request_id)
			data_request_status_r = requests.get(url=data_request_url, headers=self.request_header)
			data_request_status_r.raise_for_status()

			data_request_status_j = data_request_status_r.json()
			if data_request_status_j["status"] == "EXPIRED":
				raise Exception("Request_id: {} is no longer valid. \n".format(request_id) + json.dumps(data_request_status_j))
			elif data_request_status_j["status"] == "COMPLETED":
				return data_request_status_j
			else:
				print "Status:", data_request_status_j["status"], "Events:", data_request_status_j["total"], "ID:", data_request_status_j["id"]
				print "Waiting for events download url, sleep {} seconds".format(self.SLEEP_SECONDS)
				time.sleep(self.SLEEP_SECONDS)

	def download_file(self, download_url):
		print "downloading file"
		download_r = requests.get(url=download_url)
		download_json = json.loads(download_r.content)
		self.write_to_output_file(self.output_file, download_json)
		print "download complete"
		
	def write_to_output_file(self, file_name, events_data_json):
		if os.path.exists(file_name):
		    os.remove(file_name)
		text_file = open(file_name, "w")
		text_file.write(json.dumps(events_data_json, indent=4, sort_keys=True))
		text_file.close()

if __name__ == "__main__":
	DownloadErrorEvents().load_event_data()