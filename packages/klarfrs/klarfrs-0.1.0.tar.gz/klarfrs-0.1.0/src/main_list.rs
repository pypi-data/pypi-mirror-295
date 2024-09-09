use std::str::FromStr;

#[derive(Debug)]
struct DefectRecord {
    defect_id: i32,
    xrel: f64,
    yrel: f64,
    xindex: i32,
    yindex: i32,
    xsize: f64,
    ysize: f64,
    defect_area: f64,
    dsize: f64,
    class_number: i32,
    test: i32,
    cluster_number: i32,
    rough_bin_number: i32,
    fine_bin_number: i32,
    review_sample: i32,
    adc_size: f64,
}

fn parse_defect_records(input: &str) -> Result<Vec<DefectRecord>, Box<dyn std::error::Error>> {
    let mut records = Vec::new();
    let lines: Vec<&str> = input.lines().collect();

    let data_start = lines.iter().position(|&line| line.trim() == "DefectList").ok_or("DefectList not found")?;

    for line in &lines[data_start + 1..] {
        if line.trim().is_empty() {
            continue;
        }

        let fields: Vec<&str> = line.split_whitespace().collect();
        if fields.len() < 19 {
            return Err(format!("Invalid record format: expected 170 fields, got {}", fields.len()).into());
        }

        let record = DefectRecord {
            defect_id: i32::from_str(fields[0])?,
            xrel: f64::from_str(fields[1])?,
            yrel: f64::from_str(fields[2])?,
            xindex: i32::from_str(fields[3])?,
            yindex: i32::from_str(fields[4])?,
            xsize: f64::from_str(fields[5])?,
            ysize: f64::from_str(fields[6])?,
            defect_area: f64::from_str(fields[7])?,
            dsize: f64::from_str(fields[8])?,
            class_number: i32::from_str(fields[9])?,
            test: i32::from_str(fields[10])?,
            cluster_number: i32::from_str(fields[11])?,
            rough_bin_number: i32::from_str(fields[12])?,
            fine_bin_number: i32::from_str(fields[13])?,
            review_sample: i32::from_str(fields[14])?,
            adc_size: f64::from_str(fields[15])?,
        };

        records.push(record);
    }

    Ok(records)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input = r#"DefectRecordSpec 170 DEFECTID XREL YREL ...
DefectList
1 12041.000 149816.184 0 0 0.000 0.000 0.000000 0.020 0 6 0 0 0 0 67.084091 ... 0 0
2 48513.813 240323.265 0 0 0.000 0.000 0.000000 0.160 0 6 0 0 0 0 105033.476562 ... 0 0
3 33093.649 169451.783 0 0 0.000 0.000 0.000000 0.042 0 6 0 0 0 0 208.075806 ... 0 0"#;

    let records = parse_defect_records(input)?;
    
    for (index, record) in records.iter().enumerate() {
        println!("Record {}: {:?}", index + 1, record);
    }

    Ok(())
}