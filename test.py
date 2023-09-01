from app.services.utils import GlobalApiClient


GLOBALSMM_API_URL = 'https://global-smm.com/api/v2/'
GLOBALSMM_API_KEY = 'b3e9a678aca8c3657dd23ef40572368e'

client = GlobalApiClient(GLOBALSMM_API_URL, GLOBALSMM_API_KEY)
status = client.get_status(22459555)
print(status)
