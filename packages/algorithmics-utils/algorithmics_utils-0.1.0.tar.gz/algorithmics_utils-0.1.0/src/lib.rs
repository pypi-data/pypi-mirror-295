use pyo3::prelude::*;
use pyo3::types::PyFunction;
use pyo3::types::PyDict;
use pyo3::wrap_pyfunction;
use rand::Rng;
use std::time::Instant;

/// https://stackoverflow.com/questions/59164456/how-do-i-return-an-array-from-a-rust-function
#[pyfunction]
#[pyo3(text_signature = "(size, range_start, range_end)")]
fn generate_list(size: usize, range_start: i32, range_end: i32) -> PyResult<Vec<i32>> {
    let mut rng = rand::thread_rng();
    let mut vec = Vec::with_capacity(size);
    for _ in 0..size {
        vec.push(rng.gen_range(range_start..range_end+1));
    }
    Ok(vec)
}

/// Timing function
#[pyfunction]
#[pyo3(signature = (repeat, func, **kwargs))]
fn time_function(py: Python, repeat: u128, func: Py<PyFunction>, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<u128> {

    let mut total: u128 = 0;

    for _ in 0..repeat {
        let now: Instant = Instant::now();
        func.call_bound(py, (), kwargs)?;
        total += now.elapsed().as_millis();
    }
    let average: u128 = total / repeat;
    Ok(average)
}

/// A Python module implemented in Rust with random OS things.
#[pymodule]
fn algo_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_list, m)?)?;
    m.add_function(wrap_pyfunction!(time_function, m)?)?;
    Ok(())
}
