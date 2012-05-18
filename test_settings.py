"""Special settings file for use when testing.  This specifies a SQLite
database to use when running tests.

Just make sure you run the tests and specify this file:
> ./manage.py test --settings=test_settings
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
		'NAME': ':memory:',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INSTALLED_APPS = ('report_tracking',)
