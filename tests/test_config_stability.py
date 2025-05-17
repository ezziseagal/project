from pyats.topology import loader
from genie.libs.sdk.triggers.blitz.blitz import Blitz
from genie.harness.main import gRun

def main():
    testbed = loader.load('testbed.yaml')

    gRun(
        trigger_datafile='tests/config_change_check.yaml',
        testbed=testbed
    )

if __name__ == '__main__':
    main()
