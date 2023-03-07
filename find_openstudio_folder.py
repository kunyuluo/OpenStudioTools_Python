def _find_openstudio_folder():
    """Find the most recent OpenStudio installation in its default location.
    Returns:
        File directory and full path to executable in case of success.
        None in case of failure.
    """

    def getversion(openstudio_path):
        """Get digits for the version of OpenStudio."""
        try:
            ver = ''.join(s for s in openstudio_path if (s.isdigit() or s == '.'))
            return sum(int(d) * (10 ** i)
                       for i, d in enumerate(reversed(ver.split('.'))))
        except ValueError:  # folder starting with 'openstudio' and no version
            return 0

    # first check if there's a version installed in the ladybug_tools folder
    lb_install = lb_config.folders.ladybug_tools_folder
    os_folders = []
    if os.path.isdir(lb_install):
        for f in os.listdir(lb_install):
            f_path = os.path.join(lb_install, f)
            if f.lower().startswith('openstudio') and os.path.isdir(f_path):
                os_folders.append(f_path)

    # then check the default installation folders
    if len(os_folders) != 0 and os.path.isdir(os.path.join(os_folders[0], 'bin')):
        pass  # we found a version of openstudio in the ladybug_tools folder
    elif os.name == 'nt':  # search the C:/ drive on Windows
        for f in os.listdir('C:\\'):
            f_path = 'C:\\{}'.format(f)
            if f.lower().startswith('openstudio') and os.path.isdir(f_path):
                os_folders.append(f_path)
    elif platform.system() == 'Darwin':  # search the Applications folder on Mac
        for f in os.listdir('/Applications/'):
            f_path = '/Applications/{}'.format(f)
            if f.lower().startswith('openstudio') and os.path.isdir(f_path):
                os_folders.append(f_path)
    elif platform.system() == 'Linux':  # search the usr/local folder
        for f in os.listdir('/usr/local/'):
            f_path = '/usr/local/{}'.format(f)
            if f.lower().startswith('openstudio') and os.path.isdir(f_path):
                os_folders.append(f_path)
    else:  # unknown operating system
        os_folders = None

    if not os_folders:  # No Openstudio installations were found
        return None

    # get the most recent version of OpenStudio that was found
    os_path = sorted(os_folders, key=getversion, reverse=True)[0]

    return os.path.join(os_path, 'bin')