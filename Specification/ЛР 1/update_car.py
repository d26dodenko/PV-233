def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    if car.brand_id:
        brand = db.query(Brand).filter(Brand.id == car.brand_id).first()
        if not brand:
            raise HTTPException(status_code=400, detail="Brand not found")
        db_car.brand_id = car.brand_id
    if car.model_id:
        model = db.query(Model).filter(Model.id == car.model_id).first()
        if not model:
            raise HTTPException(status_code=400, detail="Model not found")
        db_car.model_id = car.model_id
    if car.parking_id:
        parking = db.query(Parking).filter(Parking.id == car.parking_id).first()
        if not parking:
            raise HTTPException(status_code=400, detail="Parking not found")
        db_car.parking_id = car.parking_id
    db_car.year = car.year
    db_car.color = car.color
    db_car.plate = car.plate
    db_car.price = car.price
    db.commit()
    db.refresh(db_car)
    return CarResponse(
        id=db_car.id,
        brand=db_car.brand_rel.name if db_car.brand_rel else None,
        model=db_car.model_rel.name if db_car.model_rel else None,
        year=db_car.year,
        color=db_car.color,
        license_plate=db_car.plate,
        price=db_car.price,
        parking=db_car.parking_rel.name if db_car.parking_rel else None
    )