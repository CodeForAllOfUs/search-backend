import json
from queue import PriorityQueue
from urllib.request import urlopen
from threading import Thread, Timer
from datetime import datetime
from .models import Organization, Project, GitHubCache as GithubCacheModel

class GitHubHeartbeat():
    priority_uncached = 0
    priority_user_requested = 10
    priority_normal = 20

    interval_check_database = 900
    # @TODO: change this to `1` in production
    interval_uncached = 5
    interval_user_requested = 30
    @property
    def interval_normal(self):
        return self.rate_limit['time_left'] / self.queue.qsize()

    __rate_limit = None

    @property
    def rate_limit(self):
        if not self.__rate_limit or self.__rate_limit['reset_date'] < datetime.now():
            data = urlopen('https://api.github.com/rate_limit').read().decode(encoding='UTF8')
            data = json.loads(data)['resources']['core']
            self.__rate_limit = {
                'limit':       data['limit'],
                'remaining':   data['remaining'],
                'reset_date':  datetime.fromtimestamp(data['reset']),
            }

        self.__rate_limit['time_left'] = (self.__rate_limit['reset_date'] - datetime.now()).total_seconds()
        return self.__rate_limit

    def __init__(self):
        self.queue = PriorityQueue()
        self.queued = {}
        self.check_database_timer = None
        self.fetch_timer = None

    def queue_items(items, user_requested=False):
        for item in items:
            path = item.github_path

            # always put highest priority on uncached items.
            # make sure not to queue uncached items twice if they're queued again during the timer delay
            if item.github_data == None and path not in self.queued:
                self.queued[path] = priority_uncached
                self.queue.put((priority_uncached, path))

            # queue the item as user-requested only if it's not in the queue, or is, but with lower priority
            elif user_requested and (path not in self.queued or self.queued[path] > priority_user_requested):
                self.queued[path] = priority_user_requested
                self.queue.put((priority_user_requested, path))

            else:
                self.queued[path] = priority_normal
                self.queue.put((priority_normal, path))

    def enqueue(self, manager, github_paths):
        """
        public interface for user-requested github paths through the API
        """
        if isinstance(github_paths, str):
            github_paths = (github_paths,)

        items = manager.objects.filter(github_path__in=github_paths)
        # @TODO: need to differentiate between Orgs and Projects to do DB query
        self.queue_items(items, user_requested=True)

    def check_database(self):
        """
        check the database for new organizations and projects to enqueue
        """
        orgs = Organization.objects.filter(github_path__isnull=False)
        projects = Project.objects.filter(github_path__isnull=False)

        self.queue_items(orgs)
        self.queue_items(projects)

        self.check_database_timer = Timer(self.interval_check_database, self.check_database)
        self.check_database_timer.start()

    def fetch_next(self, github_paths):
        """
        pop the next github path from the queue and fetch it using the GitHub API
        """
        # if user-requested, remove it from the queue when done since it's already got a normal_priority instance to be recycled in the queue.
        def worker():
            # use a try block in case the model's been deleted during the timer wait
            # add any new Languages to ProgrammingLanguage Model and link them to GitHubCache foreign key
            # GitHubCache has its own db fields for issue_count etc so the client can use the API to query them
            # hook the GitHubCache back up with its original requester Organization/Project
            #   maybe should use the 'type' prop in the returned JSON
            #   maybe should just expand the data held by queue to be a dictionary

            # url: `https://api.github.com/repos/${this.owner}/${this.repo}`,
            # headers: {
            #     'Accept': 'application/vnd.github.v3+json'
            # },
            # json.loads(str, ensure_ascii=False)
            pass

        if rate_limit['remaining'] <= 0:
            interval = self.rate_limit['time_left']
        else:
            # get a task from the queue
            # download GitHub data for the item and store it in the database
            self.rate_limit['remaining'] -= 1
            url = self.queue.pop()[1]
            Thread(target=worker, args=(self.queue, url))

            # set timer for getting the next task
            next_task = self.queue.pop()
            next_priority = next_task[0]
            self.queue.put(next_task)

            if next_priority == priority_uncached:
                interval = self.interval_uncached
            elif next_priority == priority_user_requested:
                interval = self.interval_user_requested
            else:
                interval = self.interval_normal

        self.fetch_timer = Timer(interval, self.fetch_next)
        self.fetch_timer.start()

    def start(self):
        # initialize queue
        self.check_database()

        # start queue threads
        self.check_database_timer = Timer(self.interval_check_database, self.check_database)
        self.check_database_timer.start()
        self.fetch_timer = Timer(1, self.fetch_next)
        self.fetch_timer.start()

    def stop(self):
        if self.check_database_timer:
            self.check_database_timer.cancel()
        if self.fetch_timer:
            self.fetch_timer.cancel()

        self.check_database_timer = None
        self.fetch_timer = None
