# Generated by Django 2.1.4 on 2018-12-16 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('color_id', models.AutoField(primary_key=True, serialize=False)),
                ('color_name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Movie Color',
                'verbose_name_plural': 'Movie Colors',
                'db_table': 'color',
                'ordering': ['color_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContentRating',
            fields=[
                ('content_rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_rating', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Movie ContentRating',
                'verbose_name_plural': 'Movie ContentRatings',
                'db_table': 'content_rating',
                'ordering': ['content_rating'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CountryArea',
            fields=[
                ('country_area_id', models.AutoField(primary_key=True, serialize=False)),
                ('country_area_name', models.CharField(max_length=100, unique=True)),
                ('m49_code', models.SmallIntegerField()),
                ('iso_alpha3_code', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'UNSD M49 Country or Area',
                'verbose_name_plural': 'UNSD M49 Countries or Areas',
                'db_table': 'country_area',
                'ordering': ['country_area_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DevStatus',
            fields=[
                ('dev_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('dev_status_name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name': 'UNSD M49 Country or Area Development Status',
                'verbose_name_plural': 'UNSD M49 Country or Area Development Statuses',
                'db_table': 'dev_status',
                'ordering': ['dev_status_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('director_id', models.AutoField(primary_key=True, serialize=False)),
                ('director_name', models.CharField(max_length=225, unique=True)),
            ],
            options={
                'verbose_name': 'Movie director_name',
                'verbose_name_plural': 'Movie director_names',
                'db_table': 'director',
                'ordering': ['director_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Movie genre',
                'verbose_name_plural': 'Movie genres',
                'db_table': 'genre',
                'ordering': ['genre'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('movie_title', models.CharField(max_length=225, unique=True)),
                ('title_year', models.IntegerField()),
                ('imdb_score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('duration', models.IntegerField()),
                ('movie_imdb_link', models.TextField()),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movies',
                'db_table': 'movie',
                'ordering': ['movie_title'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieGenres',
            fields=[
                ('movie_genres_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'MovieGenre',
                'verbose_name_plural': 'MovieGenres',
                'db_table': 'movie_genres',
                'ordering': ['movie', 'genre'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieKeywords',
            fields=[
                ('movie_keywords_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'MovieKeyword',
                'verbose_name_plural': 'MovieKeywords',
                'db_table': 'movie_keywords',
                'ordering': ['movie', 'keyword'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieLanguage',
            fields=[
                ('language_id', models.AutoField(primary_key=True, serialize=False)),
                ('language_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Language Name',
                'verbose_name_plural': 'Language Names',
                'db_table': 'movie_language',
                'ordering': ['language_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlotKeyword',
            fields=[
                ('keyword_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=225, unique=True)),
            ],
            options={
                'verbose_name': 'Movie keyword',
                'verbose_name_plural': 'Movie keywords',
                'db_table': 'plot_keyword',
                'ordering': ['keyword'],
                'managed': False,
            },
        ),
    ]