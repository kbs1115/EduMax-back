# Generated by Django 4.2.7 on 2024-04-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_alter_like_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='category_d1',
            field=models.CharField(choices=[('KO', 'Korean'), ('EN', 'English'), ('MA', 'Math'), ('TM', 'Tamgu')], max_length=2),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('FR', 'Free'), ('NO', 'Notice'), ('KQ', 'Korean Question'), ('EQ', 'Eng Question'), ('MQ', 'Math Question'), ('TQ', 'Tamgu Question'), ('KD', 'Korean Data'), ('ED', 'Eng Data'), ('MD', 'Math Data'), ('TD', 'Tamgu Data')], default='FR', max_length=2),
        ),
    ]
