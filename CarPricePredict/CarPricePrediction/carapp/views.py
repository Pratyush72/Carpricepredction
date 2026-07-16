from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os
from django.conf import settings

# ================= HOME =================
def home(request):
    return render(request, "index.html")


# ================= PREDICT + RESULT (Combined) =================
def predict(request):
    result2 = None
    n1 = n2 = n3 = n4 = n5 = ""

    # Agar form submit hua hai
    if request.GET.get('n1'):
        try:
            csv_path = os.path.join(settings.BASE_DIR, "Cleaned_Car_data.csv")
            df = pd.read_csv(csv_path)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            X = df[['name', 'company', 'year', 'kms_driven', 'fuel_type']]
            y = df['Price']

            X = pd.get_dummies(X, drop_first=True)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            model = LinearRegression()
            model.fit(X_train, y_train)

            # User Input
            name = request.GET.get('n1')
            company = request.GET.get('n2')
            year = int(request.GET.get('n3'))
            kms_driven = int(request.GET.get('n4'))
            fuel_type = request.GET.get('n5')

            n1, n2, n3, n4, n5 = name, company, year, kms_driven, fuel_type

            # Prepare input for prediction
            input_data = pd.DataFrame([{
                'name': name,
                'company': company,
                'year': year,
                'kms_driven': kms_driven,
                'fuel_type': fuel_type
            }])

            input_data = pd.get_dummies(input_data)

            missing_cols = set(X.columns) - set(input_data.columns)
            for col in missing_cols:
                input_data[col] = 0

            input_data = input_data.reindex(columns=X.columns, fill_value=0)

            # Predict
            prediction = model.predict(input_data)[0]
            result2 = f"Predicted Price : ₹ {round(prediction):,}"

        except Exception as e:
            result2 = f"Error in prediction: {str(e)}"

    context = {
        'result2': result2,
        'n1': n1,
        'n2': n2,
        'n3': n3,
        'n4': n4,
        'n5': n5,
    }

    return render(request, "predict.html", context)