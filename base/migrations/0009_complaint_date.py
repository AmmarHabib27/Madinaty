from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_user_is_phone_verified_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
