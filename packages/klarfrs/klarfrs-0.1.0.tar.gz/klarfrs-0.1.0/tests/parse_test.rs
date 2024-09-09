use std::path::PathBuf;
use klarf_data::{KlarfData, parse};

#[test]
fn test_parse_klarf_file() {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("klarf01.txt");
    
    let result = parse(path.to_str().unwrap()).unwrap();

    println!("Parsed KlarfData: {:#?}", result); // Debug print

    // Update these assertions based on the content of klarf01.txt
    assert_eq!(result.file_version, "1 2");
    assert_eq!(result.file_timestamp, "08-12-24 23:41:25");
    assert_eq!(result.inspection_station_id, vec!["KLA-Tencor", "SP7", "SP7-61"]);
    assert_eq!(result.sample_type, "WAFER");
    assert_eq!(result.result_timestamp, "08-12-24 23:40:18");
    assert_eq!(result.lot_id, "MBXJA-0P018760EP7R205J");
    assert_eq!(result.sample_size, vec![1, 300]);
    assert_eq!(result.setup_id, vec!["EP7R2XXX", "08-12-24 23:20:53"]);
    assert_eq!(result.step_id, "EP7R2XXX");
    assert_eq!(result.wafer_id, "BW0835606546");
    assert_eq!(result.slot, 2);

    // Check DefectRecordSpec
    assert_eq!(result.defect_record_spec[0], "DEFECTID");
    assert_eq!(result.defect_record_spec[1], "XREL");
    assert_eq!(result.defect_record_spec[2], "YREL");
    // ... add more assertions for other fields ...

    // Check first defect in DefectList
    let first_defect = &result.defect_list[0];
    assert_eq!(first_defect.get("DEFECTID"), Some(&1.0));
    assert_eq!(first_defect.get("XREL"), Some(&12041.0));
    assert_eq!(first_defect.get("YREL"), Some(&149816.184));
    // ... add more assertions for other fields ...
}