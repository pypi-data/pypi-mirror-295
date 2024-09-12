# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from os.path import join, exists
from pathlib import Path
from html import escape

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils.html import format_html
from django.utils.translation import pgettext_lazy as pgettext

from lino.utils.html import E, join_elems
from lino.api import dd, rt, _
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My

# from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator
from lino.modlib.office.roles import OfficeStaff
from lino.mixins import Referrable
from lino.utils.mldbc.mixins import BabelNamed
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.publisher.mixins import Publishable

from .actions import CameraStream
from .choicelists import Shortcuts, UploadAreas
from .mixins import UploadBase

from . import VOLUMES_ROOT


class Volume(Referrable):

    class Meta:
        app_label = "uploads"
        verbose_name = _("Library volume")
        verbose_name_plural = _("Library volumes")

    preferred_foreignkey_width = 5

    root_dir = dd.CharField(_("Root directory"), max_length=255)
    # base_url = dd.CharField(_("Base URL"), max_length=255, blank=True)
    description = dd.CharField(_("Description"), max_length=255, blank=True)

    def __str__(self):
        return self.ref or self.root_dir

    def full_clean(self, *args, **kw):
        # if self.ref == "uploads":
        #     raise ValidationError("Invalid reference for a volume.")
        super().full_clean(*args, **kw)
        pth = Path(dd.plugins.uploads.get_volumes_root(), self.ref)
        if pth.exists():
            if pth.resolve().absolute() != Path(self.root_dir).resolve().absolute():
                raise ValidationError(
                    "Existing %s must resolve to %s", pth, self.root_dir)
        else:
            settings.SITE.makedirs_if_missing(pth.parent)
            pth.symlink_to(self.root_dir)

    def get_filenames(self):
        root_len = len(self.root_dir) + 1
        for root, dirs, files in os.walk(self.root_dir):
            relroot = root[root_len:]
            if relroot:
                relroot += "/"
            for fn in files:
                # print(relroot + "/" + fn)
                yield relroot + fn


class UploadType(BabelNamed):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, "UploadType")
        verbose_name = _("Upload type")
        verbose_name_plural = _("Upload types")

    upload_area = UploadAreas.field(default="general")

    max_number = models.IntegerField(
        _("Max. number"),
        default=-1,
        # help_text=string_concat(
        #     _("No need to upload more uploads than N of this type."),
        #     "\n",
        #     _("-1 means no limit.")))
        help_text=format_lazy(
            "{}\n{}",
            _("No need to upload more uploads than N of this type."),
            _("-1 means no limit."),
        ),
    )
    wanted = models.BooleanField(
        _("Wanted"),
        default=False,
        help_text=_("Add a (+) button when there is no upload of this type."),
    )

    shortcut = Shortcuts.field(blank=True)


