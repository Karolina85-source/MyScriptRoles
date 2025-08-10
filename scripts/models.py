from django.db import models
from django.contrib.auth.models import User


class Script(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='scripts/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scripts')

    def __str__(self):
        return self.title


class Character(models.Model):
    name = models.CharField(max_length=100)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='characters')

    def __str__(self):
        return self.name


class Scene(models.Model):
    title = models.CharField(max_length=100)
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='scenes')
    characters = models.ManyToManyField(Character, related_name='scenes', blank=True)

    def __str__(self):
        return f"{self.title} ({self.script.title})"


class SceneContent(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='lines')
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='lines')
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.character.name} ({self.scene.title}) [{self.order}]: {self.text[:30]}"


class CharacterStat(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='stat')
    lines_count = models.PositiveIntegerField(default=0)
    scenes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Statystyki dla: {self.character.name}"


class Overlay(models.Model):
    name = models.CharField(max_length=100)
    contents = models.ManyToManyField(SceneContent, related_name='overlays', blank=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

