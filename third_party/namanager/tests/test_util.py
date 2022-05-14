import time

import namanager.tests.helper as helper
import namanager.util as util


ESCAPE_CHARS = ['.', '*', '?', '/', "\\", '^', '$']


class TestUtil():
    def test_name(self):
        name = util.name
        errors = []
        foo = 123
        global bar
        bar = 456
        self.baz = 789
        data = [
            {'expect': 'foo', 'actual': name(foo, locals())},
            {'expect': None, 'actual': name(bar, locals())},
            {'expect': None, 'actual': name(self.baz, locals())},
            {'expect': 'bar', 'actual': name(bar, globals())},
            {'expect': None, 'actual': name(foo, globals())},
            {'expect': None, 'actual': name(self.baz, globals())},
            {'expect': 'baz', 'actual': name(self.baz, self.__dict__)},
            {'expect': None, 'actual': name(foo, self.__dict__)},
            {'expect': None, 'actual': name(bar, self.__dict__)},
        ]

        for datum in data:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                datum['expect'] == datum['actual'],
                "Expect: {0}\nActual: {1}".format(
                    datum['expect'], datum['actual']))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_gen_unique_str(self):
        gen_unique_str = util.gen_unique_str
        u = gen_unique_str('')

        # functional testing
        s = ''
        assert gen_unique_str(s) not in s, Exception(
            "'{0}' is in '{1}'".format(gen_unique_str(s), s))
        s = u
        assert gen_unique_str(s) not in s, Exception(
            "'{0}' is in '{1}'".format(gen_unique_str(s), s))
        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            gen_unique_str(u * 256)

        assert time.time() - start < 1, Exception(
            'The algorithm is not efficient.')

    def test_get_first_word(self):
        get_first_word = util.get_first_word
        errors = []
        words = {'': ('', -1, 0),
                 'H': ('H', 0, 1),
                 'HTTP': ('HTTP', 0, 4),
                 'HTTPProtocol': ('HTTP', 0, 4),
                 'HttpProtocol': ('Http', 0, 4),
                 'httpProtocol': ('http', 0, 4),
                 '*H': ('H', 1, 2),
                 '*HTTP': ('HTTP', 1, 5),
                 '*HTTPProtocol': ('HTTP', 1, 5),
                 '*HttpProtocol': ('Http', 1, 5),
                 '*httpProtocol': ('http', 1, 5),
                 'H*': ('H', 0, 1),
                 'HTTP*': ('HTTP', 0, 4),
                 'HTTP*Protocol': ('HTTP', 0, 4),
                 'Http*Protocol': ('Http', 0, 4),
                 'http*Protocol': ('http', 0, 4),
                 }

        # functional testing
        for s, expect in words.items():
            actual = get_first_word(s)
            helper.append_to_error_if_not_expect_with_msg(
                errors, expect == actual, (
                    "expect is '{0}', actual is '{1}'".format(
                        expect, actual)))
        # benchmark
        start = time.time()
        for i in range(0, 1000):
            # 256 chars
            get_first_word('U' + 'l' * 255)
            get_first_word('Word' * 64)
            get_first_word('l' * 256)
            get_first_word('U' * 256)
        helper.append_to_error_if_not_expect_with_msg(
            errors, time.time() - start < 5, (
                'The algorithm is not efficient.'))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_get_words(self):
        get_words = util.get_words
        convert_words_to_case = util.convert_words_to_case
        errors = []
        test_data = {'lower_case': [
                        '',
                        '.',
                        '....',
                        'http.error.response.for.request.of.soap',
                        '.http.error.response.for.request.of.soap',
                        'http.error.response.for.request.of.soap.',
                        '.http.error.response.for.request.of.soap.',
                        '....http.error.response.for.request.of.soap',
                        'http.error.response.for.request.of.soap....',
                        '....http.error.response.for.request.of.soap....',
                        ],
                     'upper_case': [
                        '',
                        '.',
                        '....',
                        'HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP',
                        '.HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP',
                        'HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP.',
                        '.HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP.',
                        '....HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP',
                        'HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP....',
                        '....HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP....',
                        ],
                     'camel_case': [
                        '',
                        '.',
                        '....',
                        'http.Error.Response.For.Request.Of.Soap',
                        '.http.Error.Response.For.Request.Of.Soap',
                        'http.Error.Response.For.Request.Of.Soap.',
                        '.http.Error.Response.For.Request.Of.Soap.',
                        '....http.Error.Response.For.Request.Of.Soap',
                        'http.Error.Response.For.Request.Of.Soap....',
                        '....http.Error.Response.For.Request.Of.Soap....',
                        'httpErrorResponseForRequestOfSoap',
                        '.httpErrorResponseForRequestOfSoap',
                        'httpErrorResponseForRequestOfSoap.',
                        '.httpErrorResponseForRequestOfSoap.',
                        '....httpErrorResponseForRequestOfSoap',
                        'httpErrorResponseForRequestOfSoap....',
                        '....httpErrorResponseForRequestOfSoap....',
                        ],
                     'pascal_case': [
                        '',
                        '.',
                        '....',
                        'Http.Error.Response.For.Request.Of.Soap',
                        '.Http.Error.Response.For.Request.Of.Soap',
                        'Http.Error.Response.For.Request.Of.Soap.',
                        '.Http.Error.Response.For.Request.Of.Soap.',
                        '....Http.Error.Response.For.Request.Of.Soap',
                        'Http.Error.Response.For.Request.Of.Soap....',
                        '....Http.Error.Response.For.Request.Of.Soap....',
                        'HttpErrorResponseForRequestOfSoap',
                        '.HttpErrorResponseForRequestOfSoap',
                        'HttpErrorResponseForRequestOfSoap.',
                        '.HttpErrorResponseForRequestOfSoap.',
                        '....HttpErrorResponseForRequestOfSoap',
                        'HttpErrorResponseForRequestOfSoap....',
                        '....HttpErrorResponseForRequestOfSoap....',
                        ]
                     }
        words_only = [[], [], []]
        for i in range(0, len(test_data['pascal_case']) - 2):
            words_only.append(
                ['http', 'error', 'response', 'for', 'request', 'of', 'soap'])
        words_with_other_char = [
            [],
            ['.'],
            ['....'],
            ['http', '.', 'error', '.', 'response', '.', 'for', '.', 'request',
             '.', 'of', '.', 'soap'],
            ['.', 'http', '.', 'error', '.', 'response', '.', 'for', '.',
             'request', '.', 'of', '.', 'soap'],
            ['http', '.', 'error', '.', 'response', '.', 'for', '.', 'request',
             '.', 'of', '.', 'soap', '.'],
            ['.', 'http', '.', 'error', '.', 'response', '.', 'for', '.',
             'request', '.', 'of', '.', 'soap', '.'],
            ['....', 'http', '.', 'error', '.', 'response', '.', 'for', '.',
             'request', '.', 'of', '.', 'soap'],
            ['http', '.', 'error', '.', 'response', '.', 'for', '.', 'request',
             '.', 'of', '.', 'soap', '....'],
            ['....', 'http', '.', 'error', '.', 'response', '.', 'for', '.',
             'request', '.', 'of', '.', 'soap', '....'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap'],
            ['.', 'Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap', '.'],
            ['.', 'Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap',
             '.'],
            ['....', 'Http', 'Error', 'Response', 'For', 'Request', 'Of',
             'Soap'],
            ['Http', 'Error', 'Response', 'For', 'Request', 'Of', 'Soap',
             '....'],
            ['....', 'Http', 'Error', 'Response', 'For', 'Request', 'Of',
             'Soap', '....'],
        ]

        for include_non_letter in [True, False]:
            if include_non_letter:
                with_or_not = "with"
            else:
                with_or_not = "without"

            for case, sentences in test_data.items():
                for i, sentence in enumerate(sentences):
                    if include_non_letter:
                        words = words_with_other_char[i]
                    else:
                        words = words_only[i]

                    for sep in ESCAPE_CHARS:
                        # substitute escape charachars
                        expt = []
                        for e in words:
                            expt += [e.replace(r'.', sep)]
                        expt = convert_words_to_case(expt, case)
                        actl = get_words(sentence.replace(r'.', sep),
                                         include_non_letter)

                        helper.append_to_error_if_not_expect_with_msg(
                            errors, actl == expt, (
                                "The '{0}' {1} non-alphabet in {2}"
                                "\nexpect: {3}\nactual: {4}").format(
                                    sentence.replace(r'.', sep),
                                    with_or_not, case, expt,
                                    actl))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_word_to_case(self):
        # only test exceptions
        convert_word_to_case = util.convert_word_to_case
        errors = []

        try:
            case = 'some_case'
            actual = convert_word_to_case('abc', case)
            errors.append(  # pragma: no cover
                "passing: {0}\nexpect: raise KeyError\nactual: {1}.".format(
                    case, actual))
        except KeyError:
            assert True

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_words_to_case(self):
        # only test exceptions
        convert_words_to_case = util.convert_words_to_case
        errors = []

        try:
            case = 'some_case'
            actual = convert_words_to_case('abc', case)
            errors.append(  # pragma: no cover
                "passing: {0}\nexpect: raise KeyError\nactual: {1}.".format(
                    case, actual))
        except KeyError:
            assert True

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_sentence_to_case(self):
        """test_convert_sentence_to_case
        This test is assumed that
        convert_words will be called indirectly by convert_sentence
        """

        convert_sentence_to_case = util.convert_sentence_to_case
        errors = []
        CASES = ['lower_case', 'upper_case', 'camel_case', 'pascal_case']
        expect_with_separator = {
            'lower_case': 'http.error.response.for.request.of.soap',
            'upper_case': 'HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP',
            'camel_case': 'http.Error.Response.For.Request.Of.Soap',
            'pascal_case': 'Http.Error.Response.For.Request.Of.Soap',
        }
        strings_with_separator = [
            'http.error.response.for.request.of.soap',
            'HTTP.ERROR.RESPONSE.FOR.REQUEST.OF.SOAP',
            'http.Error.Response.For.Request.Of.Soap',
            'Http.Error.Response.For.Request.Of.Soap',
        ]
        expect_without_separator = {
            'lower_case': 'httperrorresponseforrequestofsoap',
            'upper_case': 'HTTPERRORRESPONSEFORREQUESTOFSOAP',
            'camel_case': 'httpErrorResponseForRequestOfSoap',
            'pascal_case': 'HttpErrorResponseForRequestOfSoap',
        }
        strings_without_separator = [
            'httpErrorResponseForRequestOfSoap',
            'HttpErrorResponseForRequestOfSoap',
        ]

        # boundary
        for case in CASES:
            helper.append_to_error_if_not_expect_with_msg(
                errors, '' == convert_sentence_to_case('', case), (
                    "'' != {0}".format(
                        convert_sentence_to_case('', case))))
        # with separator
        for case in CASES:
            for s in strings_with_separator:
                for sep in ESCAPE_CHARS:
                    expt = expect_with_separator[case].replace(r'.', sep)
                    actl = convert_sentence_to_case(s.replace(r'.', sep), case)
                    helper.append_to_error_if_not_expect_with_msg(
                        errors, expt == actl, (
                            "In format: {0} within any separator"
                            "\nexpect: {1} !=\nactual: {2}".format(
                                case, expt, actl)))
        # without separator
        for case in CASES:
            for s in strings_without_separator:
                expt = expect_without_separator[case]
                actl = convert_sentence_to_case(s, case)
                helper.append_to_error_if_not_expect_with_msg(
                    errors, expt == actl, (
                        "In format: {0} without any separator"
                        "\nexpect: {1} !=\nactual: {2}".format(
                            case, expt, actl)))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_convert_sep(self):
        convert_sep = util.convert_sep
        errors = []
        SEPS = ['dash_to_underscore', 'underscore_to_dash']

        # boundary
        for sep in helper.gen_all_possible_pair(SEPS):
            actl = convert_sep('', sep)
            helper.append_to_error_if_not_expect_with_msg(
                errors, '' == actl, (
                    "'' != {0}".format(actl)))
        for s in ['_', '_a', 'a_', 'a_a', '-', '-a', 'a-', 'a-a']:
            actl = convert_sep(s, [])
            helper.append_to_error_if_not_expect_with_msg(
                errors, s == actl, (
                    "{0} != {1}".format(s, actl)))
        # dash_to_underscore
        actl = convert_sep('-', ['dash_to_underscore'])
        helper.append_to_error_if_not_expect_with_msg(errors, '_' == actl, (
            "expect '_' != actlual '{0}'".format(actl)))
        actl = convert_sep('-a', ['dash_to_underscore'])
        helper.append_to_error_if_not_expect_with_msg(errors, '_a' == actl, (
            "expect '_a' != actlual '{0}'".format(actl)))
        actl = convert_sep('a-', ['dash_to_underscore'])
        helper.append_to_error_if_not_expect_with_msg(errors, 'a_' == actl, (
            "expect 'a_' != actlual '{0}'".format(actl)))
        actl = convert_sep('a-a', ['dash_to_underscore'])
        helper.append_to_error_if_not_expect_with_msg(errors, 'a_a' == actl, (
            "expect 'a_a' != actlual '{0}'".format(actl)))
        # underscore_to_dash
        actl = convert_sep('_', ['underscore_to_dash'])
        helper.append_to_error_if_not_expect_with_msg(errors, '-' == actl, (
            "expect '-' != actlual '{0}'".format(actl)))
        actl = convert_sep('_a', ['underscore_to_dash'])
        helper.append_to_error_if_not_expect_with_msg(errors, '-a' == actl, (
            "expect '-a' != actlual '{0}'".format(actl)))
        actl = convert_sep('a_', ['underscore_to_dash'])
        helper.append_to_error_if_not_expect_with_msg(errors, 'a-' == actl, (
            "expect 'a-' != actlual '{0}'".format(actl)))
        actl = convert_sep('a_a', ['underscore_to_dash'])
        helper.append_to_error_if_not_expect_with_msg(errors, 'a-a' == actl, (
            "expect 'a-a' != actlual '{0}'".format(actl)))
        # not support
        try:
            actl = convert_sep('_', ['abc'])
            errors.append(
                "expect raise KeyError actual '{0}'.".format(
                    actl))  # pragma: no cover
        except KeyError:
            assert True

        assert errors == [], Exception(helper.get_error_string(errors))
