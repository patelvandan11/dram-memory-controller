from controller.scheduler import FCFSScheduler
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType

scheduler = FCFSScheduler()

scheduler.add_request(
    MemoryRequest(
        request_id=1,
        address=0x1000,
        row=10,
        column=5,
        bank=0,
        operation=RequestType.READ,
        arrival_time=0,
    )
)

scheduler.add_request(
    MemoryRequest(
        request_id=2,
        address=0x2000,
        row=20,
        column=7,
        bank=1,
        operation=RequestType.WRITE,
        arrival_time=2,
    )
)

print(scheduler.queue_length())

print(scheduler.peek_next_request())

print(scheduler.remove_request())

print(scheduler.queue_length())