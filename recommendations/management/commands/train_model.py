from django.core.management.base import BaseCommand
from recommendations.ml_utils import train_and_save_model


class Command(BaseCommand):
    help = 'Train the recommendation model'

    def handle(self, *args, **options):
        self.stdout.write('Training model...')
        train_and_save_model()
        self.stdout.write('Model trained and saved successfully.')
