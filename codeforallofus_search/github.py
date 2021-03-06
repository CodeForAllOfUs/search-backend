import json
import itertools
import requests
import arrow
from queue import PriorityQueue
from threading import Thread, Timer
from urllib.request import urlopen

from .models import Organization, Project, GitHubOrganizationCache, GitHubProjectCache, ProgrammingLanguage

# tie-breaker for priority queue, ensures that
# tasks are popped from the queue in insertion order
counter = itertools.count()

class DaemonTimer(Timer):
    def __init__(self, *args, **kwargs):
        Timer.__init__(self, *args, **kwargs)
        self.daemon = True

class GitHubHeartbeat():
    priority_uncached = 0
    priority_user_requested = 10
    priority_normal = 20

    stale_threshold = 900
    interval_check_database = 900

    # @TODO: change this to `1` in production
    interval_uncached = 5
    interval_user_requested = 30
    @property
    def interval_normal(self):
        return min(self.rate_limit['time_left'] / (self.queue.qsize() or 1), 300)

    __rate_limit = None

    @property
    def rate_limit(self):
        if not self.__rate_limit or self.__rate_limit['reset_date'] < arrow.utcnow():
            data = urlopen('https://api.github.com/rate_limit').read().decode(encoding='UTF8')
            data = json.loads(data)['resources']['core']
            self.__rate_limit = {
                'limit':       data['limit'],
                'remaining':   data['remaining'],
                'reset_date':  arrow.get(data['reset']).replace(seconds=+5),
            }

        self.__rate_limit['time_left'] = (self.__rate_limit['reset_date'] - arrow.utcnow()).total_seconds()
        return self.__rate_limit

    def __init__(self):
        self.queue = PriorityQueue()
        self.queued = {}
        self.check_database_timer = None
        self.fetch_timer = None

    def decrement_rate_limit_remaining(self):
        self.rate_limit['remaining'] -= 1

    def queue_items(self, items, user_requested=False):
        priority_normal = self.priority_normal
        priority_uncached = self.priority_uncached
        priority_user_requested = self.priority_user_requested
        stale_threshold = self.stale_threshold

        for item in items:
            path = item.github_path

            if not path in self.queued:
                # always queue every item once with normal priority so that
                # it can be fetched on rotation in order to keep the data fresh
                print('Queueing normal priority for url:', path)
                self.queued[path] = priority_normal
                self.queue.put((priority_normal, next(counter), path))

            current_priority = self.queued[path]

            # always put highest priority on uncached items.
            # only queue items as uncached once during the life of the server
            if item.github_data == None and current_priority > priority_uncached:
                print('Queueing uncached priority for url:', path)
                self.queued[path] = priority_uncached
                self.queue.put((priority_uncached, next(counter), path))
            # only queue items as user_requested once during the life of the server
            elif user_requested and self.queued[path] > priority_user_requested:
                if item.github_data and (arrow.utcnow() - item.github_data.fetched).total_seconds() > stale_threshold:
                    print('Queueing user requested priority for url:', path)
                    self.queued[path] = priority_user_requested
                    self.queue.put((priority_user_requested, next(counter), path))

    def enqueue(self, manager, github_paths):
        """
        public interface for user-requested github paths through the API
        """
        if isinstance(github_paths, str):
            github_paths = (github_paths,)

        items = manager.objects.filter(github_path__isnull=False, github_path__in=github_paths)
        self.queue_items(items, user_requested=True)

    def check_database(self):
        """
        check the database for new organizations and projects to enqueue
        """
        orgs = Organization.objects.filter(github_path__isnull=False)
        projects = Project.objects.filter(github_path__isnull=False)

        self.queue_items(orgs)
        self.queue_items(projects)

        self.check_database_timer = DaemonTimer(self.interval_check_database, self.check_database)
        self.check_database_timer.start()

    class Downloader(Thread):
        org_url = 'https://api.github.com/orgs/%s'
        project_url = 'https://api.github.com/repos/%s'
        headers = {'accept': 'application/vnd.github.v3+json'}

        def __init__(self, heartbeat, github_path, priority, *args, **kwargs):
            Thread.__init__(self, *args, daemon=True, **kwargs)
            self.heartbeat = heartbeat
            self.github_path = github_path
            self.priority = priority

        def run(self):
            if '/' not in self.github_path:
                url = self.org_url % self.github_path
                manager = Organization
            else:
                url = self.project_url % self.github_path
                manager = Project

            try:
                model = manager.objects.get(github_path=self.github_path)
            except:
                self.finish(errored=True)
                return

            response = self.download_data(url)

            if response.status_code == 200:
                if manager == Organization:
                    print('Filling organization with data:', response.text)
                    self.fill_org_data(model, response)
                else:
                    print('Filling project with data:', response.text)
                    self.fill_project_data(model, response)
            else:
                # @TODO: if not a 200 status code, send an email with the details
                print('GitHub API Error getting url:', url)
                print('Response status code was:', response.status_code)
                print('Error message was:', response.text)

            if response.status_code != 404:
                self.requeue()

            self.finish()

        def download_data(self, url):
            print('Getting GitHub API url:', url, 'with priority', self.priority)
            self.heartbeat.decrement_rate_limit_remaining()
            return requests.get(url, headers=self.headers)

        def fill_org_data(self, model, response):
            try:
                cache = GitHubOrganizationCache.objects.get(github_path=self.github_path)
            except:
                cache = GitHubOrganizationCache(github_path=self.github_path)

            data = response.json()

            cache.fetched = arrow.utcnow().datetime
            cache.json = json.dumps(data)
            cache.save()

            model.github_data = cache
            model.save()

        def fill_project_data(self, model, response):
            try:
                cache = GitHubProjectCache.objects.get(github_path=self.github_path)
            except:
                cache = GitHubProjectCache(github_path=self.github_path)

            data = response.json()
            # @TODO: If you are using MySQL, be sure to use the READ COMMITTED isolation level rather than REPEATABLE READ (the default), otherwise you may see cases where get_or_create will raise an IntegrityError but the object won’t appear in a subsequent get() call.
            # ref: https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create-kwargs
            language, was_created = ProgrammingLanguage.objects.get_or_create(name=data['language'])

            try:
                last_commit_date = arrow.get(data['pushed_at']).datetime
            except:
                last_commit_date = None

            cache.fetched = arrow.utcnow().datetime
            cache.json = json.dumps(data)
            cache.open_issues_count = data['open_issues_count']
            cache.stargazers_count = data['stargazers_count']
            cache.last_commit = last_commit_date
            cache.language = language
            cache.save()

            model.github_data = cache
            model.save()

        def requeue(self):
            # normal_priority task is automatically queued and requeued for all items.
            # this keeps them on rotation so the cache data stays fresh.
            # all other priorities are special requests that don't require a requeue.
            if self.priority == self.heartbeat.priority_normal:
                print('Requeueing path:', self.github_path)
                self.heartbeat.queue.put((self.heartbeat.priority_normal, next(counter), self.github_path))

        def finish(self, errored=False):
            if not errored and self.priority != self.heartbeat.priority_normal:
                # reset priority for that github_path in case it needs to be elevated again by a user request
                self.heartbeat.queued[self.github_path] = self.heartbeat.priority_normal

            self.heartbeat.queue.task_done()

    def fetch_next(self):
        """
        pop the next github path from the queue and fetch it using the GitHub API
        """
        if self.rate_limit['remaining'] <= 0:
            print('Rate Limit exhausted. Waiting until', self.rate_limit['reset_date'], 'seconds left:', self.rate_limit['time_left'])
            interval = self.rate_limit['time_left']
        else:
            priority, q_insertion_num, github_path = self.queue.get()

            # Spawn a thread to download the GitHub data for the item and store it in the database
            self.Downloader(self, github_path, priority).start()

            # set timer for getting the next task.
            # keep q_insertion_num the same to keep sort order
            next_task = self.queue.get()
            next_priority = next_task[0]
            self.queue.put(next_task)

            if next_priority == self.priority_uncached:
                interval = self.interval_uncached
            elif next_priority == self.priority_user_requested:
                interval = self.interval_user_requested
            else:
                interval = self.interval_normal

        self.fetch_timer = DaemonTimer(interval, self.fetch_next)
        self.fetch_timer.start()

    def start(self):
        # initialize queue
        self.check_database()

        # start queue threads
        self.check_database_timer = DaemonTimer(self.interval_check_database, self.check_database)
        self.check_database_timer.start()
        self.fetch_timer = DaemonTimer(1, self.fetch_next)
        self.fetch_timer.start()

    def stop(self):
        if self.check_database_timer:
            self.check_database_timer.cancel()
        if self.fetch_timer:
            self.fetch_timer.cancel()

        self.check_database_timer = None
        self.fetch_timer = None
