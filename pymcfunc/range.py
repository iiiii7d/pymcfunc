from dataclasses import dataclass


@dataclass
class FloatRange:
    lower: int | float | Ellipsis
    upper: int | float | Ellipsis

    def __str__(self):
        lower_str = "" if self.lower is ... else str(self.lower)
        upper_str = "" if self.upper is ... else str(self.upper)
        return lower_str + ".." + upper_str