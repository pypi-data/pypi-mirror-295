import os
import sys
import asyncio
import logging
from easyschedule import EasyScheduler
from syncservers.config import Config, ConfigSync
from syncservers.async_task_queue import AsyncTaskQueue
from syncservers.syncs import LiveSync, CronSync


logger = logging.getLogger(__name__)


class SyncServersApp:

    def __init__(self, config_file_path, schedule=None) -> None:
        self._config_file_path = config_file_path
        self._schedule = schedule

    async def run(self):
        tasks = self._run()
        # wait for tasks
        await asyncio.gather(*tasks)

    def _run(self):
        logger.info(f"starting sync servers")

        tasks = []

        # config
        config = Config(self._config_file_path)
        if not config.load_config():
            sys.exit(1)

        config_sync = ConfigSync(config)

        config_sync_task = config_sync.run()
        tasks.append(config_sync_task)

        # scheduler
        if not self._schedule:
            self._schedule = EasyScheduler()
            schedule_task = asyncio.create_task(self._schedule.start())
            tasks.append(schedule_task)

        # async queue
        async_queue = AsyncTaskQueue(config)

        async_queue_tasks = async_queue.run()
        tasks.extend(async_queue_tasks)

        # live sync
        if config.get_path_mappings(LiveSync.PATH_TYPE):
            live_sync = LiveSync(config, async_queue)
            live_sync.add_retry_task_to_schedule(self._schedule)
            live_sync.add_to_startup_sync()
            live_sync_tasks = live_sync.run()
            tasks.extend(live_sync_tasks)

        # cron sync
        if config.get_path_mappings(CronSync.PATH_TYPE):
            cron_sync = CronSync(config, async_queue)
            cron_sync.add_retry_task_to_schedule(self._schedule)
            cron_sync.add_to_startup_sync()
            cron_sync.add_to_schedule(self._schedule)

        return tasks


if __name__ == "__main__":
    # init logging
    from syncservers import config_logging
    logs_folder_path = os.path.abspath("logs")
    os.makedirs(logs_folder_path, exist_ok=True)
    log_file_path = os.path.join(logs_folder_path, "syncservers.log")
    config_logging(log_file_path)

    # config
    config_file_path = os.path.abspath(os.path.join("config", "syncservers.ini"))

    app = SyncServersApp(config_file_path)
    asyncio.run(app.run())
