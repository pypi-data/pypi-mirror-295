from enum import Enum


class HTTP:
    """
    HTTP status codes constants.

    """

    STATUS_200_OK = 200
    STATUS_201_CREATED = 201
    STATUS_202_ACCEPTED = 202
    STATUS_204_NO_CONTENT = 204
    STATUS_226_IM_USED = 226

    STATUS_301_MOVED_PERMANENTLY = 301
    STATUS_308_PERMANENT_REDIRECT = 308

    STATUS_400_BAD_REQUEST = 400
    STATUS_401_UNAUTHORIZED = 401
    STATUS_403_FORBIDDEN = 403
    STATUS_NOT_FOUND = 404

    STATUS_500_INTERNAL_SERVER_ERROR = 500
    STATUS_503_SERVICE_UNAVAILABLE = 503
    STATUS_504_GATEWAY_TIMEOUT = 504
    STATUS_511_NETWORK_AUTHENTICATION_REQUIRED = 511


class CountMatrixInput(Enum):
    """
    Constants for the count matrix input type.

    """

    X: str = "X"
    RAW_X: str = "raw.X"


class Headers:
    """
    Header constants that are potentially sent to the CAS API.

    """

    # The authorization header.
    authorization = "Authorization"
    # The client session id that is used to track a user's CAS client session.
    client_session_id = "x-client-session-id"
    # The client action id that is used to track a user's logical action that may span multiple requests.
    client_action_id = "x-client-action-id"
