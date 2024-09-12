import pathlib
from pathlib import Path


class SortingMetadata:
    """
    To analyse a probe experiment we need to bring together
    file paths from a variety of sources. This class therefore
    represents an experiment's data:

    Kilosort sorting directory (spike sorting outputs, i.e. spike times and raw traces)
    Behavioural data (camera and photodiode)
    Histology data (i.e. probe tracks and whole brain images, brainreg_util-segment outputs)
    Output directories

    """

    def __init__(
        self,
        mouse_id,
        root,
        atlas="kim_mouse_10um",
        probe=True,
        make_mouse_dirs=False,
        behaviour=True,
        serial2p_dir=None,


    ):
        self.probe = probe
        self.mouse_id = mouse_id
        self.root = Path(root)
        self.mouse_dir = self.root / mouse_id
        self.raw_mouse_dir = get_raw_mouse_path(self)
        if serial2p_dir is not None:
            self.serial2p_dir = serial2p_dir

        if not self.raw_mouse_dir.exists():
            if make_mouse_dirs:
                self.raw_mouse_dir.mkdir()
            else:
                raise ValueError(f"Mouse ID not found at {self.raw_mouse_dir}...")

        self.histology_dir = self.get_path(atlas, self.mouse_dir)
        self.sessions = []

        self.figures_directory = self.root / mouse_id / "figures"
        if not self.figures_directory.exists():
            self.figures_directory.mkdir(parents=True)

        self.session_dirs = sorted(self.mouse_dir.rglob("ses-*"))

        for session_path in list(self.session_dirs):
            self.sessions.append(SortingMetadataSession(session_path, probe=self.probe))

    def get_path(self, key, folder):
        return get_path(key, folder)

    def get_session(self, session_folder_name):
        for s in self.sessions:
            if s.behav_name == session_folder_name:
                return s

    def get_session_from_type(self, session_type):
        for s in self.sessions:
            if s.name == session_type:
                return s

    def session_types(self):
        return [s.name for s in self.sessions]


class SortingMetadataSession:
    """ """

    def __init__(self, session_path, probe=True, behaviour=True):
        self.session_path_derivatives = session_path
        self.session_path_raw = pathlib.Path(str(session_path).replace('derivatives', 'rawdata'))

        self.histology_dir = self.session_path_derivatives.parent / "histology"
        self.figures_path = self.session_path_derivatives.parent / "figures"

        self.behav_raw = get_path("behav", self.session_path_raw)
        self.behav_derivatives = get_path("behav", self.session_path_derivatives)

        self.ephys_raw = get_path("ephys", self.session_path_raw)
        self.ephys_derivatives = get_path("ephys", self.session_path_derivatives)

        self.trigger_path = self.get_trigger_path()
        self.name = self.session_path_raw.stem.split('-')[-1]

        if behaviour:
            self.behav_name = list(self.behav_derivatives.rglob("**/"))[1].stem
            self.behav_data_folder = list(self.behav_derivatives.glob("*"))[0]
            self.condition = self.behav_name

        if probe:
            self.run_paths_raw = list(self.ephys_raw.glob("*run*"))
            if not isinstance(self.ephys_derivatives, str):
                self.run_paths_derivatives = list(self.ephys_derivatives.glob("*run*"))
            self.raw_meta_path = get_raw_traces_path(self.session_path_raw, ext="*ap.meta")
            self.raw_traces_path = get_raw_traces_path(self.session_path_raw)
            self.quality_path = get_path("quality_metrics.csv", self.session_path_derivatives)
            self.kilosort_dir = get_path("sorter_output", self.session_path_derivatives)
            if self.kilosort_dir:
                self.bombcell_dir = self.kilosort_dir.parent / "bombcell"
                self.unitmatch_waveforms_dir = self.bombcell_dir / "RawWaveforms"

    def get_trigger_path(self):
        trigger_path = get_path("trigger.npy", self.session_path_derivatives)
        if trigger_path == "":
            if self.ephys_derivatives:
                trigger_path = self.ephys_derivatives / "trigger.npy"
        return trigger_path


def get_raw_traces_path(session_path, ext="*ap.bin"):
    raw_session_path = get_raw_session_path(session_path)
    print(raw_session_path)
    return list(raw_session_path.rglob(ext))[0]


def get_raw_mouse_path(mtd):
    raw_mouse_path = Path(
        str(mtd.mouse_dir).replace("derivatives", "rawdata")
    )
    return raw_mouse_path


def get_raw_session_path(session_path):
    raw_session_path = Path(
        str(session_path).replace("derivatives", "rawdata")
    )
    return raw_session_path


def get_path(key, folder):
    paths = list(folder.rglob(key))
    if len(paths) == 1:
        return paths[0]
    elif len(paths) > 1:
        raise ValueError(f"too many paths found for {key} at {folder}")
    else:
        print(f"no paths found, returning null for {key} at {folder}")
        return ""


def contains_ephys(s):
    if (not s.ephys_raw) or len(list(s.ephys_raw.glob("*"))) == 0:
        warnings.warn(f"no derivatives data found at {s.ephys_raw}, skipping..")
        return False
    else:
        return True
