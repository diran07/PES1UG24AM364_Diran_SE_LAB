import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning


# ---------- attendance_percent ----------

# total_classes <= 0 : True / False
def test_total_zero():
    with pytest.raises(ValueError):
        attendance_percent(0, 0, 0)

def test_total_negative():
    with pytest.raises(ValueError):
        attendance_percent(0, -5, 0)

# attended < 0 or attended > total : both sides of the 'or'
def test_attended_negative():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)

def test_attended_more_than_total():
    with pytest.raises(ValueError):
        attendance_percent(41, 40, 0)

def test_attended_equals_total():
    assert attendance_percent(40, 40, 0) == 100

def test_attended_zero():
    assert attendance_percent(0, 40, 0) == 0

# medical_leave_days > 5 : True / False / boundary
def test_medical_not_capped():
    assert attendance_percent(30, 40, 0) == 75

def test_medical_exactly_five():
    assert attendance_percent(20, 40, 5) == 62

def test_medical_capped():
    # 6 -> 5, so 25/40
    assert attendance_percent(20, 40, 6) == 62

# credited > total : True / False / boundary
def test_credited_capped():
    assert attendance_percent(38, 40, 10) == 100

def test_credited_exactly_total():
    assert attendance_percent(35, 40, 5) == 100

def test_credited_below_total():
    assert attendance_percent(10, 40, 2) == 30


# ---------- exam_eligibility ----------

def test_fees_pending():
    assert exam_eligibility(90, True, False) == "fees pending"

def test_eligible_above_75():
    assert exam_eligibility(80, False, True) == "eligible"

def test_eligible_exactly_75():
    assert exam_eligibility(75, False, True) == "eligible"

def test_74_with_condonation():
    assert exam_eligibility(74, True, True) == "eligible"

def test_74_without_condonation():
    assert exam_eligibility(74, False, True) == "condonation required"

def test_exactly_65_with_condonation():
    assert exam_eligibility(65, True, True) == "eligible"

def test_exactly_65_without_condonation():
    assert exam_eligibility(65, False, True) == "condonation required"

def test_64_detained():
    assert exam_eligibility(64, True, True) == "detained"

def test_detained_low():
    assert exam_eligibility(10, False, True) == "detained"


# ---------- attendance_warning ----------

def test_no_warning_above_85():
    assert attendance_warning(95, 1) is None

def test_no_warning_exactly_85():
    assert attendance_warning(85, 10) is None

def test_reminder_84():
    assert attendance_warning(84, 10) == "reminder"

def test_reminder_exactly_75():
    assert attendance_warning(75, 1) == "reminder"

def test_critical():
    assert attendance_warning(74, 5) == "critical"

def test_final_notice_exactly_4_weeks():
    assert attendance_warning(74, 4) == "final notice"

def test_final_notice_zero_weeks():
    assert attendance_warning(50, 0) == "final notice"