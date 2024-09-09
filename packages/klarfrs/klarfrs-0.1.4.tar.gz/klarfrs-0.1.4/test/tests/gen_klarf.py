import random
import datetime

def generate_random_float(min_val, max_val):
    return random.uniform(min_val, max_val)

def generate_random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def generate_random_string(length):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def generate_klarf_file(filename, num_defects):
    with open(filename, 'w') as f:
        # Write header information
        now = datetime.datetime.now()
        f.write(f"FileVersion 1 2;\n")
        f.write(f"FileTimestamp {now.strftime('%m-%d-%y %H:%M:%S')};\n")
        f.write(f"InspectionStationID \"KLA-Tencor\" \"SP7\" \"SP7-{generate_random_int(1, 99)}\";\n")
        f.write(f"SampleType WAFER;\n")
        f.write(f"ResultTimestamp {now.strftime('%m-%d-%y %H:%M:%S')};\n")
        f.write(f"LotID \"{generate_random_string(8)}-{generate_random_string(16)}\";\n")
        f.write(f"SampleSize 1 300;\n")
        f.write(f"DeviceID \"None\";\n")
        f.write(f"SetupID \"{generate_random_string(7)}\" {now.strftime('%m-%d-%y %H:%M:%S')};\n")
        f.write(f"StepID \"{generate_random_string(7)}\";\n")
        f.write(f"SampleOrientationMarkType NOTCH;\n")
        f.write(f"OrientationMarkLocation DOWN;\n")
        f.write(f"DiePitch {generate_random_float(1e5, 5e5):.10e} {generate_random_float(1e5, 5e5):.10e};\n")
        f.write(f"DieOrigin 0.0000000000e+00 0.0000000000e+00;\n")
        f.write(f"WaferID \"{generate_random_string(2)}{generate_random_int(1000000000, 9999999999)}\";\n")
        f.write(f"Slot {generate_random_int(1, 25)};\n")
        f.write(f"SampleCenterLocation {generate_random_float(1e5, 2e5):.10e} {generate_random_float(1e5, 2e5):.10e};\n")
        f.write(f"OrientationInstructions \"Front \";\n")
        f.write(f"CoordinatesMirrored NO;\n")
        f.write(f"InspectionOrientation DOWN;\n")

        # Write inspection test information
        for i in range(4, 14):
            if i not in [5, 10, 11, 12]:
                f.write(f"InspectionTest {i};\n")
                f.write(f"SampleTestPlan 1\n")
                f.write(f"  0 0 ;\n")
                f.write(f"AreaPerTest {generate_random_float(6e10, 7e10):.10e};\n")

        # Write defect record specification
        f.write("DefectRecordSpec 170 DEFECTID XREL YREL XINDEX YINDEX XSIZE YSIZE DEFECTAREA DSIZE CLASSNUMBER TEST CLUSTERNUMBER ROUGHBINNUMBER FINEBINNUMBER REVIEWSAMPLE ADCSIZE ADCSIZE_DN_OBLIQUE ADCSIZE_DW1_OBLIQUE ADCSIZE_DW2_OBLIQUE CLASSCODE_DN_OBLIQUE CLASSCODE_DW1_OBLIQUE CLASSCODE_DW2_OBLIQUE COLUMNINDEX_DN_OBLIQUE COLUMNINDEX_DW1_OBLIQUE COLUMNINDEX_DW2_OBLIQUE ENCENERGY_DN_OBLIQUE ENCENERGY_DW1_OBLIQUE ENCENERGY_DW2_OBLIQUE HAZEAVERAGE_DN_OBLIQUE HAZEAVERAGE_DW1_OBLIQUE HAZEAVERAGE_DW2_OBLIQUE INDEX1_DN_OBLIQUE INDEX1_DW1_OBLIQUE INDEX1_DW2_OBLIQUE INDEX2_DN_OBLIQUE INDEX2_DW1_OBLIQUE INDEX2_DW2_OBLIQUE LPDE1 LPDE2 LPDE3 LPDE4 LPMHAZEAVERAGEADC_DN_OBLIQUE LPMHAZEAVERAGEADC_DW1_OBLIQUE LPMHAZEAVERAGEADC_DW2_OBLIQUE LPMMAXADC LPMMAXADC_DN_OBLIQUE LPMMAXADC_DW1_OBLIQUE LPMMAXADC_DW2_OBLIQUE LPMMAXAMPLITUDE LPMMAXAMPLITUDE_DN_OBLIQUE LPMMAXAMPLITUDE_DW1_OBLIQUE LPMMAXAMPLITUDE_DW2_OBLIQUE LPMMAXAMPLITUDENPPM LPMMAXAMPLITUDENPPM_DN_OBLIQUE LPMMAXAMPLITUDENPPM_DW1_OBLIQUE LPMMAXAMPLITUDENPPM_DW2_OBLIQUE LPMMAXAMPLITUDERPPM LPMMAXAMPLITUDERPPM_DN_OBLIQUE LPMMAXAMPLITUDERPPM_DW1_OBLIQUE LPMMAXAMPLITUDERPPM_DW2_OBLIQUE LPMMAXSNR LPMMAXSNR_DN_OBLIQUE LPMMAXSNR_DW1_OBLIQUE LPMMAXSNR_DW2_OBLIQUE LPMTRIGGERED_DN_OBLIQUE LPMTRIGGERED_DW1_OBLIQUE LPMTRIGGERED_DW2_OBLIQUE NPPMSIZE NPPMSIZE_DN_OBLIQUE NPPMSIZE_DW1_OBLIQUE NPPMSIZE_DW2_OBLIQUE POSITION_RCENTROID POSITION_THETACENTROID RPPMHAZEAVERAGE_DN_OBLIQUE RPPMHAZEAVERAGE_DW1_OBLIQUE RPPMHAZEAVERAGE_DW2_OBLIQUE RPPMSIZE RPPMSIZE_DN_OBLIQUE RPPMSIZE_DW1_OBLIQUE RPPMSIZE_DW2_OBLIQUE DEFECTSIZE SIZE_DN_OBLIQUE SIZE_DN_OBLIQUE_TO_SIZE_DW1_OBLIQUE SIZE_DN_OBLIQUE_TO_SIZE_DW2_OBLIQUE SIZE_DW1_OBLIQUE SIZE_DW1_OBLIQUE_TO_SIZE_DN_OBLIQUE SIZE_DW1_OBLIQUE_TO_SIZE_DW2_OBLIQUE SIZE_DW2_OBLIQUE SIZE_DW2_OBLIQUE_TO_SIZE_DN_OBLIQUE SIZE_DW2_OBLIQUE_TO_SIZE_DW1_OBLIQUE SN_RATIO SN_RATIO_DN_OBLIQUE SN_RATIO_DW1_OBLIQUE SN_RATIO_DW2_OBLIQUE AREA ASPECT_RATIO POSITION_BOX_REND POSITION_BOX_RSTART POSITION_BOX_THETAEND POSITION_BOX_THETASTART LENGTH HAZEAVERAGE CLASSCODE COLUMNINDEX ENCENERGY INDEX1 INDEX2 LPMHAZEAVERAGEADC LPMTRIGGERED ROWINDEX RPPMHAZEAVERAGE ADCSIZE_PCC_OBLIQUE CLASSCODE_PCC_OBLIQUE COLUMNINDEX_PCC_OBLIQUE DEFECTSIZENEGADC_PCC_OBLIQUE DEFECTSIZEPOSADC_PCC_OBLIQUE DEFECTSIZESHE_PCC_OBLIQUE ENCENERGY_PCC_OBLIQUE HAZEAVERAGE_PCC_OBLIQUE INDEX1_PCC_OBLIQUE INDEX2_PCC_OBLIQUE LATERALEXTENTRADIALNEGUM_PCC_OBLIQUE LATERALEXTENTRADIALPOSUM_PCC_OBLIQUE LATERALEXTENTRADIALUM_PCC_OBLIQUE LATERALEXTENTTANGENTIALNEGUM_PCC_OBLIQUE LATERALEXTENTTANGENTIALPOSUM_PCC_OBLIQUE LATERALEXTENTTANGENTIALUM_PCC_OBLIQUE LPMHAZEAVERAGEADC_PCC_OBLIQUE LPMMAXADC_PCC_OBLIQUE LPMMAXAMPLITUDE_PCC_OBLIQUE LPMMAXAMPLITUDENPPM_PCC_OBLIQUE LPMMAXAMPLITUDERPPM_PCC_OBLIQUE LPMMAXSNR_PCC_OBLIQUE LPMTRIGGERED_PCC_OBLIQUE NPPMSIZE_PCC_OBLIQUE PCCADCRATIO_PCC_OBLIQUE PCCBCKGRNDINTENSITYADC_PCC_OBLIQUE PCCNUMCLUSTEREDDEFECTS_PCC_OBLIQUE PPD_POLARITY POLARITY_PCC_OBLIQUE POSANDNEGSEPARATIONRADIALUM_PCC_OBLIQUE POSANDNEGSEPARATIONTANGENTIALUM_PCC_OBLIQUE RPPMHAZEAVERAGE_PCC_OBLIQUE RPPMSIZE_PCC_OBLIQUE SIZE_PCC_OBLIQUE SN_RATIO_PCC_OBLIQUE XNEG_PCC_OBLIQUE XPOS_PCC_OBLIQUE YNEG_PCC_OBLIQUE YPOS_PCC_OBLIQUE DEFECTSIZENEGADC DEFECTSIZEPOSADC DEFECTSIZESHE LATERALEXTENTRADIALNEGUM LATERALEXTENTRADIALPOSUM LATERALEXTENTRADIALUM LATERALEXTENTTANGENTIALNEGUM LATERALEXTENTTANGENTIALPOSUM LATERALEXTENTTANGENTIALUM PCCADCRATIO PCCBCKGRNDINTENSITYADC PCCNUMCLUSTEREDDEFECTS POSANDNEGSEPARATIONRADIALUM POSANDNEGSEPARATIONTANGENTIALUM XNEG XPOS YNEG YPOS IMAGECOUNT IMAGELIST ;\n")

        # Write defect list
        f.write("DefectList\n")
        for i in range(1, num_defects + 1):
            defect_data = [i] + [generate_random_float(0, 300000) for _ in range(2)]
            defect_data += [0, 0] + [generate_random_float(0, 1) for _ in range(3)]
            defect_data += [generate_random_float(0, 0.2), 0, generate_random_int(4, 13), 0, 0, 0, 0]
            defect_data += [generate_random_float(0, 150000) for _ in range(3)]
            defect_data += [0, 0, 0] + [generate_random_float(0, 2000) for _ in range(3)]
            defect_data += [generate_random_float(0, 1) for _ in range(3)]
            defect_data += [generate_random_float(0, 1) for _ in range(3)]
            defect_data += [generate_random_int(0, 10000) for _ in range(3)]
            defect_data += [0, 0, 0] * 4
            defect_data += [generate_random_float(0, 1000) for _ in range(170 - len(defect_data))]
            f.write(' '.join(f"{x:.6f}" if isinstance(x, float) else f"{x}" for x in defect_data) + '\n')


x = range(50)
for n in x:
    generate_klarf_file(f"files/generated_klarf-{n}.txt", random.randint(10, 150))
