from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.db.transaction import Atomic, get_connection


class LockedAtomicTransaction(Atomic):
    def __init__(self, model, using=None, savepoint=None):
        if using is None:
            using = DEFAULT_DB_ALIAS
        super().__init__(using, savepoint)
        self.model = model

    def __enter__(self):
        super(LockedAtomicTransaction, self).__enter__()
        engine = settings.DATABASES[self.using]['ENGINE']
        if engine != 'django.db.backends.sqlite3':
            cursor = None
            try:
                cursor = get_connection(self.using).cursor()
                cursor.execute(
                    'LOCK TABLE {db_table_name}'.format(
                        db_table_name=self.model._meta.db_table
                    )
                )
            finally:
                if cursor and not cursor.closed:
                    cursor.close()
