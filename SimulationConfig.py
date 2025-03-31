from dataclasses import dataclass
from typing import List
import json

@dataclass
class GlobalParameters:
    numHubs: int
    numPeople: int
    gamma: float
    betaValues: List[float]

    @staticmethod
    def from_dict(data: dict) -> "GlobalParameters":
        return GlobalParameters(
            numHubs=data["numHubs"],
            numPeople=data["numPeople"],
            gamma=data["gamma"],
            betaValues=data["betaValues"]
        )

@dataclass
class Pattern:
    name: str
    percentage: int
    matrix: List[List[float]]

    @staticmethod
    def from_dict(data: dict) -> "Pattern":
        return Pattern(
            name=data["name"],
            percentage=data["percentage"],
            matrix=data["matrix"]
        )

@dataclass
class Config:
    globalParameters: GlobalParameters
    patterns: List[Pattern]

    @staticmethod
    def from_dict(data: dict) -> "Config":
        return Config(
            globalParameters=GlobalParameters.from_dict(data["globalParameters"]),
            patterns=[Pattern.from_dict(p) for p in data["patterns"]],
        )