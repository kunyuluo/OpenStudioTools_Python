import os


class Folders:
    def __init__(self, config_file=None,mute=True):
        self.mute = bool(mute)
        self.config_file = config_file

    @property
    def openstudio_path(self):
        return self._openstudio_path

    @openstudio_path.setter
    def openstudio_path(self, path):
        if not path:
            path = self._find_openstudio_folder()

        if os.name == 'nt':
            exe_name = 'openstudio.exe'
        else:
            exe_name = 'openstudio'

        os_exe_path = os.path.join(path, exe_name)

        # set the openstudio_path
        self._openstudio_path = path
        self._openstudio_exe = os_exe_path

    @property
    def openstudio_exe(self):
        return self._openstudio_exe

    @staticmethod
    def _find_openstudio_folder():
        lb_install = "C:\Program Files\ladybug_tools"
        os_folder = []
        if os.path.isdir(lb_install):
            for f in os.listdir(lb_install):
                f_path = os.path.join(lb_install, f)
                if f.lower().startswith('openstudio') and os.path.isdir(f_path):
                    os_folder.append(f_path)

        os_path = os_folder[0]
        return os.path.join(os_path, 'bin')

# Main
folders = Folders()
print(folders.openstudio_exe())