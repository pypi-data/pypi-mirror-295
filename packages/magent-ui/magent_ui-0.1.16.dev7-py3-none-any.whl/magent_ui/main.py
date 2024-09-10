import uvicorn
import logging
from multiprocessing import cpu_count
from magent_ui.shared import SharedManager
from magent_ui.config import to_uvicorn_config, app_config
from agentuniverse.base.util.system_util import get_project_root_path
from uvicorn.config import LOGGING_CONFIG

# Use uvicorn's default logging configuration
logging.config.dictConfig(LOGGING_CONFIG)  # type: ignore


def launch(**kwargs):
    # init shared manager
    shared_manager = SharedManager()

    # init config
    project_root_path = get_project_root_path()
    app_config.load_config(project_root_path=project_root_path,
                           **kwargs)

    # launch server
    uvicorn_config = to_uvicorn_config(app_config.config)
    uvicorn.run('magent_ui.app_module:create_app', log_level='info',
                workers=cpu_count(),
                factory=True,  **uvicorn_config)

    # clean up
    shared_manager.cleanup()
