import unittest

from core.log_args import LogArgumentsError, parse_log_arguments


class LogArgumentParsingTests(unittest.TestCase):
    def test_default_line_count_and_optional_service(self):
        self.assertEqual(
            (None, 40),
            parse_log_arguments([]),
        )
        self.assertEqual(
            ("gateway", 40),
            parse_log_arguments(["gateway"]),
        )

    def test_short_and_long_options_before_or_after_service(self):
        self.assertEqual(
            (None, 5),
            parse_log_arguments(["-n", "5"]),
        )
        self.assertEqual(
            ("gateway", 5),
            parse_log_arguments(["--lines", "5", "gateway"]),
        )
        self.assertEqual(
            ("gateway", 5),
            parse_log_arguments(["gateway", "-n", "5"]),
        )
        self.assertEqual(
            (None, 7),
            parse_log_arguments(["--lines=7"]),
        )

    def test_rejects_non_positive_or_non_integer_counts(self):
        for arguments in (
            ["-n", "0"],
            ["--lines", "-2"],
            ["--lines", "1.5"],
            ["--lines", "five"],
            ["--lines="],
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaisesRegex(
                    LogArgumentsError,
                    "positive integer",
                ):
                    parse_log_arguments(arguments)

    def test_rejects_missing_duplicate_and_extra_arguments(self):
        for arguments in (
            ["--lines"],
            ["-n", "5", "--lines", "6"],
            ["gateway", "frontend"],
            ["--unknown"],
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaises(LogArgumentsError):
                    parse_log_arguments(arguments)


if __name__ == "__main__":
    unittest.main()
