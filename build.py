from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

executables = [
    Executable('scrapperGui.pyw', 'Console', targetName = 'LS.exe')
]

setup(name='LighteningScrapper',
      version = '0.5',
      description = 'Look through lists of proxies to find live ones',
      options = dict(build_exe = buildOptions),
      executables = executables)
