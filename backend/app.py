from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/improve', methods=['POST'])
def improve_dataset():
    try:
        # Step 1: Receive the data
        data = request.get_json()
        df = pd.DataFrame(data)

        # Step 2: Replace non-standard missing values with NaN
        df.replace(["N/A", "n/a", "null", ""], pd.NA, inplace=True)

        # Step 3: Calculate statistics
        stats = {
            "Nombre de lignes": len(df),
            "Nombre de colonnes": len(df.columns),
            "Valeurs manquantes": int(df.isnull().sum().sum()),
        }

        # Step 4: Detailed statistics using describe()
        describe_stats = df.describe(include="all").transpose().fillna("N/A").to_dict()

        # Step 5: Fill missing values (optional)
        df.fillna("N/A", inplace=True)

        # Convert dataset to a serializable format
        dataset_serializable = df.astype(str).to_dict(orient="records")

        return jsonify({
            "dataset": dataset_serializable,
            "stats": stats,
            "describe": describe_stats,  # Detailed statistics
        })

    except Exception as e:
        print("Erreur survenue :", str(e))
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