class Upload(UploadBase, UserAuthored, Controllable, Publishable):

    class Meta(object):
        abstract = dd.is_abstract_model(__name__, "Upload")
        verbose_name = _("Upload file")
        verbose_name_plural = _("Upload files")

    memo_command = "upload"

    upload_area = UploadAreas.field(default="general")
    type = dd.ForeignKey("uploads.UploadType", blank=True, null=True)
    volume = dd.ForeignKey("uploads.Volume", blank=True, null=True)
    library_file = models.CharField(_("Library file"), max_length=255, blank=True)
    description = models.CharField(_("Description"), max_length=200, blank=True)
    source = dd.ForeignKey("sources.Source", blank=True, null=True)

    camera_stream = CameraStream()

    def __str__(self):
        if self.description:
            s = self.description
        elif self.file:
            s = filename_leaf(self.file.name)
        elif self.library_file:
            s = "{}:{}".format(self.volume.ref, self.library_file)
        else:
            s = str(self.id)
        if self.type:
            s = str(self.type) + " " + s
        return s

    def get_memo_command(self, ar=None):
        if dd.is_installed("memo"):
            cmd = f"[upload {self.pk}"
            if self.description:
                cmd += " " + self.description + "]"
            else:
                cmd += "]"
            return cmd
        return None

    def get_file_url(self):
        if self.file.name:
            return settings.SITE.build_media_url(self.file.name)
        if self.library_file and self.volume_id and self.volume.ref:
            return settings.SITE.build_media_url(
                VOLUMES_ROOT, self.volume.ref, self.library_file)
            # return self.volume.base_url + self.library_file
        return None

    def get_real_file_size(self):
        if self.file:
            return self.file.size
        if self.volume_id and self.library_file:
            pth = os.path.join(
                dd.plugins.uploads.get_volumes_root(),
                self.volume.ref, self.library_file)
            # pth = os.path.join(settings.MEDIA_ROOT, self.volume.ref, self.library_file)
            return os.path.getsize(pth)

    def disabled_fields(self, ar):
        df = super().disabled_fields(ar)
        if ar.renderer.front_end.app_label != "react":
            df.add("camera_stream")
        return df

    @dd.displayfield(_("Description"))
    def description_link(self, ar):
        s = str(self)
        if ar is None:
            return s
        return self.get_file_button(s)

    @dd.chooser(simple_values=True)
    def library_file_choices(self, volume):
        if volume is None:
            return []
        return list(volume.get_filenames())

    @dd.chooser()
    def type_choices(self, upload_area):
        M = dd.resolve_model("uploads.UploadType")
        # logger.info("20140430 type_choices %s", upload_area)
        if upload_area is None:
            return M.objects.all()
        return M.objects.filter(upload_area=upload_area)

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        if self.type is not None:
            self.upload_area = self.type.upload_area

    def get_gallery_item(self, ar):
        d = super().get_gallery_item(ar)
        d.update(title=str(self), id=self.pk)
        cmd = self.get_memo_command(ar)
        if cmd is not None:
            d.update(memo_cmd=cmd)
        return d

    @dd.htmlbox()
    def preview(self, ar):
        url = self.get_file_url()
        if url is None or url.endswith(".pdf"):
            txt = _("No preview available")
            return '<p style="text-align: center;padding: 2em;">({})</p>'.format(txt)
        return '<img src="{}" style="max-width: 100%; max-height: 20em">'.format(url)

    @dd.htmlbox(_("Thumbnail"))
    def thumbnail(self, ar):
        # url = settings.SITE.build_media_url(self.file.name)
        url = self.get_file_url()
        return '<img src="{}" style="height: 15ch; max-width: 22.5ch">'.format(url)

    @dd.htmlbox(_("Thumbnail Medium"))
    def thumbnail_medium(self, ar):
        # url = settings.SITE.build_media_url(self.file.name)
        url = self.get_file_url()
        return '<img src="{}" style="width: 30ch;">'.format(url)

    @dd.htmlbox(_("Thumbnail Large"))
    def thumbnail_large(self, ar):
        # url = settings.SITE.build_media_url(self.file.name)
        url = self.get_file_url()
        return '<img src="{}" style="width: 70ch;">'.format(url)

    def as_page(self, ar, **kwargs):
        yield format_html("<h1>{}</h1>", self)
        url = self.get_file_url()
        yield format_html('<img src="{}" style="width: 100%;">', url)
        if self.description:
            yield escape(self.description)
        if self.source:
            yield _("Source") + ": "
            yield ar.obj2htmls(self.source)

    # def get_choices_text(self, ar, actor, field):
    #     if self.file:
    #         return str(obj) + "&nbsp;<span style=\"float: right;\">" + obj.thumbnail + "</span>"
    #     return str(obj)


dd.update_field(Upload, "user", verbose_name=_("Uploaded by"))


