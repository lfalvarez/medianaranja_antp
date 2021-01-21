# Generated by Django 3.0.11 on 2021-01-12 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dj_proposals_candidates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidatura',
            fields=[
                ('candidate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dj_proposals_candidates.Candidate')),
                ('position_in_array', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('dj_proposals_candidates.candidate',),
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('territory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dj_proposals_candidates.Territory')),
                ('matriz', models.BinaryField(blank=True, default=(('1', '0', '1'), ('1', '0', '1')), null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('dj_proposals_candidates.territory',),
        ),
        migrations.CreateModel(
            name='Propuesta',
            fields=[
                ('proposal_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dj_proposals_candidates.Proposal')),
                ('position_in_array', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('dj_proposals_candidates.proposal',),
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comunas', to='mn_juego.Distrito')),
            ],
        ),
    ]
