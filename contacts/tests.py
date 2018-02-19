from django.test import TestCase

from . import utils


class UtilsTests(TestCase):

    def test_unique(self):
        self.assertEqual(utils.unique([1, 2, 3]), [1, 2, 3])
        self.assertEqual(utils.unique([1, 1, 2, 3]), [1, 2, 3])
        self.assertEqual(utils.unique([1, 2, 3, 2, 1]), [1, 2, 3])

    def test_generate_verification_code(self):
        self.assertEqual(
            utils.generate_verification_code('2004011344', '韩文弢'),
            'ae025c')

    def test_split_class_name(self):
        self.assertEqual(utils.split_class_name(''), ('', -1, -1, ''))
        self.assertEqual(utils.split_class_name('计44'), ('计', 4, 4, ''))
        self.assertEqual(utils.split_class_name('计40'), ('计', 4, 0, ''))
        self.assertEqual(utils.split_class_name('计44', 2004), ('计', -1, 4, ''))
        self.assertEqual(utils.split_class_name('工物41'), ('工物', 4, 1, ''))
        self.assertEqual(utils.split_class_name('建环4'), ('建环', 4, -1, ''))
        self.assertEqual(utils.split_class_name('文科4A'), ('文科', 4, -1, 'A'))
        self.assertEqual(utils.split_class_name('无410'), ('无', 4, 10, ''))
