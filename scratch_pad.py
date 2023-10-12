import io, random, string, re, os


def fuck_pigs():
    cdc = random.choices(string.ascii_lowercase, k=26)
    cdc[-6:-4] = map(str.upper, cdc[-6:-4])
    cdc[2] = cdc[0]
    cdc[3] = "_"
    return "".join(cdc).encode()


def patch_exe():
    executable_path = r"C:\Users\dmcfa\AppData\Roaming\undetected_edgedriver\msedgedriver.exe"
    linect = 0
    replacement = fuck_pigs()
    with io.open(executable_path, "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"cdc_" in line:
                fh.seek(-len(line), 1)
                newline = re.sub(b"cdc_.{22}", replacement, line)
                fh.write(newline)
                linect += 1
        return linect


def find_edge_executable():
    """
    Finds the edge, edge beta, edge canary executable
    Returns
    -------
    executable_path :  str
        the full file path to found executable
    """
    candidates = set()

    for item in map(
            os.environ.get, ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")
    ):
        for subitem in (
                "Microsoft/Edge/Application",
                "Microsoft/Edge Beta/Application",
                "Microsoft/Edge Canary/Application",
        ):
            candidates.add(os.sep.join((item, subitem, "msedge.exe")))
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)

