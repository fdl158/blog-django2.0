from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class WebOwner(models.Model):
    photo = models.ImageField(upload_to='WebOwner/image', verbose_name=u"头像", max_length=100,
                              default='default/tx3.jpg', null=True, blank=True)
    name = models.CharField(max_length=10, verbose_name=u"名字", null=False, blank=False, default=u'暂无')
    net_name = models.CharField(max_length=10, verbose_name=u"网名", null=False, blank=False, default=u'暂无')
    major = models.CharField(max_length=20, verbose_name=u"职业", null=False, blank=False, default=u'暂无')
    phone = models.CharField(max_length=18, verbose_name=u"电话", null=False, blank=False, default=u'暂无')
    now_place = models.CharField(max_length=50, verbose_name=u"现居", null=False, blank=False, default=u'暂无')
    email = models.EmailField(verbose_name=u"邮箱", default='xxx@qq.com', null=False, blank=False)
    wx = models.ImageField(upload_to='WebOwner/image', verbose_name=u"微信",
                           max_length=100, default='default/wx.jpg', null=True, blank=True)
    qq = models.CharField(max_length=15, verbose_name=u'QQ号', null=True, blank=True)
    web_name = models.CharField(max_length=15, verbose_name=u'网站名称', null=True, blank=True, default=u'暂无')
    copyright = models.CharField(max_length=100, verbose_name=u'网站版权', null=True, blank=True,
                                 default=u'Copyright © Jason All Rights Reserved.')

    class Meta:
        verbose_name = u"站主信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=10, verbose_name=u"标签名", null=False, blank=False)

    class Meta:
        verbose_name = u"文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class ArticleType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=15, verbose_name=u"类型名称", null=False, blank=False)

    class Meta:
        verbose_name = u"文章类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class WebNavSet(models.Model):
    nav_name = models.CharField(max_length=10, verbose_name=u"导航名", null=False,
                                blank=False, default=u'首页')
    nav_url = models.CharField(verbose_name=u"绑定URL", default='/', max_length=200)
    nav_articles_tag = models.ForeignKey(ArticleTag, on_delete=models.CASCADE, verbose_name=u"绑定文章标签作为URL（绑定后URL字段无效）",
                                         null=True, blank=True, related_name='MainCoreApp_WebNavSet_related')
    nav_articles_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE,
                                          verbose_name=u"绑定文章类型作为URL（绑定后标签和URL字段无效）", null=True, blank=True)
    nav_sort = models.IntegerField(default=1, verbose_name=u"排序(数字越小越左)")

    class Meta:
        verbose_name = u"博客导航栏设置"
        verbose_name_plural = verbose_name

    def get_up(self):
        from django.utils.safestring import mark_safe
        text = "<a href=\"javascript:;\" id=\"getup" + str(self.pk) + "\">上调</a><script>$('#getup" + str(self.pk) + "').click(function(){ $.ajax({url : '/GetSoreUpView/WebNavSet/" + str(self.pk) + "/True/', headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()}, type: 'PATCH', data: '', dataType: false, processData: false, success: function(data){ location.reload(); }})});</script>"
        return mark_safe(text)
    get_up.short_description = '上调'

    def get_down(self):
        from django.utils.safestring import mark_safe
        text = "<a href=\"javascript:;\" id=\"getdown" + str(self.pk) + "\">下调</a><script>$('#getdown" + str(self.pk) + "').click(function(){ $.ajax({url : '/GetSoreUpView/WebNavSet/" + str(self.pk) + "/False/', headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()}, type: 'PATCH', data: '', dataType: false, processData: false, success: function(data){ location.reload(); }})});</script>"
        return mark_safe(text)
    get_down.short_description = '下调'

    def __str__(self):
        return self.nav_name


