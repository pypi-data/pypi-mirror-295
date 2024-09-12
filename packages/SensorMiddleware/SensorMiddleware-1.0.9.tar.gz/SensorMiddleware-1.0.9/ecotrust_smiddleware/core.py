# -*- coding: utf-8 -*-
from ecotrust_smiddleware.aws import get_scan_data_from_s3_bucket
from ecotrust_smiddleware.abstract import Sensor
from pathlib import Path
from typing import NoReturn, AnyStr, Dict, Union
from requests_toolbelt.sessions import BaseUrlSession
from requests import Response
from rich import print # noqa

try:
    from typing import Final
except ImportError:
    from typing_extensions import Final

import requests.exceptions
import configparser
import os
import json
import time
import io

DEBUG = os.getenv('DEBUG', False)


# URL That should be called back when the scan finishes or some error occurs
# AUTOMATICALLY INJECTED BY ECS FARGATE
SCAN_CALLBACK_URL = os.getenv('SCAN_CALLBACK_URL')


class BadManifestSyntax(SyntaxError):
    """
        Raised when manifest.ini is not with the proper syntax/sections.
    """
    pass


class CannotReadScanData(Exception):
    """
        Raised when the scan data cannot be read from envvar/...
    """
    pass


class Super:
    """
        Non-canonical class to refer to the super within the upper class
    """
    pass


