# auth settings
ESCHER_TOKEN_URL = '/apisec/escher/token_management/serviceapi/apisec_token_management/token'
SCOPE = 'MARVIN_SDK'
SIGN_URL = '/jwt'  # we sign a fixed endpoint serviceME rather than the explicit request
JWT_TIMEOUT_MS = 1800000  # 30 minutes

DEFAULT_BASE_URL = "https://panoptica.inspection.marvin.prod.outshift.ai"
DEFAULT_AUTH_HOST = "https://auth.marvin.prod.outshift.ai"
