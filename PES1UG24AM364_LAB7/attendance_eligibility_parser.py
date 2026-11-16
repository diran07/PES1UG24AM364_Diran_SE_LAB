def normalize_srn(srn):
    """
    Trims and upper-cases a student registration number.
    Returns None if srn is not a non-empty string.
    """
    if not isinstance(srn, str):
        return None
    srn = srn.strip().replace(' ', '').upper()
    if srn == '':
        return None
    return srn

def attendance_from_ratio(text):
    """
    Converts 'ATTENDED/HELD' into a whole-number percentage.
    Returns None for anything that is not a valid ratio.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split('/')
    if len(parts) != 2:
        return None
    attended, held = parts[0].strip(), parts[1].strip()
    if not (attended.isascii() and attended.isdigit()):
        return None
    if not (held.isascii() and held.isdigit()):
        return None
    attended, held = int(attended), int(held)
    if held == 0 or attended > held:
        return None
    return attended * 100 // held

def attendance_from_register(marks):
    """
    Works out the attendance percentage from a string of P (present) and A (absent).
    Returns None if marks is empty or has anything other than P and A.
    """
    if not isinstance(marks, str):
        return None
    marks = marks.strip().upper()
    if marks == '':
        return None
    for m in marks:
        if m not in 'PA':
            return None
    return marks.count('P') * 100 // len(marks)

def main():
    print("==== Running normalize_srn ====")
    value = input("Enter an SRN (e.g. pes1ug23cs001): ")
    result = normalize_srn(value)
    if result is None:
        print("Invalid SRN")
    else:
        print("Normalized SRN:", result)

    print("\n==== Running attendance_from_ratio ====")
    value = input("Enter classes attended and held as ATTENDED/HELD (e.g. 30/40): ")
    result = attendance_from_ratio(value)
    if result is None:
        print("Invalid ratio")
    else:
        print("Attendance percent:", result)

    print("\n==== Running attendance_from_register ====")
    value = input("Enter the register as P/A marks (e.g. PPAPP): ")
    result = attendance_from_register(value)
    if result is None:
        print("Invalid register")
    else:
        print("Attendance percent:", result)

if __name__ == "__main__":
    main()