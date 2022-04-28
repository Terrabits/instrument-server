from asyncio import all_tasks



def no_clients_running():
    # this should be the only task
    return len(all_tasks()) == 1
