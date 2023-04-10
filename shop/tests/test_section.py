from django.test import TestCase

from shop.models import Section


class SectionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Section.objects.create(title='Main', slug='main')

    def test_title_max_length(self):
        obj = Section.objects.get(id=1)
        max_length = obj._meta.get_field('title').max_length
        self.assertEqual(max_length, 70)

    def test_title_help_text(self):
        obj = Section.objects.get(id=1)
        help_text = obj._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Тут надо ввести название раздела')

    def test_title_unique(self):
        obj = Section.objects.get(id=1)
        unique = obj._meta.get_field('title').unique
        self.assertTrue(unique)

    def test_title_verbose_name(self):
        obj = Section.objects.get(id=1)
        verbose_name = obj._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Название раздела')

    def test_slug_max_length(self):
        obj = Section.objects.get(id=1)
        max_length = obj._meta.get_field('slug').max_length
        self.assertEqual(max_length, 40)

    def test_slug_verbose_name(self):
        obj = Section.objects.get(id=1)
        verbose_name = obj._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Псевдоним')

    def test_slug_default(self):
        obj = Section.objects.get(id=1)
        default = obj._meta.get_field('slug').default
        self.assertEqual(default, '')

    def test_meta_ordering(self):
        obj = Section.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ['id'])

    def test_meta_verbose_name(self):
        obj = Section.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Раздел')

    def test_meta_verbose_name_plural(self):
        obj = Section.objects.get(id=1)
        verbose_name_plural = obj._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Разделы')

    def test_get_absolute_url(self):
        obj = Section.objects.get(id=1)
        self.assertEqual(obj.get_absolute_url(), '/shop/section/' + obj.slug)

    def test_str(self):
        obj = Section.objects.get(id=1)
        self.assertEqual(str(obj), obj.title)
