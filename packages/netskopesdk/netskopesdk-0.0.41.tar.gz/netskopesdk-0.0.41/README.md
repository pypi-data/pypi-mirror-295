# Netskope SDK

Neskope SDK is Python library for dealing with API's to download the Netskope events. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NetskopeSDK.

```bash
pip install netskopesdk
```

## Rest sdk Usage to pull the Alert & Events 

```python
from netskope_api.iterator.netskope_iterator import NetskopeIterator
from netskope_api.iterator.const import Const
from requests.exceptions import RequestException
import time

# Construct the params dict to pass the authentication details 
params = {
        Const.NSKP_TOKEN : "<REST-API-TOKEN>",
        Const.NSKP_TENANT_HOSTNAME : "<HOSTNAME>",
        # Optional param to pass the proxy hosts.
        Const.NSKP_PROXIES : {"<PROXY-HOSTS>"},
        Const.NSKP_EVENT_TYPE : "<EVENT-TYPE>",
        Const.NSKP_ITERATOR_NAME : "<ITERATOR-NAME>",
        Const.NSKP_USER_AGENT : "<SPLUNK-TENANT-HOSTNAME>"
    
        # To query specific alert pass the NSKP_EVENT_TYPE as "alert" and the alert type.
        # Const.NSKP_EVENT_TYPE : Const.EVENT_TYPE_ALERT,
        # Const.NSKP_ALERT_TYPE : Const.ALERT_TYPE_DLP
    }

DEFAULT_WAIT_TIME = 30
RESULT = "result"
WAIT_TIME = "wait_time"

# Create an Iterator
iterator = NetskopeIterator(params)

# Use the next() iterator to download the logs. 
# Consume the message indefinitely in a loop and ingest the data to SIEM
while True:
    response = (iterator.next())
    try:
        if response:
            data = response.json()
            if RESULT in data and len(data[RESULT]) != 0:
                # processData() 
                # sleep() the thread to avoid constant polling
                if WAIT_TIME in data:
                    time.sleep(data[WAIT_TIME])
                else:
                    time.sleep(DEFAULT_WAIT_TIME)
            else:
                print("No response received from the iterator")
                time.sleep(DEFAULT_WAIT_TIME)
    except Exception as e:
        time.sleep(DEFAULT_WAIT_TIME)
        raise RequestException(e)
```

## Rest sdk Usage to retrieve tokens used for subscribing to transaction events from PSL.

```python
from requests.exceptions import RequestException
from netskope_api.iterator.const import Const
from netskope_api.token_management.netskope_management import NetskopeTokenManagement

if __name__ == '__main__':
    params = {
        Const.NSKP_TOKEN: "",
        Const.NSKP_TENANT_HOSTNAME: "<HOSTNAME>",
        # Optional param to pass the proxy hosts.
        Const.NSKP_PROXIES : {"<PROXY-HOSTS>"}
    }

    sub_path_response = None
    sub_key_response = None
    try:
        # Create token_management client
        token_management = NetskopeTokenManagement(params)
        token_management_response = token_management.get()
        if token_management_response:
            if "subscription" in token_management_response:
                sub_path_response = token_management_response["subscription"]
            if "subscription-key" in token_management_response:
                sub_key_response = token_management_response["subscription-key"]
    except Exception as e:
        raise RequestException(e)
```

Api response will carry 200 status code, subscription-key and subscription in the response for successful api calls
and a meaningfull error_msg and respective status codes in case of failures.


1. 200 response code means Customer is authorized to create/get subscription key and path.

2. 401 response code means Customer is not authorized to create/get subscription key and path.
   This is a licensed feature, please contact Netskope support to purchase.

3. 449 response code means Existing customer authorized for transaction events, subscription key and path were already downloaded.
   Use regenerate_and_get() to regenerate the subscription key.
   This is a one time step to onboard the existing customer to the API.

4. 503 response code means services responsibles for Transaction events are not available yet in the
   region where the customer is located.
   
API response examples:
  ```
        {
            "ok": 1,
            "status": 200,
            "subscription-key": "sub-key-value",
            "subscription": "sub-path-value"

        }               
        {
            "ok": 0,
            "status": 401,
            "error_msg": "This is a licensed feature, please contact Netskope support to purchase"
        }                                
        {
            "ok": 0,
            "status": 503,
            "error_msg": "Service is unavailable in this region"
        } 
   ```

## When to use regenerate_and_get() API.
    regenerate_and_get() API must only be used:
    1. if google-cloud-pubsublite throws 401 invalid credentials exception
    while using subscription key and path retrieved by using Netskope API.
    2. To handle 449 response code as explained above.

    Example error:
    google.api_core.exceptions.Unauthenticated: 401 Request had invalid authentication credentials
    grpc.aio._call.AioRpcError: <AioRpcError of RPC that terminated with:
    status = StatusCode.UNAUTHENTICATED
    details = "Request had invalid authentication credentials. Expected OAuth 2 access token, login cookie or other valid authentication credential.

    Regenerating subscription key will invalidate the existing key but subscription path will not be updated
    so that clients can continue consuming events where they left off.

## How to use regenerate_and_get() API.
    1. regenerate_and_get() API must only be used if google-cloud-pubsublite throws 401 Request had invalid authentication credentials errors.
    2. Retry 3 times with get() API with some Exponential backoff logic with an intial time interval of 60 seconds.
    3. If the responses returned by get() API continues to be invalid credentials. Use regenerate_and_get() API and use the new credentials.

## Note: Regenerating subscription key will invalidate the existing key.


```python
from requests.exceptions import RequestException
from netskope_api.iterator.const import Const
from netskope_api.token_management.netskope_management import NetskopeTokenManagement

if __name__ == '__main__':
    params = {
        Const.NSKP_TOKEN: "",
        Const.NSKP_TENANT_HOSTNAME: "<HOSTNAME>",
        # Optional param to pass the proxy hosts.
        Const.NSKP_PROXIES : {"<PROXY-HOSTS>"}
    }

    sub_path_response = None
    sub_key_response = None
    try:
        # Create token_management client
        token_management = NetskopeTokenManagement(params)
        token_management_response = token_management.regenerate_and_get()
        if token_management_response:
            if "subscription" in token_management_response:
                sub_path_response = token_management_response["subscription"]
            if "subscription-key" in token_management_response:
                sub_key_response = token_management_response["subscription-key"]
    except Exception as e:
        raise RequestException(e)
```
