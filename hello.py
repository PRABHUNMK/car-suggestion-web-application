from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:wOZWDxIwGMtYFgDe@db.fhsdtrvvhamyxamvbkje.supabase.co:5432/postgres"
db = SQLAlchemy(app)

class Sug(db.Model):
    __tablename__= "suggestiontable"

    id=db.Column(db.Integer,primary_key=True)
    sugg_text=db.Column(db.String)


class Car(db.Model):
    __tablename__ = "carsdata"
    id = db.Column(db.Integer, primary_key=True)
    City_ml = db.Column(db.Integer)
    Classification = db.Column(db.String)
    Driveline = db.Column(db.String)
    Engine_Type = db.Column(db.String)
    Fuel_Type = db.Column(db.String)
    Height = db.Column(db.Integer)
    Highway_ml = db.Column(db.Integer)
    Horsepower = db.Column(db.Integer)
    Hybrid = db.Column(db.String)
    Cars_ID = db.Column(db.String)
    Length = db.Column(db.Integer)
    Make = db.Column(db.String)
    Model_Year = db.Column(db.String)
    Number_of_Forward_Gears = db.Column(db.Integer)
    Torque = db.Column(db.Integer)
    Transmission = db.Column(db.String)
    Width =db. Column(db.Integer)
    Year = db.Column(db.Integer)
    cylinders = db.Column(db.Integer)
    engine_capacity = db.Column(db.Integer)
    price = db.Column(db.Integer)




@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/suggestion/",methods=["POST"])
def put_suggestion():
    new_sugg = request.form.get("suggestiontext")
    new_suggg = Sug(sugg_text=new_sugg)
    db.session.add(new_suggg)
    db.session.commit()

    return render_template("index.html")
   

@app.route("/cars/", methods=["POST"])
def get_filtered_cars():
    fuel_type = request.form.get("fuel_type")
    price_range = request.form.get("price")
    mileage = request.form.get("mileage")
    power = request.form.get("power")
    usage = request.form.get("usage")
    control = request.form.get("control")
    released_year = request.form.get("year")
    model = request.form.get("model")



    # cars = Car.query.filter_by(
    #     Fuel_Type=fuel_type,  
    #     Price_Range=price_range,
    #     Mileage=mileage,
    #     Power=power,
    #     Usage=usage,
    #     Control=control,
    #     Year=released_year,
    #     Make=model
    # )

    cars=Car.query

    if fuel_type:
        cars= cars.filter(Car.Fuel_Type == fuel_type)

    if released_year:
        cars = cars.filter(Car.Year == released_year)

    if model:
        cars= cars.filter(Car.Make == model)

    if power:
        if power=="High":
            cars=cars.filter(Car.Horsepower>=400)

        elif power=="Medium":
            cars=cars.filter(Car.Horsepower>=200, Car.Horsepower<=399)

        else:
            cars=cars.filter(Car.Horsepower>=100, Car.Horsepower<=199)


    if control:
        if control=="Automatic transmission":
            cars=cars.filter(Car.Transmission=='Automatic transmission')

        else:
            cars=cars.filter(Car.Transmission!='Manual transmission')

    if usage=="Business":

        if mileage == "high":
            cars = cars.filter(Car.City_ml == Car.query.with_entities(Car.Model, db.func.max(Car.City_ml )))
        elif mileage == "average":
            cars = cars.filter(Car.City_ml > Car.query.with_entities(Car.Model, db.func.avg(Car.City_ml )))
        elif mileage == "above-average":
            cars = cars.filter(Car.City_ml > Car.query.with_entities(Car.Model, db.func.avg(Car.City_ml )))

    else:
        if mileage == "high":
            cars = cars.filter(Car.Highway_ml == Car.query.with_entities(Car.Model, db.func.max(Car.Highway_ml)))
        elif mileage == "average":
            cars = cars.filter(Car.Highway_ml > Car.query.with_entities(Car.Model, db.func.avg(Car.Highway_ml)))
        elif mileage == "above-average":
            cars = cars.filter(Car.Highway_ml > Car.query.with_entities(Car.Model, db.func.avg(Car.Highway_ml)))

    if price_range:
        if price_range == "1":
            cars = cars.filter(Car.price >= 2000000, Car.price <= 3000000)
        elif price_range == "2":
            cars = cars.filter(Car.price >= 3000000, Car.price <= 4000000)
        elif price_range == "3":
            cars = cars.filter(Car.price >= 4000000, Car.price <= 5000000)


    cars=cars.all()

    return render_template("index.html", cars=cars)


