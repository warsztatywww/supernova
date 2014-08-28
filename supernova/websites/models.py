from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255)
    pagerank = models.FloatField()
    def __str__ (self):
        return "<Domain {} with pagerank {}>".format(self.name, self.pagerank)


class Webpage(models.Model):
    domain = models.ForeignKey(Domain)
    path = models.CharField(max_length=4095)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1023)
    keywords = models.CharField(max_length=1023)
    content = models.TextField()
    def __str__ (self):
        return "<Webpage {} with title {} on domain {}>".format(self.path, self.title, self.domain.name)


class Link(models.Model):
    start = models.ForeignKey(Webpage, related_name='link_start')
    end = models.ForeignKey(Webpage, related_name='link_end')
    def __str__ (self):
        return "<Link from {} to {}>".format(self.start.webpage, self.end.webpage)
