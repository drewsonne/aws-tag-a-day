from pkg_resources import iter_entry_points


class Services(object):
    def __init__(self, session, services, cache, proposals):

        init_params = {
            'session': session, 'table': proposals,
            'cache': cache
        }
        self._mapping = list(map(
            lambda ep: ep.load()(**init_params),
            filter(
                lambda ep: ep.name in services,
                iter_entry_points(group='tag_a_day', name=None)
            )
        ))

        self._current = 0

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current < len(self._mapping):
            self._current += 1
            return self._mapping[self._current - 1]
        else:
            raise StopIteration()