//! Интеграция HTTP routing, сериализации, авторизации и хранилища без TCP/mock.
use axum::{
    Router,
    body::Body,
    http::{Request, StatusCode},
};
use http_body_util::BodyExt;
use moroz_shop::{AppState, app};
use serde_json::{Value, json};
use tower::ServiceExt;

async fn call(
    app: &Router,
    method: &str,
    path: &str,
    body: Value,
    token: &str,
) -> (StatusCode, Value) {
    let mut request = Request::builder()
        .method(method)
        .uri(path)
        .header("content-type", "application/json");
    if !token.is_empty() {
        request = request.header("authorization", format!("Bearer {token}"));
    }
    let response = app
        .clone()
        .oneshot(request.body(Body::from(body.to_string())).unwrap())
        .await
        .unwrap();
    let status = response.status();
    let bytes = response.into_body().collect().await.unwrap().to_bytes();
    (
        status,
        serde_json::from_slice(&bytes).unwrap_or_else(|_| json!(String::from_utf8_lossy(&bytes))),
    )
}
async fn user(app: &Router, email: &str) -> String {
    assert_eq!(
        call(
            app,
            "POST",
            "/api/users/register",
            json!({"fullName":"Roman Moroz", "email":email,"password":"StrongPass!123"}),
            ""
        )
        .await
        .0,
        StatusCode::CREATED
    );
    let (status, data) = call(
        app,
        "POST",
        "/api/users/login",
        json!({"email":email,"password":"StrongPass!123"}),
        "",
    )
    .await;
    assert_eq!(status, StatusCode::OK);
    data["token"].as_str().unwrap().into()
}
fn item(quantity: u32) -> Value {
    json!({"productId":"p1","quantity":quantity,"size":"M","price":1,"userId":"attacker"})
}

