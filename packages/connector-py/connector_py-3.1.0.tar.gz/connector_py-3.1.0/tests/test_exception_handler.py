from types import FunctionType
from typing import Any
from unittest import (
    TestCase,
)

from connector.errors import ConnectorError, ErrorCodes, ExceptionHandler
from connector.serializers.lumos import (
    EncounteredErrorResponse,
)
from connector.serializers.response import Response
from connector.sync_.exception_handler import connector_handler


class TestExceptionHandler(TestCase):
    def test_class_decorator_decorates_methods_correctly(self):
        # Mock a class with some methods
        class TestClass:
            def method1(self):
                pass

            def method2(self):
                pass

        # Call the class decorator
        decorated_class = connector_handler([])(TestClass)

        # Verify that methods are decorated
        self.assertTrue(hasattr(decorated_class.method1, "__wrapped__"))
        self.assertTrue(hasattr(decorated_class.method2, "__wrapped__"))

    def test_class_decorator_handles_exceptions(self):
        # Mock a class with some methods
        class TestClass:
            def method1():
                raise ValueError("Error 1")  # Raise a ValueError

        # Call the class decorator
        decorated_class = connector_handler([])(TestClass)
        raised = False
        response = None

        try:
            response = decorated_class.method1()
        except ValueError:
            raised = True

        # Verify that the exception was not raised and handled gracefully
        self.assertFalse(raised, "ValueError not raised")
        self.assertLogs("connector.errors", level="ERROR")
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.response, EncounteredErrorResponse)

    def test_class_decorator_handles_undefined_exceptions(self):
        # Mock a custom error class
        class CustomError(Exception):
            pass

        # Mock a class with some methods
        class TestClass:
            def method1():
                raise CustomError("Custom Error has been handled")  # Raise a custom error

        # Call the class decorator
        decorated_class = connector_handler([])(TestClass)
        raised = False
        response = None

        try:
            response = decorated_class.method1()
        except Exception:
            raised = True

        # Verify that the exception was not raised and handled gracefully
        self.assertFalse(raised, "CustomError not raised")
        self.assertLogs("connector.errors", level="ERROR")
        self.assertEqual(response.response.message, "Custom Error has been handled")

    def test_class_decorator_handles_connector_exception(self):
        # Mock a class with some methods
        class TestClass:
            app_id = "test"

            def method1():
                raise ConnectorError(
                    "ConnectorError has been raised.", ErrorCodes.INTERNAL_ERROR
                )  # Raise a ConnectorError

        # Call the class decorator
        decorated_class = connector_handler([])(TestClass)
        raised = False
        response = None

        try:
            response = decorated_class.method1()
        except ConnectorError:
            raised = True

        # Verify that the exception was not raised and handled gracefully, with an error code
        self.assertFalse(raised, "ConnectorError not raised")
        self.assertEqual(response.response.message, "ConnectorError has been raised.")
        self.assertEqual(response.response.error_code, "test.internal_error")

    def test_class_decorator_handles_custom_handler(self):
        # Mock a class with some methods
        class TestClass:
            app_id = "test"

            def method1():
                raise ValueError("ValueError has been raised.")  # Raise a ConnectorError

        # Create a custom handler class
        class CustomHandler(ExceptionHandler):
            @staticmethod
            def handle(
                e: Exception,
                original_func: FunctionType,
                response: Response[Any],
                error_code: str | ErrorCodes | None = None,
            ) -> Response[Any]:
                response.response.error_code = "custom_error_code"
                return response

        # Call the class decorator
        decorated_class = connector_handler([(ValueError, CustomHandler, None)])(TestClass)
        raised = False
        response = None

        try:
            response = decorated_class.method1()
        except ConnectorError:
            raised = True

        # Verify that our custom handler was ran and the exception was handled gracefully
        self.assertFalse(raised, "Error not raised")
        self.assertEqual(response.response.message, "ValueError has been raised.")
        self.assertEqual(response.response.error_code, "custom_error_code")
