from django.core.files import File
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from aiarena import settings
from aiarena.core.models import User, Map, Bot, Match, Result
from aiarena.core.tests import BaseTestCase
from aiarena.core.utils import EnvironmentType


def create_match(as_user):
    return Match.start_next_match(as_user)


def create_result(match, type, as_user):
    with open(BaseTestCase.test_replay_path, 'rb') as result_replay:
        result = Result.objects.create(match=match, type=type, replay_file=File(result_replay), duration=1,
                                       submitted_by=as_user)
        result.finalize_submission(None, None)


def run_seed():
    devadmin = User.objects.create_superuser(username='devadmin', password='x', email='devadmin@aiarena.net')
    Token.objects.create(user=devadmin)
    devuser = User.objects.create(username='devuser', password='x', email='devuser@aiarena.net')
    Map.objects.create(name='test_map')

    with open(BaseTestCase.test_bot_zip_path, 'rb') as bot_zip:
        Bot.objects.create(user=devadmin, name='devadmin_bot1', active=True, plays_race='T', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devadmin, name='devadmin_bot2', active=True, plays_race='Z', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devadmin, name='devadmin_bot3', plays_race='P', type='python',
                           bot_zip=File(bot_zip))  # inactive bot

        Bot.objects.create(user=devuser, name='devuser_bot1', active=True, plays_race='P', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser, name='devuser_bot2', active=True, plays_race='Z', type='python',
                           bot_zip=File(bot_zip))
        Bot.objects.create(user=devuser, name='devuser_bot3', plays_race='T', type='python',
                           bot_zip=File(bot_zip))  # inactive bot

    # 4 active bots - 6 games per round
    # Round 1
    match = create_match(devadmin)
    create_result(match, 'Player1Win', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Player2Win', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Player1Crash', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Player1TimeOut', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Tie', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Timeout', devadmin)
    # Round 2
    match = create_match(devadmin)
    create_result(match, 'MatchCancelled', devadmin)
    match = create_match(devadmin)
    create_result(match, 'InitializationError', devadmin)
    match = create_match(devadmin)
    create_result(match, 'Player2Crash', devadmin)


class Command(BaseCommand):
    help = "Seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        if settings.ENVIRONMENT_TYPE == EnvironmentType.DEVELOPMENT:
            run_seed()
        else:
            self.stdout.write('Seeding failed: This is not a development environment!')

        self.stdout.write('Done.')
