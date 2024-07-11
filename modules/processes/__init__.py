from .Start import StartProcess
from .StepHandler import NextStepHandler
from .Restrict import KillProcess, ShutUpProcess, UnmuteProcess
from .Interactive import InteractiveProcess
from .ChangeCustomNameProcess import ChangeCustomNameProcess

handlers_to_add = [
    NextStepHandler,

    StartProcess,
    InteractiveProcess,
    ChangeCustomNameProcess,

    KillProcess,
    ShutUpProcess,
    UnmuteProcess,
]