class UploadChecker(Checker):
    verbose_name = _("Check metadata of upload files")
    model = Upload

    def get_checkdata_problems(self, obj, fix=False):
        if obj.file:
            if not exists(join(settings.MEDIA_ROOT, obj.file.name)):
                yield (
                    False,
                    format_lazy(_("Upload entry {} has no file"), obj.file.name),
                )
                return

        file_size = obj.get_real_file_size()

        if obj.file_size != file_size:
            tpl = "Stored file size {} differs from real file size {}"
            yield (False, format_lazy(tpl, obj.file_size, file_size))


UploadChecker.activate()


class UploadsFolderChecker(Checker):
    verbose_name = _("Find orphaned files in uploads folder")

    def get_checkdata_problems(self, obj, fix=False):
        assert obj is None  # this is an unbound checker
        Upload = rt.models.uploads.Upload
        pth = dd.plugins.uploads.get_uploads_root()
        assert str(pth).startswith(settings.MEDIA_ROOT)
        start = len(settings.MEDIA_ROOT) + 1
        for filename in Path(pth).rglob("*"):
            # print(filename)
            if filename.is_dir():
                continue
            rel_filename = str(filename)[start:]
            qs = Upload.objects.filter(file=rel_filename)
            n = qs.count()
            if n == 0:
                msg = format_lazy(_("File {} has no upload entry."), rel_filename)
                # print(msg)
                yield (dd.plugins.uploads.remove_orphaned_files, msg)
                if fix and dd.plugins.uploads.remove_orphaned_files:
                    filename.unlink()
            # else:
            #     print("{} has {} entries.".format(filename, n))
            # elif n > 1:
            #     msg = _("Multiple upload entries for {} ").format(filename)
            #     yield (False, msg)
            #     This is no problem. A same file should be linkable to diffeerent controlers.


UploadsFolderChecker.activate()



@dd.receiver(dd.pre_analyze)
def before_analyze(sender, **kwargs):
    # This is the successor for `quick_upload_buttons`.

    # remember that models might have been overridden.
    UploadType = sender.models.uploads.UploadType
    Shortcuts = sender.models.uploads.Shortcuts

    for i in Shortcuts.items():

        def f(obj, ar):
            if obj is None or ar is None:
                return E.div()
            try:
                utype = UploadType.objects.get(shortcut=i)
            except UploadType.DoesNotExist:
                return E.div()
            items = []
            target = sender.modules.resolve(i.target)
            sar = ar.spawn_request(
                actor=target, master_instance=obj, known_values=dict(type=utype)
            )
            # param_values=dict(pupload_type=et))
            n = sar.get_total_count()
            if n == 0:
                iar = target.insert_action.request_from(sar, master_instance=obj)
                btn = iar.ar2button(
                    None,
                    _("Upload"),
                    icon_name="page_add",
                    title=_("Upload a file from your PC to the server."),
                )
                items.append(btn)
            elif n == 1:
                after_show = ar.get_status()
                obj = sar.data_iterator[0]
                items.append(
                    sar.renderer.href_button(
                        obj.get_file_url(),
                        _("show"),
                        target="_blank",
                        icon_name="page_go",
                        style="vertical-align:-30%;",
                        title=_("Open the uploaded file in a new browser window"),
                    )
                )
                after_show.update(record_id=obj.pk)
                items.append(
                    sar.window_action_button(
                        sar.ah.actor.detail_action,
                        after_show,
                        _("Edit"),
                        icon_name="application_form",
                        title=_("Edit metadata of the uploaded file."),
                    )
                )
            else:
                obj = sar.sliced_data_iterator[0]
                items.append(ar.obj2html(obj, pgettext("uploaded file", "Last")))

                btn = sar.renderer.action_button(
                    obj,
                    sar,
                    sar.bound_action,
                    _("All {0} files").format(n),
                    icon_name=None,
                )
                items.append(btn)

            return E.div(*join_elems(items, ", "))

        vf = dd.VirtualField(dd.DisplayField(i.text), f)
        dd.inject_field(i.model_spec, i.name, vf)
        # logger.info("Installed upload shortcut field %s.%s",
        #             i.model_spec, i.name)

from .ui import *
