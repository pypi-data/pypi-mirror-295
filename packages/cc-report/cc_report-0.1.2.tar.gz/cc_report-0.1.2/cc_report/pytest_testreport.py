# -*- coding: utf-8 -*-
import platform
import requests
import datetime
import json
import os
import time
import pytest
from jinja2 import Environment, FileSystemLoader

test_result = {
    "title": "",
    "tester": "",
    "desc": "",
    "cases": {},
    'rerun': 0,
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "start_time": 0,
    "run_time": 0,
    "begin_time": "",
    "all": 0,
    "testModules": set(),
    "test_env": "",  # 2024.9.10 add
    "business": ""  # 2024.9.11 add
}


# =============2024。6。27===========

def time_strp(cur_time):
    struct_time = time.strptime(cur_time, "%Y-%m-%d_%H_%M_%S")
    timestamp = int(time.mktime(struct_time))
    return timestamp


def send_lark(content='test_result', executors=None, channel="cb513bbf-9121-4674-bebc-036124033284"):
    executors = [] if not executors else executors
    send_url = 'http://qa-platform-release:8080/msg/sendTestResult'
    # send_url = 'http://172.23.75.11:8080/msg/sendTestResult'
    json_data = {
        "channel": channel,
        "content": content,
        "executors": executors
    }
    requests.post(url=send_url, json=json_data)


def exec_record(**kwargs):
    exec_url = 'http://qa-flask-server:8080/autotest_record'
    # exec_url = 'http://172.23.74.62:8080/autotest_record'
    requests.post(url=exec_url, json=kwargs)


# ===============END=================

def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, dict):
        return val.get('title') or val.get('desc')


def pytest_runtest_logreport(report):
    report.duration = '{:.6f}'.format(report.duration)
    test_result['testModules'].add(report.fileName)
    if report.when == 'call':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        test_result["cases"][report.nodeid] = report
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        test_result["cases"][report.nodeid] = report


def pytest_sessionstart(session):
    start_ts = datetime.datetime.now()
    test_result["start_time"] = start_ts.timestamp()
    test_result["begin_time"] = start_ts.strftime("%Y-%m-%d %H:%M:%S")


def handle_history_data(report_dir, test_result):
    """
    处理历史数据
    :return:
    """
    try:
        # with open(os.path.join(report_dir, 'history.json'), 'r', encoding='utf-8') as f:
        with open(os.path.join(report_dir, 'reports', 'history.json'), 'r', encoding='utf-8') as f:
            history = json.load(f)
    except:
        history = []
    history.append({'success': test_result['passed'],
                    'all': test_result['all'],
                    'fail': test_result['failed'],
                    'skip': test_result['skipped'],
                    'error': test_result['error'],
                    'runtime': test_result['run_time'],
                    'begin_time': test_result['begin_time'],
                    'pass_rate': test_result['pass_rate'],
                    })

    # with open(os.path.join(report_dir, 'history.json'), 'w', encoding='utf-8') as f:
    with open(os.path.join(report_dir, 'reports', 'history.json'), 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=True)
    return history


def pytest_sessionfinish(session):
    """在整个测试运行完成之后调用的钩子函数,可以在此处生成测试报告"""
    report2 = session.config.getoption('--report')

    if report2:
        test_result['title'] = session.config.getoption('--title') or '测试报告'
        test_result['tester'] = session.config.getoption('--tester') or '小测试'
        test_result['desc'] = session.config.getoption('--desc') or '无'
        test_result['test_env'] = session.config.getoption('--testenv') or '无'  # 2024.9.10 add
        test_result['business'] = session.config.getoption('--business') or '无'  # 2024.9.10 add
        templates_name = session.config.getoption('--template') or '1'
        name = report2
    else:
        return

    if not name.endswith('.html'):
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name + '.html'
    else:
        file_name = time.strftime("%Y-%m-%d_%H_%M_%S") + name

    # if os.path.isdir('reports'):
    #     pass
    # else:
    #     os.mkdir('reports')
    # ===========
    paths = str(report2).split('/')[-4:]
    # paths[-1] = time.strftime("%Y-%m-%d_%H_%M_%S_") + paths[-1]
    # ===========
    file_name = os.path.join(*paths)
    test_result["run_time"] = '{:.6f} s'.format(time.time() - test_result["start_time"])
    test_result['all'] = len(test_result['cases'])
    if test_result['all'] != 0:
        test_result['pass_rate'] = '{:.2f}'.format(test_result['passed'] / test_result['all'] * 100)
    else:
        test_result['pass_rate'] = 0
    # 保存历史数据
    # test_result['history'] = handle_history_data('reports', test_result)
    test_result['history'] = handle_history_data(paths[0], test_result)
    # 渲染报告
    template_path = os.path.join(os.path.dirname(__file__), './templates')
    env = Environment(loader=FileSystemLoader(template_path))

    if templates_name == '2':
        template = env.get_template('templates2.html')
    else:
        template = env.get_template('templates.html')
    report = template.render(test_result)
    with open(file_name, 'wb') as f:
        f.write(report.encode('utf8'))
    # ================2024.6.24================
    report_time = paths[-1].split('.')[0]
    context = f'执行环境：{test_result["test_env"]}\n' \
              f'场景描述：{test_result["desc"]}\n' \
              f'用例总数：{test_result["all"]}\n' \
              f'执行通过率：{test_result["pass_rate"]}%\n' \
              f'报告地址：http://upex-ui-test-rest.test1.bitget.tools/api/uiTestExecution/viewReport/{time_strp(report_time)}\n'
    if 'macos' in platform.platform().lower():
        pass
    else:
        if test_result['test_env'] == 'online':
            executors = ["cc.cheng", "sum.sum"] if test_result['failed'] else []
            send_lark(content=context, executors=executors, channel='ff1108a1-ea42-4a80-8d9e-1a560d82b4e8')
        else:
            executors = [test_result['tester']]
            send_lark(content=context, executors=executors)
        if test_result["pass_rate"]:
            exec_record(business_type=test_result["business"], executor=test_result['tester'],
                        exec_env=test_result['test_env'], begin_time=test_result['begin_time'],
                        exec_time=test_result['run_time'], all_case=test_result['all'],
                        success_case=test_result['passed'], fail_case=test_result['failed'],
                        case_desc=test_result["desc"], pass_rate=f'{test_result["pass_rate"]}%')
    # ================END==================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    fixture_extras = getattr(item.config, "extras", [])
    plugin_extras = getattr(report, "extra", [])
    report.extra = fixture_extras + plugin_extras
    report.fileName = item.location[0]
    if hasattr(item, 'callspec'):
        report.desc = item.callspec.id or item._obj.__doc__
    else:
        report.desc = item._obj.__doc__
    report.method = item.location[2].split('[')[0]


def pytest_addoption(parser):
    group = parser.getgroup("testreport")
    group.addoption(
        "--report",
        action="store",
        metavar="path",
        default=None,
        help="create html report file at given path.",
    )
    group.addoption(
        "--title",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a title of the report",
    )
    group.addoption(
        "--tester",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a tester of the report",
    )
    group.addoption(
        "--desc",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a description of the report",
    )
    group.addoption(
        "--template",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a template of the report",
    )
    group.addoption(  # 2024.9.10 add
        "--testenv",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a template of the report",
    )
    group.addoption(  # 2024.9.11 add
        "--business",
        action="store",
        metavar="path",
        default=None,
        help="pytest-testreport Generate a template of the report",
    )
