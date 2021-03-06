import idtool
import unittest


class IDGeneratorTest(unittest.TestCase):

    def test_default_chars_without_initial(self):
        id_generator = idtool.IDGenerator(length=2)
        targets = ['01', '02', '03', '04']
        results = []
        for i in range(4):
            id_generator.next()
            results.append(id_generator.get_id())
        self.assertEqual(targets, results)

    def test_default_chars_with_initial(self):
        id_generator = idtool.IDGenerator(length=6, initial='01209x')
        targets = ['01209y', '01209z', '0120a0', '0120a1']
        results = []
        for i in range(4):
            id_generator.next()
            results.append(id_generator.get_id())
        self.assertEqual(targets, results)

    def test_custom_chars(self):
        id_generator = idtool.IDGenerator(
            length=2,
            chars=['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九'],
            initial='一七'
        )
        targets = ['一八', '一九', '二〇', '二一']
        results = []
        for i in range(4):
            id_generator.next()
            results.append(id_generator.get_id())
        self.assertEqual(targets, results)

    def test_carry(self):
        id_generator = idtool.IDGenerator(length=2, chars=['0', '1'], initial='10')
        self.assertFalse(id_generator.next())
        self.assertTrue(id_generator.next())

    def test_duplicate_chars(self):
        with self.assertRaises(idtool.IDGenerator.DuplicateChars):
            idtool.IDGenerator(length=2, chars=['1', '2', '1'])

    def test_illegal_initial_length_mismatch(self):
        with self.assertRaises(idtool.IDGenerator.IllegalIDFormat):
            idtool.IDGenerator(length=2, chars=['0', '1'], initial='001')

    def test_illegal_initial_chars_mismatch(self):
        with self.assertRaises(idtool.IDGenerator.IllegalIDFormat):
            idtool.IDGenerator(length=2, chars=['0', '1'], initial='12')

    def test_length_not_positive(self):
        with self.assertRaises(ValueError):
            idtool.IDGenerator(length=0, chars=['0', '1'])

    def test_type_error_length(self):
        with self.assertRaises(TypeError):
            idtool.IDGenerator(length='2')

    def test_type_error_chars(self):
        with self.assertRaises(TypeError):
            idtool.IDGenerator(length=2, chars=12)

    def test_type_error_initial(self):
        with self.assertRaises(TypeError):
            idtool.IDGenerator(length=2, initial=12)


class IDManagerTest(unittest.TestCase):

    def setUp(self):
        self.id_manager = idtool.IDManager()
        self.id_manager.add_id(idtool.IDGenerator(length=2, chars=['0', '1']), auto_increase=True)
        self.id_manager.add_id(idtool.IDGenerator(length=2, chars=['0', '1'], initial='11'))
        self.id_manager.add_separator('/')
        self.id_manager.add_id(idtool.IDGenerator(length=2, chars=['0', '1'], initial='11'), auto_increase=True)
        self.id_manager.add_separator('/')
        self.id_manager.add_id(idtool.IDGenerator(length=2, chars=['0', '1'], initial='11'), auto_increase=True)
        self.id_manager.add_separator('-')
        self.id_manager.add_id(idtool.IDGenerator(length=2, chars=['0', '1'], initial='11'))

    def test_get_id(self):
        self.assertEqual('0011/11/11-11', self.id_manager.get_id())

    def test_set_id(self):
        self.id_manager.set_id(1, '10')
        self.assertEqual('0010/11/11-11', self.id_manager.get_id())

    def test_next_auto_increase_default(self):
        self.id_manager.next()
        self.assertEqual('0011/00/00-00', self.id_manager.get_id())

    def test_next_auto_increase_not_default(self):
        self.id_manager.next(3)
        self.assertEqual('0011/00/00-11', self.id_manager.get_id())

    def test_next_not_auto_increase(self):
        self.id_manager.next(1)
        self.assertEqual('0100/11/11-11', self.id_manager.get_id())
