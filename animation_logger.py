"""
Animations Logger
"""

import xlsxwriter


def animation_logger(name, motor, a_timing, a_rotations, row, col):
    """ Log animation to Excel file """

    workbook = xlsxwriter.Workbook("./animations/animations_t.xlsx")
    worksheet = workbook.add_worksheet("animations")

    rotation_type = {
        "M1": "RotationY",
        "M2": "RotationZ",
        "M3": "RotationY",
    }

    # Animation Name
    worksheet.write(row, col, "Animation")
    worksheet.write(row, col + 1, name)

    # Animated Element (motor)
    worksheet.write(row + 2, col, "AnimatedElement")
    worksheet.write(row + 2, col + 1, motor)

    # Animation Timing
    worksheet.write(row + 3, col, "Time")
    for i, t in enumerate(a_timing):
        worksheet.write(row + 3, i + 1, t)

    # Animation Rotations
    worksheet.write(row + 4, col, rotation_type[motor])
    for i, rot in enumerate(a_rotations):
        worksheet.write(row + 4, i + 1, rot)

    # TranslationX
    worksheet.write(row + 5, col, "TranslationX")
    for i, t in enumerate(a_timing):
        worksheet.write(row + 5, i + 1, 0)

    # TransitionType
    worksheet.write(row + 6, col, "TransitionType")
    worksheet.write(row + 6, col + 3, "none")

    workbook.close()


# timing = [0.0, 1.0, 2.1, 3.1, 4.2, 5.2, 6.2, 7.3, 8.3]
# rotations = [0, 0, -52, 52, -52, 52, -52, 52, 0]

# Function Call
# animation_logger("Intrusion", "M1", timing, rotations, 0, 0)
