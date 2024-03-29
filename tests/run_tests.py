from unittest import TextTestRunner, TestSuite, TestLoader
from tests.test_contact import TestContact
from tests.test_invoice import TestInvoice


test_cases = [
    TestContact,
    # TestInvoice,
]


def load_tests() -> TestSuite:
    loader = TestLoader()
    suite = TestSuite()

    for _test_case in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(_test_case))

    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(load_tests())
