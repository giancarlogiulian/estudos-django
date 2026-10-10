from django.db import models


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.titulo
