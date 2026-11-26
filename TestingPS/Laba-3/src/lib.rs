//! Учебный backend магазина. Сервер хранит данные в памяти; перезапуск их очищает.
use argon2::{
    Argon2, PasswordHash, PasswordHasher, PasswordVerifier,
    password_hash::{SaltString, rand_core::OsRng},
};
use axum::{
    Json, Router,
    extract::{Path, State},
    http::{HeaderMap, StatusCode},
    routing::{delete, get, post},
};
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
    time::{Duration, Instant},
};
use tower_http::services::{ServeDir, ServeFile};
use uuid::Uuid;

type ApiError = (StatusCode, Json<Value>);
type ApiResult = Result<Json<Value>, ApiError>;

fn error(code: StatusCode, message: &str) -> ApiError {
    (code, Json(json!({"message":message})))
}

#[derive(Clone, Default)]
pub struct AppState(Arc<Mutex<Store>>);

#[derive(Default)]
struct Store {
    users: HashMap<String, User>,
    sessions: HashMap<String, (String, Instant)>,
    carts: HashMap<String, Vec<CartItem>>,
    orders: HashMap<String, Vec<Value>>,
}
struct User {
    id: String,
    password_hash: String,
}

#[derive(Clone, Serialize)]
pub struct Product {
    #[serde(rename = "_id")]
    pub id: String,
    pub title: String,
    pub price: u64,
    pub images: Vec<String>,
    pub sizes: Vec<String>,
    pub brand: String,
    pub rating: f32,
    pub reviews: String,
    pub description: String,
}

pub fn products() -> Vec<Product> {
    [
        ("p1", "Rust Hoodie", 80),
        ("p2", "Quality T-Shirt", 25),
        ("p3", "Test Engineer Backpack", 120),
    ]
    .into_iter()
    .map(|(id, title, price)| Product {
        id: id.into(),
        title: title.into(),
        price,
        images: vec!["/product.svg".into()],
        sizes: vec!["S".into(), "M".into(), "L".into(), "XL".into()],
        brand: "Moroz Studio".into(),
        rating: 4.8,
        reviews: "12".into(),
        description: "Designed for everyday work and learning.".into(),
    })
    .collect()
}

