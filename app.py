from flask import Flask, request, jsonify
from flask_cors import CORS
from jobspy import scrape_jobs
import json
from flask import Response

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route("/scrape_jobs_linkedin", methods=["GET"])
def scrape_linkedin():
    job_title = request.args.get("job_title")
    city = request.args.get("city")
    country = request.args.get("country")

    if not job_title or not city or not country:
        return jsonify({"error": "Please provide job_title, city, and country"}), 400

    location = f"{city}, {country}"

    try:
        jobs_df = scrape_jobs(
            site_name=["linkedin"],
            search_term=job_title,
            location=location,
            results_wanted=20,
            linkedin_fetch_description=True,
            country_indeed=country  # safe to include
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if jobs_df.empty:
        return jsonify([])

    jobs_json = []
    for _, row in jobs_df.iterrows():
        jobs_json.append({
            "job_url": row.get("job_url"),
            "title": row.get("title"),
            "company": row.get("company"),
            "location": row.get("location"),
            "date_posted": row.get("date_posted").isoformat() if row.get("date_posted") else None,
            "job_type": row.get("job_type"),
            "job_url_direct": row.get("job_url_direct", row.get("job_url"))
        })

    return Response(
    json.dumps({"data": jobs_json}),
    mimetype='application/json'
)



@app.route("/scrape_jobs_indeed", methods=["GET"])
def scrape_indeed():
    job_title = request.args.get("job_title")
    city = request.args.get("city")
    country = request.args.get("country")

    if not job_title or not city or not country:
        return jsonify({"error": "Please provide job_title, city, and country"}), 400

    location = f"{city}, {country}"

    try:
        jobs_df = scrape_jobs(
            site_name=["indeed"],
            search_term=job_title,
            location=location,
            country_indeed=country,
            results_wanted=30,
            # Optional filters:
            # job_type='fulltime',  # e.g. 'parttime', 'internship', 'contract'
            # is_remote=False,
            hours_old=None,  # no time limit
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if jobs_df.empty:
        return jsonify([])

    jobs_json = []
    for _, row in jobs_df.iterrows():
        jobs_json.append({
            "job_url": row.get("job_url"),
            "title": row.get("title"),
            "company": row.get("company"),
            "location": row.get("location"),
            "date_posted": row.get("date_posted").isoformat() if row.get("date_posted") else None,
            "job_type": row.get("job_type"),
            "job_url_direct": row.get("job_url_direct", row.get("job_url")),
            "company_logo": row.get("company_logo")
        })

    return Response(
    json.dumps({"data": jobs_json}),
    mimetype='application/json'
)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
