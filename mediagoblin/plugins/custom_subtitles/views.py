# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import six

from datetime import datetime

from itsdangerous import BadSignature
from werkzeug.exceptions import Forbidden
from werkzeug.utils import secure_filename

from mediagoblin import messages
from mediagoblin import mg_globals

from mediagoblin.plugins.custom_subtitles import forms
from mediagoblin.decorators import (require_active_login, active_user_from_url,
                            get_media_entry_by_id, path_subtitle, user_may_delete_media)
from mediagoblin.tools.metadata import (compact_and_validate, DEFAULT_CHECKER,
                                        DEFAULT_SCHEMA)
from mediagoblin.tools.response import (render_to_response,
                                        redirect, redirect_obj, render_404)

import mimetypes

from mediagoblin.plugins.custom_subtitles.tools import open_subtitle,save_subtitle

UNSAFE_MIMETYPES = [
        'text/html',
        'text/svg+xml']

@get_media_entry_by_id
@user_may_delete_media
@require_active_login
def edit_subtitles(request, media):
    form = forms.EditSubtitlesForm(request.form)

    # Add any subtitles
    if 'subtitle_file' in request.files \
        and request.files['subtitle_file']:
        if mimetypes.guess_type(
                request.files['subtitle_file'].filename)[0] in \
                UNSAFE_MIMETYPES:
            public_filename = secure_filename('{0}.notsafe'.format(
                request.files['subtitle_file'].filename))
        else:
            public_filename = secure_filename(
                    request.files['subtitle_file'].filename)

        subtitle_public_filepath \
            = mg_globals.public_store.get_unique_filepath(
            ['media_entries', six.text_type(media.id), 'subtitle',
             public_filename])

        subtitle_public_file = mg_globals.public_store.get_file(
            subtitle_public_filepath, 'wb')

        try:
            subtitle_public_file.write(
                request.files['subtitle_file'].stream.read())
        finally:
            request.files['subtitle_file'].stream.close()

        media.subtitle_files.append(dict(
                name=form.subtitle_language.data \
                    or request.files['subtitle_file'].filename,
                filepath=subtitle_public_filepath,
                created=datetime.utcnow(),
                ))

        media.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            ("You added the subttile %s!") %
                (form.subtitle_language.data or
                 request.files['subtitle_file'].filename))

        return redirect(request,
                        location=media.url_for_self(request.urlgen))
    return render_to_response(
        request,
        'mediagoblin/plugins/custom_subtitles/subtitles.html',
        {'media': media,
         'form': form})


@require_active_login
@get_media_entry_by_id
@user_may_delete_media
@path_subtitle
def custom_subtitles(request,media,path=None):
    text=""
    text = open_subtitle(path)
    form = forms.CustomizeSubtitlesForm(request.form,
                                         subtitle=text)
    if request.method == 'POST' and form.validate():
        subtitle_data = form.subtitle.data
        save_subtitle(path,subtitle_data)
        messages.add_message(
            request,
            messages.SUCCESS,
            ("Subtitle file changed!!!"))
        return render_to_response(
        request,
        "mediagoblin/plugins/custom_subtitles/custom_subtitles.html",
        {"path": path,
         "media": media,
         "form": form })

    """delete_container = None
                index = 0
                for subtitle in media.subtitle_files:
                    if subtitle["name"] == "Two And A Half Men S02E02.srt":
                        delete_container = index
                    index += 1
                print media.subtitle_files.pop(delete_container)
                media.save()"""
        
    return render_to_response(
        request,
        "mediagoblin/plugins/custom_subtitles/custom_subtitles.html",
        {"path": path,
         "media": media,
         "form": form })