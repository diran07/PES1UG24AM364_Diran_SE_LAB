import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning


# attendance_percent
def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75

def test_invalid_total():
    with pytest.raises(ValueError):
        attendance_percent(10, 0, 0)

def test_invalid_attended():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)

def test_medical_capped_and_credited_capped():
    # medical 10 -> 5, credited 43 -> 40
    assert attendance_percent(38, 40, 10) == 100


# exam_eligibility
def test_fees_pending():
    assert exam_eligibility(90, False, False) == "fees pending"

def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"

def test_eligible_with_condonation():
    assert exam_eligibility(70, True, True) == "eligible"

def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"

def test_detained():
    assert exam_eligibility(50, False, True) == "detained"


# attendance_warning
def test_no_warning():
    assert attendance_warning(90, 5) is None

def test_critical():
    assert attendance_warning(60, 6) == "critical"

def test_final_notice():
    assert attendance_warning(60, 2) == "final notice"

def test_reminder():
    assert attendance_warning(80, 3) == "reminder"