#[derive(Clone, Serialize)]
struct CartItem {
    #[serde(rename = "_id")]
    id: String,
    #[serde(rename = "productId")]
    product_id: String,
    title: String,
    price: u64,
    quantity: u32,
    img1: String,
    size: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct Credentials {
    email: String,
    password: String,
    full_name: Option<String>,
}

pub fn valid_email(email: &str) -> bool {
    email.len() <= 254
        && email.bytes().filter(|b| *b == b'@').count() == 1
        && !email.chars().any(char::is_whitespace)
        && email.split_once('@').is_some_and(|(name, domain)| {
            !name.is_empty()
                && domain.contains('.')
                && !domain.starts_with('.')
                && !domain.ends_with('.')
        })
}

fn authorized(store: &Store, headers: &HeaderMap) -> Result<String, ApiError> {
    headers
        .get("authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
        .and_then(|token| store.sessions.get(token))
        .filter(|(_, created)| created.elapsed() < Duration::from_secs(3600))
        .map(|(user, _)| user.clone())
        .ok_or_else(|| error(StatusCode::UNAUTHORIZED, "Authentication required"))
}

async fn register(
    State(state): State<AppState>,
    Json(input): Json<Credentials>,
) -> Result<(StatusCode, Json<Value>), ApiError> {
    let email = input.email.trim().to_lowercase();
    if !valid_email(&email)
        || !(8..=128).contains(&input.password.len())
        || input
            .full_name
            .as_ref()
            .is_none_or(|n| n.trim().is_empty() || n.len() > 100)
    {
        return Err(error(StatusCode::BAD_REQUEST, "Invalid registration data"));
    }
    // Дорогой Argon2 вынесен из async executor и выполняется до захвата Mutex.
    let hash = tokio::task::spawn_blocking(move || {
        Argon2::default()
            .hash_password(input.password.as_bytes(), &SaltString::generate(&mut OsRng))
            .map(|h| h.to_string())
    })
    .await
    .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Password worker failed"))?
    .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Password hashing failed"))?;
    let mut store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    if store.users.contains_key(&email) {
        return Err(error(StatusCode::CONFLICT, "Email already registered"));
    }
    store.users.insert(
        email,
        User {
            id: Uuid::new_v4().to_string(),
            password_hash: hash,
        },
    );
    Ok((
        StatusCode::CREATED,
        Json(json!({"message":"Registration successful"})),
    ))
}

async fn login(State(state): State<AppState>, Json(input): Json<Credentials>) -> ApiResult {
    let email = input.email.trim().to_lowercase();
    let (id, hash) = {
        let store = state
            .0
            .lock()
            .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
        let user = store
            .users
            .get(&email)
            .ok_or_else(|| error(StatusCode::UNAUTHORIZED, "Invalid credentials"))?;
        (user.id.clone(), user.password_hash.clone())
    };
    let verified = tokio::task::spawn_blocking(move || {
        PasswordHash::new(&hash).is_ok_and(|h| {
            Argon2::default()
                .verify_password(input.password.as_bytes(), &h)
                .is_ok()
        })
    })
    .await
    .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Password worker failed"))?;
    if !verified {
        return Err(error(StatusCode::UNAUTHORIZED, "Invalid credentials"));
    }
    let token = Uuid::new_v4().to_string();
    state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?
        .sessions
        .insert(token.clone(), (id.clone(), Instant::now()));
    Ok(Json(
        json!({"token":token,"userId":id,"message":"Login successful"}),
    ))
}

async fn logout(State(state): State<AppState>, headers: HeaderMap) -> ApiResult {
    let mut store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    authorized(&store, &headers)?;
    if let Some(token) = headers
        .get("authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
    {
        store.sessions.remove(token);
    }
    Ok(Json(json!({"message":"Logged out"})))
}

async fn list_products() -> Json<Value> {
    Json(json!(products()))
}
async fn product(Path(id): Path<String>) -> ApiResult {
    products()
        .into_iter()
        .find(|p| p.id == id)
        .map(|p| Json(json!(p)))
        .ok_or_else(|| error(StatusCode::NOT_FOUND, "Product not found"))
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct AddItem {
    product_id: String,
    quantity: u32,
    size: String,
}

async fn add_cart(
    State(state): State<AppState>,
    headers: HeaderMap,
    Json(input): Json<AddItem>,
) -> ApiResult {
    let mut store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    let user = authorized(&store, &headers)?;
    let product = products()
        .into_iter()
        .find(|p| p.id == input.product_id)
        .ok_or_else(|| error(StatusCode::NOT_FOUND, "Product not found"))?;
    if !(1..=99).contains(&input.quantity) || !product.sizes.contains(&input.size) {
        return Err(error(StatusCode::BAD_REQUEST, "Invalid quantity or size"));
    }
    let cart = store.carts.entry(user).or_default();
    if let Some(item) = cart
        .iter_mut()
        .find(|i| i.product_id == input.product_id && i.size == input.size)
    {
        if item.quantity + input.quantity > 99 {
            return Err(error(StatusCode::BAD_REQUEST, "Quantity limit exceeded"));
        }
        item.quantity += input.quantity;
    } else {
        cart.push(CartItem {
            id: Uuid::new_v4().to_string(),
            product_id: product.id,
            title: product.title,
            price: product.price,
            quantity: input.quantity,
            img1: product.images[0].clone(),
            size: input.size,
        });
    }
    Ok(Json(json!({"message":"Added to cart"})))
}

async fn cart(State(state): State<AppState>, headers: HeaderMap) -> ApiResult {
    let store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    let user = authorized(&store, &headers)?;
    Ok(Json(json!(
        store.carts.get(&user).cloned().unwrap_or_default()
    )))
}

async fn remove_cart(
    State(state): State<AppState>,
    headers: HeaderMap,
    Path(id): Path<String>,
) -> ApiResult {
    let mut store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    let user = authorized(&store, &headers)?;
    let cart = store.carts.entry(user).or_default();
    let index = cart
        .iter()
        .position(|i| i.id == id)
        .ok_or_else(|| error(StatusCode::NOT_FOUND, "Cart item not found"))?;
    cart.remove(index);
    Ok(Json(json!({"message":"Item removed"})))
}

pub fn order_total(items: &[(u64, u32)]) -> Option<u64> {
    items.iter().try_fold(0_u64, |sum, (price, quantity)| {
        sum.checked_add(price.checked_mul(u64::from(*quantity))?)
    })
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct OrderInput {
    shipping_address: String,
}

async fn create_order(
    State(state): State<AppState>,
    headers: HeaderMap,
    Json(input): Json<OrderInput>,
) -> Result<(StatusCode, Json<Value>), ApiError> {
    let mut store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    let user = authorized(&store, &headers)?;
    if !(5..=500).contains(&input.shipping_address.trim().len()) {
        return Err(error(StatusCode::BAD_REQUEST, "Invalid shipping address"));
    }
    let cart = store.carts.get(&user).cloned().unwrap_or_default();
    if cart.is_empty() {
        return Err(error(StatusCode::CONFLICT, "Cart is empty"));
    }
    let total = order_total(
        &cart
            .iter()
            .map(|i| (i.price, i.quantity))
            .collect::<Vec<_>>(),
    )
    .ok_or_else(|| error(StatusCode::BAD_REQUEST, "Total overflow"))?;
    let order = json!({"_id":Uuid::new_v4().to_string(),"products":cart,"totalPrice":total,"shippingAddress":input.shipping_address.trim(),"paymentStatus":"Pending","orderStatus":"Pending"});
    store
        .orders
        .entry(user.clone())
        .or_default()
        .push(order.clone());
    store.carts.remove(&user);
    Ok((StatusCode::CREATED, Json(order)))
}

async fn orders(State(state): State<AppState>, headers: HeaderMap) -> ApiResult {
    let store = state
        .0
        .lock()
        .map_err(|_| error(StatusCode::INTERNAL_SERVER_ERROR, "Store unavailable"))?;
    let user = authorized(&store, &headers)?;
    Ok(Json(json!(
        store.orders.get(&user).cloned().unwrap_or_default()
    )))
}

pub fn app(state: AppState) -> Router {
    Router::new()
        .route(
            "/api/health",
            get(|| async { Json(json!({"status":"ok"})) }),
        )
        .route("/api/users/register", post(register))
        .route("/api/users/login", post(login))
        .route("/api/users/logout", post(logout))
        .route("/api/products", get(list_products))
        .route("/api/products/{id}", get(product))
        .route("/api/cart", get(cart))
        .route("/api/cart/add", post(add_cart))
        .route("/api/cart/remove/{id}", delete(remove_cart))
        .route("/api/orders/create", post(create_order))
        .route("/api/orders/get", get(orders))
        .route(
            "/api/{*path}",
            get(|| async { error(StatusCode::NOT_FOUND, "API endpoint not found") })
                .post(|| async { error(StatusCode::NOT_FOUND, "API endpoint not found") }),
        )
        .fallback_service(
            ServeDir::new("TestingPS/Laba-3/frontend/dist")
                .fallback(ServeFile::new("TestingPS/Laba-3/frontend/dist/index.html")),
        )
        .layer(axum::extract::DefaultBodyLimit::max(16 * 1024))
        .with_state(state)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn total_empty() {
        assert_eq!(order_total(&[]), Some(0));
    }
    #[test]
    fn total_multiple() {
        assert_eq!(order_total(&[(80, 2), (25, 3)]), Some(235));
    }
    #[test]
    fn total_overflow_multiply() {
        assert_eq!(order_total(&[(u64::MAX, 2)]), None);
    }
    #[test]
    fn total_overflow_sum() {
        assert_eq!(order_total(&[(u64::MAX, 1), (1, 1)]), None);
    }
    #[test]
    fn catalog_has_unique_ids_and_positive_prices() {
        let catalog = products();
        let ids: std::collections::HashSet<_> = catalog.iter().map(|p| &p.id).collect();
        assert_eq!(catalog.len(), ids.len());
        assert!(catalog.iter().all(|p| p.price > 0 && !p.sizes.is_empty()));
    }
    #[test]
    fn email_valid() {
        for e in ["qa@example.test", "a+b@sub.example.test"] {
            assert!(valid_email(e));
        }
    }
    #[test]
    fn email_invalid() {
        for e in ["", "@a.b", "a@b", "a@.b", "a@b.", "a b@a.b", "a@b@c.d"] {
            assert!(!valid_email(e));
        }
    }
    #[test]
    fn expired_session_rejected() {
        let mut store = Store::default();
        store.sessions.insert(
            "expired".into(),
            ("user".into(), Instant::now() - Duration::from_secs(3601)),
        );
        let mut headers = HeaderMap::new();
        headers.insert("authorization", "Bearer expired".parse().unwrap());
        assert!(authorized(&store, &headers).is_err());
    }
}