#[tokio::test]
async fn health_and_catalog() {
    let app = app(AppState::default());
    assert_eq!(
        call(&app, "GET", "/api/health", Value::Null, "").await.1["status"],
        "ok"
    );
    let (status, data) = call(&app, "GET", "/api/products", Value::Null, "").await;
    assert_eq!(status, StatusCode::OK);
    assert_eq!(data.as_array().unwrap().len(), 3);
    assert_eq!(
        call(&app, "GET", "/api/products/p1", Value::Null, "")
            .await
            .1["price"],
        80
    );
    assert_eq!(
        call(&app, "GET", "/api/products/missing", Value::Null, "")
            .await
            .0,
        StatusCode::NOT_FOUND
    );
}
#[tokio::test]
async fn registration_rejects_invalid_input() {
    let app = app(AppState::default());
    for data in [
        json!({"email":"bad","password":"StrongPass!123","fullName":"QA"}),
        json!({"email":"qa@a.b","password":"short","fullName":"QA"}),
        json!({"email":"qa@a.b","password":"StrongPass!123","fullName":" "}),
        json!({"email":"qa@a.b","password":"StrongPass!123"}),
    ] {
        assert_eq!(
            call(&app, "POST", "/api/users/register", data, "").await.0,
            StatusCode::BAD_REQUEST
        );
    }
}
#[tokio::test]
async fn duplicate_email_is_case_insensitive() {
    let app = app(AppState::default());
    user(&app, "qa@example.test").await;
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/users/register",
            json!({"email":" QA@EXAMPLE.TEST ","password":"StrongPass!123","fullName":"QA"}),
            ""
        )
        .await
        .0,
        StatusCode::CONFLICT
    );
}
#[tokio::test]
async fn wrong_and_unknown_credentials() {
    let app = app(AppState::default());
    user(&app, "qa@example.test").await;
    for email in ["qa@example.test", "unknown@example.test"] {
        assert_eq!(
            call(
                &app,
                "POST",
                "/api/users/login",
                json!({"email":email,"password":"incorrect"}),
                ""
            )
            .await
            .0,
            StatusCode::UNAUTHORIZED
        );
    }
}
#[tokio::test]
async fn protected_resources_require_token() {
    let app = app(AppState::default());
    for token in ["", "invalid"] {
        for (method, path, body) in [
            ("GET", "/api/cart", Value::Null),
            ("POST", "/api/cart/add", item(1)),
            ("DELETE", "/api/cart/remove/missing", Value::Null),
            (
                "POST",
                "/api/orders/create",
                json!({"shippingAddress":"Test address"}),
            ),
            ("GET", "/api/orders/get", Value::Null),
            ("POST", "/api/users/logout", Value::Null),
        ] {
            assert_eq!(
                call(&app, method, path, body, token).await.0,
                StatusCode::UNAUTHORIZED
            );
        }
    }
}
#[tokio::test]
async fn checkout_uses_server_prices_and_clears_cart() {
    let app = app(AppState::default());
    let token = user(&app, "qa@example.test").await;
    assert_eq!(
        call(&app, "POST", "/api/cart/add", item(2), &token).await.0,
        StatusCode::OK
    );
    let (status, order) = call(
        &app,
        "POST",
        "/api/orders/create",
        json!({"shippingAddress":"Test street 10","totalPrice":1,"paymentStatus":"Paid"}),
        &token,
    )
    .await;
    assert_eq!(status, StatusCode::CREATED);
    assert_eq!(order["totalPrice"], 160);
    assert_eq!(order["paymentStatus"], "Pending");
    assert_eq!(
        call(&app, "GET", "/api/cart", Value::Null, &token).await.1,
        json!([])
    );
    let history = call(&app, "GET", "/api/orders/get", Value::Null, &token)
        .await
        .1;
    assert_eq!(history.as_array().unwrap().len(), 1);
    assert_eq!(history[0], order);
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/orders/create",
            json!({"shippingAddress":"Test street 10"}),
            &token
        )
        .await
        .0,
        StatusCode::CONFLICT
    );
}
#[tokio::test]
async fn cart_and_orders_are_isolated_by_session() {
    let app = app(AppState::default());
    let a = user(&app, "a@example.test").await;
    let b = user(&app, "b@example.test").await;
    call(&app, "POST", "/api/cart/add", item(1), &a).await;
    let cart_a = call(&app, "GET", "/api/cart", Value::Null, &a).await.1;
    assert_eq!(
        call(&app, "GET", "/api/cart", Value::Null, &b).await.1,
        json!([])
    );
    let foreign_id = cart_a[0]["_id"].as_str().unwrap();
    assert_eq!(
        call(
            &app,
            "DELETE",
            &format!("/api/cart/remove/{foreign_id}"),
            Value::Null,
            &b
        )
        .await
        .0,
        StatusCode::NOT_FOUND
    );
    call(
        &app,
        "POST",
        "/api/orders/create",
        json!({"shippingAddress":"Test street 10"}),
        &a,
    )
    .await;
    assert_eq!(
        call(&app, "GET", "/api/orders/get", Value::Null, &b)
            .await
            .1,
        json!([])
    );
}
#[tokio::test]
async fn quantity_size_and_missing_product() {
    let app = app(AppState::default());
    let token = user(&app, "qa@example.test").await;
    for q in [0, 100, u32::MAX] {
        assert_eq!(
            call(&app, "POST", "/api/cart/add", item(q), &token).await.0,
            StatusCode::BAD_REQUEST
        );
    }
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/cart/add",
            json!({"productId":"p1","quantity":1,"size":"XXXL"}),
            &token
        )
        .await
        .0,
        StatusCode::BAD_REQUEST
    );
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/cart/add",
            json!({"productId":"missing","quantity":1,"size":"M"}),
            &token
        )
        .await
        .0,
        StatusCode::NOT_FOUND
    );
    call(&app, "POST", "/api/cart/add", item(98), &token).await;
    assert_eq!(
        call(&app, "POST", "/api/cart/add", item(2), &token).await.0,
        StatusCode::BAD_REQUEST
    );
    assert_eq!(
        call(&app, "POST", "/api/cart/add", item(1), &token).await.0,
        StatusCode::OK
    );
    assert_eq!(
        call(&app, "GET", "/api/cart", Value::Null, &token).await.1[0]["quantity"],
        99
    );
}
#[tokio::test]
async fn remove_item_and_validate_address() {
    let app = app(AppState::default());
    let token = user(&app, "qa@example.test").await;
    call(&app, "POST", "/api/cart/add", item(1), &token).await;
    for address in [" ".to_string(), "x".repeat(501)] {
        assert_eq!(
            call(
                &app,
                "POST",
                "/api/orders/create",
                json!({"shippingAddress":address}),
                &token
            )
            .await
            .0,
            StatusCode::BAD_REQUEST
        );
    }
    let cart = call(&app, "GET", "/api/cart", Value::Null, &token).await.1;
    let path = format!("/api/cart/remove/{}", cart[0]["_id"].as_str().unwrap());
    assert_eq!(
        call(&app, "DELETE", &path, Value::Null, &token).await.0,
        StatusCode::OK
    );
    assert_eq!(
        call(&app, "DELETE", &path, Value::Null, &token).await.0,
        StatusCode::NOT_FOUND
    );
    assert_eq!(
        call(&app, "GET", "/api/cart", Value::Null, &token).await.1,
        json!([])
    );
}
#[tokio::test]
async fn logout_revokes_token() {
    let app = app(AppState::default());
    let token = user(&app, "qa@example.test").await;
    assert_eq!(
        call(&app, "POST", "/api/users/logout", Value::Null, &token)
            .await
            .0,
        StatusCode::OK
    );
    assert_eq!(
        call(&app, "GET", "/api/cart", Value::Null, &token).await.0,
        StatusCode::UNAUTHORIZED
    );
}
#[tokio::test]
async fn malformed_json_and_wrong_types() {
    let app = app(AppState::default());
    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/users/register")
                .header("content-type", "application/json")
                .body(Body::from("{broken"))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/users/register",
            json!({"email":42,"password":"StrongPass!123"}),
            ""
        )
        .await
        .0,
        StatusCode::UNPROCESSABLE_ENTITY
    );
    assert_eq!(
        call(
            &app,
            "POST",
            "/api/cart/add",
            json!({"productId":"p1","quantity":-1,"size":"M"}),
            ""
        )
        .await
        .0,
        StatusCode::UNPROCESSABLE_ENTITY
    );
}

#[tokio::test]
async fn oversized_body_and_unknown_api_are_rejected() {
    let app = app(AppState::default());
    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/api/users/register")
                .header("content-type", "application/json")
                .body(Body::from(
                    json!({"email":"qa@example.test","password":"x".repeat(17000),"fullName":"QA"})
                        .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::PAYLOAD_TOO_LARGE);
    assert_eq!(
        call(&app, "GET", "/api/unknown", Value::Null, "").await.0,
        StatusCode::NOT_FOUND
    );
    assert_eq!(
        call(&app, "POST", "/api/unknown", json!({}), "").await.0,
        StatusCode::NOT_FOUND
    );
}
