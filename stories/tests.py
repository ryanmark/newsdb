"""
Tests for the NewsDB Stories App
"""

from django.test import TestCase
from tastypie.test import ResourceTestCase
from tastypie.serializers import Serializer
serializer = Serializer()

from stories.models import Product, Story, StoryMeta, Taxonomy, Term

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import get_current_timezone, utc

import pprint
pp = pprint.PrettyPrinter(indent=4)


class StoryTest(TestCase):
    def setUp(self):
        self.story = Story.objects.create(
            title='Lorem Ipsum',
            body='This is a test story'
        )
        self.meta = [
            self.story.meta.create(key='seo_description',
                value='Lorem ipsum test story'),
            self.story.meta.create(key='permalink',
                value='http://www.example.com/story/%s' % self.story.slug),
        ]
        self.product = self.story.products.create(name="Chicago Tribune")

    def test_story(self):
        """
        Test basic story creation and access
        """

        # Did the model get created?
        self.assertEqual('Lorem Ipsum', unicode(self.story))

        # Did the slug get generated?
        self.assertEqual('lorem-ipsum', unicode(self.story.slug))

        # Did the default site get associated?
        #self.assertEqual(Site.objects.get_current(), self.story.sites.all()[0])

        # Did the meta get saved and associated correctly?
        self.assertEqual('Lorem ipsum test story',
            unicode(self.meta[0]))
        self.assertEqual('http://www.example.com/story/%s' % self.story.slug,
            unicode(self.meta[1]))

        # Can we retrieve our story?
        self.assertEqual('Lorem Ipsum',
            unicode(Story.objects.get(slug='lorem-ipsum')))

        # Can we retrieve our permalink?
        self.assertEqual('http://www.example.com/story/lorem-ipsum',
            unicode(self.story.meta.get(key='permalink')))

        # Does get_absolute_url work?
        self.assertEqual('http://www.example.com/story/lorem-ipsum',
            self.story.get_absolute_url())

        # Did the product get associated?
        self.assertEqual('Chicago Tribune',
                unicode(self.product))

    def test_url(self):
        # When a permalink is not present, we should get a generated url
        self.story.meta.get(key='permalink').delete()

        self.assertEqual('',
            self.story.get_absolute_url())


class TaxonomyTest(TestCase):
    def setUp(self):
        self.tax = Taxonomy.objects.create(
            name='Category'
        )
        self.terms = [
            self.tax.terms.create(name='Real Estate'),
            self.tax.terms.create(name='News'),
        ]
        self.terms[0].meta.create(key='seo_description',
                value='Real Estate news')
        self.terms[0].meta.create(key='permalink',
                value='http://www.example.com/category/real-estate/')
        self.terms[1].meta.create(key='seo_description',
                value='Breaking National news')
        self.terms[1].meta.create(key='permalink',
                value='http://www.example.com/category/news/')

    def test_tax(self):
        """
        Test basic object fields
        """
        self.assertEqual('Category', unicode(self.tax))

        self.assertEqual('category', unicode(self.tax.slug))

        self.assertEqual('Real Estate', unicode(self.terms[0]))
        self.assertEqual('real-estate', unicode(self.terms[0].slug))

        self.assertEqual('News', unicode(self.terms[1]))
        self.assertEqual('news', unicode(self.terms[1].slug))

        self.assertEqual('Category',
                unicode(Taxonomy.objects.get(slug='category')))

    def test_story_term(self):
        story = Story.objects.create(
            title='Lorem Ipsum',
            body='This is a test story'
        )

        story.terms = self.terms

        self.assertEqual('Real Estate', unicode(story.terms.all()[0]))
        self.assertEqual('real-estate', unicode(story.terms.all()[0].slug))

        self.assertEqual('News', unicode(story.terms.all()[1]))
        self.assertEqual('news', unicode(story.terms.all()[1].slug))


class ApiTest(ResourceTestCase):
    def setUp(self):
        self.tax = Taxonomy.objects.create(
            name='Category'
        )
        self.terms = [
            self.tax.terms.create(name='Real Estate'),
            self.tax.terms.create(name='News'),
        ]

    def test_create_story(self):
        pass

    def test_update_story(self):
        pass

    def test_delete_story(self):
        pass


