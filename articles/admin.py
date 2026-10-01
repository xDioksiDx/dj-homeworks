from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        scopes_count = 0
        main_count = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            cleaned = form.cleaned_data

            if cleaned.get("DELETE"):
                continue

            tag = cleaned.get("tag")
            if not tag:
                continue

            scopes_count += 1
            if cleaned.get("is_main"):
                main_count += 1

        if scopes_count == 0:
            raise ValidationError("У статьи должен быть указан хотя бы один раздел.")

        if main_count != 1:
            raise ValidationError("Должен быть выбран один и только один основной раздел.")


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ("title", "published_at")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)