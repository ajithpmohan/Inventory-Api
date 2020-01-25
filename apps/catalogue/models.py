from __future__ import unicode_literals

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.utils import helpers


class Category(models.Model):
    """
    A particular group of related products
    """
    name = models.CharField(_('Name'), unique=True, max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True, editable=True)

    class Meta:
        app_label = 'catalogue'
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product Catalogue
    """
    name = models.CharField(_('Name'), max_length=128, db_index=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    category = models.ForeignKey(
        'catalogue.Category', _('Category'), related_name='%(class)ss', related_query_name='product',
        help_text=_('A particular group of related products')
    )
    image = models.ImageField(
        _('Image'), upload_to=helpers.default_content_path, blank=True, null=True, max_length=255
    )
    description = models.TextField()

    class Meta:
        app_label = 'catalogue'
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("products:product-detail", kwargs={"slug": self.slug})


class ProductStock(models.Model):
    product = models.OneToOneField(
        'catalogue.Product', _('Product'), related_name='stock', related_query_name='stock',
    )
    qty = models.PositiveSmallIntegerField(_('Stock Quantity'))  # Values from 0 to 32767
    limit = models.PositiveSmallIntegerField(
        _('Stock Limit'), validators=[MinValueValidator(1)],
        help_text=_('Admin get notification when stock quantity value is less than stock limit value.')
    )

    class Meta:
        app_label = 'catalogue'
        ordering = ['product__name']
        verbose_name = _('ProductStock')
        verbose_name_plural = _('ProductStocks')

    def __str__(self):
        return '%s - %d qty' % (self.product.name, self.qty)


class RequestItem(models.Model):
    """
    Requested Product Catalogue
    """

    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    product = models.ForeignKey(
        'catalogue.Product', related_name='%(class)ss', related_query_name='request_item', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'auth.User', _('Requested By'), related_name='%(class)ss', related_query_name='request_item',
        help_text=_('The user who requested the product.')
    )
    qty = models.PositiveSmallIntegerField(_('Stock Needed'), validators=[MinValueValidator(1)])
    timestamp = models.DateTimeField(_('Date Created'), auto_now_add=True)
    status = models.CharField(_('Status'), max_length=1, default=PENDING, choices=STATUS_CHOICES)
    summary = models.TextField(blank=True)

    class Meta:
        app_label = 'catalogue'
        ordering = ['-timestamp']
        verbose_name = _('RequestItem')
        verbose_name_plural = _('RequestItems')

    def __str__(self):
        return '%s requested %d quantity of %s' % (self.user.username, self.qty, self.product.name)


class IssueItem(models.Model):
    """
    Issued Product Catalogue
    """
    requested_item = models.OneToOneField(
        'catalogue.RequestItem', related_name='%(class)ss', related_query_name='issue_item', on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'catalogue.Product', related_name='%(class)ss', related_query_name='issue_item', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'auth.User', _('Issued To'), related_name='%(class)ss', related_query_name='issue_item',
        help_text=_('The user in which product is issued.')
    )
    qty = models.PositiveSmallIntegerField(_('Stock'), validators=[MinValueValidator(1)])
    timestamp = models.DateTimeField(_('Date Created'), auto_now_add=True)
    summary = models.TextField(blank=True)

    class Meta:
        app_label = 'catalogue'
        ordering = ['-timestamp']
        verbose_name = _('IssuedItem')
        verbose_name_plural = _('IssuedItems')

    def __str__(self):
        return '%s of %d qty is issued to %s' % (self.product.name, self.qty, self.user.username)
