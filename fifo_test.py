from controller.scheduler import FCFSScheduler
from memory_requests.memory_request import MemoryRequest
from utils.enums import RequestType

scheduler = FCFSScheduler()

for i in range(5):
    scheduler.add_request(
        MemoryRequest(
            request_id=i,
            address=1000 + i,
            row=i,
            column=0,
            bank=0,
            operation=RequestType.READ,
            arrival_time=i,
        )
    )

while scheduler.queue_length() > 0:
    print(scheduler.remove_request())