from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from djangocms_blog.models import BasePostPlugin, BlogCategory, LatestPostsPlugin, Post
from djangocms_blog.settings import get_setting
from taggit_autosuggest.managers import TaggableManager

from .utils import upcoming_events_query


class PostExtension(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="extension")
    event_start_date = models.DateTimeField(verbose_name=_("Event start"))
    event_end_date = models.DateTimeField(
        verbose_name=_("Event end"),
        null=True,
        blank=True,
        help_text=_("If the event is held over several days"),
    )

    class Meta:
        verbose_name = _("Event infos")
        verbose_name_plural = _("Events infos")

    def __str__(self):
        return _("Event infos") + " (#" + str(self.id) + ")"


class UpcomingEventsPlugin(BasePostPlugin):
    """Django-CMS forbids the inheritance of other classes than:
    - CMSPlugin
    - abstract classes inheriting from CMSPlugin
    So we must redefine here all fields form class djangocms_blog.LatestPostsPlugin.
    """

    latest_posts = models.IntegerField(
        _("articles"),
        default=get_setting("LATEST_POSTS"),
        help_text=_("The number of latests " "articles to be displayed."),
    )
    show_until_event_end = models.BooleanField(
        verbose_name=_("Show events until their end date"), default=True
    )
    tags = TaggableManager(
        _("filter by tag"),
        blank=True,
        help_text=_("Show only the blog articles tagged with chosen tags."),
        related_name="djangocms_blog_agenda_upcoming_events",
    )
    categories = models.ManyToManyField(
        "djangocms_blog.BlogCategory",
        blank=True,
        verbose_name=_("filter by category"),
        help_text=_("Show only the blog articles tagged " "with chosen categories."),
    )

    def copy_relations(self, oldinstance):
        for tag in oldinstance.tags.all():
            self.tags.add(tag)
        for category in oldinstance.categories.all():
            self.categories.add(category)

    def get_posts(self, request, published_only=True):
        posts = self.post_queryset(request, published_only)
        if self.tags.exists():
            posts = posts.filter(tags__in=list(self.tags.all()))
        if self.categories.exists():
            posts = posts.filter(categories__in=list(self.categories.all()))
        return self.optimize(posts.distinct())[: self.latest_posts]

    def __str__(self):
        return _("{} upcoming events").format(self.latest_posts)

    class Meta:
        verbose_name = _("Upcoming events plugin")
        verbose_name_plural = _("Upcoming events plugins")


class PastEventsPlugin(LatestPostsPlugin):
    def __str__(self):
        return _("{} past events").format(self.latest_posts)

    class Meta:
        proxy = True
        verbose_name = _("Past events plugin")
        verbose_name_plural = _("Past events plugins")


class AgendaBlogCategory(BlogCategory):
    class Meta:
        proxy = True

    @cached_property
    def count(self):
        return self.linked_posts.filter(upcoming_events_query).published().count()
