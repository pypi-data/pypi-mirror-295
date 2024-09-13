from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import (
    Page,
    Orderable,
)
from wagtail.fields import (
    RichTextField,
)
from wagtail.contrib.routable_page.models import (
    RoutablePageMixin, path,
)
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    TitleFieldPanel,
)
from wagtail.admin.widgets.slug import SlugInput
from modelcluster.fields import ParentalKey
from datetime import datetime

from .settings import (
    PLACES_EXTEND_TEMPLATE,
    google_api_key,
)
from .util import (
    matcher,
)

# Create your models here.
class Place(Orderable):
    page = ParentalKey("places.PlacesPage", related_name="places", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text=_("What's the name of this place? I.E. 'New York City', 'Amsterdam'"))
    slug = models.SlugField(max_length=255, help_text=_("Slug of the place"), blank=False, null=False)
    place_id = models.CharField(max_length=255, help_text=_("(Optional) Google Place ID"), blank=True, null=True)
    address = models.CharField(max_length=255, help_text=_("Full address of the place"), blank=True, null=True)
    description = RichTextField(help_text=_("Description of the place"), blank=True, null=True, features=[
        "bold",
        "italic",
        "link",
        "ol",
        "ul",
        "hr",
        "ai",
        "document-link",
        "image",
        "embed",
    ])

    panels = [
        TitleFieldPanel("name", targets=["slug"]),
        FieldPanel("slug", widget=SlugInput),
        FieldRowPanel([
            FieldPanel("place_id"),
            FieldPanel("address"),
        ]),
        FieldPanel("description"),
    ]

    def clean(self):
        super().clean()

        if not self.place_id and not self.address:
            raise ValidationError(_("You must provide either a Place ID or an address"))
        
        if not self.slug:
            self.slug = slugify(self.name)

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        ordering = ["sort_order"]

class PlacesPage(RoutablePageMixin, Page):
    template = "places/places_page.html"
    detail_template = "places/places_detail.html"

    places: models.QuerySet[Place]

    sidebar_title = models.CharField(
        max_length=255,
        help_text=_("Title of the sidebar"),
        blank=True,
        null=True,
    )

    no_place_message = RichTextField(
        help_text=_("Message to display when no place is selected"),
        blank=True,
        null=True,
        features=[
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "ai",
            "document-link",
            "image",
            "embed",
        ],
    )

    description = RichTextField(
        help_text=_("Description of the places"),
        blank=True,
        null=True,
        features=[
            "h2", "h3", "h4", "h5", "h6",
            "bold", "italic", "link", "ol",
            "ul", "hr", "ai",
            "document-link", "image", "embed",
        ],
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("no_place_message"),
        TitleFieldPanel("sidebar_title", targets=[], placeholder=_("Sidebar Title")),
        InlinePanel("places", heading=_("Sidebar Places"), label=_("Place")),
    ]

    class Meta:
        verbose_name = _("Places Page")
        verbose_name_plural = _("Places Pages")

    def get_context(self, request, *args, **kwargs):
        return super().get_context(request, *args, **kwargs) | {
            "EXTEND_TEMPLATE": PLACES_EXTEND_TEMPLATE,
            "places": self.places.all(),
        }

    @path("places/<slug:slug>/", name="places_detail")
    def places_detail(self, request, slug):
        place = get_object_or_404(
            self.places, slug=slug,
        )

        context = {
            "place": place,
            "google_maps_api_key": google_api_key(
                request,
            ),
        }

        if hasattr(request, "is_htmx") and request.is_htmx or\
                request.headers.get("HX-Request") == "true":
            
            # Render the detail (htmx partial) template.
            return self.render(
                request,
                context_overrides=context,
                template=self.detail_template,
            )

        # Render the full page template.
        # 
        # This is necessary to render the full page template when the user
        # navigates to the page directly
        return self.render(
            request,
            context_overrides=context
        )

    # Calculate the change frequency of the page.
    # 
    # This is useful for sitemaps.
    def calc_changefreq(self, page: "PlacesPage"):
        freq = getattr(page, "change_frequency", None)
        if freq:
            return freq

        freqlist: list[datetime] = list(page.revisions.values_list("created_at", flat=True))
        if not freqlist:
            return "monthly"
        
        if len(freqlist) == 1:
            return "monthly"
        
        freqlist.sort()
        freqlist.reverse()
        delta = freqlist[0] - freqlist[-1]

        return str(matcher(delta.days, lambda days, cmp: days < cmp, (
                (1, "daily"),
                (7, "weekly"),
                (30, "monthly"),
                (365, "yearly"),
            ), default="monthly"))

    # Get the sitemap urls for the page.
    # 
    # This tells Wagtail what urls to include in the sitemap.
    def get_sitemap_urls(self, request = None, priority_mul = 1.0, get_translations = True):
        urls = []

        full_url = self.get_full_url(request=request)

        change_freq = self.calc_changefreq(self)

        urls.append({
            "location": full_url,
            "changefreq": change_freq,
            "lastmod": self.latest_revision_created_at,
            "priority": f"{priority_mul:.1f}",
        })

        places = self.places.all()
        for place in places:
            urls.append({
                "changefreq": change_freq,
                "location": f"{full_url}places/{place.slug}/",
                "priority": f"{(0.8 * priority_mul):.1f}",
            })

        if get_translations:
            for page in self.get_translations(inclusive=False):
                page: "PlacesPage"

                translated_sitemap_urls = page.get_sitemap_urls(
                    request=request,
                    priority_mul=0.8,
                    get_translations=False,
                )

                urls.extend(
                    translated_sitemap_urls,
                )

        return urls

