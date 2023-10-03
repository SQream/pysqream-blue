
def pytest_addoption(parser):
    parser.addoption("--domain", action="store", help="SQream Server ip", required=True)
    parser.addoption("--use_logs", action="store_true", help="use logs", default=False)
    parser.addoption("--log_path", action="store", help="path of logs", default=None)
    parser.addoption("--log_level", action="store", help="log level", default='INFO')


def pytest_generate_tests(metafunc):
    metafunc.config.getoption("domain")
