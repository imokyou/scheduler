# coding=utf8
from django.db import models


class Schedule(models.Model):
    stype = models.CharField(max_length=16)
    subject = models.CharField(max_length=512)
    sdate = models.DateTimeField()
    targets = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedule'


class ScheduleConfig(models.Model):
    schedule = models.ForeignKey(Schedule)
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schedule_config'


class CodeMemo(models.Model):
    ctype = models.CharField(max_length=16)
    description = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'code_memo'
