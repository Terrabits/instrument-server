from   .basic_command import BasicCommand
import json


class ErrorsCommand(BasicCommand):
    # define
    command = "errors?"
    args    = {}

    def __init__(self, error_queue):
        super().__init__()
        self.error_queue = error_queue

    def code(self, devices, args):
        # process errors into strings
        prev_errors = [str(i) for i in self.error_queue]

        # clear queue
        self.error_queue.clear()

        # TODO: fix format
        return json.dumps(prev_errors)
