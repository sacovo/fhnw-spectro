from dataclasses import dataclass


@dataclass
class PatchPosition:
    x: int
    y: int
    w: int
    h: int
    rotation_angle: float


@dataclass
class Config:
    patch_position: PatchPosition
