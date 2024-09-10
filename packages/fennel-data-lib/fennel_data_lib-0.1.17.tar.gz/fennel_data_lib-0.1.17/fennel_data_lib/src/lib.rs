use std::sync::Arc;
use arrow::record_batch::RecordBatch;
use arrow::pyarrow::ToPyArrow;
use arrow::pyarrow::FromPyArrow;
use anyhow::{bail, Result};
pub mod schema_proto;
pub mod arrow_lib;
pub mod df;
pub mod expr;
pub mod primitive;
pub mod rowcol;
pub mod schema;
pub mod testutils;
pub mod types;
pub mod value;
mod debezium;

pub use {
    arrow_lib::{
        deserialize_recordbatch, from_arrow_array, from_arrow_recordbatch, serialize_recordbatch,
        to_arrow_array, to_arrow_dtype, to_arrow_field, to_arrow_recordbatch, to_arrow_schema,
    },
    df::Dataframe,
    expr::{BinOp, CompiledExpr, Expr, UnOp},
    rowcol::{Col, Row},
    schema::{DSSchema, Field, Schema},
    types::Type,
    value::{List, Map, UTCTimestamp, Value},
};
pub use rowcol::{BoolSeries, TSSeries};
pub use testutils::DSSchemaBuilder;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use pyo3::types::{PyString, PyBytes, PyDict, PyBool};
use crate::schema_proto::expr::Expr as ProtoExpr;
use prost::{DecodeError, Message};
use crate::schema_proto::schema::DataType as ProtoType;

fn decode_expr(request_bytes: &[u8]) -> Result<Expr> {
    let decode_expr: Result<ProtoExpr, DecodeError> = Message::decode(request_bytes);
    if let Err(err) = decode_expr {
        bail!("failed to decode expression to proto: {}", err);
    }
    let decode_expr = decode_expr.unwrap();
    let expr: anyhow::Result<Expr> = decode_expr.try_into();
    if let Err(err) = expr {
        bail!("failed to convert proto expression to fennel expression: {}", err);
    }
    Ok(expr.unwrap())

}


/// Decode a schema from a dictionary of field names to serialized types.
/// The dictionary should be a dictionary of strings to bytes.
/// The bytes should be a serialized ProtoType.
/// Optionally, a list of columns can be provided to filter the schema to only include
/// fields that are in the list.
fn decode_schema(dict: &PyDict, columns: &[String]) -> Result<Schema> {
    let fields = dict.into_iter().map(|(key, value)| {
        // Key, val is dictionary of field name and dtype serialized to bytes. Unwrapping
        // is safe here because we know the types are correct.
        let key = key.downcast::<PyString>().unwrap().to_string();
        let dtype_bytes = value.downcast::<PyBytes>().unwrap();
        let dtype: Result<ProtoType, DecodeError>  = Message::decode(dtype_bytes.as_bytes());
        if dtype.is_err() {
            bail!("failed to decode dtype: {}", dtype.unwrap_err()); 
        }
        let dtype = dtype.unwrap();
        let dtype = Type::try_from(dtype)?;
        Ok(Field::new(key, dtype))
    }).collect::<Vec<Result<Field>>>();
    let fields = fields.into_iter().collect::<Result<Vec<Field>>>()?;
    if columns.is_empty() {
        return Schema::new(fields);
    }
    let fields = fields.into_iter().filter(|field| columns.contains(&field.name().to_string())).collect::<Vec<Field>>();
    Schema::new(fields)
}


#[pyfunction]
fn eval(py: Python, expr_bytes: &PyBytes, df: PyObject, dict: &PyDict) -> PyResult<PyObject> {
    let request_bytes: &[u8] = expr_bytes.as_bytes();
    let expr = decode_expr(request_bytes);
    if expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode expression: {}", expr.unwrap_err())));
    }
    let expr = expr.unwrap();

    let record_batch = RecordBatch::from_pyarrow(df.as_ref(py))?;
    let columns: Vec<String> = record_batch.schema().fields().iter().map(|field| field.name().clone()).collect();
    let schema = decode_schema(dict, &columns);
    if schema.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode schema: {}", schema.unwrap_err())));
    }
    let df = from_arrow_recordbatch(Arc::new(schema.unwrap()), &record_batch);
    if df.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert record batch to dataframe {}", df.unwrap_err())));
    }
    let df = df.unwrap();

    let compiled_expr = expr.compile(df.schema().clone());
    if compiled_expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to compile expression: {}", compiled_expr.unwrap_err())));
    }
    let compiled_expr = compiled_expr.unwrap();

    let col = df.eval(&compiled_expr, compiled_expr.dtype().clone(), "output");
    if col.is_err() {
        return Err(PyValueError::new_err(format!("Failed to evaluate expression: {}", col.unwrap_err())));
    }
    let col = col.unwrap();
    let arrow_col = to_arrow_array(col.values(), col.dtype(), col.dtype().is_nullable())
    .map_err(|err| {
        PyValueError::new_err(format!(
            "failed to convert column to arrow array: {}",
            err
        ))
    })?
    .to_data()
    .to_pyarrow(py);
    if arrow_col.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert column to pyarrow: {}", arrow_col.unwrap_err())));
    }
    Ok(arrow_col.unwrap())

}


