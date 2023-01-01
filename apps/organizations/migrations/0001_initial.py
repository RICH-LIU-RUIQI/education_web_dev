# Generated by Django 2.2 on 2022-12-28 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityDict',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=20, verbose_name='city')),
                ('desc', models.CharField(max_length=200, verbose_name='desp')),
            ],
            options={
                'verbose_name': 'org city',
                'verbose_name_plural': 'org city',
            },
            bases=('users.basemodel',),
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=50, verbose_name='org name')),
                ('desc', models.TextField(verbose_name='description of org')),
                ('tag', models.CharField(default='country known', max_length=10, verbose_name='organization')),
                ('category', models.CharField(choices=[('pxjg', 'organization'), ('gr', 'personal'), ('gx', 'college')], default='pxjg', max_length=20, verbose_name='organization category')),
                ('click_nums', models.IntegerField(default=0, verbose_name='click')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='favor')),
                ('image', models.ImageField(upload_to='org/%Y/%m', verbose_name='logo')),
                ('address', models.CharField(max_length=150, verbose_name='organization address')),
                ('students', models.IntegerField(default=0, verbose_name='people learn')),
                ('course_nums', models.IntegerField(default=0, verbose_name='course number')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.CityDict', verbose_name='city')),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organization',
            },
            bases=('users.basemodel',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.BaseModel')),
                ('name', models.CharField(max_length=50, verbose_name='teacher name')),
                ('work_years', models.IntegerField(default=0, verbose_name='working year')),
                ('work_company', models.CharField(max_length=50, verbose_name='organization name')),
                ('work_position', models.CharField(max_length=50, verbose_name='title in company')),
                ('points', models.CharField(max_length=50, verbose_name='teaching characteristic')),
                ('click_nums', models.IntegerField(default=0, verbose_name='click')),
                ('fav_nums', models.IntegerField(default=0, verbose_name='favor')),
                ('age', models.IntegerField(default=18, verbose_name='age')),
                ('image', models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='profile image')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='organization')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teacher',
            },
            bases=('users.basemodel',),
        ),
    ]