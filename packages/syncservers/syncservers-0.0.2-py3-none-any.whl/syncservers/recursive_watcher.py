from pathlib import Path
import logging
from asyncinotify import Inotify, Mask


logger = logging.getLogger(__name__)


class RecursiveWatcher:
    """
    copied from https://github.com/ProCern/asyncinotify/blob/master/examples/recursivewatch.py
    """
    def __init__(self, path, mask) -> None:
        self._path = path
        self._mask = mask
    
    def _get_directories_recursive(self, path: Path):
        '''Recursively list all directories under path, including path itself, if
        it's a directory.

        The path itself is always yielded before its children are iterated, so you
        can pre-process a path (by watching it with inotify) before you get the
        directory listing.

        Passing a non-directory won't raise an error or anything, it'll just yield
        nothing.
        '''
        if path.is_dir():
            yield path
            for child in path.iterdir():
                yield from self._get_directories_recursive(child)

    async def watch_recursive(self):
        mask = self._mask | Mask.MOVED_FROM | Mask.MOVED_TO | Mask.CREATE | Mask.IGNORED
        with Inotify() as inotify:
            for directory in self._get_directories_recursive(self._path):
                logger.info(f"watching folder: {directory}")
                inotify.add_watch(directory, mask)

            # Things that can throw this off:
            #
            # * Moving a watched directory out of the watch tree (will still
            #   generate events even when outside of directory tree)
            #
            # * Doing two changes on a directory or something before the program
            #   has a time to handle it (this will also throw off a lot of inotify
            #   code, though)
            #
            # * Moving a watched directory within a watched directory will get the
            #   wrong path. This needs to use the cookie system to link events
            #   together and complete the move properly, which can still make some
            #   events get the wrong path if you get file events during the move or
            #   something silly like that, since MOVED_FROM and MOVED_TO aren't
            #   guaranteed to be contiguous.  That exercise is left up to the
            #   reader.
            #
            # * Trying to watch a path that doesn't exist won't automatically
            #   create it or anything of the sort.
            #
            # * Deleting and recreating or moving the watched directory won't do
            #   anything special, but it probably should.
            async for event in inotify:
                # Add subdirectories to watch if a new directory is added.  We do
                # this recursively here before processing events to make sure we
                # have complete coverage of existing and newly-created directories
                # by watching before recursing and adding, since we know
                # get_directories_recursive is depth-first and yields every
                # directory before iterating their children, we know we won't miss
                # anything.

                # logger.info(f"inotify event: {event}")

                if (Mask.CREATE in event.mask or Mask.MOVED_TO in event.mask) \
                    and Mask.ISDIR in event.mask and event.path is not None:
                    # create new folder, add watch
                    for directory in self._get_directories_recursive(event.path):
                        logger.info(f"watching folder: {directory}")
                        inotify.add_watch(directory, mask)
                
                if Mask.MOVED_FROM in event.mask and Mask.ISDIR in event.mask and event.path is not None:
                    # a folder is moved, remove watch for this folder and subfolders
                    for watch in inotify._watches.values():
                        if watch.path.is_relative_to(event.path):
                            logger.info(f"unwatching folder: {watch.path}")
                            inotify.rm_watch(watch)
                
                # If there is at least some overlap, assume the user wants this event.
                if event.mask & self._mask:
                    yield event
                else:
                    # Note that these events are needed for cleanup purposes.
                    # We'll always get IGNORED events so the watch can be removed
                    # from the inotify.  We don't need to do anything with the
                    # events, but they do need to be generated for cleanup.
                    # We don't need to pass IGNORED events up, because the end-user
                    # doesn't have the inotify instance anyway, and IGNORED is just
                    # used for management purposes.
                    pass
                    # logger.info(f"un-yielded event: {event}")                    
