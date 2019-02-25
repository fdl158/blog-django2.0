from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from pure_paginatiSon import Paginator
from django.utils.http import unquote
from . import models
from . import forms
import json


class IndexView(View):
    def get(self, request):
        title = '博客首页'
        user = models.WebOwner.objects.all()[0]
        nav = models.WebNavSet.objects.all().order_by('nav_sort')[:7]
        article = models.ArticlesMake.objects.all()
        banner = article.filter(is_banner=True).order_by('-is_recommend', '-like_num',
                                                         '-read_num', '-article_make_time')[:4]
        headline = article.filter(is_close_banner=True).order_by('-is_recommend', '-like_num',
                                                                 '-read_num', '-article_make_time')[:2]
        article_type = models.ArticleType.objects.all()[:8]
        article_type_articles = {}
        for index, item in enumerate(article_type):
            article_type_articles[index] = {
                'articles': item.MainCoreApp_ArticlesMake_related.order_by('-like_num',
                                                                           '-read_num', '-article_make_time')[:5],
                'recommends': item.MainCoreApp_ArticlesMake_related.filter(is_article_type_top=True).order_by(
                    '-like_num', '-read_num', '-article_make_time')[:2]
            }
        article_tag = models.ArticleTag.objects.all()
        article_tags = []
        for item in article_tag:
            tmp = 0
            for i in item.MainCoreApp_ArticlesMake_related.all():
                tmp += i.read_num
            article_tags.append({
                'tag': item,
                'num': tmp
            })
        article_tags = article_tags[:6]
        new_articles = article.order_by('-is_top', '-article_make_time')
        notice = article.filter(is_notice=True)[:4]
        read_list = article.order_by('-read_num')[:6]
        recommend = article.filter(is_recommend=True).order_by('-like_num', '-read_num')[:6]
        fp_lnk = models.FriendshipLink.objects.all()
        adv = models.AddAdvertisement.objects.all()
        left_adv = adv.filter(position='left')
        right_adv = adv.filter(position='right')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        pure = Paginator(new_articles, 10, request=request)
        new = pure.page(page)
        return render(request, 'index.html', locals())


