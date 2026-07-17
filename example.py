from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType

request = MemoryRequest(
    request_id=1,
    address=0x1A2B,
    row=128,
    column=64,
    bank=2,
    operation=RequestType.READ,
    arrival_time=15,
)

print(request)