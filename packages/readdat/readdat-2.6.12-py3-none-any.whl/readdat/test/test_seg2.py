import os
import obspy
import pytest

from readdat.read import read
from readdat.test.test_filesamples import FILESAMPLES
from readdat.seg2.read_seg2 import _read_seg2_without_obspy_warning, autodetect_seg2_acquisition_system
from readdat.seg2.read_seg2musc import is_seg2musc
from readdat.seg2.read_seg2coda import is_seg2coda
from readdat.seg2.read_seg2ondulys import is_seg2ondulys


from readdat.test.validate_seg2_contents import \
    validate_seg2file_content, \
    validate_seg2file_musc_content, \
    validate_seg2file_ondulys_content, \
    validate_seg2file_coda_content_naive, \
    validate_seg2file_coda_content_utc

# ==================== file existence tested in filesamples

# ==================== Format detection
def test_is_seg2musc():
    assert is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC"]))
    assert is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC1"]))

    assert not is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE"]))
    assert not is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA"]))
    assert not is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA1"]))
    assert not is_seg2musc(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_ONDULYS"]))

def test_is_seg2coda():
    assert is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE"]))
    assert is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA"]))
    assert is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA1"]))

    assert not is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC"]))
    assert not is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC1"]))
    assert not is_seg2coda(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_ONDULYS"]))


def test_is_seg2ondulys():
    assert is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_ONDULYS"]))

    assert not is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE"]))
    assert not is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC"]))
    assert not is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_MUSC1"]))
    assert not is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA"]))
    assert not is_seg2ondulys(_read_seg2_without_obspy_warning(FILESAMPLES["SEG2FILE_CODA1"]))


def test_autodetect_seg2_acquisition_system():
    #with pytest.warns(UserWarning):
    #    # standard seg2 files are supposed to produce a user warning
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE'])) == "CODA"
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE_MUSC'])) == "MUSC"
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE_MUSC1'])) == "MUSC"
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE_ONDULYS'])) == "ONDULYS"
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE_CODA'])) == "CODA"
    assert autodetect_seg2_acquisition_system(_read_seg2_without_obspy_warning(FILESAMPLES['SEG2FILE_CODA1'])) == "CODA"

# =================== File contents
def test_read_seg2():

    stream = read(FILESAMPLES['SEG2FILE'], format="SEG2", acquisition_system=None)
    validate_seg2file_content(stream)

def test_read_seg2musc():

    stream = read(FILESAMPLES['SEG2FILE_MUSC'], format="SEG2", acquisition_system="MUSC")
    validate_seg2file_musc_content(stream)

def test_read_seg2musc_auto():

    stream = read(FILESAMPLES['SEG2FILE_MUSC'], format="AUTO", acquisition_system="AUTO")
    validate_seg2file_musc_content(stream)


def test_read_seg2ondulys():

    with pytest.warns(UserWarning):
        stream = read(FILESAMPLES['SEG2FILE_ONDULYS'], format="SEG2", acquisition_system="ONDULYS")

    validate_seg2file_ondulys_content(stream)

def test_read_seg2ondulys_auto():

    with pytest.warns(UserWarning):
        stream = read(FILESAMPLES['SEG2FILE_ONDULYS'], format="AUTO", acquisition_system="AUTO")

    validate_seg2file_ondulys_content(stream)

def test_read_seg2coda_naive():

    stream = read(FILESAMPLES['SEG2FILE_CODA'], format="SEG2", acquisition_system="CODA")
    validate_seg2file_coda_content_naive(stream)

    stream = read(FILESAMPLES['SEG2FILE_CODA'], format="SEG2", acquisition_system="CODA", timezone=None)
    validate_seg2file_coda_content_naive(stream)

def test_read_seg2coda_utc():

    stream = read(FILESAMPLES['SEG2FILE_CODA'], format="SEG2", acquisition_system="CODA", timezone="Europe/Paris")
    validate_seg2file_coda_content_utc(stream)

def test_read_seg2coda_auto():

    stream = read(FILESAMPLES['SEG2FILE_CODA'], format="AUTO", acquisition_system="AUTO", timezone="Europe/Paris")
    validate_seg2file_coda_content_utc(stream)
