use std::process::Command;

fn main() {
    println!("cargo:rerun-if-changed=build.rs");

    // Get Python configuration
    let python_config = Command::new("python3-config")
        .arg("--ldflags")
        .arg("--embed")
        .output()
        .expect("Failed to execute python3-config");

    let python_ldflags = String::from_utf8_lossy(&python_config.stdout);
    println!("Python ldflags: {}", python_ldflags);

    // Extract library path and name
    for flag in python_ldflags.split_whitespace() {
        if flag.starts_with("-L") {
            println!("cargo:rustc-link-search=native={}", &flag[2..]);
        } else if flag.starts_with("-l") {
            println!("cargo:rustc-link-lib={}", &flag[2..]);
        }
    }

    // Add PyO3 extension module link args
    pyo3_build_config::add_extension_module_link_args();

}