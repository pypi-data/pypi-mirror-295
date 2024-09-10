use pyo3::prelude::*;

use crate::exporters::Templates;
use crate::python::bindings;

pub mod datamodel;
pub mod exporters;
pub mod pipeline;
pub mod validation;

pub(crate) mod attribute;
pub(crate) mod object;
pub(crate) mod primitives;
pub(crate) mod schema;
pub(crate) mod xmltype;

pub(crate) mod json {
    mod datatype;
    pub(crate) mod parser;
}

pub(crate) mod markdown {
    pub(crate) mod frontmatter;
    pub(crate) mod parser;
}

pub mod python {
    pub(crate) mod bindings;
}

#[pymodule]
fn mdmodels_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<bindings::DataModel>()?;
    m.add_class::<Templates>()?;
    Ok(())
}
