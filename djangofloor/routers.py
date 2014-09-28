#coding=utf-8


__author__ = 'flanker'


# noinspection PyUnusedLocal,PyProtectedMember
class BaseRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    @staticmethod
    def db_for_read(model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        return None

    @staticmethod
    def db_for_write(model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        return None

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return None

    @staticmethod
    def allow_syncdb(db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        return None

if __name__ == '__main__':
    import doctest

    doctest.testmod()
