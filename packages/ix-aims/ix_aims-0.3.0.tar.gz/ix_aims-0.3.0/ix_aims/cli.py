import datetime

import typer
from typing_extensions import Annotated

from .lib import auto_ix


def get_current_year():
    return datetime.datetime.utcnow().year


@typer.run
def main(
    doy: Annotated[int, typer.Argument(help="The collection GPS day of year")],
    year: Annotated[
        int,
        typer.Option(
            "--year", "-y", default_factory=get_current_year, help="The collection year"
        ),
    ],
    rgb: Annotated[
        bool,
        typer.Option("--rgb", "-3", help="Create RGB images instead of 4-band images"),
    ] = False,
    confidence: Annotated[
        float,
        typer.Option(
            "--confidence", "-c", help="Confidence level for image recognition"
        ),
    ] = 0.9,
):
    """For ACO WORK_ORDER, setup iX Capture with the correct configuration and
    calibration parameters."""
    auto_ix(year, doy, rgb, confidence)


if __name__ == "__main__":
    main()
