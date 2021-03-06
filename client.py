# coding=utf-8

import requests
import json
import hashlib
import hmac
from datetime import datetime
from urllib.parse import urlencode


class Client(object):
    '''
    Client for Bittrex for V3 API
    '''

    API_URL = 'https://api.bittrex.com/v3/'

    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()

    def _init_session(self):
        session = requests.session()
        session.headers.update({'Content-Type': 'application/json', 'Accept': 'application/json'})
        return session

    def _request(self, method, endpoint, **kwargs):
        uri = self.API_URL + endpoint
        self.response = getattr(self.session, method)(uri, **kwargs)
        return self.response.json()

    def _authenticated_request(self, method, endpoint, **kwargs):
        request_data = dict()
        payload = ''
        if len(kwargs) > 0:
            if method == "get":
                endpoint = endpoint + "?" + urlencode(kwargs)
            else:
                request_data['data'] = payload = json.dumps(kwargs)

        mill_timestamp = str(int(datetime.now().timestamp()) * 1000)
        content_hash = hashlib.sha512(payload.encode()).hexdigest()
        uri = self.API_URL + endpoint
        _pre_sign = mill_timestamp + uri + method.upper() + content_hash
        signature = hmac.new(self.API_SECRET.encode(), _pre_sign.encode(), hashlib.sha512).hexdigest()
        self.session.headers.update({'Api-Key': self.API_KEY,
                                     'Api-Timestamp': mill_timestamp,
                                     'Api-Content-Hash': content_hash,
                                     'Api-Signature': signature
                                     })

        self.response = getattr(self.session, method)(uri, **request_data)
        return self.response.json()

    def ping(self):
        return self._request("get", "ping")

    def get_account(self):
        '''
        Retrieve information for the account associated with the request
        :return:
        {
          "subaccountId": "string (uuid)",
          "accountId": "string (uuid)"
        }
        '''
        return self._authenticated_request("get", "account")

    def get_account_volume(self):
        '''
        Get 30 day volume for account
        :return:
        {
          "updated": "string (date-time)",
          "volume30days": "number (double)"
        }
        '''
        return self._authenticated_request("get", "account/volume")

    def get_addresses(self):
        '''
        List deposit addresses that have been requested or provisioned
        :return:
        [
          {
            "status": "string",
            "currencySymbol": "string",
            "cryptoAddress": "string",
            "cryptoAddressTag": "string"
          }
        ]
        '''
        return self._authenticated_request("get", "addresses")

    def get_balances(self):
        '''
        Used to retrieve all balances from your account.
        :return:
        [
          {
            "currencySymbol": "string",
            "total": "number (double)",
            "available": "number (double)",
            "updatedAt": "string (date-time)"
          }
        ]
        '''
        return self._authenticated_request("get", "balances")

    def get_closed_orders(self, **params):
        '''
        List closed orders.
        StartDate and EndDate filters apply to the ClosedAt field.
        Pagination and the sort order of the results are in inverse order of the ClosedAt field.
        @param marketSymbol optional - filter by market
        @param nextPageToken optional - The unique identifier of the item that the resulting query result should
            start after, in the sort order of the given endpoint
        @param previousPageToken optional - The unique identifier of the item that the resulting query result
            should end before, in the sort order of the given endpoint.
        @param pageSize optional - maximum number of items to retrieve -- default 100, minimum 1, maximum 200
        @param startDate optional - Filters out results before this timestamp.
            In ISO 8601 format (e.g., "2019-01-02T16:23:45Z")
        @param endDate optional - Filters out result after this timestamp. Uses the same format as StartDate.
            Either, both, or neither of StartDate and EndDate can be set.
        :return:
        [
          {
            "id": "string (uuid)",
            "marketSymbol": "string",
            "direction": "string",
            "type": "string",
            "quantity": "number (double)",
            "limit": "number (double)",
            "ceiling": "number (double)",
            "timeInForce": "string",
            "clientOrderId": "string (uuid)",
            "fillQuantity": "number (double)",
            "commission": "number (double)",
            "proceeds": "number (double)",
            "status": "string",
            "createdAt": "string (date-time)",
            "updatedAt": "string (date-time)",
            "closedAt": "string (date-time)",
            "orderToCancel": {
              "type": "string",
              "id": "string (uuid)"
            }
          }
        ]
        '''
        return self._authenticated_request("get", "orders/closed", **params)

    def get_deposits_open(self, **params):
        '''
        List open deposits. Results are sorted in inverse order of UpdatedAt, and are limited to the first 1000.
        @param status optional - string enum
        @param currencySymbol optional - string
        :return:
        '''
        return self._authenticated_request("get", "deposits/open", **params)

    def get_deposits_closed(self, **params):
        '''
        List closed deposits. StartDate and EndDate filters apply to the CompletedAt field. Pagination and the
        sort order of the results are in inverse order of the CompletedAt field.
        @param status optional - string enum
        @param currencySymbol optional - string
        @param nextPageToken optional - string. The unique identifier of the item that the resulting
            query result should start after, in the sort order of the given endpoint. Used for traversing
            a paginated set in the forward direction. (Optional. May only be specified if PreviousPageToken
            is not specified.)
        @param previousPageToken optional - string. The unique identifier of the item that the resulting
            query result should end before, in the sort order of the given endpoint. Used for traversing a
            paginated set in the reverse direction. (Optional. May only be specified if NextPageToken is
            not specified.)
        @param pageSize optional - integer. maximum number of items to retrieve
            default 100, minimum 1, maximum 200
        @param startDate optional - ISO8601. Filters out results before this timestamp
        @param endDate optional - ISO8601. Filters out results after this timestamp
        :return:
        [
          {
            "id": "string (uuid)",
            "currencySymbol": "string",
            "quantity": "number (double)",
            "cryptoAddress": "string",
            "txId": "string",
            "confirmations": "integer (int32)",
            "updatedAt": "string (date-time)",
            "completedAt": "string (date-time)",
            "status": "string",
            "source": "string"
          }
        ]
        '''
        return self._authenticated_request("get", "deposits/closed", **params)

    def get_withdrawals_open(self, **params):
        '''
        List open withdrawals. Results are sorted in inverse order of UpdatedAt, and are limited to the first 1000.
        @param status optional - string enum
        @param currencySymbol optional - string
        :return:
        [
          {
            "id": "string (uuid)",
            "currencySymbol": "string",
            "quantity": "number (double)",
            "cryptoAddress": "string",
            "cryptoAddressTag": "string",
            "txCost": "number (double)",
            "txId": "string",
            "status": "string",
            "createdAt": "string (date-time)",
            "completedAt": "string (date-time)"
          }
        ]
        '''
        return self._authenticated_request("get", "withdrawals/open", **params)

    def get_withdrawals_closed(self, **params):
        '''
        List closed withdrawals. StartDate and EndDate filters apply to the CompletedAt field. Pagination and the
        sort order of the results are in inverse order of the CompletedAt field.
        @param status optional - string enum
        @param currencySymbol optional - string
        @param nextPageToken optional - string. The unique identifier of the item that the resulting
            query result should start after, in the sort order of the given endpoint. Used for traversing
            a paginated set in the forward direction. (Optional. May only be specified if PreviousPageToken
            is not specified.)
        @param previousPageToken optional - string. The unique identifier of the item that the resulting
            query result should end before, in the sort order of the given endpoint. Used for traversing a
            paginated set in the reverse direction. (Optional. May only be specified if NextPageToken is
            not specified.)
        @param pageSize optional - integer. maximum number of items to retrieve
            default 100, minimum 1, maximum 200
        @param startDate optional - ISO8601. Filters out results before this timestamp
        @param endDate optional - ISO8601. Filters out results after this timestamp
        :return:
        [
          {
            "id": "string (uuid)",
            "currencySymbol": "string",
            "quantity": "number (double)",
            "cryptoAddress": "string",
            "txId": "string",
            "status": "string",
            "createdAt": "string (date-time)",
            "completedAt": "string (date-time)"
          }
        ]
        '''
        return self._authenticated_request("get", "withdrawals/closed", **params)
