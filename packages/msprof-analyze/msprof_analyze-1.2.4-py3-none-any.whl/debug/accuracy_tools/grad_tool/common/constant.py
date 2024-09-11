
class GradConst:

    FRAMEWORKS = {"PyTorch", "MindSpore"}
    PYTORCH = "PyTorch"
    MindSpore = "MindSpore"

    GRAD_FILE_SUFFIX = {"npy", "pt"}
    NPY_SUFFIX = "npy"
    PT_SUFFIX = "pt"

    # for callback
    CURRENT_STEP = "current_step"

    PARAM_LIST = "param_list"
    RANK = "rank"
    STEP = "step"
    BOUNDS = "bounds"
    OUTPUT_PATH = "output_path"

    # level const
    LEVEL = "level"
    LEVEL0 = "L0"
    LEVEL1 = "L1"
    LEVEL2 = "L2"
    SUPPORTED_LEVEL = {"L0", "L1", "L2"}

    # numpy coding
    STEP_IDX = 0
    SHAPE_DIM_IDX = 4
    MAX_SIZE = 10 * 1024 * 1024 * 1024

    # direction suffix
    DIR_SUFFIX = "dir.npy"

    # file safty
    DATA_DIR_AUTHORITY = 0o750
    DATA_FILE_AUTHORITY = 0o640
    DIRECTORY_LENGTH = 4096
    FILE_NAME_LENGTH = 255
    FILE_VALID_PATTERN = r"^[a-zA-Z0-9_.:/-]+$"
    PARAM_VALID_PATTERN = r"^[a-zA-Z0-9_.:-]+$"
    DIR = "dir"
    FILE = "file"

    STEP_FINISH = "step_finish"

    SUMMARY = "summary"

    # csv header entry
    MD5 = "MD5"
    DISTRIBUTION = "distribution"
    SHAPE = "shape"
    MAX = "max"
    MIN = "min"
    NORM = "norm"