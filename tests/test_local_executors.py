import sys
import os.path as osp
import pytest
from coffea import hist, processor

if sys.platform.startswith("win"):
    pytest.skip("skipping tests that only function in linux", allow_module_level=True)


@pytest.mark.parametrize("compression", [None, 0, 2])
@pytest.mark.parametrize(
    "executor", [processor.iterative_executor, processor.futures_executor]
)
def test_nanoevents_analysis(executor, compression):
    from coffea.processor.test_items import NanoEventsProcessor

    filelist = {
        "ZJets": [osp.abspath("tests/samples/nano_dy.root")],
        "Data": [osp.abspath("tests/samples/nano_dimuon.root")],
    }
    treename = "Events"

    exe_args = {
        "workers": 1,
        "schema": processor.NanoAODSchema,
        "compression": compression,
    }

    hists = processor.run_uproot_job(
        filelist, treename, NanoEventsProcessor(), executor, executor_args=exe_args
    )

    assert hists["cutflow"]["ZJets_pt"] == 18
    assert hists["cutflow"]["ZJets_mass"] == 6
    assert hists["cutflow"]["Data_pt"] == 84
    assert hists["cutflow"]["Data_mass"] == 66


@pytest.mark.parametrize("compression", [None, 0, 2])
@pytest.mark.parametrize(
    "executor", [processor.iterative_executor, processor.futures_executor]
)
def test_nanoevents0_analysis(executor, compression):
    from coffea.processor.test_items import NanoEvents0Processor

    filelist = {
        "ZJets": [osp.abspath("tests/samples/nano_dy.root")],
        "Data": [osp.abspath("tests/samples/nano_dimuon.root")],
    }
    treename = "Events"

    exe_args = {
        "workers": 1,
        "schema": processor.NanoEvents,
        "compression": compression,
    }

    hists = processor.run_uproot_job(
        filelist, treename, NanoEvents0Processor(), executor, executor_args=exe_args
    )

    assert hists["cutflow"]["ZJets_pt"] == 18
    assert hists["cutflow"]["ZJets_mass"] == 6
    assert hists["cutflow"]["Data_pt"] == 84
    assert hists["cutflow"]["Data_mass"] == 66


@pytest.mark.parametrize("flatten", [True, False])
@pytest.mark.parametrize(
    "executor", [processor.iterative_executor, processor.futures_executor]
)
def test_dataframe_analysis(executor, flatten):
    from coffea.processor.test_items import NanoTestProcessor

    filelist = {
        "ZJets": [osp.abspath("tests/samples/nano_dy.root")],
        "Data": [osp.abspath("tests/samples/nano_dimuon.root")],
    }
    treename = "Events"

    exe_args = {
        "workers": 1,
        "flatten": flatten,
    }

    hists = processor.run_uproot_job(
        filelist, treename, NanoTestProcessor(), executor, executor_args=exe_args
    )

    assert hists["cutflow"]["ZJets_pt"] == 18
    assert hists["cutflow"]["ZJets_mass"] == 6
    assert hists["cutflow"]["Data_pt"] == 84
    assert hists["cutflow"]["Data_mass"] == 66
