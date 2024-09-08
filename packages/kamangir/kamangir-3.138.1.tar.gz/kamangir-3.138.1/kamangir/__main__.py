from kamangir import NAME, VERSION, DESCRIPTION, ICON
from kamangir import README
from kamangir.logger import logger
from blueness.argparse.generic import main

main(
    ICON=ICON,
    NAME=NAME,
    DESCRIPTION=DESCRIPTION,
    VERSION=VERSION,
    main_filename=__file__,
    tasks={
        "build_README": lambda _: README.build(),
    },
    logger=logger,
)
