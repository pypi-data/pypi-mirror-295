import os
import platform
import subprocess
import kabaret.app.resources as resources
from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow.users import PresetSessionValue
from libreflow.baseflow.file import RenderBlenderPlayblast, PublishAndRenderPlayblast
from libreflow.flows.default.flow.file import TrackedFile
from libreflow.utils.b3d import wrap_python_expr
from libreflow.resources.icons import gui as _, libreflow as _

from . import _version
__version__ = _version.get_versions()['version']


class PlayblastQuality(flow.values.ChoiceValue):

    CHOICES = ['Viewport', 'Final']


class ANPORenderBlenderPlayblast(RenderBlenderPlayblast):

    quality = flow.Param('Viewport', PlayblastQuality)
    # resolution_percentage = flow.Param('100', ResolutionChoiceValue).ui(
    #     label='Resolution scale (%)'
    # )

    _files = flow.Parent(2)
    _task = flow.Parent(3)

    with flow.group('Advanced'):
        use_simplify = flow.SessionParam(False, PresetSessionValue).ui(
            tooltip="Use low-definition rigs",
            editor='bool',
            hidden=True
            )

    # with flow.group('Advanced'):
    #     reduce_textures = flow.SessionParam(False, PresetSessionValue).ui(
    #         tooltip="Reduce texture sizes before render, to reduce memory footprint",
    #         editor='bool',
    #     )
    #     target_texture_width = flow.SessionParam(4096, PresetSessionValue).ui(
    #         tooltip="Size to reduce textures to",
    #         editor='int',
    #     )

    def __init__(self, parent, name):
        super(ANPORenderBlenderPlayblast, self).__init__(parent, name)
        self.file_settings = get_contextual_dict(
            self._file, "settings", ["sequence", "shot"]
        )

    def get_run_label(self):
        return 'ANPO Render playblast {seq} {shot}'.format(
            seq=self.file_settings.get("sequence", "undefined"),
            shot=self.file_settings.get("shot", "undefined")
        )
   
    def check_default_values(self):
        self.revision_name.revert_to_default()
        self.auto_play_playblast.apply_preset()
        # self.resolution_percentage.apply_preset()
        # self.reduce_textures.apply_preset()
        # self.target_texture_width.apply_preset()
    
    def update_presets(self):
        self.auto_play_playblast.update_preset()
        # self.resolution_percentage.update_preset()
        # self.reduce_textures.update_preset()
        # self.target_texture_width.update_preset()

    def extra_argv(self):
        project_name = self.root().project().name()
        revision = self._file.get_revision(self.revision_name.get())
        do_render = self.quality.get() == 'Final'
        python_expr = """import bpy
bpy.ops.lfs.playblast(do_render=%s, filepath='%s', studio='%s', project='%s', sequence='%s', scene='%s', quality='%s', version='%s', do_autoplay=%s,frame_count=%d)""" % (
            str(do_render),
            self.output_path,
            self.root().project().get_current_site().name(),
            project_name,
            self.file_settings.get("sequence", "undefined"),
            self.file_settings.get("shot", "undefined"),
            'PREVIEW' if self.quality.get() == 'Viewport' else 'FINAL',
            self.revision_name.get(),
            self.auto_play_playblast.get() and platform.system() == "Windows",
            self.get_shot_frame_count(),
        )

        if not do_render:
            python_expr += "\nbpy.ops.wm.quit_blender()"
        
        args = [
            revision.get_path(),
            "--addons",
            "mark_sequence",
            "--python-expr",
            wrap_python_expr(python_expr),
        ]

        if do_render:
            args.insert(0, '-b')
        
        return args


class ANPOPublishAndRenderBlenderPlayblast(PublishAndRenderPlayblast):
    ICON = ('icons.libreflow', 'publish-blender')
    label = flow.Label('<h2>Playblast</h2>')
    quality = flow.Param('Viewport', PlayblastQuality)
    auto_play_playblast = flow.SessionParam(True, PresetSessionValue).ui(
        tooltip="Play playblast when render is finished",
        editor='bool')

    def allow_context(self, context):
        allow_context = super(ANPOPublishAndRenderBlenderPlayblast, self).allow_context(context)
        return allow_context and self._file.render_blender_playblast.allow_context(context)

    def check_default_values(self):
        super(ANPOPublishAndRenderBlenderPlayblast, self).check_default_values()
        self.quality.revert_to_default() # required to override the param value in the default action

    def _configure_and_render(self, revision_name):
        self._file.render_blender_playblast.revision_name.set(revision_name)
        self._file.render_blender_playblast.quality.set(self.quality.get())
        self._file.render_blender_playblast.auto_play_playblast.set(self.auto_play_playblast.get())
        return self._file.render_blender_playblast.run('Render')


def render_blender_playblast(parent):
    if isinstance(parent, TrackedFile) and parent.format.get() == 'blend':
        rp = flow.Child(ANPORenderBlenderPlayblast).ui(label='Render playblast')
        rp.name = 'render_blender_playblast'
        rp.index = 29
        prp = flow.Child(ANPOPublishAndRenderBlenderPlayblast).ui(label='Publish and playblast')
        prp.name = 'publish_and_playblast_blender'
        prp.index = 26
        return [rp, prp]


def install_extensions(session): 
    return {
        "playblast": [
            render_blender_playblast,
        ],
    }
