from django.db import models

# 1) 개발툴
class DevTool(models.Model):
    name = models.CharField('이름', max_length=50)
    kind = models.CharField('종류', max_length=50)
    content = models.TextField('개발툴 설명')

    def __str__(self):
        return self.name


# 2) 아이디어
class Idea(models.Model):
    title = models.CharField('아이디어명', max_length=100)
    image = models.ImageField('이미지', upload_to='idea/', blank=True, null=True)
    content = models.TextField('아이디어 설명')
    interest = models.IntegerField('아이디어 관심도', default=0)
    devtool = models.ForeignKey(
        DevTool,
        on_delete=models.CASCADE,
        related_name='ideas', 
        verbose_name='예상 개발툴'
    )
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title
    
    def is_starred(self):
        return self.stars.exists()


# 3) 찜하기
class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')

    def __str__(self):
        return f"{self.idea.title} 찜"
