use std::sync::Arc;

use kv::*;
use parking_lot::Mutex;
use tauri::AppHandle;

pub fn get_kv_bucket<T: Value>(
    app_handle: AppHandle,
    namespace: String,
    name: String,
) -> Result<Bucket<'static, String, T>, String> {
    let app_dir = match app_handle.path_resolver().app_data_dir() {
        Some(dir) => dir.to_owned(),
        None => return Err(String::from("Could not get app data dir.")),
    };
    let storage_path = app_dir.join(namespace).to_string_lossy().to_string();

    let cfg = Config::new(storage_path);
    let store =
        Store::new(cfg).map_err(|err| format!("Could not create storage bucket: {}", err))?;

    store
        .bucket::<String, T>(Some(&name))
        .map_err(|err| format!("Could not get bucket: {}", err))
}

pub type StateBucket<T> = Arc<Mutex<Bucket<'static, String, T>>>;

pub fn get_state_json<T: kv::Value>(bucket_arc: &StateBucket<T>, key: &String) -> T {
    bucket_arc.clone().lock().get(key).unwrap().unwrap()
}

pub async fn remove_data<T: kv::Value>(
    bucket_arc: &StateBucket<T>,
    path: &str,
) -> Result<(), String> {
    let bucket = bucket_arc.lock();
    let file_path = String::from(path);
    bucket.remove(&file_path).map_err(|e| format!("{}", e))?;
    bucket.flush().map_err(|e| format!("{}", e))?;
    Ok(())
}