// Assign is very similar to eval, the main difference is that it takes the output dtype to cast the output to the correct type. 
#[pyfunction]
fn assign(py: Python, expr_bytes: &PyBytes, df: PyObject, dict: &PyDict, type_bytes: &PyBytes) -> PyResult<PyObject> {
    let request_bytes: &[u8] = expr_bytes.as_bytes();
    let expr = decode_expr(request_bytes);
    if expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode expression: {}", expr.unwrap_err())));
    }
    let expr = expr.unwrap();

    let record_batch = RecordBatch::from_pyarrow(df.as_ref(py))?;
    let columns: Vec<String> = record_batch.schema().fields().iter().map(|field| field.name().clone()).collect();
    let schema = decode_schema(dict, &columns);
    if schema.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode schema: {}", schema.unwrap_err())));
    }
    let df = from_arrow_recordbatch(Arc::new(schema.unwrap()), &record_batch);
    if df.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert record batch to dataframe {}", df.unwrap_err())));
    }
    let df = df.unwrap();

    let type_bytes: &[u8] = type_bytes.as_bytes();
    let dtype: Result<ProtoType, DecodeError> = Message::decode(type_bytes);
    if dtype.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode dtype: {}", dtype.unwrap_err())));
    }
    let dtype = dtype.unwrap();
    let dtype = Type::try_from(dtype);
    if dtype.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert dtype: {}", dtype.unwrap_err())));
    }
    let dtype = dtype.unwrap();

    let compiled_expr = expr.compile(df.schema().clone());
    if compiled_expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to compile expression: {}", compiled_expr.unwrap_err())));
    }
    let compiled_expr = compiled_expr.unwrap();

    let col = df.eval(&compiled_expr, dtype, "output");
    if col.is_err() {
        return Err(PyValueError::new_err(format!("Failed to evaluate expression: {}", col.unwrap_err())));
    }
    let col = col.unwrap();
    let arrow_col = to_arrow_array(col.values(), col.dtype(), col.dtype().is_nullable())
    .map_err(|err| {
        PyValueError::new_err(format!(
            "failed to convert column to arrow array: {}",
            err
        ))
    })?
    .to_data()
    .to_pyarrow(py);
    if arrow_col.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert column to pyarrow: {}", arrow_col.unwrap_err())));
    }
    Ok(arrow_col.unwrap())

}


#[pyfunction]
fn type_of<'a>(py: Python<'a>, expr_bytes: &'a PyBytes, dict: &'a PyDict) -> PyResult<&'a PyBytes> {    
    let request_bytes: &[u8] = expr_bytes.as_bytes();
    let expr = decode_expr(request_bytes);
    if expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode expression: {}", expr.unwrap_err())));
    }
    let expr = expr.unwrap();

    let schema = decode_schema(dict, &[]);
    if schema.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode schema: {}", schema.unwrap_err())));
    }
    let compiled_expr = expr.compile(Arc::new(schema.unwrap()));
    if compiled_expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to compile expression: {}", compiled_expr.unwrap_err())));
    }
    let compiled_expr = compiled_expr.unwrap();
    let proto_type: ProtoType = compiled_expr.dtype().into(); 
    let mut bytes = Vec::new();
    proto_type.encode(&mut bytes).map_err(|err| {
        PyValueError::new_err(format!("Failed to encode dtype: {}", err))
    })?;
    Ok(PyBytes::new(py, &bytes))
}

/// Check if the expression matches the provided type.
#[pyfunction]
fn matches<'a>(py: Python<'a>, expr_bytes: &'a PyBytes, dict: &'a PyDict, type_bytes: &'a PyBytes) -> PyResult<&'a PyBool> { 
    let request_bytes: &[u8] = expr_bytes.as_bytes();
    let expr = decode_expr(request_bytes);
    if expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode expression: {}", expr.unwrap_err())));
    }
    let expr = expr.unwrap();

    let schema = decode_schema(dict, &[]);
    if schema.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode schema: {}", schema.unwrap_err())));
    }

    let compiled_expr = expr.compile(Arc::new(schema.unwrap()));
    if compiled_expr.is_err() {
        return Err(PyValueError::new_err(format!("Failed to compile expression: {}", compiled_expr.unwrap_err())));
    }
    let compiled_expr = compiled_expr.unwrap();

    let type_bytes: &[u8] = type_bytes.as_bytes();
    let dtype: Result<ProtoType, DecodeError> = Message::decode(type_bytes);
    if dtype.is_err() {
        return Err(PyValueError::new_err(format!("Failed to decode dtype: {}", dtype.unwrap_err())));
    }
    let dtype = dtype.unwrap();
    let dtype = Type::try_from(dtype);
    if dtype.is_err() {
        return Err(PyValueError::new_err(format!("Failed to convert dtype: {}", dtype.unwrap_err())));
    }
    let dtype = dtype.unwrap();

    let compatible_dtype = compiled_expr.matches(&dtype); 
    Ok(PyBool::new(py, compatible_dtype))
}

/// A Python module implemented in Rust.
#[pymodule]
fn fennel_data_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(eval, m)?)?;
    m.add_function(wrap_pyfunction!(type_of, m)?)?;
    m.add_function(wrap_pyfunction!(matches, m)?)?;
    m.add_function(wrap_pyfunction!(assign, m)?)?;
    Ok(())
}