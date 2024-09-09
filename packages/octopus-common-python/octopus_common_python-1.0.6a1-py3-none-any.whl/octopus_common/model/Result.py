from octopus_common.model import ResultDetail


class Result:
    def __init__(self, task, result_detail: ResultDetail):
        self.taskType = task["type"]
        self.buildTime = task["buildTime"]
        self.taskId = task["id"]
        self.taskLevel = task["level"]
        self.resultDetail = result_detail.__dict__
        self.task = task
