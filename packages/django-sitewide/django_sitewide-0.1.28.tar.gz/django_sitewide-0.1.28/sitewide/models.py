from django.db import models

# Create your models here.


class Term(models.Model):
    """Terminology used by a niche Group"""

    niche = models.CharField(max_length=255)
    phrase = models.CharField(max_length=255)
    rephrase = models.CharField(max_length=255)

    def __str__(self):
        """Return the Rephrased version of Phrase as per specified niche"""

        return self.rephrase

    class Meta:
        """Meta for Term"""

        managed = True
        db_table = "term"
        constraints = [
            models.UniqueConstraint(fields=["niche", "phrase"], name="unique_phrase"),
        ]
