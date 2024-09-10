import logging
import weakref

from .wsHandle import InoDriveWS
from .file import File
from .discoverWs import DiscoverWs
from .IO import IO
from .userApp import UserApp
from .sysControl import SysControl


class InoDrive(object):
    _kwargs = None
    _callbacks = {}
    _connection_handle_instance = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        logging.debug('Create InoDrive instance...')
        self._auto_connect = kwargs.get('autoConnect', False)

        # ==============================================================================================================
        # MODULES BEGIN
        # ==============================================================================================================
        self.File = File(**kwargs, get_connection_handle=self._get_connection_handle)
        self.Discover = DiscoverWs(**kwargs, get_connection_handle=self._get_connection_handle)
        self.IO = IO(**kwargs, get_connection_handle=self._get_connection_handle)
        self.UserApp = UserApp(**kwargs, get_connection_handle=self._get_connection_handle)
        self.SysControl = SysControl(**kwargs, get_connection_handle=self._get_connection_handle)
        # ==============================================================================================================
        # MODULES END
        # ==============================================================================================================

        # ==============================================================================================================
        # CONNECTION
        # ==============================================================================================================
        if "useFallback" in self._kwargs:
            self._use_fallback = False if self._kwargs["useFallback"] == False else True
        else:
            self._use_fallback = True

        if "secureConnection" in self._kwargs:
            False if self._kwargs["secureConnection"] == False else True
        else:
            self._kwargs["secureConnection"] = True

        if self._auto_connect:
            self.connect()
        # ==============================================================================================================
        # CONNECTION END
        # ==============================================================================================================

        # Finalizer weak reference to ensure InoDrive Object is cleaned up on code exit
        self._finalizer = weakref.finalize(self, self.dispose)

    def __del__(self):
        self._finalizer()

    def dispose(self):
        try:
            if self.UserApp:
                self.UserApp.dispose()

            if self._connection_handle_instance is not None:
                self._connection_handle_instance = self._connection_handle_instance.dispose()
        except Exception as ex:
            logging.exception(ex)

    def connect(self):
        try:
            if self._connection_handle_instance is None:
                # Connection handle is not created yet
                if self._kwargs["secureConnection"]:
                    try:
                        connection_handle = InoDriveWS(**self._kwargs, callbacks=self._callbacks, secure=True)
                        connection_handle.connect()
                        self._connection_handle_instance = connection_handle
                    except Exception as ex:
                        logging.exception(ex)
                        if connection_handle:
                            connection_handle = connection_handle.dispose()

                        if not self._use_fallback:
                            return
                else:
                    connection_handle = InoDriveWS(**self._kwargs, callbacks=self._callbacks, secure=False)
                    connection_handle.connect()
                    self._connection_handle_instance = connection_handle
            else:
                self._connection_handle_instance.connect()
        except Exception as ex:
            logging.exception(ex)

    def disconnect(self):
        try:
            if self._connection_handle_instance is not None:
                self._connection_handle_instance.disconnect()
        except Exception as ex:
            logging.exception(ex)

    def set_target(self, target):
        if type(target) is not str:
            return

        if self._connection_handle_instance is not None:
            return self._connection_handle_instance.set_target(target)

        self._kwargs.host = target

    def on(self, evt, func):
        try:
            match evt:
                case "connect":
                    self._callbacks['onConnect'] = func if callable(func) else None
                case "disconnect":
                    self._callbacks['onDisconnect'] = func if callable(func) else None
                case "error":
                    self._callbacks['onError'] = func if callable(func) else None
                case "message":
                    self._callbacks['onMessage'] = func if callable(func) else None
        except Exception as ex:
            logging.exception(ex)

    @property
    def connected(self):
        if self._connection_handle_instance is not None:
            return self._connection_handle_instance.connected

        return False

    def _get_connection_handle(self):
        if self._connection_handle_instance is not None:
            return self._connection_handle_instance
