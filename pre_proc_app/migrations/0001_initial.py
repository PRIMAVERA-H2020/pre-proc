# Generated by Django 2.1.2 on 2018-11-02 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClimateModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Climate Model',
            },
        ),
        migrations.CreateModel(
            name='DataRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_label', models.CharField(blank=True, max_length=20, null=True, verbose_name='Variant Label')),
                ('table_id', models.CharField(max_length=50, verbose_name='Table name')),
                ('cmor_name', models.CharField(max_length=50, verbose_name='CMOR variable name')),
            ],
            options={
                'verbose_name': 'Data Request',
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Experiment',
            },
        ),
        migrations.CreateModel(
            name='FileFix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'File Fix',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Institution',
            },
        ),
        migrations.AddField(
            model_name='datarequest',
            name='experiment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pre_proc_app.Experiment', verbose_name='Experiment'),
        ),
        migrations.AddField(
            model_name='datarequest',
            name='fixes',
            field=models.ManyToManyField(to='pre_proc_app.FileFix'),
        ),
        migrations.AddField(
            model_name='datarequest',
            name='institution_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pre_proc_app.Institution', verbose_name='Institution'),
        ),
        migrations.AddField(
            model_name='datarequest',
            name='source_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pre_proc_app.ClimateModel', verbose_name='Climate Model'),
        ),
        migrations.AlterUniqueTogether(
            name='datarequest',
            unique_together={('institution_id', 'source_id', 'experiment_id', 'variant_label', 'table_id', 'cmor_name')},
        ),
    ]
