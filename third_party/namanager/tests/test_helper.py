import namanager.tests.helper as helper
import sys
import itertools
import json

# Backward Compatibility
try:
    unicode()
except NameError:
    unicode = str
try:
    long()
except NameError:
    long = int


class TestHelper():
    def test_get_error_string(self):
        get_error_string = helper.get_error_string

        assert isinstance(get_error_string([]), str)
        assert isinstance(get_error_string(['a', 'b']), str)

    def test_append_to_error_if_not_expect_with_msg(self):
        append_to_error_if_not_expect_with_msg = (
            helper.append_to_error_if_not_expect_with_msg)

        actual = []
        append_to_error_if_not_expect_with_msg(actual, 1 == 0, "123")
        assert actual == ["123"]

        actual = []
        append_to_error_if_not_expect_with_msg(actual, 1 == 1, "123")
        assert actual == []

    def test_gen_random_alphabet_string(self):
        gen_random_alphabet_string = helper.gen_random_alphabet_string
        strings = []
        for _ in range(0, 1000):
            s = gen_random_alphabet_string(1000)
            assert s not in strings
            strings.append(s)

    def test_gen_all_possible_pair(self):
        gen_all_possible_pair = helper.gen_all_possible_pair
        errors = []
        data = [
            '',
            'a',
            'ab',
            'abc',
            [],
            ['a'],
            ['a', 'bc'],
            ['a', 'bc', 'def'],
        ]
        expect = [
            [],
            [('a', )],
            [('a', ), ('b', ), ('a', 'b'), ('b', 'a')],
            [('a', ), ('b', ), ('c', ), ('a', 'b'), ('b', 'a'), ('a', 'c'), ('c', 'a'), ('b', 'c'), ('c', 'b'), ('a', 'b', 'c'), ('a', 'c', 'b'), ('b', 'a', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b'), ('c', 'b', 'a')],  # noqa: E501
            [],
            [('a', )],
            [('a', ), ('bc', ), ('a', 'bc'), ('bc', 'a')],
            [('a', ), ('bc', ), ('def', ), ('a', 'bc'), ('bc', 'a'), ('a', 'def'), ('def', 'a'), ('bc', 'def'), ('def', 'bc'), ('a', 'bc', 'def'), ('a', 'def', 'bc'), ('bc', 'a', 'def'), ('bc', 'def', 'a'), ('def', 'a', 'bc'), ('def', 'bc', 'a')],  # noqa: E501
        ]

        actual = []
        for datum in data:
            actual.append(gen_all_possible_pair(datum))
        for i in range(0, len(data)):
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                expect[i] == actual[i],
                "Expect:\n{0}\nActual:\n{1}".format(expect[i], actual[i]))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_get_all_type_values_of_json(self):
        # only test values is valid or else.
        get_all_type_values_of_json = helper.get_all_type_values_of_json
        errors = []

        actual = get_all_type_values_of_json()
        for actl in actual:
            try:
                json.loads(json.dumps(actl))
            except Exception as e:
                errors.append("{0} is not valid json format:\n{1}".format(
                    actl, e))

        assert errors == [], Exception(helper.get_error_string(errors))

    def _get_is_same_disorderly_func_true_test_data(self, i, j):
        test_data = ()

        for pi in itertools.permutations(i):
            for pj in itertools.permutations(j):
                test_data += ((True, pi, pj),)

        return test_data

    def _get_is_same_disorderly_func_false_test_data(self, i, j,
                                                     swapped=False):
        test_data = ()

        if (isinstance(i, (dict, set, tuple, list))):
            for pi in itertools.permutations(i):
                test_data += ((False, pi, j),)
        else:
            for pj in itertools.permutations(j):
                test_data += ((False, i, pj),)

        if not swapped:
            test_data += (
                self._get_is_same_disorderly_func_false_test_data(j, i, True))
        return test_data

    def test_is_in_tuple(self):
        is_in_tuple = helper.is_in_tuple
        errors = []
        test_data = [None, True, False, 1, '1', [1, 2], {1, 2}, {1}, (1, 2)]

        # test single
        for index_i, data_i in enumerate(test_data):
            for index_j, data_j in enumerate(test_data):
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    (index_i == index_j) is is_in_tuple(data_i, (data_j,)),
                    "Expect: {0} equals ({1} in [{2}])".format(
                        (index_i == index_j), data_i, data_j))
        # test multiple
        for index_i, data_i in enumerate(test_data):
            exclude = []
            for index_j, data_j in enumerate(test_data):
                if index_i != index_j:
                    exclude.append(data_j)
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                not is_in_tuple(data_i, tuple(exclude)),
                "Expect: False equals ({0} in {1})".format(
                    data_i, exclude))
        for i in test_data:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                is_in_tuple(i, tuple(test_data)),
                "Expect: True equals ({0} in {1})".format(
                    i, test_data))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_is_equal(self):
        is_equal = helper.is_equal
        errors = []
        truthy = [True, 1, 1.1, 1j, [1], (1,), {1}, {1: 1}, 's']
        falsy = [
            None, False, 0, 0.0, 0j, list(), tuple(), set(), dict(), str()]

        # test true
        for data in [truthy, falsy]:
            for datum in data:
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    True is is_equal(datum, datum),
                    "Expect: True\nvalue1: {0}\nvalue2: {1}".format(
                        datum, datum))
        # test false
        for data in [truthy, falsy]:
            for i1 in range(0, len(data)):
                for i2 in range(i1 + 1, len(data)):
                    helper.append_to_error_if_not_expect_with_msg(
                        errors,
                        False is is_equal(data[i1], data[i2]),
                        "Expect: False\nvalue1: {0}\nvalue2: {1}".format(
                            data[i1], data[i2]))
        # test __len__ and __bool__ of objects
        for t in truthy:
            if t is not True:
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    False is is_equal(bool(TruthyCls()), t),
                    "Expect: False\nvalue1: {0}(TruthyClass)"
                    "\nvalue2: {1}".format(bool(TruthyCls()), t))
            if t is not 1:
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    False is is_equal(len(TruthyCls()), t),
                    "Expect: False\nvalue1: {0}(TruthyClass)"
                    "\nvalue2: {1}".format(len(TruthyCls()), t))
        for f in falsy:
            if f is not False:
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    False is is_equal(bool(FalsyCls()), f),
                    "Expect: False\nvalue1: {0}(FalsyClass)"
                    "\nvalue2: {1}".format(bool(FalsyCls()), f))
            if f is not 0:
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    False is is_equal(len(FalsyCls()), f),
                    "Expect: False\nvalue1: {0}(FalsyClass)"
                    "\nvalue2: {1}".format(len(FalsyCls()), f))
        helper.append_to_error_if_not_expect_with_msg(
            errors,
            True is is_equal(bool(TruthyCls()), True),
            "Expect: True\nvalue1: {0} (FalsyClass)"
            "\nvalue2: True".format(bool(TruthyCls())))
        helper.append_to_error_if_not_expect_with_msg(
            errors,
            True is is_equal(len(TruthyCls()), 1),
            "Expect: True\nvalue1: {0} (FalsyClass)"
            "\nvalue2: 1".format(len(TruthyCls())))
        helper.append_to_error_if_not_expect_with_msg(
            errors,
            True is is_equal(bool(FalsyCls()), False),
            "Expect: True\nvalue1: {0} (FalsyClass)"
            "\nvalue2: False".format(bool(FalsyCls())))
        helper.append_to_error_if_not_expect_with_msg(
            errors,
            True is is_equal(len(FalsyCls()), 0),
            "Expect: True\nvalue1: {0} (FalsyClass)"
            "\nvalue2: 0".format(len(FalsyCls())))

        assert errors == [], Exception(helper.get_error_string(errors))

    def _get_is_same_disorderly_func_test_data(self):
        expect_type_values = helper.get_all_type_values_of_json()
        test_data = ()

        for i in expect_type_values:
            for j in expect_type_values:
                if helper.is_equal(i, j):
                    if isinstance(i, (dict, set, tuple, list)):
                        test_data += (
                            self._get_is_same_disorderly_func_true_test_data(
                                i, j))
                    else:
                        test_data += ((True, i, j),)
                else:
                    if (isinstance(i, (dict, set, tuple, list)) or
                       isinstance(j, (dict, set, tuple, list))):
                        test_data += (
                            self._get_is_same_disorderly_func_false_test_data(
                                i, j))
                    else:
                        test_data += ((False, i, j),)

        return test_data

    def test_is_same_disorderly(self):
        # no test for objects
        is_same_disorderly = helper.is_same_disorderly
        errors = []
        test_data = (
            (True, [{"_id": "5aa7e06b512a2d14536fa60d", "index": 0, "guid": "4637b81e-cda1-481d-aa16-b0bb59716a87", "isActive": True, "balance": "$1, 463.33", "picture": "http://placehold.it/32x32", "age": 37, "eyeColor": "brown", "name": "Kaye Hendrix", "gender": "female", "company": "GLUID", "email": "kayehendrix@gluid.com", "phone": "+1 (913) 583-2820", "address": "729 Putnam Avenue, Lookingglass, Maine, 1481", "about": "Mollit in commodo culpa Lorem adipisicing laboris mollit non culpa sunt ex officia. Adipisicing enim culpa id elit amet velit adipisicing. Ullamco elit culpa occaecat do aliquip aliquip consequat nostrud cupidatat. Fugiat exercitation ex ex occaecat laborum veniam incididunt deserunt aliqua. Officia ut quis exercitation excepteur dolor magna. Minim Lorem duis proident culpa aliqua nisi in culpa cupidatat.", "registered": "2014-02-26T06:25:02 -08:00", "latitude": -62.201946, "longitude": 169.994082, "tags": ["labore", "duis", "sint", "exercitation", "culpa", "laboris", "tempor"], "friends": [{"id": 0, "name": "Jenny Vance"}, {"id": 1, "name": "Beatriz Dillard"}, {"id": 2, "name": "Rutledge Greer"}], "greeting": "Hello, Kaye Hendrix! You have 9 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e06b6ccce147881187ea", "index": 1, "guid": "c0e466dc-84c5-4774-9940-6d17c7fa0871", "isActive": False, "balance": "$3, 501.37", "picture": "http://placehold.it/32x32", "age": 24, "eyeColor": "brown", "name": "Alyssa Levine", "gender": "female", "company": "COMSTAR", "email": "alyssalevine@comstar.com", "phone": "+1 (940) 430-3529", "address": "190 Oriental Boulevard, Volta, Oklahoma, 9380", "about": "Esse ipsum culpa non dolor labore laborum nisi. Sit commodo aliquip fugiat ipsum ut et dolore esse consequat labore. Ea velit officia in incididunt commodo. Aliquip aute fugiat in proident dolore non nisi Lorem ullamco aute nostrud sit ut. Dolore mollit nostrud culpa id et id sunt.", "registered": "2017-10-18T03:18:42 -08:00", "latitude": -0.890316, "longitude": -71.479988, "tags": ["deserunt", "elit", "eiusmod", "labore", "excepteur", "occaecat", "exercitation"], "friends": [{"id": 0, "name": "Daugherty Roy"}, {"id": 1, "name": "Baird Guerra"}, {"id": 2, "name": "Rosario Henson"}], "greeting": "Hello, Alyssa Levine! You have 10 unread messages.", "favoriteFruit": "banana"}, {"_id": "5aa7e06b3d52c9d133624784", "index": 2, "guid": "161487fe-7387-4585-a03d-1415ba8d434e", "isActive": True, "balance": "$1, 748.45", "picture": "http://placehold.it/32x32", "age": 29, "eyeColor": "green", "name": "Sawyer Schwartz", "gender": "male", "company": "PEARLESEX", "email": "sawyerschwartz@pearlesex.com", "phone": "+1 (865) 590-2841", "address": "561 Rapelye Street, Takilma, South Dakota, 2108", "about": "Labore eu eiusmod irure aute non. Officia reprehenderit anim tempor reprehenderit pariatur nisi tempor aliqua mollit anim ea velit. Id sunt amet amet commodo eiusmod cillum pariatur enim ullamco minim. Qui dolore duis culpa anim exercitation dolor excepteur tempor nostrud.", "registered": "2016-04-05T03:53:32 -08:00", "latitude": -53.24698, "longitude": -175.027866, "tags": ["nostrud", "voluptate", "reprehenderit", "labore", "anim", "excepteur", "nostrud"], "friends": [{"id": 0, "name": "Gretchen Pearson"}, {"id": 1, "name": "Opal Fry"}, {"id": 2, "name": "Alba Downs"}], "greeting": "Hello, Sawyer Schwartz! You have 5 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e06ba14f1aa9487877c0", "index": 3, "guid": "f0190a4a-ce2c-445d-b2c6-6bc31b7890d3", "isActive": True, "balance": "$1, 228.08", "picture": "http://placehold.it/32x32", "age": 24, "eyeColor": "blue", "name": "Larsen Lawson", "gender": "male", "company": "COMVEX", "email": "larsenlawson@comvex.com", "phone": "+1 (902) 448-3363", "address": "808 Elizabeth Place, Movico, Palau, 5801", "about": "Enim anim enim elit mollit ullamco esse laboris amet eiusmod Lorem ea. Irure laborum mollit ut aliquip adipisicing enim qui voluptate ut do aute. Ea tempor adipisicing proident ex quis exercitation aute elit pariatur consequat id. Enim non enim occaecat exercitation eu do cupidatat eiusmod minim occaecat laboris. Anim sint reprehenderit labore magna non enim ad esse et veniam. Eiusmod non sunt aliquip consequat in.", "registered": "2016-07-09T08:30:58 -08:00", "latitude": -5.380871, "longitude": -169.813139, "tags": ["culpa", "sit", "et", "duis", "occaecat", "fugiat", "voluptate"], "friends": [{"id": 0, "name": "Lowery Irwin"}, {"id": 1, "name": "Susanna Kim"}, {"id": 2, "name": "Case Conley"}], "greeting": "Hello, Larsen Lawson! You have 2 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e06bb98834d8a65ace21", "index": 4, "guid": "4149a931-0695-471d-8b52-29eb877e1c8e", "isActive": True, "balance": "$3, 955.24", "picture": "http://placehold.it/32x32", "age": 39, "eyeColor": "green", "name": "Esperanza Wells", "gender": "female", "company": "VERBUS", "email": "esperanzawells@verbus.com", "phone": "+1 (941) 452-2795", "address": "410 Montieth Street, Dunbar, Texas, 7446", "about": "Incididunt adipisicing voluptate nulla ad in labore duis duis. Lorem in esse magna magna esse officia enim officia velit aliquip exercitation incididunt officia Lorem. Aliqua fugiat nisi nisi ea in sunt. Aliquip adipisicing adipisicing ut laboris magna occaecat qui esse dolor quis. Occaecat reprehenderit non elit irure. Eiusmod exercitation cupidatat ullamco laborum aute cupidatat adipisicing ipsum veniam nostrud sit incididunt quis.", "registered": "2018-01-31T08:52:42 -08:00", "latitude": -85.155293, "longitude": -42.666217, "tags": ["enim", "quis", "amet", "non", "incididunt", "id", "nisi"], "friends": [{"id": 0, "name": "Duran Sexton"}, {"id": 1, "name": "Mindy Swanson"}, {"id": 2, "name": "Jeri Gray"}], "greeting": "Hello, Esperanza Wells! You have 6 unread messages.", "favoriteFruit": "strawberry"}], [{"_id": "5aa7e06b512a2d14536fa60d", "index": 0, "guid": "4637b81e-cda1-481d-aa16-b0bb59716a87", "isActive": True, "balance": "$1, 463.33", "picture": "http://placehold.it/32x32", "age": 37, "eyeColor": "brown", "name": "Kaye Hendrix", "gender": "female", "company": "GLUID", "email": "kayehendrix@gluid.com", "phone": "+1 (913) 583-2820", "address": "729 Putnam Avenue, Lookingglass, Maine, 1481", "about": "Mollit in commodo culpa Lorem adipisicing laboris mollit non culpa sunt ex officia. Adipisicing enim culpa id elit amet velit adipisicing. Ullamco elit culpa occaecat do aliquip aliquip consequat nostrud cupidatat. Fugiat exercitation ex ex occaecat laborum veniam incididunt deserunt aliqua. Officia ut quis exercitation excepteur dolor magna. Minim Lorem duis proident culpa aliqua nisi in culpa cupidatat.", "registered": "2014-02-26T06:25:02 -08:00", "latitude": -62.201946, "longitude": 169.994082, "tags": ["labore", "duis", "sint", "exercitation", "culpa", "laboris", "tempor"], "friends": [{"id": 0, "name": "Jenny Vance"}, {"id": 1, "name": "Beatriz Dillard"}, {"id": 2, "name": "Rutledge Greer"}], "greeting": "Hello, Kaye Hendrix! You have 9 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e06b6ccce147881187ea", "index": 1, "guid": "c0e466dc-84c5-4774-9940-6d17c7fa0871", "isActive": False, "balance": "$3, 501.37", "picture": "http://placehold.it/32x32", "age": 24, "eyeColor": "brown", "name": "Alyssa Levine", "gender": "female", "company": "COMSTAR", "email": "alyssalevine@comstar.com", "phone": "+1 (940) 430-3529", "address": "190 Oriental Boulevard, Volta, Oklahoma, 9380", "about": "Esse ipsum culpa non dolor labore laborum nisi. Sit commodo aliquip fugiat ipsum ut et dolore esse consequat labore. Ea velit officia in incididunt commodo. Aliquip aute fugiat in proident dolore non nisi Lorem ullamco aute nostrud sit ut. Dolore mollit nostrud culpa id et id sunt.", "registered": "2017-10-18T03:18:42 -08:00", "latitude": -0.890316, "longitude": -71.479988, "tags": ["deserunt", "elit", "eiusmod", "labore", "excepteur", "occaecat", "exercitation"], "friends": [{"id": 0, "name": "Daugherty Roy"}, {"id": 1, "name": "Baird Guerra"}, {"id": 2, "name": "Rosario Henson"}], "greeting": "Hello, Alyssa Levine! You have 10 unread messages.", "favoriteFruit": "banana"}, {"_id": "5aa7e06b3d52c9d133624784", "index": 2, "guid": "161487fe-7387-4585-a03d-1415ba8d434e", "isActive": True, "balance": "$1, 748.45", "picture": "http://placehold.it/32x32", "age": 29, "eyeColor": "green", "name": "Sawyer Schwartz", "gender": "male", "company": "PEARLESEX", "email": "sawyerschwartz@pearlesex.com", "phone": "+1 (865) 590-2841", "address": "561 Rapelye Street, Takilma, South Dakota, 2108", "about": "Labore eu eiusmod irure aute non. Officia reprehenderit anim tempor reprehenderit pariatur nisi tempor aliqua mollit anim ea velit. Id sunt amet amet commodo eiusmod cillum pariatur enim ullamco minim. Qui dolore duis culpa anim exercitation dolor excepteur tempor nostrud.", "registered": "2016-04-05T03:53:32 -08:00", "latitude": -53.24698, "longitude": -175.027866, "tags": ["nostrud", "voluptate", "reprehenderit", "labore", "anim", "excepteur", "nostrud"], "friends": [{"id": 0, "name": "Gretchen Pearson"}, {"id": 1, "name": "Opal Fry"}, {"id": 2, "name": "Alba Downs"}], "greeting": "Hello, Sawyer Schwartz! You have 5 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e06ba14f1aa9487877c0", "index": 3, "guid": "f0190a4a-ce2c-445d-b2c6-6bc31b7890d3", "isActive": True, "balance": "$1, 228.08", "picture": "http://placehold.it/32x32", "age": 24, "eyeColor": "blue", "name": "Larsen Lawson", "gender": "male", "company": "COMVEX", "email": "larsenlawson@comvex.com", "phone": "+1 (902) 448-3363", "address": "808 Elizabeth Place, Movico, Palau, 5801", "about": "Enim anim enim elit mollit ullamco esse laboris amet eiusmod Lorem ea. Irure laborum mollit ut aliquip adipisicing enim qui voluptate ut do aute. Ea tempor adipisicing proident ex quis exercitation aute elit pariatur consequat id. Enim non enim occaecat exercitation eu do cupidatat eiusmod minim occaecat laboris. Anim sint reprehenderit labore magna non enim ad esse et veniam. Eiusmod non sunt aliquip consequat in.", "registered": "2016-07-09T08:30:58 -08:00", "latitude": -5.380871, "longitude": -169.813139, "tags": ["culpa", "sit", "et", "duis", "occaecat", "fugiat", "voluptate"], "friends": [{"id": 0, "name": "Lowery Irwin"}, {"id": 1, "name": "Susanna Kim"}, {"id": 2, "name": "Case Conley"}], "greeting": "Hello, Larsen Lawson! You have 2 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e06bb98834d8a65ace21", "index": 4, "guid": "4149a931-0695-471d-8b52-29eb877e1c8e", "isActive": True, "balance": "$3, 955.24", "picture": "http://placehold.it/32x32", "age": 39, "eyeColor": "green", "name": "Esperanza Wells", "gender": "female", "company": "VERBUS", "email": "esperanzawells@verbus.com", "phone": "+1 (941) 452-2795", "address": "410 Montieth Street, Dunbar, Texas, 7446", "about": "Incididunt adipisicing voluptate nulla ad in labore duis duis. Lorem in esse magna magna esse officia enim officia velit aliquip exercitation incididunt officia Lorem. Aliqua fugiat nisi nisi ea in sunt. Aliquip adipisicing adipisicing ut laboris magna occaecat qui esse dolor quis. Occaecat reprehenderit non elit irure. Eiusmod exercitation cupidatat ullamco laborum aute cupidatat adipisicing ipsum veniam nostrud sit incididunt quis.", "registered": "2018-01-31T08:52:42 -08:00", "latitude": -85.155293, "longitude": -42.666217, "tags": ["enim", "quis", "amet", "non", "incididunt", "id", "nisi"], "friends": [{"id": 0, "name": "Duran Sexton"}, {"id": 1, "name": "Mindy Swanson"}, {"id": 2, "name": "Jeri Gray"}], "greeting": "Hello, Esperanza Wells! You have 6 unread messages.", "favoriteFruit": "strawberry"}]),  # noqa: E501
            (False, [{"_id": "5aa7e1446f2ds19ea32ff19480", "index": 0, "guid": "12c2e30b-ce49-4b45-ba05-f97cc0eb5c61", "isActive": False, "balance": "$2, 420.74", "picture": "http://placehold.it/32x32", "age": 36, "eyeColor": "green", "name": "Gladys Cameron", "gender": "female", "company": "QOT", "email": "gladyscameron@qot.com", "phone": "+1 (845) 438-2756", "address": "832 Schaefer Street, Morgandale, Virgin Islands, 5536", "about": "Et magna nostrud et tempor excepteur non nisi nostrud anim adipisicing elit consectetur. Nostrud culpa ex amet non cillum sit. Nulla anim esse deserunt nulla incididunt voluptate amet ea exercitation proident magna eiusmod ipsum proident. Nisi occaecat ipsum veniam consectetur ea do in est in commodo Lorem cupidatat exercitation. In anim ad proident ex ex duis sit cillum mollit. Irure ea enim officia aliqua est fugiat magna.", "registered": "2016-09-06T12:34:36 -08:00", "latitude": 8.151066, "longitude": -56.353479, "tags": ["laboris", "commodo", "veniam", "non", "dolor", "laboris", "dolor"], "friends": [{"id": 0, "name": "Mccall Webster"}, {"id": 1, "name": "Chapman Richmond"}, {"id": 2, "name": "Williamson Patton"}], "greeting": "Hello, Gladys Cameron! You have 4 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e144062184fc5ab13db1", "index": 1, "guid": "ffe46063-0d8b-4b11-9da0-c63f0e7dcadc", "isActive": False, "balance": "$2, 036.89", "picture": "http://placehold.it/32x32", "age": 28, "eyeColor": "blue", "name": "Karla Hayes", "gender": "female", "company": "SIGNITY", "email": "karlahayes@signity.com", "phone": "+1 (823) 546-3737", "address": "756 Kathleen Court, Homeland, Minnesota, 4435", "about": "Ex voluptate cupidatat dolor consequat aliqua in ad. Labore irure culpa aliquip labore laboris voluptate. Quis sint elit commodo id ullamco anim non Lorem deserunt laborum consequat ullamco et.", "registered": "2016-07-02T03:34:21 -08:00", "latitude": 2.308308, "longitude": 114.903784, "tags": ["excepteur", "magna", "tempor", "aliquip", "esse", "consequat", "nostrud"], "friends": [{"id": 0, "name": "Sheree Butler"}, {"id": 1, "name": "Wagner Cherry"}, {"id": 2, "name": "Myrna Sykes"}], "greeting": "Hello, Karla Hayes! You have 4 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e144d3d4eee28f2a4646", "index": 2, "guid": "da20aedf-e9f0-4c82-a4a7-d9de76bfada0", "isActive": False, "balance": "$1, 185.35", "picture": "http://placehold.it/32x32", "age": 39, "eyeColor": "blue", "name": "Morgan Ramos", "gender": "female", "company": "EARTHPURE", "email": "morganramos@earthpure.com", "phone": "+1 (890) 558-3649", "address": "944 Hornell Loop, Fidelis, Marshall Islands, 4863", "about": "Nostrud Lorem eiusmod esse eu reprehenderit tempor ullamco tempor commodo cillum aliqua adipisicing consequat velit. Exercitation occaecat dolor ad cillum laboris. Cupidatat tempor enim dolor ad mollit. Non do aliquip exercitation ipsum eiusmod ullamco ipsum qui sint mollit in veniam esse.", "registered": "2014-10-24T11:34:31 -08:00", "latitude": -73.439898, "longitude": -112.746249, "tags": ["incididunt", "elit", "incididunt", "dolor", "eu", "dolor", "magna"], "friends": [{"id": 0, "name": "Liza Acevedo"}, {"id": 1, "name": "Leila Kane"}, {"id": 2, "name": "Gabrielle Wilkins"}], "greeting": "Hello, Morgan Ramos! You have 6 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e144143bb32c10992cad", "index": 3, "guid": "88e1f863-d31c-4156-9396-703d92891b35", "isActive": True, "balance": "$1, 120.41", "picture": "http://placehold.it/32x32", "age": 25, "eyeColor": "green", "name": "Sampson Washington", "gender": "male", "company": "PARAGONIA", "email": "sampsonwashington@paragonia.com", "phone": "+1 (923) 408-3496", "address": "766 Milford Street, Wakarusa, Oklahoma, 958", "about": "Ex aute amet nostrud exercitation esse elit nisi tempor nostrud. Eiusmod excepteur ea ullamco esse quis ex. Do cillum velit laborum mollit.", "registered": "2014-03-15T06:38:37 -08:00", "latitude": 43.094847, "longitude": 82.475895, "tags": ["ex", "elit", "culpa", "reprehenderit", "enim", "excepteur", "id"], "friends": [{"id": 0, "name": "Deidre Rosa"}, {"id": 1, "name": "Solis Gomez"}, {"id": 2, "name": "Bettie Hudson"}], "greeting": "Hello, Sampson Washington! You have 2 unread messages.", "favoriteFruit": "banana"}, {"_id": "5aa7e14404937743c6126177", "index": 4, "guid": "06808954-ecbb-43a7-9544-129114fbbcf6", "isActive": False, "balance": "$2, 754.82", "picture": "http://placehold.it/32x32", "age": 33, "eyeColor": "green", "name": "Brown Case", "gender": "male", "company": "EARTHMARK", "email": "browncase@earthmark.com", "phone": "+1 (855) 428-3216", "address": "298 Oceanic Avenue, Gambrills, Georgia, 3438", "about": "Magna quis proident sit est non qui deserunt irure velit reprehenderit. Veniam enim mollit pariatur consectetur. Ipsum fugiat ipsum mollit eu excepteur proident. Laboris ipsum minim aute ex eu elit enim Lorem. Culpa consectetur nulla reprehenderit eu ullamco laboris adipisicing aliquip. Nostrud aliquip officia culpa voluptate nulla laboris excepteur do laboris proident laboris et cupidatat.", "registered": "2015-08-17T07:28:53 -08:00", "latitude": -67.251279, "longitude": 77.718694, "tags": ["est", "labore", "sunt", "cillum", "excepteur", "veniam", "do"], "friends": [{"id": 0, "name": "Wanda Roman"}, {"id": 1, "name": "Marcy Levy"}, {"id": 2, "name": "Avis Hart"}], "greeting": "Hello, Brown Case! You have 7 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e144a58af4a4ffad8135", "index": 5, "guid": "bb5a4d1d-dd5e-47f4-af76-e8bd95720c38", "isActive": True, "balance": "$1, 561.07", "picture": "http://placehold.it/32x32", "age": 40, "eyeColor": "brown", "name": "Pacheco Banks", "gender": "male", "company": "MOMENTIA", "email": "pachecobanks@momentia.com", "phone": "+1 (978) 450-2829", "address": "349 Dare Court, Faywood, Texas, 1553", "about": "Cupidatat anim quis veniam et reprehenderit excepteur ullamco cillum ipsum cillum eiusmod adipisicing. Excepteur aliqua ipsum proident duis labore enim veniam est aute. Minim tempor magna cupidatat quis ut sint dolore magna aliquip in aliquip commodo velit cupidatat. Minim exercitation nostrud tempor ullamco aliquip nisi non labore do minim aliqua consectetur amet. Voluptate laboris veniam cupidatat nisi cillum dolor.", "registered": "2014-07-31T12:46:26 -0800", "latitude": 51.612576, "longitude": 88.287491, "tags": ["irure", "adipisicing", "Lorem", "aliquip", "ex", "est", "mollit"], "friends": [{"id": 0, "name": "Angelita Boyer"}, {"id": 1, "name": "Natasha Ramirez"}, {"id": 2, "name": "Mcgowan Farley"}], "greeting": "Hello, Pacheco Banks! You have 4 unread messages.", "favoriteFruit": "strawberry"}], [{"_id": "5aa7e1446f219ea32ff19480", "index": 0, "guid": "12c2e30b-ce49-4b45-ba05-f97cc0eb5c61", "isActive": False, "balance": "$2, 420.74", "picture": "http://placehold.it/32x32", "age": 36, "eyeColor": "green", "name": "Gladys Cameron", "gender": "female", "company": "QOT", "email": "gladyscameron@qot.com", "phone": "+1 (845) 438-2756", "address": "832 Schaefer Street, Morgandale, Virgin Islands, 5536", "about": "Et magna nostrud et tempor excepteur non nisi nostrud anim adipisicing elit consectetur. Nostrud culpa ex amet non cillum sit. Nulla anim esse deserunt nulla incididunt voluptate amet ea exercitation proident magna eiusmod ipsum proident. Nisi occaecat ipsum veniam consectetur ea do in est in commodo Lorem cupidatat exercitation. In anim ad proident ex ex duis sit cillum mollit. Irure ea enim officia aliqua est fugiat magna.", "registered": "2016-09-06T12:34:36 -08:00", "latitude": 8.151066, "longitude": -56.353479, "tags": ["laboris", "commodo", "veniam", "non", "dolor", "laboris", "dolor"], "friends": [{"id": 0, "name": "Mccall Webster"}, {"id": 1, "name": "Chapman Richmond"}, {"id": 2, "name": "Williamson Patton"}], "greeting": "Hello, Gladys Cameron! You have 4 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e144062184fc5ab13db1", "index": 1, "guid": "ffe46063-0d8b-4b11-9da0-c63f0e7dcadc", "isActive": False, "balance": "$2, 036.89", "picture": "http://placehold.it/32x32", "age": 28, "eyeColor": "blue", "name": "Karla Hayes", "gender": "female", "company": "SIGNITY", "email": "karlahayes@signity.com", "phone": "+1 (823) 546-3737", "address": "756 Kathleen Court, Homeland, Minnesota, 4435", "about": "Ex voluptate cupidatat dolor consequat aliqua in ad. Labore irure culpa aliquip labore laboris voluptate. Quis sint elit commodo id ullamco anim non Lorem deserunt laborum consequat ullamco et.", "registered": "2016-07-02T03:34:21 -08:00", "latitude": 2.308308, "longitude": 114.903784, "tags": ["excepteur", "magna", "tempor", "aliquip", "esse", "consequat", "nostrud"], "friends": [{"id": 0, "name": "Sheree Butler"}, {"id": 1, "name": "Wagner Cherry"}, {"id": 2, "name": "Myrna Sykes"}], "greeting": "Hello, Karla Hayes! You have 4 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e144d3d4eee28f2a4646", "index": 2, "guid": "da20aedf-e9f0-4c82-a4a7-d9de76bfada0", "isActive": False, "balance": "$1, 185.35", "picture": "http://placehold.it/32x32", "age": 39, "eyeColor": "blue", "name": "Morgan Ramos", "gender": "female", "company": "EARTHPURE", "email": "morganramos@earthpure.com", "phone": "+1 (890) 558-3649", "address": "944 Hornell Loop, Fidelis, Marshall Islands, 4863", "about": "Nostrud Lorem eiusmod esse eu reprehenderit tempor ullamco tempor commodo cillum aliqua adipisicing consequat velit. Exercitation occaecat dolor ad cillum laboris. Cupidatat tempor enim dolor ad mollit. Non do aliquip exercitation ipsum eiusmod ullamco ipsum qui sint mollit in veniam esse.", "registered": "2014-10-24T11:34:31 -08:00", "latitude": -73.439898, "longitude": -112.746249, "tags": ["incididunt", "elit", "incididunt", "dolor", "eu", "dolor", "magna"], "friends": [{"id": 0, "name": "Liza Acevedo"}, {"id": 1, "name": "Leila Kane"}, {"id": 2, "name": "Gabrielle Wilkins"}], "greeting": "Hello, Morgan Ramos! You have 6 unread messages.", "favoriteFruit": "strawberry"}, {"_id": "5aa7e144143bb32c10992cad", "index": 3, "guid": "88e1f863-d31c-4156-9396-703d92891b35", "isActive": True, "balance": "$1, 120.41", "picture": "http://placehold.it/32x32", "age": 25, "eyeColor": "green", "name": "Sampson Washington", "gender": "male", "company": "PARAGONIA", "email": "sampsonwashington@paragonia.com", "phone": "+1 (923) 408-3496", "address": "766 Milford Street, Wakarusa, Oklahoma, 958", "about": "Ex aute amet nostrud exercitation esse elit nisi tempor nostrud. Eiusmod excepteur ea ullamco esse quis ex. Do cillum velit laborum mollit.", "registered": "2014-03-15T06:38:37 -08:00", "latitude": 43.094847, "longitude": 82.475895, "tags": ["ex", "elit", "culpa", "reprehenderit", "enim", "excepteur", "id"], "friends": [{"id": 0, "name": "Deidre Rosa"}, {"id": 1, "name": "Solis Gomez"}, {"id": 2, "name": "Bettie Hudson"}], "greeting": "Hello, Sampson Washington! You have 2 unread messages.", "favoriteFruit": "banana"}, {"_id": "5aa7e14404937743c6126177", "index": 4, "guid": "06808954-ecbb-43a7-9544-129114fbbcf6", "isActive": False, "balance": "$2, 754.82", "picture": "http://placehold.it/32x32", "age": 33, "eyeColor": "green", "name": "Brown Case", "gender": "male", "company": "EARTHMARK", "email": "browncase@earthmark.com", "phone": "+1 (855) 428-321", "address": "298 Oceanic Avenue, Gambrills, Georgia, 3438", "about": "Magna quis proident sit est non qui deserunt irure velit reprehenderit. Veniam enim mollit pariatur consectetur. Ipsum fugiat ipsum mollit eu excepteur proident. Laboris ipsum minim aute ex eu elit enim Lorem. Culpa consectetur nulla reprehenderit eu ullamco laboris adipisicing aliquip. Nostrud aliquip officia culpa voluptate nulla laboris excepteur do laboris proident laboris et cupidatat.", "registered": "2015-08-17T07:28:53 -08:00", "latitude": -67.251279, "longitude": 77.718694, "tags": ["est", "labore", "sunt", "cillum", "excepteur", "veniam", "do"], "friends": [{"id": 0, "name": "Wanda Roman"}, {"id": 1, "name": "Marcy Levy"}, {"id": 2, "name": "Avis Hart"}], "greeting": "Hello, Brown Case! You have 7 unread messages.", "favoriteFruit": "apple"}, {"_id": "5aa7e144a58af4a4ffad8135", "index": 5, "guid": "bb5a4d1d-dd5e-47f4-af76-e8bd95720c38", "isActive": True, "balance": "$1, 561.07", "picture": "http://placehold.it/32x32", "age": 40, "eyeColor": "brown", "name": "Pacheco Banks", "gender": "male", "company": "MOMENTIA", "email": "pachecobanks@momentia.com", "phone": "+1 (978) 450-2829", "address": "349 Dare Court, Faywood, Texas, 1553", "about": "Cupidatat anim quis veniam et reprehenderit excepteur ullamco cillum ipsum cillum eiusmod adipisicing. Excepteur aliqua ipsum proident duis labore enim veniam est aute. Minim tempor magna cupidatat quis ut sint dolore magna aliquip in aliquip commodo velit cupidatat. Minim exercitation nostrud tempor ullamco aliquip nisi non labore do minim aliqua consectetur amet. Voluptate laboris veniam cupidatat nisi cillum dolor.", "registered": "2014-07-31T12:46:26 -0800", "latitude": 51.612576, "longitude": 88.287491, "tags": ["irure", "adipisicing", "Lorem", "aliquip", "ex", "est", "mollit"], "friends": [{"id": 0, "name": "Angelita Boyer"}, {"id": 1, "name": "Natasha Ramirez"}, {"id": 2, "name": "Mcgowan Farley"}], "greeting": "Hello, Pacheco Banks! You have 4 unread messages.", "favoriteFruit": "strawberry"}]),  # noqa: E501
        )
        test_data += self._get_is_same_disorderly_func_test_data()
        # Backward compability
        if sys.version_info[0] < 3:  # pragma: no cover
            backward_test_data = (
                (False, '1', u'1'),
                (False, r'1', u'1'),
            )
        else:  # pragma: no cover
            backward_test_data = (
                (True, '1', u'1'),
                (True, r'1', u'1'),
            )

        for d in test_data:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                d[0] == is_same_disorderly(d[1], d[2]),
                "expect: {0} equals\n'{1}'\n==\n'{2}'".format(d[0], d[1], d[2])
            )
            # Backward compability
            if sys.version_info[0] >= 3:  # pragma: no cover
                helper.append_to_error_if_not_expect_with_msg(
                    errors,
                    d[0] == is_same_disorderly(d[1], d[2], False),
                    "expect: {0} equals\n'{1}'\n==\n'{2}'".format(
                        d[0], d[1], d[2])
                )
        for d in backward_test_data:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                d[0] == is_same_disorderly(d[1], d[2], False),
                "expect: {0} in '{1}' and '{2}'".format(d[0], d[1], d[2])
            )

        assert errors == [], Exception(helper.get_error_string(errors))


class FalsyCls():
    def __len__(self):
        return 0

    def __bool__(self):
        return False


class TruthyCls():
    def __len__(self):
        return 1

    def __bool__(self):
        return True
