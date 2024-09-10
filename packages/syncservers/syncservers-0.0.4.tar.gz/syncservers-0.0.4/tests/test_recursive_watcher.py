import tempfile
import asyncio
import os
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from asyncinotify import Mask
from syncservers.recursive_watcher import RecursiveWatcher


class Test(IsolatedAsyncioTestCase):

    async def read_events(self, watcher, events):
        async for event in watcher.watch_recursive():
            print(f"path: {event.path.resolve()} event: {event}")
            events.append(event)

    async def test_watch_recursive(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            events = []
            
            watcher = RecursiveWatcher(Path(tmpdirname), Mask.CLOSE_WRITE | Mask.MOVED_TO | Mask.CREATE)
            watch_task = asyncio.create_task(self.read_events(watcher, events))

            await asyncio.sleep(0.3)
            # create file
            file_path = os.path.join(tmpdirname, "f1.txt")
            with open(str(file_path), "w") as f:
                f.write("filef1")
            
            await asyncio.sleep(0.3)
            # create folder and a file inside
            folder_path = os.path.join(tmpdirname, "d1")
            os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "d1f1.txt")
            with open(str(file_path), "w") as f:
                f.write("filed1f1")

            await asyncio.sleep(0.3)
            # move file
            file_path = os.path.join(tmpdirname, "f1.txt")
            move_file_path =  os.path.join(tmpdirname, "d1", "f1.txt")
            os.rename(file_path, move_file_path)

            await asyncio.sleep(0.3)
            # create cascade folders
            folder_path = os.path.join(tmpdirname, "d2", "dd1", "ddd1")
            os.makedirs(folder_path)

            await asyncio.sleep(0.3)
            # move folder
            folder_path = os.path.join(tmpdirname, "d2", "dd1")
            move_folder_path = os.path.join(tmpdirname, "d1", "dd1")
            os.rename(folder_path, move_folder_path)
            await asyncio.sleep(1)
            # then create file
            file_path = os.path.join(tmpdirname, "d1", "dd1", "ddd1", "ddd1f1.txt")
            with open(str(file_path), "w") as f:
                f.write("fileddd1f1")

            await asyncio.sleep(0.3)
            # delete folder
            folder_path = os.path.join(tmpdirname, "d2")
            os.removedirs(folder_path)

            await asyncio.sleep(0.3)
            # delete file
            file_path = os.path.join(tmpdirname, "d1", "d1f1.txt")
            os.remove(file_path)

            await asyncio.sleep(0.3)
            watch_task.cancel()
            await asyncio.gather(watch_task, return_exceptions=True)

            self.assertEqual(len(events), 8)
            self.assertEqual(str(events[0].path), os.path.join(tmpdirname, "f1.txt"))
            self.assertTrue(events[0].mask & Mask.CREATE)

            self.assertEqual(str(events[1].path), os.path.join(tmpdirname, "f1.txt"))
            self.assertTrue(events[1].mask & Mask.CLOSE_WRITE)

            self.assertEqual(str(events[2].path), os.path.join(tmpdirname, "d1"))
            self.assertTrue(events[2].mask & Mask.CREATE)
            self.assertTrue(events[2].mask & Mask.ISDIR)

            self.assertEqual(str(events[3].path), os.path.join(tmpdirname, "d1", "f1.txt"))
            self.assertTrue(events[3].mask & Mask.MOVED_TO)

            self.assertEqual(str(events[4].path), os.path.join(tmpdirname, "d2"))
            self.assertTrue(events[4].mask & Mask.CREATE)
            self.assertTrue(events[4].mask & Mask.ISDIR)

            self.assertEqual(str(events[5].path), os.path.join(tmpdirname, "d1", "dd1"))
            self.assertTrue(events[5].mask & Mask.MOVED_TO)
            self.assertTrue(events[5].mask & Mask.ISDIR)

            self.assertEqual(str(events[6].path), os.path.join(tmpdirname, "d1", "dd1", "ddd1", "ddd1f1.txt"))
            self.assertTrue(events[6].mask & Mask.CREATE)

            self.assertEqual(str(events[7].path), os.path.join(tmpdirname, "d1", "dd1", "ddd1", "ddd1f1.txt"))
            self.assertTrue(events[7].mask & Mask.CLOSE_WRITE)
