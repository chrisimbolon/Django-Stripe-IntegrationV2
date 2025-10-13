# payments/management/commands/seed_sessions.py
from django.core.management.base import BaseCommand
from payments.models import TherapySession


class Command(BaseCommand):
    help = 'Seeds the database with sample therapy sessions'

    def handle(self, *args, **kwargs):
        # Clear existing sessions
        TherapySession.objects.all().delete()
        self.stdout.write('Cleared existing sessions...')

        # Sample sessions data
        sessions = [
            {
                'title': 'Rock Your Anxiety Away',
                'therapy_type': 'individual',
                'description': 'One-on-one session to help you overcome anxiety and stress. We\'ll rock through your worries together and find your inner peace.',
                'duration': 60,
                'price': 100.00,
                'available': True,
            },
            {
                'title': 'Couples Harmony Session',
                'therapy_type': 'couples',
                'description': 'Strengthen your relationship and improve communication. Let\'s create beautiful harmony in your partnership, one session at a time.',
                'duration': 90,
                'price': 150.00,
                'available': True,
            },
            {
                'title': 'Group Therapy Jam',
                'therapy_type': 'group',
                'description': 'Connect with others facing similar challenges in a supportive group environment. Share experiences and grow together.',
                'duration': 120,
                'price': 75.00,
                'available': True,
            },
            {
                'title': 'Family Rock Fest',
                'therapy_type': 'family',
                'description': 'Improve family dynamics and communication. Work through conflicts and build stronger bonds with your loved ones.',
                'duration': 90,
                'price': 180.00,
                'available': True,
            },
            {
                'title': 'Depression Deep Dive',
                'therapy_type': 'individual',
                'description': 'Specialized session for dealing with depression. Learn coping strategies and work towards feeling better.',
                'duration': 60,
                'price': 110.00,
                'available': True,
            },
            {
                'title': 'Quick Mental Tune-Up',
                'therapy_type': 'individual',
                'description': 'Short session for a quick mental health check-in. Perfect for maintaining your well-being.',
                'duration': 30,
                'price': 60.00,
                'available': True,
            },
            {
                'title': 'Teen Rock Session',
                'therapy_type': 'individual',
                'description': 'Specialized therapy for teenagers dealing with school, relationships, and identity. A safe space to express yourself.',
                'duration': 60,
                'price': 90.00,
                'available': True,
            },
            {
                'title': 'Trauma Recovery Journey',
                'therapy_type': 'individual',
                'description': 'Work through past trauma in a safe, supportive environment. Healing takes time, and we\'re here for you.',
                'duration': 75,
                'price': 130.00,
                'available': True,
            },
        ]

        # Create sessions
        created_count = 0
        for session_data in sessions:
            session = TherapySession.objects.create(**session_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created: {session.title}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎸 Successfully created {created_count} therapy sessions!')
        )