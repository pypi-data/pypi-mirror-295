use std::collections::HashMap;
use std::path::Path;

use pyo3::prelude::*;
use pyo3::types::PyType;

use crate::datamodel;
use crate::exporters::Templates;

#[pyclass]
pub struct DataModel {
    pub model: datamodel::DataModel,
}

#[pymethods]
impl DataModel {
    #[classmethod]
    fn from_markdown(cls: &Bound<'_, PyType>, path: String) -> PyResult<Self> {
        Ok(Self {
            model: datamodel::DataModel::from_markdown(Path::new(&path)).unwrap(),
        })
    }

    fn __repr__(&self) -> String {
        self.model.sdrdm_schema()
    }

    fn convert_to(&mut self, template: Templates, config: Option<HashMap<String, String>>) -> String {
        let config = config.unwrap_or_default();
        self.model.convert_to(&template, Some(&config)).expect("Failed to convert to template")
    }
}
