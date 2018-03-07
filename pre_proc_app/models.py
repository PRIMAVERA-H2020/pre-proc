# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class FileFix(models.Model):
    """
    The FileFix objects that can be applied to files that make up data
    requests.
    """
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'File Fix'


class Institution(models.Model):
    """
    An institution (institution_id in CMIP6 terminology)
    """
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Institution'


class ClimateModel(models.Model):
    """
    A climate model (source_id in CMIP6 terminology)
    """
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Climate Model'


class Experiment(models.Model):
    """
    An experiment (experiment_id in CMIP6 terminology)
    """
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Experiment'


class DataRequest(models.Model):
    """
    A data request that matches a variable and table with a model and
    experiment.
    """
    institution_id = models.ForeignKey(Institution, null=False,
                                       verbose_name='Institution',
                                       on_delete=models.CASCADE)
    source_id = models.ForeignKey(ClimateModel, null=False,
                                  verbose_name='Climate Model',
                                  on_delete=models.CASCADE)
    experiment_id = models.ForeignKey(Experiment, null=False,
                                      verbose_name='Experiment',
                                      on_delete=models.CASCADE)

    table_id = models.CharField(max_length=50, null=False, blank=False,
                                verbose_name='CMOR variable name')
    cmor_name = models.CharField(max_length=50, null=False, blank=False,
                                 verbose_name='CMOR variable name')

    fixes = models.ManyToManyField(FileFix)

    def __unicode__(self):
        return u'{}/{} {}/{}'.format(self.source_id, self.experiment_id,
                                     self.table_id, self.cmor_name)

    class Meta:
        verbose_name = 'Data Request'
        unique_together = ('institution_id', 'source_id', 'experiment_id',
                           'table_id', 'cmor_name')
