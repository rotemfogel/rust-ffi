use pyo3::prelude::*;
use rayon::prelude::*;

fn search_line(line: &str, needle: &str) -> usize {
    let mut total: usize = 0;
    for word in line.split(' ') {
        if word == needle {
            total += 1;
        }
    }
    total
}

#[pyfunction]
fn search_rs(contents: &str, needle: &str) -> PyResult<usize> {
    Ok(contents.lines().map(|line| search_line(line, needle)).sum())
}

#[pyfunction]
fn par_search_rs(contents: &str, needle: &str) -> PyResult<usize> {
    Ok(contents
        .par_lines()
        .map(|line| search_line(line, needle))
        .sum())
}
/// A Python module implemented in Rust.
#[pymodule]
fn rust_ffi(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search_rs, m)?)?;
    m.add_function(wrap_pyfunction!(par_search_rs, m)?)?;
    Ok(())
}
