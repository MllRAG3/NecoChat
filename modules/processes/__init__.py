from .Start import StartProcess
from .StepHandler import NextStepHandler
from .Restrict import KillProcess, ShutUpProcess, UnmuteProcess
from .Interactive import InteractiveProcess
from .ChangeCustomNameProcess import ChangeCustomNameProcess
from .FWords import AddFWord, RemoveFWord, FWordsList
from .CheckFWords import CheckFWords
from .StatsProcess import SendUserStats, FinalLog

handlers_to_add = [
    NextStepHandler,

    StartProcess,
    InteractiveProcess,
    ChangeCustomNameProcess,

    KillProcess,
    ShutUpProcess,
    UnmuteProcess,

    AddFWord,
    RemoveFWord,
    FWordsList,
    CheckFWords,

    SendUserStats,
    FinalLog  # ВСЕГДА ПОСЛЕДНИЙ!!!
]