class SensorControler(Sensor):
    SENSOR_MANIFEST_PATH	= Path('/opt/manifest.ini') # noqa

    # Keys to get in the manifest.ini
    SENSOR_PATH_CNF_NAME    = 'sensor_path' # noqa
    SENSOR_PORT_CNF_NAME    = 'default_port' # noqa
    SENSOR_ENGINE_CNF_NAME  = 'engine_proc_name' # noqa

    ENGINE_READY_STATUS 	= 'READY' # noqa
    ENGINE_ERROR_STATUS 	= 'ERROR' # noqa
    SCAN_RUNNING_STATUS 	= ['STARTED', 'SCANNING', 'PAUSING', 'STOPING', 'UNKNOWN'] # noqa
    SCAN_ERROR_STATUS       = ['ERROR', 'INEXISTENT-SCAN'] # noqa
    SCAN_FINISHED_STATUS    = ['FINISHED'] # noqa

    def __init__(self, manifest=None, scan_data=None):
        self.scan_data: 	  Union[Dict, None] = None
        self.sensor_manifest: Union[Dict, None] = None
        self._sensor_api:	  Union[SensorControler.SensorAPIControler, None] = None # noqa

        if scan_data:
            # GET SCAN DATA VIA STRING
            self.scan_data = scan_data
        else:
            # GET SCAN DATA FROM S3 BUCKET
            self._get_scan_from_s3_and_settovar()

        if manifest:
            # GET MANIFEST DATA VIA STRING
            config = configparser.ConfigParser()
            config.read_file(io.StringIO(manifest))
            self.sensor_manifest = dict(config['sensor_info'])
        else:
            # GET MANIFEST DATA FROM HOST MACHINE
            self._read_sensor_manifest_and_settovar()

        # Normalize some data
        self.scan_data['options'] = self.scan_data.pop('engine_policy', {})
        self.scan_data['scan_id'] = self.scan_data.pop('id', '4747')

        # Get engine name and scan id from readed scan data / manifest
        self.engine_name = self.sensor_manifest[SensorControler.SENSOR_ENGINE_CNF_NAME]  # noqa
        self.scan_id     = self.scan_data['scan_id']  # noqa

    @property
    def sensor_api(self):
        if self._sensor_api is None:
            # Initialize
            try:
                sensor_api_url_path = self.sensor_manifest[SensorControler.SENSOR_PATH_CNF_NAME]
                sensor_api_url_port = self.sensor_manifest[SensorControler.SENSOR_PORT_CNF_NAME]
            except KeyError:
                raise NameError('sensor_manifest is not initialized yet !')
            else:
                self._sensor_api = SensorControler._SensorAPIControler(sensor_api_url_path, sensor_api_url_port, self.scan_id)

        return self._sensor_api

    @staticmethod
    def fail_scan(error_message: str) -> NoReturn:
        if SCAN_CALLBACK_URL is None:
            print('[bold red] CRITICAL ERROR: SCAN_CALLBACK_URL is NULL [/bold red]')
            return

        callback_response = requests.get(SCAN_CALLBACK_URL, params={
            'errmsg': error_message,
            'status': 'error'
        })

        if DEBUG:
            print(f'[bold green] Callback repsonse:'
                  f'Status code: {callback_response.status_code} '
                  f'Text Response: {callback_response.text}')

    @staticmethod
    def finish_scan():
        if SCAN_CALLBACK_URL is None:
            print('[bold red] CRITICAL ERROR: SCAN_CALLBACK_URL is NULL [/bold red]')
            return

        callback_response = requests.get(SCAN_CALLBACK_URL, params={
            'errmsg': None,
            'status': 'finished'
        })

        if DEBUG:
            print(f'[bold green] Callback repsonse:'
                  f'Status code: {callback_response.status_code} '
                  f'Text Response: {callback_response.text}')

    def is_engine_process_running(self, __=None):
        return super().is_engine_process_running(self.engine_name)

    class _SensorAPIControler(Super):
        DEFAULT_PROTO = 'http'
        DEFAULT_ADDR  = '127.0.0.1' # noqa
        SCAN_STARTED_STATUS = ['accepted']
        SCAN_STOPPED_STATUS = ['SUCCESS', 'success']

        def __init__(self, base_api_path, base_api_port, scan_id):
            self.session = BaseUrlSession(f'{self.DEFAULT_PROTO}://{self.DEFAULT_ADDR}:{base_api_port}')
            self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=5)) # noqa
            self.base_path = base_api_path
            self.scan_id = scan_id
            self.is_scan_started = False

        def _make_request(self, method, *args, **kwargs) -> Dict:
            """
            Method that concats base_api_path to the middle of the URL and set some default values to the request.

            :param method: HTTP method
            :param args: Args to pass to the request method
            :param kwargs: Kwargs to pass to the request method
            :return: <Response> object
            """

            # Get req object
            do_request = getattr(self.session, method)

            # Do some changes
            kwargs['url'] = f'{self.base_path}{kwargs["url"][1:]}'
            kwargs['allow_redirects'] = False
            kwargs['verify'] = False

            # Do the request
            response: Response = do_request(*args, **kwargs)
            if DEBUG:
                print(f'[bold green] {method} -> {kwargs["url"]} RET: {response.status_code} TEXT: {response.text} [/bold green]') # noqa

            # Check for 5xx errors
            response.raise_for_status()

            # Parse response (JSON)
            try:
                rjson = response.json()
            except json.decoder.JSONDecodeError:
                rjson = {}
            # Todo: Log ?

            return rjson

        class _Decorators:
            @classmethod
            def after_scan_starts(cls, fn):
                """
                Decorator that checks if the scan is started before calling the function.
                :param fn:
                :return: wrapper
                """
                def wrapper(self, *args):
                    if not self.is_scan_started:
                        raise RuntimeError('Scan not started yet !')

                    return fn(self, *args)

                return wrapper

        def call_enginestatus(self) -> AnyStr:
            """
            Get engine status
            :return:
            """
            try:
                rjson = self._make_request(method='get', url='/status')
            except requests.exceptions.RequestException:
                rjson = {}

            return rjson.get('status', 'WAIT')

        def call_startscan(self, scan_data: Dict) -> (bool, AnyStr):
            """
            Starts a scan with the given data

            :param
            :return: (is_scan_started, refused_reason)
            """
            if DEBUG:
                print(f'[bold green] Calling /startscan with: {str(scan_data)} [/bold green]')
            rjson = self._make_request(method='post', url='/startscan', json=scan_data)

            is_accepeted = rjson['status'] in self.SCAN_STARTED_STATUS
            refused_reason = 'n/a'

            if not is_accepeted:
                try:
                    refused_reason = rjson['details']['reason']
                except KeyError:
                    refused_reason = 'n/a'
            else:
                self.is_scan_started = True

            return is_accepeted, refused_reason

        @_Decorators.after_scan_starts
        def call_stopscan(self) -> (bool, AnyStr):
            """
            Stop a scan with the given scan_id

            :param:
            :return: (is_scan_stopped, reason of error)
            """

            try:
                rjson = self._make_request(method='get', url=f'/stop/{str(self.scan_id)}')
            except requests.exceptions.RequestException:
                rjson = {}

            is_stopped = rjson.get('status', 'sucess') in self.SCAN_STOPPED_STATUS
            non_stopped_reason = 'n/a'

            if not is_stopped:
                try:
                    non_stopped_reason = rjson['reason']
                except KeyError:
                    non_stopped_reason = 'n/a'

            return is_stopped, non_stopped_reason

        @_Decorators.after_scan_starts
        def call_scanstatus(self) -> AnyStr:
            """
            :param:
            :return: Scan status
            """
            try:
                rjson = self._make_request(method='get', url=f'/status/{str(self.scan_id)}')
            except requests.exceptions.RequestException:
                rjson = {'status': 'NETWORK-ERROR'}

            return rjson.get('status', 'UNKNOWN')

        @_Decorators.after_scan_starts
        def call_getfindings(self) -> (bool, Dict, AnyStr):
            """
            Get findings from a scan
            :param:
            :return: (got the findings, findings, reason of error)
            """
            try:
                rjson = self._make_request(method='get', url=f'/getfindings/{str(self.scan_id)}')
            except requests.exceptions.RequestException:
                rjson = {}

            got_findings = rjson.get('status', 'ERROR') == 'success'
            err_reason = 'n/a'

            if not got_findings:
                try:
                    err_reason = rjson['reason']
                except KeyError:
                    err_reason = 'n/a'

            return got_findings, rjson, err_reason

    def _get_scan_from_s3_and_settovar(self) -> NoReturn:
        """
            Get data about the scan we're going to run.
        :return:
        """
        self.scan_data = get_scan_data_from_s3_bucket()

    def _read_sensor_manifest_and_settovar(self) -> NoReturn:
        """
            Reads and parses manifest.ini of the sensor, to get some important fields like:
                * sensor_path
                * default_dir
                .
        :return:
        """
        if not os.path.exists(SensorControler.SENSOR_MANIFEST_PATH):
            raise FileNotFoundError(f'Sensor Manifest file not Found in {SensorControler.SENSOR_MANIFEST_PATH.__str__()}!')

        config = configparser.ConfigParser()
        config.read(SensorControler.SENSOR_MANIFEST_PATH)

        try:
            # Read sensor info section
            self.sensor_manifest = dict(config['sensor_info'])

            # Assert if all the mandatory keys are present (Dev)
            assert SensorControler.SENSOR_PATH_CNF_NAME in self.sensor_manifest, 'key not found'
            assert SensorControler.SENSOR_PORT_CNF_NAME in self.sensor_manifest, 'key not found'
            assert SensorControler.SENSOR_ENGINE_CNF_NAME in self.sensor_manifest, 'key not found'

            # Assert if the mandatory keys are present, if no, raise a KeyError
            for mandatory_key in [
                SensorControler.SENSOR_PATH_CNF_NAME,
                SensorControler.SENSOR_PORT_CNF_NAME,
                SensorControler.SENSOR_ENGINE_CNF_NAME]:
                if mandatory_key not in self.sensor_manifest:
                    raise KeyError(f'Key {mandatory_key} not found in {SensorControler.SENSOR_MANIFEST_PATH} !')

        except KeyError:
            raise BadManifestSyntax(f'Section \"sensor_info\" not found in {SensorControler.SENSOR_MANIFEST_PATH} !')

    def start_scan(self) -> (bool, AnyStr):
        is_scan_started, refusal_msg = self.sensor_api.call_startscan(self.scan_data)
        return is_scan_started, refusal_msg

    def stop_scan(self):
        is_stopped, non_stopped_msg = self.sensor_api.call_stopscan()
        if not is_stopped:
            # Todo: Log ? (scan not stopped)
            pass

        return is_stopped

    def wait_scan(self) -> bool:
        """
        Blocking method that waits for some scan to be finished.
            -> Also checks if the engine process is still really running, if not, force the loop to break.
        :return: true|false -> Is report ready ? (status == FINISHED)
        """

        # Sleep vars
        ST_POOLING_TIME: 		 Final[int] = 2
        ST_MAX_WAIT_ENGINE:      Final[int] = 47
        ST_AFTER_ENGINE_EXIT:    Final[int] = 5

        # Error control vars
        MAX_NON_STOP_ERRORS:     Final[int] = 15 # noqa
        errnow = 0
        waitnw = 0
        is_report_ready = False

        # WAIT ENGINE PROC TO INIT (continue after ST_MAX_WAIT_ENGINE)
        while not self.is_engine_process_running():
            if DEBUG:
                print('[bold green] Waiting engine proc to init.. [/bold green]')

            time.sleep(ST_POOLING_TIME)
            waitnw += ST_POOLING_TIME

            if waitnw >= ST_MAX_WAIT_ENGINE:
                break

        # WAIT SCAN TO FINISH
        while True:
            # Get new status from the API
            scan_status: str = str(self.sensor_api.call_scanstatus()).upper()
            is_scan_running = scan_status in self.SCAN_RUNNING_STATUS
            is_report_ready = scan_status in self.SCAN_FINISHED_STATUS
            is_error_status = scan_status in self.SCAN_ERROR_STATUS

            if DEBUG:
                print(f'[bold green] Got scan status: {scan_status} [/bold green]')

            # 1º Break -> Report ready to be downloaded
            if is_report_ready:
                break

            # Error counter
            # Todo: replace for the match-case syntax in Python 3.10
            if is_error_status:
                errnow += 1
            else:
                errnow = 0

            # 2º Break -> Got consecutive "error" statuses
            if errnow >= MAX_NON_STOP_ERRORS:
                break

            # 3º Break -> Engine process is not running anymore
            if not self.is_engine_process_running():
                # Wait flask after getting things up 
                time.sleep(ST_AFTER_ENGINE_EXIT)

                # Get status again (just to make sure)
                scan_status = self.sensor_api.call_scanstatus()
                is_report_ready = scan_status in self.SCAN_FINISHED_STATUS
                break

            # 4º Break -> Scan is not running and not in error status (What happneed ? ! )
            if not is_scan_running and not is_error_status:
                break

            time.sleep(ST_POOLING_TIME)

        return is_report_ready

    def wait_report(self):
        """
            No need to be implemented.
        :return:
        """
        raise NotImplementedError

    def wait_engine(self):
        ST_POOLING_TIME: Final[int] = 2
        engine_status:   AnyStr     = self.sensor_api.call_enginestatus() # noqa

        if DEBUG:
            print(f'[bold green] Got first engine status: {engine_status}')

        # Wait for the engine to be ready
        while engine_status != self.ENGINE_READY_STATUS:
            # Check for errors
            if engine_status == self.ENGINE_ERROR_STATUS:
                raise RuntimeError('Engine hang with error!')

            time.sleep(ST_POOLING_TIME)
            engine_status = self.sensor_api.call_enginestatus()
            if DEBUG:
                print(f'[bold green] Got new status: {engine_status}')

    def get_report(self) -> (bool, Dict, AnyStr):
        """
        Get the report of the scan
        :return: Dict with the report
        """
        return self.sensor_api.call_getfindings()