class WebSubNavSet(models.Model):
    nav_name = models.CharField(max_length=10, verbose_name=u"导航名", null=False,
                                blank=False, default=u'首页')
    nav_url = models.CharField(verbose_name=u"绑定URL", default='/', max_length=200)
    nav_articles_tag = models.ForeignKey(ArticleTag, on_delete=models.CASCADE, verbose_name=u"绑定文章标签作为URL（绑定后URL字段无效）",
                                         null=True, blank=True, related_name='MainCoreApp_WebSubNavSet_related')
    nav_articles_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE,
                                          verbose_name=u"绑定文章类型作为URL（绑定后标签和URL字段无效）", null=True, blank=True)
    nav_up = models.ForeignKey(WebNavSet, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='MainCoreApps_WebSubNavSet_related', verbose_name=u'父级导航')

    class Meta:
        verbose_name = u"博客子导航栏设置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nav_name


class ArticlesMake(models.Model):
    id = models.AutoField(primary_key=True)
    cover = models.ImageField(upload_to='article/images', verbose_name=u"封面", max_length=100,
                              default='default/default.jpg', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name=u"标题", null=False,
                             blank=False, default=u'暂无')
    introduction = models.TextField(max_length=300, verbose_name=u"简介", null=True, blank=True)
    content = RichTextUploadingField(verbose_name=u"内容")
    article_tags = models.ManyToManyField(ArticleTag, verbose_name=u"标签", null=True,
                                          blank=True, related_name='MainCoreApp_ArticlesMake_related')
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE, verbose_name=u"类型",
                                     null=False, blank=False, related_name='MainCoreApp_ArticlesMake_related')
    like_num = models.IntegerField(default=0, verbose_name=u"喜欢数")
    read_num = models.IntegerField(default=0, verbose_name=u"阅读数")
    article_brief_time = models.DateField(auto_now_add=True, verbose_name=u"完成时间(简洁)")
    article_modify_time = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    article_make_time = models.DateTimeField(auto_now_add=True, verbose_name=u"完成时间")
    is_recommend = models.BooleanField(default=False, verbose_name=u"是否推荐")
    is_top = models.BooleanField(default=False, verbose_name=u"是否置顶")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否放置轮播图")
    is_article_type_top = models.BooleanField(default=False, verbose_name=u"是否在文章类型中突出")
    is_close_banner = models.BooleanField(default=False, verbose_name=u"是否放置在轮播图旁边")
    is_notice = models.BooleanField(default=False, verbose_name=u"是否是公告文章")

    class Meta:
        verbose_name = u"编写文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FriendshipLink(models.Model):
    id = models.AutoField(primary_key=True)
    link_name = models.CharField(max_length=25, verbose_name=u"链接名", null=False, blank=False)
    link_url = models.URLField(verbose_name=u"友链")

    class Meta:
        verbose_name = u"友情链接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.link_name


class ArticleComment(models.Model):
    id = models.AutoField(primary_key=True)
    com_username = models.CharField(max_length=30, verbose_name=u"名字", null=False, blank=False)
    com_content = models.TextField(max_length=150, verbose_name=u"评论内容", null=False, blank=False)
    com_article = models.ForeignKey(ArticlesMake, on_delete=models.CASCADE, verbose_name=u"评论的文章", null=False,
                                       blank=False, related_name='MainCoreApp_ArticleCommend_relateds')
    com_make_time = models.DateTimeField(auto_now_add=True)
    com_photo = models.ImageField(upload_to='article/images', verbose_name=u"头像", default='default/tx3.jpg',
                                  max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = u"文章评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.com_username


class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=150, verbose_name=u"回复内容", null=False, blank=False)
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE,
                                verbose_name=u'回复的评论', related_name='MainCoreApp_Reply_related')

    class Meta:
        verbose_name = u"文章回评"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class AddAdvertisement(models.Model):
    id = models.AutoField(primary_key=True)
    content = RichTextUploadingField(verbose_name=u'代码', null=False, blank=False)
    position = models.CharField(max_length=5, verbose_name=u'位置', choices=(
        ('left', u'左边'),
        ('right', u'右边')
    ), null=False, blank=False)

    class Meta:
        verbose_name = u"添加广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content