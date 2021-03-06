import time

from webarchiver.database import UrlDeduplicationDatabase
from webarchiver.job import Job


class CrawlerServerJob:
    def __init__(self, identifier, filenames_set, finished_urls_set,
                 found_urls_set):
        self.stager = []
        self.started = False
        self.received_url_quota = time.time()
        self._identifier = identifier
        self._job = Job(identifier, filenames_set, finished_urls_set,
                           found_urls_set)
        self._urls = {}
        self._url_database = UrlDeduplicationDatabase(self._identifier,
            'crawler_' + self._identifier)

    def add_stager(self, s):
        if s in self.stager:
            return None
        self.stager.append(s)

    def add_url(self, s, url):
        if self.finished_url(url):
            return None
        self._urls[url] = s
        self._job.add_url(url)

    def increase_url_quota(self, i):
        self._received_url_quota = time.time()
        self._job.increase_url_quota(i)

    def get_url_stager(self, url):
        return self._urls[url]

    def delete_url_stager(self, url):
        del self._urls[url]

    def start(self):
        if self.is_started:
            return None
        self._job.start()
        self.started = True
        return True

    def finished_url(self, url):
        self._url_database.insert(url)

    def archived_url(self, url):
        return self._url_database.has_url(url)

    @property
    def is_started(self):
        return self.started or self._job.ident

