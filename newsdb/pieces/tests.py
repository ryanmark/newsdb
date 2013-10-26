"""
Tests for the NewsDB pieces App
"""

from django.test import TestCase
from .models import Piece
from newsdb.taxonomy.models import Taxonomy

from django.test.client import Client
c = Client()

import pprint
pp = pprint.PrettyPrinter(indent=4)


class PieceTest(TestCase):
    urls = 'newsdb.pieces.urls'

    def setUp(self):
        self.piece = Piece.objects.create(
            title='Lorem Ipsum'
        )
        self.meta = [
            self.piece.meta.create(
                key='seo_description',
                value='Lorem ipsum test piece'),
            self.piece.meta.create(
                key='permalink',
                value='http://www.example.com/piece/%s' % self.piece.slug),
        ]
        self.product = self.piece.publications.create(name="Chicago Tribune")

    def test_piece(self):
        """
        Test basic piece creation and access
        """

        # Did the model get created?
        self.assertEqual('Lorem Ipsum', unicode(self.piece))

        # Did the slug get generated?
        self.assertEqual('lorem-ipsum', unicode(self.piece.slug))

        # Did the default site get associated?
        #self.assertEqual(
            #Site.objects.get_current(), self.piece.sites.all()[0])

        # Did the meta get saved and associated correctly?
        self.assertEqual(
            'Lorem ipsum test piece',
            unicode(self.meta[0]))
        self.assertEqual(
            'http://www.example.com/piece/%s' % self.piece.slug,
            unicode(self.meta[1]))

        # Can we retrieve our piece?
        self.assertEqual(
            'Lorem Ipsum',
            unicode(Piece.objects.get(slug='lorem-ipsum')))

        # Can we retrieve our permalink?
        self.assertEqual(
            'http://www.example.com/piece/lorem-ipsum',
            unicode(self.piece.meta.get(key='permalink')))

        # Does get_absolute_url work?
        self.assertEqual(
            '/pieces/lorem-ipsum',
            self.piece.get_absolute_url())

        # Did the product get associated?
        self.assertEqual('Chicago Tribune', unicode(self.product))

    def test_url(self):
        # When a permalink is not present, we should get a generated url
        self.piece.meta.get(key='permalink').delete()

        self.assertEqual('/pieces/lorem-ipsum', self.piece.get_absolute_url())


class TaxonomyTest(TestCase):
    def setUp(self):
        self.tax = Taxonomy.objects.create(
            name='Category'
        )
        self.terms = [
            self.tax.terms.create(name='Real Estate'),
            self.tax.terms.create(name='News'),
        ]
        self.terms[0].meta.create(
            key='seo_description',
            value='Real Estate news')
        self.terms[0].meta.create(
            key='permalink',
            value='http://www.example.com/category/real-estate/')
        self.terms[1].meta.create(
            key='seo_description',
            value='Breaking National news')
        self.terms[1].meta.create(
            key='permalink',
            value='http://www.example.com/category/news/')

    def test_tax(self):
        """
        Test basic object fields
        """
        self.assertEqual('Category', unicode(self.tax))

        self.assertEqual('category', unicode(self.tax.slug))

        self.assertEqual('Real Estate (Category)', unicode(self.terms[0]))
        self.assertEqual('real-estate', unicode(self.terms[0].slug))

        self.assertEqual('News (Category)', unicode(self.terms[1]))
        self.assertEqual('news', unicode(self.terms[1].slug))

        self.assertEqual(
            'Category', unicode(Taxonomy.objects.get(slug='category')))

    def test_piece_term(self):
        piece = Piece.objects.create(
            title='Lorem Ipsum'
        )

        piece.terms = self.terms

        self.assertEqual(
            'Real Estate (Category)', unicode(piece.terms.all()[0]))
        self.assertEqual(
            'real-estate', unicode(piece.terms.all()[0].slug))

        self.assertEqual(
            'News (Category)', unicode(piece.terms.all()[1]))
        self.assertEqual(
            'news', unicode(piece.terms.all()[1].slug))


class PieceApiTest(TestCase):
    #fixtures = ['test_entries.json']
    urls = 'newsdb.pieces.urls'

    def setUp(self):
        pass

    def test_create_piece(self):
        response = c.post('/pieces/', {'slug': 'foo'})

        self.assertEqual(200, response.status_code)
        pp.pprint(response.data)
