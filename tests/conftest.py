

def pytest_addoption(parser):
    parser.addoption("--domain", action="store", help="SQream Server ip",required=True)


def pytest_generate_tests(metafunc):
    metafunc.config.getoption("domain")
