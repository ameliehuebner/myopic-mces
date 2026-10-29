def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "timelimit: marks tests that depend on timelimit and may behave unexpectedly on different machines (deselect with '-m \"not timelimit\"')"
    )
    config.addinivalue_line(
        "markers",
        "cpp: marks tests that depend on the c++ extension and will fail on the pure python package (deselect with '-m \"not cpp\"')"
    )
    config.addinivalue_line(
        "markers",
        "hdf5: marks tests that depend on the h5py package and will fail if the package is not installed (deselect with '-m \"not hdf5\"')"
    )
