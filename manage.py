#!/usr/bin/env python3.4
from flask.ext.script import Manager
from project import app
from project.models import init_db as init
from project.fixtures import load_fixtures
import logging
from contextlib import contextmanager
from subprocess import call

logger = logging.getLogger()


@contextmanager
def wrap_logging(before, fail, after):
    logger.info(before)
    try:
        yield
    except Exception as e:
        logger.error(fail)
        logger.error(e)
    else:
        logger.info(after)


manager = Manager(app)


@manager.command
def init_empty_db():
    """ Create empty database """
    with wrap_logging(
        before='Creating empty DB ...',
        fail='Cannot create empty DB',
        after='Done',
    ):
        init()


@manager.command
def init_db():
    """ Create database and populate it with fixtures """
    init_empty_db()
    with wrap_logging(
        before='Loading fixtures...',
        fail='Cannot populate fixtures',
        after='Done',
    ):
        load_fixtures(app.config['FIXTURES_DIR'])


@manager.command
def run():
    """ Run application """
    app.run(debug=True)


@manager.command
def collectstatic():
    """
        run external gulp build script
        NOTE: gulp must be in your PATH variable
    """
    with wrap_logging(
        before='Collecting static...',
        fail='Error while collecting static',
        after='Done',
    ):
        call(["npm", "install"])
        call(["bower", "install"])
        call(["gulp", "build"])


if __name__ == "__main__":
    manager.run()
