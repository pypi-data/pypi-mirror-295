"""This is the tool used to parse common-used command line arguments for Kasheesh ETLs.
"""


import argparse
from pandas import to_datetime, Timedelta, Timestamp
from kasheesh_tools.tool_logger import get_my_logger

class ToolCmdParser:
    def __init__(self, name='ToolCmdParser', custom_args=None):
        """* no arguments given: full history
           * only given start_date: data on and after start_date
           * only given end_date: data on and before end_date
           * only given --scheduled_job: data on current date
           * given mixed start_date/end_date & scheduled_job: start_date/end_date will be ignored and only run data on current date

        Args:
            name (str, optional): _description_. Defaults to 'ToolCmdParser'.
            custom_args (list, optional): [(name, type, help)]. Defaults to None.
        """
        self.logger = get_my_logger(name=name)
        self.parser = argparse.ArgumentParser()
        if custom_args:
            for arg in custom_args:
                self.parser.add_argument(f'--{arg[0]}', type=arg[1], help=arg[2])
        self.parser.add_argument('--start_datetime', type=str, help='starting datetime of the transactions')
        self.parser.add_argument('--end_datetime', type=str, help='ending datetime of the transactions')
        self.parser.add_argument('--scheduled_job', type=bool, help='whether this is a scheduled job', action=argparse.BooleanOptionalAction)
        self.parser.add_argument('--freq', type=str, help='frequency of the scheduled job')
        self.args = self.parser.parse_args()

    def _get_freq(self):
        if self.args.freq:
            self.freq = self.args.freq
        else:
            self.freq = 'day'
        self.logger.info(f'freq: {self.freq}')

    def _get_start_datetime(self):
        if self.args.start_datetime:
            if self.args.scheduled_job:
                self.logger.warning('start_datetime will be ignored for scheduled jobs.')
            self.start_datetime = to_datetime(self.args.start_datetime)
        else:
            self.start_datetime = None
        self.logger.info(f'start_datetime: {self.start_datetime}')

    def _get_end_datetime(self):
        if self.args.end_datetime:
            if self.args.scheduled_job:
                self.logger.warning('end_datetime will be ignored for scheduled jobs.')
            self.end_datetime = to_datetime(self.args.end_datetime)
        else:
            self.end_datetime = None
        self.logger.info(f'end_datetime: {self.end_datetime}')

    def _get_scheduled_job(self):
        if self.args.scheduled_job:
            self.scheduled_job = True
            if self.freq == 'day':
                standard_date = Timestamp.utcnow()
                self.start_datetime = standard_date - Timedelta(days=1)
                self.start_datetime = self.start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
                self.end_datetime = standard_date
                self.end_datetime = self.end_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
                self.end_datetime = self.end_datetime - Timedelta(microseconds=1)
            elif self.freq == 'hour':
                standard_date = Timestamp.utcnow()
                self.start_datetime = standard_date - Timedelta(hours=1)
                self.start_datetime = self.start_datetime.replace(minute=0, second=0, microsecond=0)
                self.end_datetime = standard_date
                self.end_datetime = self.end_datetime.replace(minute=0, second=0, microsecond=0)
                self.end_datetime = self.end_datetime - Timedelta(microseconds=1)
            else:
                self.logger.error('Invalid frequency in kasheesh_tools.tool_cmd_parser.ToolCmdParser._get_scheduled_job')
        else:
            self.scheduled_job = False
        self.logger.info(f'scheduled_job: {self.scheduled_job}')

    def get_args(self):
        self._get_freq()
        self._get_start_datetime()
        self._get_end_datetime()
        self._get_scheduled_job() # this will override the start_date and end_date if it's a scheduled job
        self.start_date = self.start_datetime
        self.end_date = self.end_datetime
        return