class ArticleView(View):

    def get(self, request, typeof, pid=''):
        if pid:
            # 获取文章
            typeof = unquote(typeof)
            article_list = models.ArticleType.objects.filter(type_name=typeof)[0].MainCoreApp_ArticlesMake_related.all()
            if article_list:
                pid = title = unquote(pid)
                article = models.ArticlesMake.objects.filter(title=pid)[0]
                user = models.WebOwner.objects.all()[0]
                nav = models.WebNavSet.objects.all()[:7]
                read_list = models.ArticlesMake.objects.order_by('-read_num')[:6]
                recommend = article_list.filter(is_recommend=True).all().order_by('-like_num', '-read_num')[:5]
                # 上下篇
                try:
                    up_page = article_list.get(id=article.id - 1)
                except:
                    up_page = False
                try:
                    down_page = article_list.get(id=article.id + 1)
                except:
                    down_page = False
                # 相关文章
                related_article = []
                for item in article.article_tags.all():
                    for i in item.MainCoreApp_ArticlesMake_related.all():
                        if (i not in related_article) and i != article:
                            related_article.append(i)
                related_article = related_article[:6]
                comment = forms.ArticleCommentForm()
                try:
                    comment_all = article.MainCoreApp_ArticleCommend_relateds.all()
                except:
                    comment_all = False
                article_tag = models.ArticleTag.objects.all()
                comments = models.ArticleComment.objects.all()
                adv = models.AddAdvertisement.objects.all()
                left_adv = adv.filter(position='left')
                right_adv = adv.filter(position='right')
                if article:
                    if str(article.id) not in request.COOKIES:
                        article.read_num += 1
                        article.save()
                    response = render(request, 'info.html', locals())
                    if str(article.id) not in request.COOKIES:
                        response.set_cookie(str(article.id), str(article.id), max_age=60*60*24)
                    return response
        else:
            # 文章列表
            title = typeof = unquote(typeof)
            is_search = False
            try:
                article_list = models.ArticleType.objects.filter(type_name=typeof)[0].MainCoreApp_ArticlesMake_related.all().order_by('-is_top', '-article_make_time')
                title = '文章类型： ' + title
            except:
                try:
                    a = models.ArticleTag.objects.filter(tag_name=typeof)
                    article_list = models.ArticleTag.objects.filter(tag_name=typeof)[0].MainCoreApp_ArticlesMake_related.all().order_by('-is_top', '-article_make_time')
                    title = '文章标签： ' + title
                except:
                    title = '搜索： ' + title
                    is_search = True
                    article_list = []
                    article_all = models.ArticlesMake.objects.all()
                    for item in article_all:
                        is_filter = False
                        is_introduction = False
                        temp = {
                            'article_search': item
                        }
                        keyword = '<span style="background-color:yellow">' + typeof + '</span>'
                        if typeof in item.title:
                            item.title = item.title[:item.title.find(typeof)] + keyword + \
                                         item.title[item.title.find(typeof) + len(typeof):]
                            is_filter = True
                        if typeof in item.introduction:
                            item.introduction = item.introduction[:item.introduction.find(typeof)] + keyword + \
                                                item.introduction[item.title.find(typeof) + len(typeof):]
                            is_introduction = True
                            is_filter = True
                        if typeof in item.content:
                            item.content = \
                                item.content[item.content.find(typeof) +
                                             len(typeof):item.content.find(typeof) + len(typeof) + (len(typeof) * 100)]
                            is_filter = True
                        if is_filter:
                            temp['title'] = item.title
                            temp['introduction'] = item.introduction
                            temp['content'] = item.content
                            temp['is_introduction'] = is_introduction
                            temp['keyword'] = keyword
                            article_list.append(temp)
            user = models.WebOwner.objects.all()[0]
            nav = models.WebNavSet.objects.all()
            article_tag = models.ArticleTag.objects.all()
            read_list = models.ArticlesMake.objects.order_by('-read_num')[:6]
            adv = models.AddAdvertisement.objects.all()
            left_adv = adv.filter(position='left')
            right_adv = adv.filter(position='right')
            try:
                recommend = article_list.filter(is_recommend=True).all().order_by('-like_num', '-read_num')[:5]
            except:
                recommend = False
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            pure = Paginator(article_list, 10, request=request)
            new = pure.page(page)
            return render(request, 'list.html', locals())

    def post(self, request, typeof='', pid=''):
        if request.is_ajax():
            if request.method == 'POST':
                comment = forms.ArticleCommentForm(request.POST, request.FILES)
                if comment.is_valid():
                    id = request.POST.get('pid', '')
                    commented = comment.save(commit=False)
                    article = models.ArticlesMake.objects.get(id=id)
                    commented.com_article = article
                    commented.com_photo = comment.data['com_photo'].replace('/media/', '')
                    commented.save()
                    comment_for_this = article.MainCoreApp_ArticleCommend_relateds.all().order_by('com_make_time')
                    comment_all = {}
                    for index, item in enumerate(comment_for_this):
                        comment_all[index] = {
                            'com_username': item.com_username,
                            'com_content': item.com_content,
                            'com_make_time': item.com_make_time.strftime('%Y-%m-%d-%H-%M-%S'),
                            'com_photo': str(item.com_photo),
                            'reply': [item.content for item in item.MainCoreApp_Reply_related.all()]
                        }
                    return HttpResponse(json.dumps(comment_all), content_type='application/json', status=200)
                else:
                    return HttpResponse(json.dumps(comment.errors), content_type='application/json', status=500)


def ThumbUp(request):
    if request.is_ajax():
        if request.method == 'GET':
            id = request.GET.get('id', '')
            article = models.ArticlesMake.objects.get(id=id)
            if article is not None:
                if request.COOKIES.get('0'+str(article.id), False):
                    response = HttpResponse(json.dumps({'mg': '你已经点过赞啦', 'tp': str(article.like_num)}),
                                            content_type='application/json', status=200)
                else:
                    article.like_num += 1
                    article.save()
                    response = HttpResponse(json.dumps({'mg': '点赞成功', 'tp': str(article.like_num)}),
                                            content_type='application/json', status=200)
                    response.set_cookie('0'+str(article.id), str(article.id), max_age=60*60*24)
                return response


class GetSoreUpView(View):
    def patch(self, request, model_name, pk, is_up):
        if request.is_ajax():
            if is_up == 'True':
                exec('tmp=models.' + model_name + '.objects.get(pk=' + str(pk) + ')')
                exec('tmp.nav_sort += 1')
                exec('tmp.save()')
                return HttpResponse(json.dumps({'true': 'true'}), content_type='application/json', status=200)
            else:
                exec('tmp=models.' + model_name + '.objects.get(pk=' + str(pk) + ')')
                exec('tmp.nav_sort -= 1')
                exec('tmp.save()')
                return HttpResponse(json.dumps({'false': 'false'}), content_type='application/json', status=200)


def page404(request):
    return render(request, '404.html', status=404)


def page500(request):
    return render(request, '500.html', status=500)


def page403(request):
    return render(request, '403.html', status=403)