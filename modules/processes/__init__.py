from .Start import StartProcess
from .StepHandler import NextStepHandler
from .Restrict import KillProcess

handlers_to_add = [
    NextStepHandler,

    StartProcess,
    KillProcess,
]
