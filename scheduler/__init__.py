from scheduler import token_scheduler
from scheduler import go_location_scheduler
from scheduler import call_scheduler
from scheduler import free_gossip_scheduler

token_scheduler.start()
go_location_scheduler.start()
call_scheduler.start()
free_gossip_scheduler.start()
