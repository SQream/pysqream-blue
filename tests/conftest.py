

def pytest_addoption(parser):
    parser.addoption("--ip", action="store", help="SQream Server ip")


def pytest_generate_tests(metafunc):
    metafunc.config.getoption("ip")