class StoryResourceTest(ResourceTestCase):
    # Use ``fixtures`` & ``urls`` as normal. See Django's ``TestCase``
    # documentation for the gory details.
    #fixtures = ['test_entries.json']

    def setUp(self):
        super(StoryResourceTest, self).setUp()

        # Create a user.
        self.username = 'admin'
        self.password = 'pass'
        self.user = User.objects.create_user(
                self.username, 'admin@example.com', self.password)
        self.user.is_superuser = True
        self.user.save()

        self.story = Story.objects.create(
            title='Lorem Ipsum',
            body='This is a test story'
        )
        self.story.meta.create(key='seo_description',
            value='Lorem ipsum test story')
        self.story.meta.create(key='permalink',
            value='http://www.example.com/story/%s' % self.story.slug)

        # We also build a detail URI, since we will be using it all over.
        # DRY, baby. DRY.
        self.detail_url = '/api/v1/story/{0}/'.format(self.story.pk)

        # The data we'll send on POST requests. Again, because we'll use it
        # frequently (enough).
        self.post_data = {
            #'user': '/api/v1/user/{0}/'.format(self.user.pk),
            'title': 'Second Post!',
            'slug': 'second-post',
            'create_date': '2012-05-01T22:05:12'
        }

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def test_get_list_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/story/', format='json'))

    def test_get_list_json(self):
        resp = self.api_client.get('/api/v1/story/', format='json',
                authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        # Scope out the data for correctness.
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        # Here, we're checking an entire structure for the expected data.
        resp_data = self.deserialize(resp)['objects'][0]
        test_data = {
            u'id': self.story.pk,
            #'user': '/api/v1/user/{0}/'.format(self.user.pk),
            u'title': u'Lorem Ipsum',
            u'slug': u'lorem-ipsum',
            u'create_date': unicode(serializer.format_datetime(self.story.create_date)),
            u'publish_date': unicode(serializer.format_datetime(self.story.publish_date)),
            u'body': u'This is a test story',
            u'brief': '',
            u'status': u'draft',
            u'terms': [],
            u'meta': [
                {u'key': u'seo_description', u'value': u'Lorem ipsum test story'},
                {u'key': u'permalink', u'value': u'http://www.example.com/story/lorem-ipsum'},
            ],
            u'type': u'story',
            u'trash': False,
            u'resource_uri': u'/api/v1/story/{0}/'.format(self.story.pk)
        }

        self.assertEqual(resp_data, test_data)

    def test_get_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
                self.api_client.get(self.detail_url, format='json'))

    def test_get_detail_json(self):
        resp = self.api_client.get(self.detail_url,
                format='json', authentication=self.get_credentials())
        self.assertValidJSONResponse(resp)

        # We use ``assertKeys`` here to just verify the keys, not all the data.
        self.assertKeys(self.deserialize(resp),
                ['body', 'brief', 'create_date', 'id', 'publish_date',
                'resource_uri', 'slug', 'status', 'terms', 'title',
                'trash', 'type', 'meta'])
        self.assertEqual(self.deserialize(resp)['title'], 'Lorem Ipsum')

    def test_post_list_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/v1/story/',
            format='json', data=self.post_data))

    def test_post_list(self):
        # Check how many are there first.
        self.assertEqual(Story.objects.count(), 1)
        req = self.api_client.post(
                '/api/v1/story/',
                format='json',
                data=self.post_data,
                authentication=self.get_credentials())
        self.assertHttpCreated(req)
        # Verify a new one has been added.
        self.assertEqual(Story.objects.count(), 2)

    def test_put_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
                self.api_client.put(self.detail_url,
                format='json',
                data={}))

    def test_put_detail(self):
        # Grab the current data & modify it slightly.
        original_data = self.deserialize(self.api_client.get(
                self.detail_url,
                format='json',
                authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['title'] = 'Updated: Lorem Ipsum'

        # Tastypie thinks this is in the local timezone if there no Z...
        new_data['create_date'] = '2012-05-01T20:06:12Z'

        self.assertEqual(Story.objects.count(), 1)

        self.assertHttpAccepted(self.api_client.put(
                self.detail_url,
                format='json',
                data=new_data,
                authentication=self.get_credentials()))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Story.objects.count(), 1)
        # Check for updated data.
        self.assertEqual(Story.objects.get(pk=1).title, 'Updated: Lorem Ipsum')
        self.assertEqual(Story.objects.get(pk=1).slug, 'lorem-ipsum')
        self.assertEqual(
                Story.objects.get(pk=1).create_date,
                datetime.datetime(2012, 5, 1, 20, 6, 12, tzinfo=utc))

    def test_delete_detail_unauthenticated(self):
        self.assertHttpUnauthorized(
                self.api_client.delete(self.detail_url, format='json'))

    def test_delete_detail(self):
        self.assertEqual(Story.objects.count(), 1)
        self.assertHttpAccepted(self.api_client.delete(
                    self.detail_url,
                    format='json',
                    authentication=self.get_credentials()))
        self.assertEqual(Story.objects.count(), 0)
