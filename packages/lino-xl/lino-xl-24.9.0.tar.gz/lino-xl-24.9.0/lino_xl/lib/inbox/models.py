# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import re
from pathlib import Path
import mailbox
import email.errors
import mimetypes
from email.utils import getaddresses, parsedate_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils.module_loading import import_string
from django.conf import settings

from lino.api import dd, rt
from lino import logger
from lino.utils import DATE_TO_DIR_TPL

allowed_chars = "_-+."
def sanitize(filename):
    # Quite similar to lino.modlib.uploads.mixins.safe_filename()  (TODO: unite
    # them.)
    filename = filename.replace(" ", "_")
    filename = "".join(c for c in filename if c.isalpha() or c.isdigit() or c in allowed_chars).strip()
    return filename

upload_area = dd.get_plugin_setting('inbox', 'upload_area', None)

# We search for a pattern #nnnn[:abc] where #nnnn is assumed to be a ticket
# number (more prcisely plugins.memo.parser.suggesters)

# TOPIC_PATTERN = re.compile(r"#(\w+)")


def process_message(key, msg):
    user = None
    for real_name, email in getaddresses(msg.get_all("from", [])):
        try:
            user = rt.models.users.User.objects.get(email=email)
            logger.info("[%s] Process message from user %s", key, user)
            break
        except ObjectDoesNotExist as e:
            pass
    if user is None:
        logger.info("[%s] Ignore unknown sender %s", key, msg.get("from"))
        return
    date = parsedate_to_datetime(msg.get("date"))
    comment_kwargs = dict(user=user, created=date)

    to_parts = msg.get("to").split("@")
    if len(to_parts) != 2:
        logger.info("[%s] Invalid header To: %s", key, msg.get("to"))
        return
    sub_parts = to_parts[0].split(dd.plugins.inbox.subaddress_separator)
    Comment = rt.models.comments.Comment
    if len(sub_parts) == 1:
        pass
    elif len(sub_parts) == 2:
        to, reply_to = sub_parts
        # print("20240902", sub_parts)
        if not reply_to.isnumeric():
            logger.info("[%s] Invalid reply_to %s", key, reply_to)
            return
        else:
            try:
                comment_kwargs.update(reply_to=Comment.objects.get(pk=reply_to))
            except Comment.DoesNotExist:
                logger.info("[%s] Invalid reply_to %s", key, reply_to)
                return
    elif len(sub_parts) == 3:
        # print("20240902", sub_parts)
        to, ct, pk = sub_parts  # content type, primary key
        try:
            ct = rt.models.contenttypes.ContentType.objects.get_for_id(ct)
            owner = ct.model_class().objects.get(pk=pk)
            comment_kwargs.update(owner=owner)
        except ObjectDoesNotExist as e:
            logger.info("[%s] Invalid ct or pk in %s", key, msg.get("to"))
            return
    else:
        logger.info("[%s] Invalid header To: %s", key, msg.get("to"))
        return

    # m = re.search(TOPIC_PATTERN, subject)
    # if m is not None:
    #     getter = dd.plugins.memo.parser.suggesters['#'].getter
    #     topic = getter(m.groups(1))
    #     logger.info("[%s] Found topic %s in subject %s", key, topic, subject)
    # else:
    #     logger.info("[%s] No topic in subject %s", key, subject)

    upload_volume = dd.plugins.inbox.get_upload_volume()
    if upload_volume is not None:
        inbox_root = Path(upload_volume.root_dir)
        upload_dir = Path(date.strftime(DATE_TO_DIR_TPL)) / key

    subject = msg.get("subject")
    counter = 0
    text_body = None
    html_body = None
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        payload = part.get_payload(decode=True)
        if not payload:
            continue
        filename = part.get_filename()
        if filename:
            if upload_area is None or upload_volume is None:
                continue
            counter += 1
            upload_options = dict(user=user, description=subject)
            upload_options.update(upload_area=upload_area)
            # filename = key + "." + filename
            filename = sanitize(filename)
            filename = upload_dir / filename
            upload_options.update(library_file=filename, volume=upload_volume)
            # if filename.exists():
            #     logger.warning("Overwriting existing %s", filename)
            filename = inbox_root / filename
            logger.info("Write file %s.", filename)
            filename.parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'wb') as fp:
                fp.write(payload)
                # upload_options.update(file=File(fp))
            obj = rt.models.uploads.Upload(**upload_options)
            obj.full_clean()
            obj.save()
        else:
            ct = part.get_content_type()
            # logger.info("[%s] %s part without filename", key, ct)
            if ct == "text/html":
                if html_body is None:
                    html_body = payload
                else:
                    logger.warning("Multiple %s parts without filename!", ct)
            elif ct == "text/plain":
                if text_body is None:
                    text_body = payload
                else:
                    logger.warning("Multiple %s parts without filename!", ct)
            else:
                logger.warning("Ignored %s part without filename!", ct)
        #     ext = mimetypes.guess_extension(part.get_content_type())
        #     if ext:
        #         filename = f'{key}-{counter:03d}{ext}'
    if html_body is None:
        body = text_body
    else:
        body = html_body

    if body:
        comment_kwargs.update(body=body)
        obj = rt.models.comments.Comment(**comment_kwargs)
        obj.full_clean()
        obj.save()



def process_inbox(ar, discard=False):
    if dd.plugins.inbox.mailbox_path is None:
        return
    logger.info("Process inbox %s ...", dd.plugins.inbox.mailbox_path)
    mailbox_type = import_string(dd.plugins.inbox.mailbox_type)
    inbox = mailbox_type(dd.plugins.inbox.mailbox_path)
    try:
        inbox.lock()
    except mailbox.ExternalClashError as e:
        return
    for key, msg in inbox.iteritems():
        process_message(key, msg)
        if discard:
            inbox.discard(key)
            inbox.flush()
    inbox.unlock()


@dd.schedule_often(300)
def read_inbox(ar):
    process_inbox(ar)
