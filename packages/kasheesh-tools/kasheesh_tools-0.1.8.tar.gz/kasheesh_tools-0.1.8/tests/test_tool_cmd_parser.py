from src.kasheesh_tools.tool_cmd_parser import ToolCmdParser
from collections import defaultdict
import shlex
from datetime import timedelta
import pandas as pd

if __name__ == '__main__':
    testing_map = defaultdict(dict)
    testing_map = {('20210101', '20210131', True, 'day'): {'start_datetime': pd.Timestamp.utcnow().date() - timedelta(days=1), 
                                                           'end_datetime': pd.Timestamp.utcnow().date() - timedelta(days=1),
                                                            'scheduled_job': True, 'freq': 'day'}, 
                   ('20210101-150000', '20210101-160000', True, 'day'): {'start_datetime': pd.Timestamp.utcnow().date() - timedelta(days=1), 
                                                                         'end_datetime': pd.Timestamp.utcnow().date() - timedelta(days=1),
                                                                         'scheduled_job': True, 'freq': 'day'},
                   ('20210101', '20210131', True, 'hour'): {'start_datetime': (pd.Timestamp.utcnow()  - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0),
                                                            'end_datetime': pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0),
                                                            'scheduled_job': True, 'freq': 'hour', }, 
                   ('20210101-150000', '20210101-160000', True, 'hour'): {
                                                            'start_datetime': (pd.Timestamp.utcnow() - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0),
                                                            'end_datetime': pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0),
                                                            'scheduled_job': True, 'freq': 'hour'}, 
                   ('20210101', '20210131', False, 'day'): {'start_datetime': '2021-01-01 00:00:00', 'end_datetime': '2021-01-31 00:00:00', 'scheduled_job': False, 'freq': 'day'},
                   ('20210101-150000', '20210101-160000', False, 'day'): {'start_datetime': '2021-01-01 15:00:00', 'end_datetime': '2021-01-01 16:00:00', 'scheduled_job': False, 'freq': 'day'}, 
                   ('20210101', '20210131', False, 'hour'): {'start_datetime': '2021-01-01 00:00:00', 'end_datetime': '2021-01-31 00:00:00', 'scheduled_job': False, 'freq': 'hour'}, 
                   ('20210101-150000', '20210101-160000', False, 'hour'): {'start_datetime': '2021-01-01 15:00:00', 'end_datetime': '2021-01-01 16:00:00', 'scheduled_job': False, 'freq': 'hour'}}
    cmdparser = ToolCmdParser()
    for key, value in testing_map.items():
        argString = ""
        argString += f" --start_datetime {key[0]} --end_datetime {key[1]} "
        if key[2]:
            argString += f' --scheduled_job --freq {key[3]} '
        else:
            argString += f' --freq {key[3]} '
        cmdparser.args = cmdparser.parser.parse_args(shlex.split(argString))
        cmdparser.get_args()
        assert pd.to_datetime(cmdparser.start_datetime, utc=True) == pd.to_datetime(value.get('start_datetime'), utc=True), f'{cmdparser.start_datetime} != {value.get("start_datetime")}'
        assert pd.to_datetime(cmdparser.end_datetime, utc=True) == pd.to_datetime(value.get('end_datetime'), utc=True), f'{cmdparser.end_datetime} != {value.get("end_datetime")}'
        assert cmdparser.scheduled_job == value.get('scheduled_job'), f'{cmdparser.scheduled_job} != {value.get("scheduled_job")}'
        assert cmdparser.freq == value.get('freq')
        print(f'{key} passed')
