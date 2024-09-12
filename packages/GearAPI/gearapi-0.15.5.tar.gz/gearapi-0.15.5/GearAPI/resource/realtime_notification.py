import pandas as pd
from GearAPI.rest_adaptor import RestAdaptor
from typing import Union
import websocket
import json
import threading

class RealtimeNotificationResource(RestAdaptor):

    """
    Class for measurements resource.


    args:
        resource - measurements resource endpoint
    
    """

    def __init__(
            self,
            rest_adaptor: RestAdaptor) -> None:
        
        super().__init__(
            user=rest_adaptor.user,
            password=rest_adaptor.password
        )
        self.resource = '/notification/realtime'
        self.client_id = None
        self.data = []
        self.lock = threading.Lock()
        

    def hand_shake(self) -> dict:
        """
        provide a hand shake with the real time notification service

        Return:
            dict: response data

        """

        headers = {
            'Authorization':  self.authorisation_header,
            'Content-Type': 'application/json'

        }
        data = [
            {
                "channel": "/meta/handshake",
                "version": "1.0"
            }
        ]

        response = self.post(endpoint=self.resource, data=data)
        if response.message == 'OK':
            print(f'Handshake successful')
            return response.data[0]

    def _set_client_id(self) -> None:
        data = self.hand_shake()
        self.client_id = data['clientId']
        print(f'Client ID: {self.client_id}')

    def subscribe(self, ids:Union[str,list], resource:str) -> dict:
        if isinstance(ids, str):
            ids = [ids]
        
        for id in ids:
            data = [
                {
                    "channel": "/meta/subscribe",
                    "clientId": self.client_id,
                    "subscription": f"/{resource}/{id}"
                }
            ]

            response = self.post(endpoint=self.resource, data=data)
            print(f"Subscribe successfully. {response.data}")

    def unsubscribe(self, ids:Union[str,list], resource:str) -> dict:
        data = [
            {
                "channel": "/meta/unsubscribe",
                "clientId": self.client_id,
                "subscription": f"/{resource}/{id}"
            }
        ]

        response = self.post(endpoint=self.resource, data=data)
        print(f"Unsubscribe successfully. {response.data}")
    
    def unsubscribe_all(self,resource:str) -> dict:
        data = [
            {
                "channel": "/meta/unsubscribe",
                "clientId": self.client_id,
                "subscription": f"/{resource}/*"
            }
        ]

        response = self.post(endpoint=self.resource, data=data)
        print(f"Unsubscribe successfully. {response.data}")

    def connect(self) -> None:
        """
        connect to the real time notification service using various method. 

        """

        data = [
            {
                "channel": "/meta/connect",
                "clientId": self.client_id,
                "connectionType": 'webSocket',
                "advice": {
                "timeout": 5400000,
                "interval": 3000
                }
            }
        ]

        def on_message(ws, message):
        
            try:
                data = json.loads(message)
                print(f'Received message: {data}')

                with self.lock:
                    # Filter out control messages
                    if data and data[0].get('channel') == '/meta/connect':
                        print("Received a control message, ignoring.")
                        return

            # Check for actual data and process it
                if data and 'successful' in data[0] and data[0]['successful']:
                    self.data.append(data)

            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"Error processing message: {e}")

        def on_error(ws, error):
            print(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("WebSocket closed")

        def on_open(ws):
            print("WebSocket connection opened")
            # Prepare the data to send upon connection
            # Send the data through the WebSocket connection
            ws.send(json.dumps(data))

        # Example URL
        ws_url = self.websocket_url + self.resource

        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        ws.on_open = on_open
        ws.run_forever()

    def get_data(self):
        with self.lock:
            return list(self.data)
        
    def initiate(self, ids:Union[str,list], resource:str):
        self._set_client_id()
        self.subscribe(ids, resource=resource)
        self.connect()

    def run(self, ids:Union[str,list], resource) -> None:
        ws_thread = threading.Thread(target=self.initiate,args=(ids,resource), daemon=True)
        ws_thread.start()
        print("ready to get data")

