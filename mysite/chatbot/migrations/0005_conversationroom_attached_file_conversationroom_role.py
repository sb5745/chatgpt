# Generated by Django 4.2.16 on 2024-10-09 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_remove_conversationroom_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationroom',
            name='attached_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='conversationroom',
            name='role',
            field=models.CharField(default='user', max_length=255),
        ),
    ]
