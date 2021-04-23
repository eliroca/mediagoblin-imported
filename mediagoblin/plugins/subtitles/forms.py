# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2016 MediaGoblin contributors.  See AUTHORS.
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

import wtforms

from mediagoblin.tools.translate import lazy_pass_to_ugettext as _

class CustomizeSubtitlesForm(wtforms.Form):
    subtitle = wtforms.TextAreaField(
        ('Subtitle'),
        [wtforms.validators.Optional()],
        description=_('Subtitles in <a href="https://en.wikipedia.org/wiki/WebVTT" target="_blank">WebVTT format</a>'))

class EditSubtitlesForm(wtforms.Form):
    subtitle_language = wtforms.StringField(
        'Language')
    subtitle_file = wtforms.FileField(
        'File',
        description=_('Subtitles in <a href="https://en.wikipedia.org/wiki/WebVTT" target="_blank">WebVTT format</a>'))
