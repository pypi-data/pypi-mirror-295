import time
import uuid
import jsonlines

class WebsocketRecorder():
    def __init__(self, page, stream=False, stdout=False):
        self.jsonl_data = []
        self.stream = stream
        self.stdout = stdout
        page.on("websocket", self._events_websocket)

    def _event(self, ws, action, payload):
        jsonl_record = {}
        jsonl_record["id"] =ws._id
        jsonl_record["timestamp"] = time.time()
        jsonl_record["url"] = ws.url
        jsonl_record["action"] = action
        jsonl_record["payload"] = payload
        self.jsonl_data.append(jsonl_record)
        if self.stream:
            print(jsonl_record)

    def _events_websocket(self, ws):
        ws._id = str(uuid.uuid4())
        self._event(ws, "opened", "")
        ws.on("framesent", lambda payload:  self._event(ws, "sent", payload))
        ws.on("framereceived", lambda payload: self._event(ws, "recd", payload))
        ws.on("socketerror", lambda payload: self._event(ws, "error", payload))
        ws.on("close", lambda payload: self._event(ws, "closed", ""))

    def write(self, outputfile="trace.websockets.jsonl"):
        if self.stdout:
            for record in self.jsonl_data:
                print(record)
        with jsonlines.open(outputfile, mode='w') as writer:
            for record in self.jsonl_data:
                writer.write(record)