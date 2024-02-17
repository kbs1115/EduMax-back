# Generated by Django 4.2.7 on 2024-02-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('html_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_location', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('youtube_id', models.CharField(max_length=11, unique=True)),
                ('category_d1', models.CharField(choices=[('KO', 'Korean'), ('EN', 'English'), ('MA', 'Math')], max_length=2)),
                ('category_d2', models.CharField(choices=[('SC', 'School Test'), ('SA', 'Sat'), ('GR', 'Grammar')], default=None, max_length=3, null=True)),
                ('category_d3', models.CharField(choices=[('TB', 'Textbook'), ('EBS', 'Ebs'), ('SCM', 'School Mock Exam'), ('SAM', 'Sat Mock Exam'), ('PGR', 'Pocket Grammar'), ('BGR', 'Basic Grammar')], default=None, max_length=3, null=True)),
                ('category_d4', models.CharField(choices=[('E0', 'English0'), ('E1', 'English1'), ('E2', 'English2'), ('RC', 'Reading Composition'), ('H1', 'High1'), ('H2', 'High2')], default=None, max_length=3, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('html_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('FR', 'Free'), ('NO', 'Notice'), ('KQ', 'Korean Question'), ('EQ', 'Eng Question'), ('MQ', 'Math Question'), ('KD', 'Korean Data'), ('ED', 'Eng Data'), ('MD', 'Math Data')], default='FR', max_length=2)),
            ],
        ),
    ]
