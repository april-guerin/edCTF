from django.db import models
from django.contrib.auth.models import User
from edctf.api.validators import *
from datetime import datetime
import time


class ctf(models.Model):
  """
  Ctf model class.
  """
  name = models.CharField(max_length=250, unique=True, validators=[validate_no_xss, validate_no_html, validate_ctf_iexact])
  live = models.BooleanField(default=False)
  challengeboard = models.ManyToManyField('challengeboard', related_name='ctfs', related_query_name='ctf')
  scoreboard = models.ManyToManyField('scoreboard', related_name='ctfs', related_query_name='ctf')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'ctfs'

  def __unicode__(self):
    return '{}'.format(self.name)


class challengeboard(models.Model):
  """
  Challengeboard model class.
  """
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'challengeboard'

  def __unicode__(self):
    return '{}'.format(self.id)


class category(models.Model):
  """
  Category model class.
  """
  name = models.CharField(max_length=50, unique=True, validators=[validate_no_xss, validate_no_html, validate_category_iexact])
  challengeboard = models.ForeignKey('challengeboard', related_name='categories', related_query_name='category')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'categories'

  def __unicode__(self):
    return '{}'.format(self.name)


class challenge(models.Model):
  """
  Challenge model class.
  """
  category = models.ForeignKey('category', related_name='challenges', related_query_name='challenge')
  title = models.CharField(max_length=200, validators=[validate_no_xss, validate_no_html])
  points = models.IntegerField(default=0, validators=[validate_positive])
  description = models.CharField(max_length=10000, validators=[validate_no_xss, validate_tags, validate_attributes])
  flag = models.CharField(max_length=100)
  created = models.DateTimeField(auto_now_add=True)

  def _get_number_solved(self):
    """
    Returns number of solved challenges.
    """
    return self.challenge_timestamps.count()
  numsolved = property(_get_number_solved)

  class Meta:
    verbose_name_plural = 'challenges'

  def __unicode__(self):
    return '{} {}'.format(self.title, self.points)


class scoreboard(models.Model):
  """
  Scoreboard model class.
  """
  numtopteams = models.IntegerField(default=10)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'scoreboards'

  def __unicode__(self):
    return '{}'.format(self.id)


class team(models.Model):
  """
  Team model class.
  """
  scoreboard = models.ForeignKey('scoreboard', related_name='teams', related_query_name='team')
  teamname = models.CharField(max_length=60, unique=True, validators=[validate_no_xss, validate_no_html, validate_team_iexact])
  points = models.IntegerField(default=0, validators=[validate_positive])
  correctflags = models.IntegerField(default=0, validators=[validate_positive])
  wrongflags = models.IntegerField(default=0, validators=[validate_positive])
  user = models.OneToOneField(User, related_name='teams', related_query_name='team')
  solved = models.ManyToManyField('challenge', blank=True, related_name='solved', through='challenge_timestamp')
  last_timestamp = models.DateTimeField(default=datetime.fromtimestamp(0))
  created = models.DateTimeField(auto_now_add=True)
    
  class Meta:
    verbose_name_plural = 'teams'
    
  def __unicode__(self):
    return 'team {}: {}'.format(self.id, self.teamname)

  def solves(self):
    challenge_timestamps = []
    team_challenge_timestamps = self.challenge_timestamps.all()
    for timestamp in team_challenge_timestamps:
      _time = int(time.mktime(timestamp.created.timetuple()))
      _id = timestamp.challenge.id
      challenge_timestamps.append((_id, _time))
    return challenge_timestamps

  def lasttimestamp(self):
    return int(self.last_timestamp.strftime('%s'))

  def team(self):
    """
    Alias for teamname.
    Created for ctftime api.
    """
    return self.teamname

  def score(self):
    """
    Alias for points.
    Created for ctftime api.
    """
    return self.points


class challenge_timestamp(models.Model):
  """
  Challenge timestamp model class.
  """
  team = models.ForeignKey('team', related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  challenge = models.ForeignKey('challenge', related_name='challenge_timestamps', related_query_name='challenge_timestamp')
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural = 'challenge_timestamps'

  def __unicode__(self):
    return 'timestamp {}: {}'.format(self.id, self.created)
